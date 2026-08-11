from __future__ import annotations

import pandas as pd

from data_intelligence_platform.analysis.report import (
    write_executive_summary,
)


def test_executive_summary_documents_cleaning_and_taxonomy(
    tmp_path,
):
    yearly = pd.DataFrame(
        {
            "year": [
                2022,
                2025,
            ],
            "complaints": [
                100,
                200,
            ],
        }
    )

    product = pd.DataFrame(
        {
            "product": [
                "Credit reporting",
            ],
            "complaints": [
                150,
            ],
            "complaint_share": [
                0.75,
            ],
        }
    )

    hotspots = pd.DataFrame(
        {
            "product": [
                "Credit reporting",
            ],
            "issue": [
                "Incorrect information",
            ],
            "complaints": [
                120,
            ],
        }
    )

    correlations = pd.DataFrame(
        {
            "x": [
                "complaints",
                "complaints",
            ],
            "y": [
                "timely_response_rate",
                "narrative_share",
            ],
            "pearson_r": [
                0.2,
                -0.8,
            ],
            "spearman_rho": [
                0.3,
                -0.7,
            ],
        }
    )

    cleaning = {
        "rows": 200,
        "source_missing_issue_rows": 1,
        "source_missing_issue_share": 0.005,
        "missing_issue_rows_handled": 1,
        "missing_issue_rows_unhandled": 0,
    }

    taxonomy = {
        "rows": 200,
        "product_rows_changed": 20,
        "product_change_share": 0.10,
        "issue_rows_changed": 5,
        "issue_change_share": 0.025,
        "any_rows_changed": 22,
        "any_change_share": 0.11,
    }

    trend = {
        "monthly_slope": 10.0,
        "intercept": 100.0,
        "r2": 0.8,
    }

    output_path = (
        tmp_path
        / "executive_summary.md"
    )

    write_executive_summary(
        output_path=output_path,
        yearly=yearly,
        product=product,
        hotspots=hotspots,
        trend=trend,
        correlations=correlations,
        cleaning=cleaning,
        taxonomy=taxonomy,
        quality_passed=True,
    )

    text = output_path.read_text(
        encoding="utf-8"
    )

    assert (
        "# Management Summary"
        in text
    )

    assert (
        "## Datenaufbereitung und Datenbereinigung"
        in text
    )

    assert (
        "Issue not provided"
        in text
    )

    assert (
        "Keine Beschwerde wird ausschließlich"
        in text
    )

    assert (
        "## Taxonomie-Harmonisierung"
        in text
    )

    assert (
        "## Relevanz für Banking und Finanzdienstleistungen"
        in text
    )

    assert (
        "## Relevanz für Versicherungen"
        in text
    )

    assert (
        "## Relevanz für Technical AI Consulting"
        in text
    )

    assert (
        "Conduct-Risk"
        in text
    )

    assert (
        "Datenqualitätsprüfung wurde **bestanden**"
        in text
    )

    assert (
        "keine kausalen Zusammenhänge"
        in text
    )

    assert (
        "datenbasierten Entscheidungsunterstützung"
        in text
    )
