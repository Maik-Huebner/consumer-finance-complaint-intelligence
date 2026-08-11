from __future__ import annotations

from data_intelligence_platform.validation.quality import (
    validate_dataframe,
)


def test_quality_report_passes_for_valid_analytical_data(
    analytical_df,
):
    report = validate_dataframe(
        analytical_df
    )

    assert report.passed is True
    assert (
        report.duplicate_complaint_ids
        == 0
    )
    assert (
        report.negative_days_to_company
        == 0
    )
    assert (
        report.missing_harmonized_products
        == 0
    )
    assert (
        report.missing_harmonized_issues
        == 0
    )
    assert (
        report.unexpected_timely_values
        == []
    )
    assert (
        report.unexpected_taxonomy_versions
        == []
    )


def test_quality_report_detects_duplicate_id(
    analytical_df,
):
    analytical_df.loc[
        1,
        "complaint_id",
    ] = analytical_df.loc[
        0,
        "complaint_id",
    ]

    report = validate_dataframe(
        analytical_df
    )

    assert report.passed is False
    assert (
        report.duplicate_complaint_ids
        == 1
    )


def test_quality_report_detects_missing_harmonized_product(
    analytical_df,
):
    analytical_df.loc[
        0,
        "harmonized_product",
    ] = None

    report = validate_dataframe(
        analytical_df
    )

    assert report.passed is False
    assert (
        report.missing_harmonized_products
        == 1
    )
