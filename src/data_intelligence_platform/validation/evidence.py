"""Validate the committed analytical evidence without requiring raw data."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
import yaml
from scipy.stats import pearsonr, spearmanr


class EvidenceValidationError(ValueError):
    """Raised when committed report artifacts contradict one another."""


def _load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Required evidence file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Required evidence file not found: {path}")
    return pd.read_csv(path)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceValidationError(message)


def _close(actual: float, expected: float, label: str, *, atol: float = 1e-9) -> None:
    if not math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=atol):
        raise EvidenceValidationError(f"{label}: expected {expected!r}, found {actual!r}")


def _linear_trend(values: pd.Series) -> tuple[float, float]:
    x = np.arange(len(values), dtype=float)
    y = values.to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    residual = float(np.square(y - predicted).sum())
    total = float(np.square(y - y.mean()).sum())
    return float(slope), 1.0 - residual / total


def _pptx_text(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required presentation file not found: {path}")
    with ZipFile(path) as archive:
        slide_xml = [
            archive.read(name).decode("utf-8")
            for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        ]
    return "\n".join(re.findall(r"<a:t>(.*?)</a:t>", "\n".join(slide_xml)))


def validate_report_evidence(repository_root: Path) -> dict[str, int | str | bool]:
    """Cross-check committed reports, provenance, narratives, and presentation.

    The repository root is explicit so validation also works when this package
    is installed normally in ``site-packages``.
    """
    root = Path(repository_root).resolve()
    reports = root / "reports"
    config_path = root / "configs" / "project.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"Project configuration not found: {config_path}")
    if not reports.is_dir():
        raise FileNotFoundError(f"Evidence directory not found: {reports}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    snapshot = _load_json(reports / "source_snapshot.json")
    quality = _load_json(reports / "data_quality_report.json")
    cleaning = _load_json(reports / "data_cleaning_summary.json")
    taxonomy = _load_json(reports / "taxonomy_harmonization_summary.json")
    trend = _load_json(reports / "linear_trend.json")
    sensitivity = _load_json(reports / "segment_sensitivity_summary.json")

    kpis = _load_csv(reports / "kpi_summary.csv").set_index("metric")["value"]
    yearly = _load_csv(reports / "yearly_summary.csv")
    monthly = _load_csv(reports / "monthly_trends.csv")
    products = _load_csv(reports / "product_summary.csv")
    hotspots = _load_csv(reports / "issue_hotspots.csv")
    correlations = _load_csv(reports / "monthly_correlations.csv")
    sensitivity_yearly = _load_csv(reports / "segment_sensitivity_yearly.csv")
    taxonomy_audit = _load_csv(reports / "taxonomy_harmonization_audit.csv")

    total = int(kpis["complaints"])
    for label, value in {
        "source snapshot rows": snapshot["analysis_rows"],
        "quality rows": quality["rows"],
        "cleaning rows": cleaning["rows"],
        "taxonomy rows": taxonomy["rows"],
    }.items():
        _require(int(value) == total, f"{label} does not match KPI complaints")

    project = config["project"]
    window = snapshot["analysis_window"]
    _require(window["start"] == project["analysis_start"], "Snapshot start differs from config")
    _require(window["end"] == project["analysis_end"], "Snapshot end differs from config")
    _require(quality["min_date"] == window["start"], "Quality minimum date differs from snapshot")
    _require(quality["max_date"] == window["end"], "Quality maximum date differs from snapshot")
    _require(quality["passed"] is True, "Committed data-quality gate is not passing")
    _require(snapshot["data_quality_passed"] is True, "Snapshot records a failed quality gate")
    _require(
        re.fullmatch(r"[0-9a-f]{64}", snapshot["sha256_recorded_by_downloader"]) is not None,
        "Snapshot SHA-256 is not a lowercase 64-character digest",
    )
    for field in (
        "duplicate_complaint_ids",
        "missing_complaint_ids",
        "missing_harmonized_products",
        "missing_harmonized_issues",
        "negative_days_to_company",
    ):
        _require(quality[field] == 0, f"Quality finding is non-zero: {field}")
    _require(not quality["unexpected_timely_values"], "Unexpected timely-response values recorded")
    _require(not quality["unexpected_taxonomy_versions"], "Unexpected taxonomy versions recorded")

    _require(int(yearly["complaints"].sum()) == total, "Yearly complaints do not sum to KPI total")
    _require(
        int(products["complaints"].sum()) == total, "Product complaints do not sum to KPI total"
    )
    _require(len(products) == int(kpis["unique_products"]), "Product count differs from KPI")
    _close(products["complaint_share"].sum(), 1.0, "Product shares")
    _close(
        np.average(products["timely_response_rate"], weights=products["complaints"]),
        kpis["timely_response_rate"],
        "Weighted product timely-response rate",
    )
    _require(not products["complaints"].duplicated().all(), "Product summary appears malformed")
    _require(int(hotspots["complaints"].max()) <= total, "Hotspot count exceeds total complaints")

    monthly["year_month"] = pd.to_datetime(monthly["year_month"], errors="raise")
    expected_months = pd.date_range(window["start"], window["end"], freq="MS")
    _require(monthly["year_month"].tolist() == expected_months.tolist(), "Monthly index has gaps")
    _require(int(monthly["complaints"].sum()) == total, "Monthly complaints do not sum to total")
    expected_rolling = monthly["complaints"].rolling(12, min_periods=12).mean()
    _require(
        np.allclose(
            monthly["rolling_complaints"].to_numpy(dtype=float),
            expected_rolling.to_numpy(dtype=float),
            equal_nan=True,
        ),
        "Rolling 12-month complaints are inconsistent",
    )
    grouped_years = monthly.groupby(monthly["year_month"].dt.year)["complaints"].sum()
    _require(
        grouped_years.to_dict() == yearly.set_index("year")["complaints"].to_dict(),
        "Monthly and yearly complaint totals differ",
    )

    slope, r2 = _linear_trend(monthly["complaints"])
    _close(slope, trend["monthly_slope"], "Linear trend slope", atol=1e-6)
    _close(r2, trend["r2"], "Linear trend R-squared")

    for row in correlations.itertuples(index=False):
        x = monthly[row.x]
        y = monthly[row.y]
        pearson = pearsonr(x, y)
        spearman = spearmanr(x, y)
        _close(pearson.statistic, row.pearson_r, f"Pearson r for {row.x}/{row.y}")
        _close(pearson.pvalue, row.pearson_p, f"Pearson p for {row.x}/{row.y}")
        _close(spearman.statistic, row.spearman_rho, f"Spearman rho for {row.x}/{row.y}")
        _close(spearman.pvalue, row.spearman_p, f"Spearman p for {row.x}/{row.y}")
        sensitivity_all = sensitivity["correlations"][f"{row.x}_vs_{row.y}"]["all"]
        for field, expected in {
            "pearson_r": row.pearson_r,
            "pearson_p": row.pearson_p,
            "spearman_rho": row.spearman_rho,
            "spearman_p": row.spearman_p,
        }.items():
            _close(
                sensitivity_all[field],
                expected,
                f"Sensitivity correlation {field} for {row.x}/{row.y}",
            )

    _require(
        np.array_equal(
            sensitivity_yearly["total_complaints"].to_numpy(),
            yearly["complaints"].to_numpy(),
        ),
        "Sensitivity and yearly totals differ",
    )
    _require(
        np.array_equal(
            sensitivity_yearly["focus_product_complaints"].to_numpy()
            + sensitivity_yearly["without_focus_product"].to_numpy(),
            sensitivity_yearly["total_complaints"].to_numpy(),
        ),
        "Sensitivity segment counts do not add to totals",
    )
    expected_share = (
        sensitivity_yearly["focus_product_complaints"] / sensitivity_yearly["total_complaints"]
    )
    _require(
        np.allclose(sensitivity_yearly["focus_product_share"], expected_share),
        "Sensitivity segment shares are inconsistent",
    )
    first = sensitivity_yearly.iloc[0]
    last = sensitivity_yearly.iloc[-1]
    expected_sensitivity = {
        "first_year": int(first["year"]),
        "last_year": int(last["year"]),
        "total_complaints_first_year": int(first["total_complaints"]),
        "total_complaints_last_year": int(last["total_complaints"]),
        "without_focus_complaints_first_year": int(first["without_focus_product"]),
        "without_focus_complaints_last_year": int(last["without_focus_product"]),
    }
    for field, expected in expected_sensitivity.items():
        _require(int(sensitivity[field]) == expected, f"Sensitivity field is inconsistent: {field}")
    _close(first["focus_product_share"], sensitivity["focus_share_first_year"], "First share")
    _close(last["focus_product_share"], sensitivity["focus_share_last_year"], "Last share")
    _close(
        (last["focus_product_share"] - first["focus_product_share"]) * 100,
        sensitivity["focus_share_change_percentage_points"],
        "Focus share change",
    )
    _close(
        last["total_complaints"] / first["total_complaints"] - 1,
        sensitivity["total_growth_first_to_last"],
        "Total growth sensitivity",
    )
    _close(
        last["without_focus_product"] / first["without_focus_product"] - 1,
        sensitivity["without_focus_growth_first_to_last"],
        "Without-focus growth sensitivity",
    )
    _close(slope, sensitivity["total_monthly_slope"], "Sensitivity total slope", atol=1e-6)
    _close(r2, sensitivity["total_trend_r2"], "Sensitivity total R-squared")
    _close(
        sensitivity["focus_monthly_slope"] + sensitivity["without_focus_monthly_slope"],
        sensitivity["total_monthly_slope"],
        "Sensitivity segment slopes",
        atol=1e-6,
    )
    _close(
        sensitivity["focus_monthly_slope"] / sensitivity["total_monthly_slope"],
        sensitivity["focus_share_of_total_linear_slope"],
        "Focus share of total slope",
    )

    changed = taxonomy_audit[taxonomy_audit["changed"].astype(bool)]
    product_changes = changed[changed["dimension"] == "product"]
    issue_changes = changed[
        (changed["dimension"] == "issue") & (changed["change_type"] == "taxonomy_harmonization")
    ]
    missing_issue_changes = changed[
        (changed["dimension"] == "issue") & (changed["change_type"] == "missing_value_handling")
    ]
    _require(
        int(product_changes["complaints"].sum()) == taxonomy["product_rows_changed"],
        "Taxonomy product audit differs from summary",
    )
    _require(
        int(issue_changes["complaints"].sum()) == taxonomy["issue_rows_changed"],
        "Taxonomy issue audit differs from summary",
    )
    _require(
        int(missing_issue_changes["complaints"].sum()) == cleaning["source_missing_issue_rows"],
        "Missing-issue audit differs from cleaning summary",
    )
    _require(
        cleaning["missing_issue_rows_handled"] == cleaning["source_missing_issue_rows"],
        "Not all missing source issues are handled",
    )
    _require(cleaning["missing_issue_rows_unhandled"] == 0, "Unhandled missing issues remain")

    narrative_files = {
        root / "README.md": "10.269.540",
        root / "reports" / "executive_summary.md": "5.442.977",
        root / "docs" / "methodology.md": "10.269.540",
        root / "notebooks" / "01_executive_eda.ipynb": "10.269.540",
    }
    for path, expected_total in narrative_files.items():
        text = path.read_text(encoding="utf-8")
        _require(expected_total in text, f"Published complaint value missing from {path}")
    pptx = root / "presentation" / "consumer_finance_complaint_intelligence_presentation.pptx"
    presentation_text = _pptx_text(pptx)
    for token in ("10.269.540", "+580,2 %", "85,9 %", "+220,3 %", "91,2 %"):
        _require(token in presentation_text, f"Presentation is missing published value: {token}")
    pdf = root / "presentation" / "consumer_finance_complaint_intelligence_presentation.pdf"
    _require(pdf.is_file() and pdf.stat().st_size > 100_000, "Presentation PDF is missing or empty")

    return {
        "status": "passed",
        "analysis_rows": total,
        "analysis_months": len(monthly),
        "products": len(products),
        "quality_passed": True,
    }
