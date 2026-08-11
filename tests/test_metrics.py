from __future__ import annotations

import math

from data_intelligence_platform.analysis.metrics import (
    data_cleaning_summary,
    executive_kpis,
    issue_hotspots,
    linear_time_trend,
    monthly_summary,
    product_summary,
    taxonomy_audit,
    taxonomy_harmonization_summary,
)


def test_executive_kpis_use_harmonized_products(
    analytical_df,
):
    kpis = (
        executive_kpis(
            analytical_df
        )
        .set_index(
            "metric"
        )[
            "value"
        ]
    )

    assert (
        kpis[
            "complaints"
        ]
        == len(
            analytical_df
        )
    )

    assert (
        analytical_df[
            "product"
        ]
        .nunique()
        == 3
    )

    assert (
        kpis[
            "unique_products"
        ]
        == 2
    )

    assert math.isclose(
        kpis[
            "timely_response_rate"
        ],
        analytical_df[
            "is_timely"
        ].mean(),
    )


def test_product_summary_shares_sum_to_one(
    analytical_df,
):
    summary = product_summary(
        analytical_df
    )

    assert math.isclose(
        summary[
            "complaint_share"
        ].sum(),
        1.0,
    )

    assert set(
        summary[
            "product"
        ]
    ) == {
        "Credit card",
        "Mortgage",
    }


def test_issue_hotspots_use_harmonized_labels(
    analytical_df,
):
    hotspots = issue_hotspots(
        analytical_df
    )

    assert (
        "Legacy payment wording"
        not in set(
            hotspots[
                "issue"
            ]
        )
    )

    assert (
        "Payment process"
        in set(
            hotspots[
                "issue"
            ]
        )
    )


def test_taxonomy_summary_detects_changed_rows(
    analytical_df,
):
    summary = (
        taxonomy_harmonization_summary(
            analytical_df
        )
    )

    assert (
        summary[
            "product_rows_changed"
        ]
        == 1
    )

    assert (
        summary[
            "issue_rows_changed"
        ]
        == 1
    )

    assert (
        summary[
            "any_rows_changed"
        ]
        == 2
    )


def test_taxonomy_audit_preserves_source_and_harmonized_values(
    analytical_df,
):
    audit = taxonomy_audit(
        analytical_df
    )

    changed = audit[
        audit[
            "changed"
        ]
    ]

    product_change = changed[
        changed[
            "dimension"
        ]
        == "product"
    ]

    issue_change = changed[
        changed[
            "dimension"
        ]
        == "issue"
    ]

    assert len(
        product_change
    ) == 1

    assert (
        product_change.iloc[
            0
        ][
            "source_value"
        ]
        == "Credit card or prepaid card"
    )

    assert (
        product_change.iloc[
            0
        ][
            "harmonized_value"
        ]
        == "Credit card"
    )

    assert (
        product_change.iloc[
            0
        ][
            "change_type"
        ]
        == "taxonomy_harmonization"
    )

    assert len(
        issue_change
    ) == 1

    assert (
        issue_change.iloc[
            0
        ][
            "source_value"
        ]
        == "Legacy payment wording"
    )

    assert (
        issue_change.iloc[
            0
        ][
            "harmonized_value"
        ]
        == "Payment process"
    )

    assert (
        issue_change.iloc[
            0
        ][
            "change_type"
        ]
        == "taxonomy_harmonization"
    )


def test_data_cleaning_summary_tracks_missing_issue_handling(
    analytical_df,
):
    cleaned = analytical_df.copy()

    cleaned.loc[
        0,
        "issue",
    ] = None

    cleaned.loc[
        0,
        "harmonized_issue",
    ] = "Issue not provided"

    cleaning = data_cleaning_summary(
        cleaned
    )

    taxonomy = (
        taxonomy_harmonization_summary(
            cleaned
        )
    )

    assert (
        cleaning[
            "source_missing_issue_rows"
        ]
        == 1
    )

    assert (
        cleaning[
            "missing_issue_rows_handled"
        ]
        == 1
    )

    assert (
        cleaning[
            "missing_issue_rows_unhandled"
        ]
        == 0
    )

    # Missing-value treatment is data cleaning, not a taxonomy revision.
    assert (
        taxonomy[
            "issue_rows_changed"
        ]
        == 1
    )


def test_taxonomy_audit_labels_missing_value_handling(
    analytical_df,
):
    cleaned = analytical_df.copy()

    cleaned.loc[
        0,
        "issue",
    ] = None

    cleaned.loc[
        0,
        "harmonized_issue",
    ] = "Issue not provided"

    audit = taxonomy_audit(
        cleaned
    )

    missing_handling = audit[
        audit[
            "change_type"
        ]
        == "missing_value_handling"
    ]

    assert len(
        missing_handling
    ) == 1

    assert (
        missing_handling.iloc[
            0
        ][
            "harmonized_value"
        ]
        == "Issue not provided"
    )


def test_monthly_summary_and_linear_trend(
    analytical_df,
):
    monthly = monthly_summary(
        analytical_df,
        rolling_window=3,
    )

    trend = linear_time_trend(
        monthly
    )

    assert len(
        monthly
    ) == 24

    assert set(
        trend
    ) == {
        "monthly_slope",
        "intercept",
        "r2",
    }

    assert (
        0
        <= trend[
            "r2"
        ]
        <= 1
    )


def test_monthly_summary_requires_full_rolling_window(
    analytical_df,
):
    monthly = monthly_summary(
        analytical_df,
        rolling_window=3,
    )

    assert (
        monthly[
            "rolling_complaints"
        ]
        .iloc[
            :2
        ]
        .isna()
        .all()
    )

    expected = (
        monthly[
            "complaints"
        ]
        .iloc[
            :3
        ]
        .mean()
    )

    actual = (
        monthly[
            "rolling_complaints"
        ]
        .iloc[
            2
        ]
    )

    assert math.isclose(
        actual,
        expected,
    )
