from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture()
def sample_raw_csv(
    tmp_path: Path,
) -> Path:
    """Create a small raw CFPB-style CSV for transformation tests."""
    rows = [
        {
            "Date received": "2022-01-05",
            "Product": "Credit card",
            "Sub-product": "General-purpose credit card",
            "Issue": "Billing dispute",
            "Sub-issue": "Transaction problem",
            "Consumer complaint narrative": "Example narrative",
            "Company public response": "Company has responded",
            "Company": "Example Bank A",
            "State": "NY",
            "ZIP code": "10001",
            "Tags": None,
            "Submitted via": "Web",
            "Date sent to company": "2022-01-06",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "1",
        },
        {
            "Date received": "2023-06-10",
            "Product": "Mortgage",
            "Sub-product": "Conventional home mortgage",
            "Issue": "Trouble during payment process",
            "Sub-issue": None,
            "Consumer complaint narrative": None,
            "Company public response": None,
            "Company": "Example Bank B",
            "State": "CA",
            "ZIP code": "90001",
            "Tags": "Older American",
            "Submitted via": "Phone",
            "Date sent to company": "2023-06-12",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "No",
            "Complaint ID": "2",
        },
        {
            "Date received": "2025-12-20",
            "Product": "Credit card",
            "Sub-product": "General-purpose credit card",
            "Issue": "Billing dispute",
            "Sub-issue": None,
            "Consumer complaint narrative": "Another example",
            "Company public response": None,
            "Company": "Example Bank A",
            "State": "TX",
            "ZIP code": "75001",
            "Tags": None,
            "Submitted via": "Web",
            "Date sent to company": "2025-12-20",
            "Company response to consumer": "Closed with monetary relief",
            "Timely response?": "Yes",
            "Complaint ID": "3",
        },
        {
            "Date received": "2026-01-02",
            "Product": "Credit card",
            "Sub-product": None,
            "Issue": "Other",
            "Sub-issue": None,
            "Consumer complaint narrative": None,
            "Company public response": None,
            "Company": "Example Bank A",
            "State": "TX",
            "ZIP code": "75001",
            "Tags": None,
            "Submitted via": "Web",
            "Date sent to company": "2026-01-03",
            "Company response to consumer": "Closed with explanation",
            "Timely response?": "Yes",
            "Complaint ID": "4",
        },
    ]

    path = (
        tmp_path
        / "complaints.csv"
    )

    pd.DataFrame(
        rows
    ).to_csv(
        path,
        index=False,
    )

    return path


@pytest.fixture()
def analytical_df() -> pd.DataFrame:
    """Create representative processed data for analytical unit tests."""
    dates = pd.date_range(
        "2022-01-01",
        periods=24,
        freq="MS",
    )

    rows = []

    for idx, date in enumerate(
        dates,
        start=1,
    ):
        if idx % 2:
            product = "Credit card"
            harmonized_product = (
                "Credit card"
            )
            issue = "Billing"
            harmonized_issue = (
                "Billing"
            )
        else:
            product = "Mortgage"
            harmonized_product = (
                "Mortgage"
            )
            issue = "Payment process"
            harmonized_issue = (
                "Payment process"
            )

        # Include one historical product label and one historical issue label
        # so taxonomy-audit behavior is exercised in the analytical tests.
        if idx == 1:
            product = (
                "Credit card or prepaid card"
            )

        if idx == 2:
            issue = (
                "Legacy payment wording"
            )

        taxonomy_version = (
            "pre_aug_2023"
            if date
            < pd.Timestamp(
                "2023-08-24"
            )
            else "aug_2023_or_later"
        )

        rows.append(
            {
                "complaint_id": str(idx),
                "date_received": date,
                "product": product,
                "issue": issue,
                "harmonized_product": harmonized_product,
                "harmonized_issue": harmonized_issue,
                "taxonomy_version": taxonomy_version,
                "company": (
                    "Bank A"
                    if idx % 3
                    else "Bank B"
                ),
                "date_sent_to_company": (
                    date
                    + pd.Timedelta(
                        days=1
                    )
                ),
                "company_response": (
                    "Closed with explanation"
                ),
                "timely_response": (
                    "Yes"
                    if idx % 5
                    else "No"
                ),
                "year": date.year,
                "year_month": date,
                "days_to_company": 1,
                "has_narrative": (
                    idx % 2 == 0
                ),
                "is_timely": (
                    idx % 5 != 0
                ),
            }
        )

    return pd.DataFrame(rows)
