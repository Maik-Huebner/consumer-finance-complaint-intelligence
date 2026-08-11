"""Data-quality checks for the analysis-ready complaint table."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

REQUIRED_COLUMNS = {
    "complaint_id",
    "date_received",
    "product",
    "issue",
    "harmonized_product",
    "harmonized_issue",
    "taxonomy_version",
    "company",
    "date_sent_to_company",
    "company_response",
    "timely_response",
    "year",
    "year_month",
    "days_to_company",
    "has_narrative",
    "is_timely",
}

EXPECTED_TAXONOMY_VERSIONS = {
    "pre_aug_2023",
    "aug_2023_or_later",
}


@dataclass
class QualityReport:
    """Structured result of processed-data quality checks."""

    rows: int
    columns: int
    duplicate_complaint_ids: int
    missing_complaint_ids: int
    missing_harmonized_products: int
    missing_harmonized_issues: int
    negative_days_to_company: int
    unexpected_timely_values: list[str]
    unexpected_taxonomy_versions: list[str]
    min_date: str | None
    max_date: str | None
    missing_percent: dict[str, float]
    passed: bool

    def to_dict(self) -> dict:
        """Convert the report to a JSON-serializable dictionary."""
        return asdict(self)


def validate_dataframe(
    df: pd.DataFrame,
) -> QualityReport:
    """Run structural and consistency checks without mutating the data."""
    missing_columns = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Processed data missing required columns: "
            f"{sorted(missing_columns)}"
        )

    timely_values = sorted(
        value
        for value in (
            df["timely_response"]
            .dropna()
            .astype(str)
            .unique()
        )
        if value not in {
            "Yes",
            "No",
        }
    )

    taxonomy_versions = sorted(
        value
        for value in (
            df["taxonomy_version"]
            .dropna()
            .astype(str)
            .unique()
        )
        if value
        not in EXPECTED_TAXONOMY_VERSIONS
    )

    duplicate_ids = int(
        df["complaint_id"]
        .duplicated()
        .sum()
    )

    missing_ids = int(
        df["complaint_id"]
        .isna()
        .sum()
    )

    missing_harmonized_products = int(
        df["harmonized_product"]
        .isna()
        .sum()
    )

    missing_harmonized_issues = int(
        df["harmonized_issue"]
        .isna()
        .sum()
    )

    negative_delays = int(
        (
            df["days_to_company"]
            .dropna()
            < 0
        )
        .sum()
    )

    missing_percent = (
        df.isna()
        .mean()
        .mul(100)
        .round(3)
        .to_dict()
    )

    dates = pd.to_datetime(
        df["date_received"],
        errors="coerce",
    )

    valid_dates = dates.dropna()

    min_date = (
        None
        if valid_dates.empty
        else valid_dates.min()
        .date()
        .isoformat()
    )

    max_date = (
        None
        if valid_dates.empty
        else valid_dates.max()
        .date()
        .isoformat()
    )

    passed = (
        duplicate_ids == 0
        and missing_ids == 0
        and missing_harmonized_products == 0
        and missing_harmonized_issues == 0
        and negative_delays == 0
        and not timely_values
        and not taxonomy_versions
    )

    return QualityReport(
        rows=len(df),
        columns=len(df.columns),
        duplicate_complaint_ids=duplicate_ids,
        missing_complaint_ids=missing_ids,
        missing_harmonized_products=missing_harmonized_products,
        missing_harmonized_issues=missing_harmonized_issues,
        negative_days_to_company=negative_delays,
        unexpected_timely_values=timely_values,
        unexpected_taxonomy_versions=taxonomy_versions,
        min_date=min_date,
        max_date=max_date,
        missing_percent=missing_percent,
        passed=passed,
    )
