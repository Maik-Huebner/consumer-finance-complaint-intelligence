from __future__ import annotations

from pathlib import Path

import polars as pl

from data_intelligence_platform.transformation.complaints import (
    build_lazy_transform,
)


def test_transform_filters_analysis_window_and_derives_fields(
    sample_raw_csv,
):
    result = build_lazy_transform(
        sample_raw_csv,
        analysis_start="2022-01-01",
        analysis_end="2025-12-31",
    ).collect()

    assert result.height == 3

    assert result[
        "complaint_id"
    ].to_list() == [
        "1",
        "2",
        "3",
    ]

    assert result[
        "year"
    ].to_list() == [
        2022,
        2023,
        2025,
    ]

    assert result[
        "days_to_company"
    ].to_list() == [
        1,
        2,
        0,
    ]

    assert result[
        "has_narrative"
    ].to_list() == [
        True,
        False,
        True,
    ]

    assert result[
        "is_timely"
    ].to_list() == [
        True,
        False,
        True,
    ]

    assert result[
        "taxonomy_version"
    ].to_list() == [
        "pre_aug_2023",
        "pre_aug_2023",
        "aug_2023_or_later",
    ]

    assert result[
        "harmonized_product"
    ].to_list() == [
        "Credit card",
        "Mortgage",
        "Credit card",
    ]

    assert result[
        "harmonized_issue"
    ].to_list() == [
        "Billing dispute",
        "Trouble during payment process",
        "Billing dispute",
    ]

    assert (
        result.schema[
            "date_received"
        ]
        == pl.Date
    )


def test_transform_harmonizes_documented_2023_taxonomy_changes(
    tmp_path: Path,
):
    rows = [
        {
            "Date received": "2022-01-10",
            "Product": (
                "Credit reporting, credit repair services, "
                "or other personal consumer reports"
            ),
            "Sub-product": "Credit reporting",
            "Issue": (
                "Problem with a credit reporting company's "
                "investigation into an existing problem"
            ),
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "NY",
            "Submitted via": "Web",
            "Date sent to company": "2022-01-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "100",
        },
        {
            "Date received": "2022-02-10",
            "Product": (
                "Credit reporting, credit repair services, "
                "or other personal consumer reports"
            ),
            "Sub-product": "Credit repair services",
            "Issue": "Fraud or scam",
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "CA",
            "Submitted via": "Web",
            "Date sent to company": "2022-02-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "101",
        },
        {
            "Date received": "2022-03-10",
            "Product": (
                "Money transfer, virtual currency, or money service"
            ),
            "Sub-product": "Debt settlement",
            "Issue": "Unexpected or other fees",
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "TX",
            "Submitted via": "Web",
            "Date sent to company": "2022-03-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "102",
        },
        {
            "Date received": "2022-04-10",
            "Product": "Credit card or prepaid card",
            "Sub-product": "General-purpose prepaid card",
            "Issue": "Trouble using the card",
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "FL",
            "Submitted via": "Web",
            "Date sent to company": "2022-04-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "103",
        },
        {
            "Date received": "2022-05-10",
            "Product": "Credit card or prepaid card",
            "Sub-product": "Store credit card",
            "Issue": "Fees or interest",
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "WA",
            "Submitted via": "Web",
            "Date sent to company": "2022-05-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "104",
        },
        {
            "Date received": "2022-06-10",
            "Product": "Payday loan, title loan, or personal loan",
            "Sub-product": "Payday loan",
            "Issue": "Can't contact lender or servicer",
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "IL",
            "Submitted via": "Web",
            "Date sent to company": "2022-06-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "105",
        },
        {
            "Date received": "2024-01-10",
            "Product": (
                "Credit reporting or other personal consumer reports"
            ),
            "Sub-product": "Credit reporting",
            "Issue": (
                "Problem with a company's investigation "
                "into an existing problem"
            ),
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "NY",
            "Submitted via": "Web",
            "Date sent to company": "2024-01-11",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "106",
        },
        {
            "Date received": "2024-03-13",
            "Product": "Checking or savings account",
            "Sub-product": None,
            "Issue": None,
            "Consumer complaint narrative": None,
            "Company": "Example Company",
            "State": "NY",
            "Submitted via": "Web",
            "Date sent to company": "2024-03-14",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "107",
        },
    ]

    csv_path = (
        tmp_path
        / "taxonomy_cases.csv"
    )

    pl.DataFrame(
        rows
    ).write_csv(
        csv_path
    )

    result = build_lazy_transform(
        csv_path,
        analysis_start="2022-01-01",
        analysis_end="2025-12-31",
    ).collect()

    by_id = {
        row[
            "complaint_id"
        ]: row
        for row
        in result.to_dicts()
    }

    assert (
        by_id[
            "100"
        ][
            "harmonized_product"
        ]
        == (
            "Credit reporting or other personal consumer reports"
        )
    )

    assert (
        by_id[
            "100"
        ][
            "harmonized_issue"
        ]
        == (
            "Problem with a company's investigation "
            "into an existing problem"
        )
    )

    assert (
        by_id[
            "101"
        ][
            "harmonized_product"
        ]
        == "Debt or credit management"
    )

    assert (
        by_id[
            "101"
        ][
            "harmonized_issue"
        ]
        == "Didn't provide services promised"
    )

    assert (
        by_id[
            "102"
        ][
            "harmonized_product"
        ]
        == "Debt or credit management"
    )

    assert (
        by_id[
            "102"
        ][
            "harmonized_issue"
        ]
        == "Charged up-front or unexpected fees"
    )

    assert (
        by_id[
            "103"
        ][
            "harmonized_product"
        ]
        == "Prepaid card"
    )

    assert (
        by_id[
            "104"
        ][
            "harmonized_product"
        ]
        == "Credit card"
    )

    assert (
        by_id[
            "105"
        ][
            "harmonized_product"
        ]
        == (
            "Payday loan, title loan, personal loan, or advance loan"
        )
    )

    assert (
        by_id[
            "106"
        ][
            "harmonized_product"
        ]
        == (
            "Credit reporting or other personal consumer reports"
        )
    )

    assert (
        by_id[
            "106"
        ][
            "taxonomy_version"
        ]
        == "aug_2023_or_later"
    )

    # Missing source information must remain missing in the source field.
    assert (
        by_id[
            "107"
        ][
            "issue"
        ]
        is None
    )

    # The analytical field explicitly represents the missing value so the
    # complaint remains visible in group-based exploratory analysis.
    assert (
        by_id[
            "107"
        ][
            "harmonized_issue"
        ]
        == "Issue not provided"
    )
