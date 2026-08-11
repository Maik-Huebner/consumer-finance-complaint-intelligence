"""Business-oriented exploratory metrics for CFPB complaint data."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

MISSING_ISSUE_LABEL = "Issue not provided"

DOMINANT_PRODUCT = (
    "Credit reporting or other personal consumer reports"
)


def _text_values(
    series: pd.Series,
) -> pd.Series:
    """Return nullable strings for reliable comparisons across pandas dtypes."""
    return series.astype(
        "string"
    )


def _different_text(
    left: pd.Series,
    right: pd.Series,
) -> pd.Series:
    """Compare textual Series while treating paired missing values as equal."""
    left_text = (
        _text_values(
            left
        )
        .fillna(
            "<missing>"
        )
    )

    right_text = (
        _text_values(
            right
        )
        .fillna(
            "<missing>"
        )
    )

    return left_text.ne(
        right_text
    )


def executive_kpis(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return a compact KPI table for the full analysis window."""
    total = len(
        df
    )

    timely_rate = (
        float(
            df[
                "is_timely"
            ].mean()
        )
        if total
        else np.nan
    )

    narrative_rate = (
        float(
            df[
                "has_narrative"
            ].mean()
        )
        if total
        else np.nan
    )

    median_days = (
        float(
            df[
                "days_to_company"
            ].median()
        )
        if total
        else np.nan
    )

    values = {
        "complaints": total,
        "unique_companies": int(
            df[
                "company"
            ].nunique(
                dropna=True
            )
        ),
        "unique_products": int(
            df[
                "harmonized_product"
            ].nunique(
                dropna=True
            )
        ),
        "timely_response_rate": timely_rate,
        "narrative_share": narrative_rate,
        "median_days_to_company": median_days,
    }

    return pd.DataFrame(
        {
            "metric": values.keys(),
            "value": values.values(),
        }
    )


def yearly_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate complaint volume and response metrics by calendar year."""
    grouped = (
        df.groupby(
            "year",
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            ),
            timely_response_rate=(
                "is_timely",
                "mean",
            ),
            narrative_share=(
                "has_narrative",
                "mean",
            ),
            unique_companies=(
                "company",
                "nunique",
            ),
        )
        .reset_index()
        .sort_values(
            "year"
        )
    )

    grouped[
        "yoy_growth"
    ] = (
        grouped[
            "complaints"
        ]
        .pct_change()
    )

    return grouped


def monthly_summary(
    df: pd.DataFrame,
    rolling_window: int = 12,
) -> pd.DataFrame:
    """Aggregate monthly metrics and a full-window rolling complaint mean."""
    monthly = (
        df.groupby(
            "year_month",
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            ),
            timely_response_rate=(
                "is_timely",
                "mean",
            ),
            narrative_share=(
                "has_narrative",
                "mean",
            ),
        )
        .reset_index()
        .sort_values(
            "year_month"
        )
    )

    monthly[
        "rolling_complaints"
    ] = (
        monthly[
            "complaints"
        ]
        .rolling(
            rolling_window,
            min_periods=rolling_window,
        )
        .mean()
    )

    return monthly


def product_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create harmonized product-level volume and response metrics."""
    total = len(
        df
    )

    summary = (
        df.groupby(
            "harmonized_product",
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            ),
            timely_response_rate=(
                "is_timely",
                "mean",
            ),
            narrative_share=(
                "has_narrative",
                "mean",
            ),
            unique_companies=(
                "company",
                "nunique",
            ),
        )
        .reset_index()
        .rename(
            columns={
                "harmonized_product": "product",
            }
        )
    )

    summary[
        "complaint_share"
    ] = (
        summary[
            "complaints"
        ]
        / total
        if total
        else np.nan
    )

    return (
        summary.sort_values(
            "complaints",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )


def product_year_matrix(
    df: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return yearly counts for the highest-volume harmonized products."""
    top_products = (
        product_summary(
            df
        )
        .head(
            top_n
        )[
            "product"
        ]
    )

    filtered = df[
        df[
            "harmonized_product"
        ].isin(
            top_products
        )
    ]

    matrix = (
        filtered.pivot_table(
            index="harmonized_product",
            columns="year",
            values="complaint_id",
            aggfunc="count",
            fill_value=0,
            observed=True,
        )
        .reindex(
            top_products
        )
    )

    matrix.index.name = (
        "product"
    )

    return matrix


def issue_hotspots(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Rank harmonized product-issue combinations and change over time."""
    base = (
        df.groupby(
            [
                "harmonized_product",
                "harmonized_issue",
            ],
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            ),
            timely_response_rate=(
                "is_timely",
                "mean",
            ),
            narrative_share=(
                "has_narrative",
                "mean",
            ),
        )
        .reset_index()
        .rename(
            columns={
                "harmonized_product": "product",
                "harmonized_issue": "issue",
            }
        )
    )

    years = sorted(
        df[
            "year"
        ]
        .dropna()
        .unique()
    )

    if len(
        years
    ) >= 2:
        first_year = years[
            0
        ]

        last_year = years[
            -1
        ]

        counts = (
            df[
                df[
                    "year"
                ].isin(
                    [
                        first_year,
                        last_year,
                    ]
                )
            ]
            .groupby(
                [
                    "harmonized_product",
                    "harmonized_issue",
                    "year",
                ],
                observed=True,
            )[
                "complaint_id"
            ]
            .count()
            .unstack(
                fill_value=0
            )
            .rename(
                columns={
                    first_year: "first_year_count",
                    last_year: "last_year_count",
                }
            )
        )

        for column in (
            "first_year_count",
            "last_year_count",
        ):
            if column not in counts:
                counts[
                    column
                ] = 0

        counts[
            "growth_first_to_last"
        ] = np.where(
            counts[
                "first_year_count"
            ]
            > 0,
            (
                counts[
                    "last_year_count"
                ]
                / counts[
                    "first_year_count"
                ]
                - 1
            ),
            np.nan,
        )

        counts = (
            counts.reset_index()
            .rename(
                columns={
                    "harmonized_product": "product",
                    "harmonized_issue": "issue",
                }
            )
        )

        base = base.merge(
            counts,
            on=[
                "product",
                "issue",
            ],
            how="left",
        )

    else:
        base[
            "first_year_count"
        ] = np.nan

        base[
            "last_year_count"
        ] = np.nan

        base[
            "growth_first_to_last"
        ] = np.nan

    return (
        base.sort_values(
            "complaints",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )


def company_timeliness(
    df: pd.DataFrame,
    minimum_complaints: int = 1000,
) -> pd.DataFrame:
    """Create exploratory company-level response-timeliness metrics."""
    summary = (
        df.groupby(
            "company",
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            ),
            timely_response_rate=(
                "is_timely",
                "mean",
            ),
            products=(
                "harmonized_product",
                "nunique",
            ),
        )
        .reset_index()
    )

    summary = summary[
        summary[
            "complaints"
        ]
        >= minimum_complaints
    ]

    return (
        summary.sort_values(
            [
                "timely_response_rate",
                "complaints",
            ],
            ascending=[
                True,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )


def data_cleaning_summary(
    df: pd.DataFrame,
) -> dict[str, int | float]:
    """Summarize explicit missing-value handling used by the EDA."""
    total = len(
        df
    )

    source_missing_issue = (
        df[
            "issue"
        ]
        .isna()
    )

    handled_issue = (
        source_missing_issue
        & (
            _text_values(
                df[
                    "harmonized_issue"
                ]
            )
            .eq(
                MISSING_ISSUE_LABEL
            )
            .fillna(
                False
            )
        )
    )

    missing_count = int(
        source_missing_issue.sum()
    )

    handled_count = int(
        handled_issue.sum()
    )

    unhandled_count = (
        missing_count
        - handled_count
    )

    return {
        "rows": total,
        "source_missing_issue_rows": missing_count,
        "source_missing_issue_share": (
            float(
                missing_count
                / total
            )
            if total
            else np.nan
        ),
        "missing_issue_rows_handled": handled_count,
        "missing_issue_rows_unhandled": unhandled_count,
    }


def taxonomy_harmonization_summary(
    df: pd.DataFrame,
) -> dict[str, int | float]:
    """Summarize documented taxonomy changes separately from data cleaning."""
    total = len(
        df
    )

    product_present = (
        df[
            "product"
        ]
        .notna()
    )

    issue_present = (
        df[
            "issue"
        ]
        .notna()
    )

    product_changed = (
        _different_text(
            df[
                "product"
            ],
            df[
                "harmonized_product"
            ],
        )
        & product_present
    )

    issue_changed = (
        _different_text(
            df[
                "issue"
            ],
            df[
                "harmonized_issue"
            ],
        )
        & issue_present
    )

    any_changed = (
        product_changed
        | issue_changed
    )

    if total:
        product_share = float(
            product_changed.mean()
        )

        issue_share = float(
            issue_changed.mean()
        )

        any_share = float(
            any_changed.mean()
        )

    else:
        product_share = np.nan
        issue_share = np.nan
        any_share = np.nan

    return {
        "rows": total,
        "product_rows_changed": int(
            product_changed.sum()
        ),
        "product_change_share": product_share,
        "issue_rows_changed": int(
            issue_changed.sum()
        ),
        "issue_change_share": issue_share,
        "any_rows_changed": int(
            any_changed.sum()
        ),
        "any_change_share": any_share,
    }


def taxonomy_audit(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create an auditable source-to-analytical classification table."""
    product_rows = pd.DataFrame(
        {
            "source_value": _text_values(
                df[
                    "product"
                ]
            ),
            "harmonized_value": _text_values(
                df[
                    "harmonized_product"
                ]
            ),
            "complaint_id": df[
                "complaint_id"
            ],
        }
    )

    product_audit = (
        product_rows.groupby(
            [
                "source_value",
                "harmonized_value",
            ],
            dropna=False,
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            )
        )
        .reset_index()
    )

    product_audit.insert(
        0,
        "dimension",
        "product",
    )

    product_audit.insert(
        1,
        "context_product",
        pd.Series(
            pd.NA,
            index=product_audit.index,
            dtype="string",
        ),
    )

    issue_rows = pd.DataFrame(
        {
            "context_product": _text_values(
                df[
                    "harmonized_product"
                ]
            ),
            "source_value": _text_values(
                df[
                    "issue"
                ]
            ),
            "harmonized_value": _text_values(
                df[
                    "harmonized_issue"
                ]
            ),
            "complaint_id": df[
                "complaint_id"
            ],
        }
    )

    issue_audit = (
        issue_rows.groupby(
            [
                "context_product",
                "source_value",
                "harmonized_value",
            ],
            dropna=False,
            observed=True,
        )
        .agg(
            complaints=(
                "complaint_id",
                "count",
            )
        )
        .reset_index()
    )

    issue_audit.insert(
        0,
        "dimension",
        "issue",
    )

    text_columns = [
        "dimension",
        "context_product",
        "source_value",
        "harmonized_value",
    ]

    for column in (
        text_columns
    ):
        product_audit[
            column
        ] = (
            product_audit[
                column
            ]
            .astype(
                "string"
            )
        )

        issue_audit[
            column
        ] = (
            issue_audit[
                column
            ]
            .astype(
                "string"
            )
        )

    audit = pd.concat(
        [
            product_audit,
            issue_audit,
        ],
        ignore_index=True,
    )

    audit[
        "changed"
    ] = (
        audit[
            "source_value"
        ]
        .fillna(
            "<missing>"
        )
        .ne(
            audit[
                "harmonized_value"
            ]
            .fillna(
                "<missing>"
            )
        )
    )

    source_missing = (
        audit[
            "source_value"
        ]
        .isna()
    )

    audit[
        "change_type"
    ] = pd.Series(
        "unchanged",
        index=audit.index,
        dtype="string",
    )

    audit.loc[
        audit[
            "changed"
        ]
        & ~source_missing,
        "change_type",
    ] = (
        "taxonomy_harmonization"
    )

    audit.loc[
        audit[
            "changed"
        ]
        & source_missing,
        "change_type",
    ] = (
        "missing_value_handling"
    )

    return (
        audit.sort_values(
            [
                "changed",
                "dimension",
                "complaints",
            ],
            ascending=[
                False,
                True,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )


def monthly_correlations(
    monthly: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate Pearson and Spearman associations on monthly aggregates."""
    pairs = [
        (
            "complaints",
            "timely_response_rate",
        ),
        (
            "complaints",
            "narrative_share",
        ),
        (
            "timely_response_rate",
            "narrative_share",
        ),
    ]

    rows = []

    for x, y in (
        pairs
    ):
        subset = (
            monthly[
                [
                    x,
                    y,
                ]
            ]
            .dropna()
        )

        if (
            len(
                subset
            )
            < 3
            or subset[
                x
            ].nunique()
            < 2
            or subset[
                y
            ].nunique()
            < 2
        ):
            rows.append(
                {
                    "x": x,
                    "y": y,
                    "pearson_r": np.nan,
                    "pearson_p": np.nan,
                    "spearman_rho": np.nan,
                    "spearman_p": np.nan,
                }
            )

            continue

        pearson = pearsonr(
            subset[
                x
            ],
            subset[
                y
            ],
        )

        spearman = spearmanr(
            subset[
                x
            ],
            subset[
                y
            ],
        )

        rows.append(
            {
                "x": x,
                "y": y,
                "pearson_r": pearson.statistic,
                "pearson_p": pearson.pvalue,
                "spearman_rho": spearman.statistic,
                "spearman_p": spearman.pvalue,
            }
        )

    return pd.DataFrame(
        rows
    )


def linear_time_trend(
    monthly: pd.DataFrame,
) -> dict[str, float]:
    """Fit a descriptive straight-line trend to monthly complaint counts."""
    if len(
        monthly
    ) < 2:
        return {
            "monthly_slope": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
        }

    x = (
        np.arange(
            len(
                monthly
            ),
            dtype=float,
        )
        .reshape(
            -1,
            1,
        )
    )

    y = (
        monthly[
            "complaints"
        ]
        .to_numpy(
            dtype=float
        )
    )

    model = (
        LinearRegression()
        .fit(
            x,
            y,
        )
    )

    predictions = (
        model.predict(
            x
        )
    )

    return {
        "monthly_slope": float(
            model.coef_[
                0
            ]
        ),
        "intercept": float(
            model.intercept_
        ),
        "r2": float(
            r2_score(
                y,
                predictions,
            )
        ),
    }


def segment_yearly_summary(
    df: pd.DataFrame,
    focus_product: str = DOMINANT_PRODUCT,
) -> pd.DataFrame:
    """Compare yearly portfolio volume with and without a dominant product."""
    focus_mask = (
        _text_values(
            df[
                "harmonized_product"
            ]
        )
        .eq(
            focus_product
        )
        .fillna(
            False
        )
    )

    total_counts = (
        df.groupby(
            "year",
            observed=True,
        )
        .size()
        .sort_index()
    )

    focus_counts = (
        focus_mask.astype(
            "int8"
        )
        .groupby(
            df[
                "year"
            ],
            observed=True,
        )
        .sum()
        .reindex(
            total_counts.index,
            fill_value=0,
        )
    )

    result = pd.DataFrame(
        {
            "year": total_counts.index,
            "total_complaints": (
                total_counts
                .to_numpy(
                    dtype="int64"
                )
            ),
            "focus_product_complaints": (
                focus_counts
                .to_numpy(
                    dtype="int64"
                )
            ),
        }
    )

    result[
        "without_focus_product"
    ] = (
        result[
            "total_complaints"
        ]
        - result[
            "focus_product_complaints"
        ]
    )

    result[
        "focus_product_share"
    ] = np.where(
        result[
            "total_complaints"
        ]
        > 0,
        (
            result[
                "focus_product_complaints"
            ]
            / result[
                "total_complaints"
            ]
        ),
        np.nan,
    )

    return (
        result.sort_values(
            "year"
        )
        .reset_index(
            drop=True
        )
    )


def _correlation_record(
    correlations: pd.DataFrame,
    x: str,
    y: str,
) -> dict[str, float | None]:
    """Extract a JSON-friendly correlation record for one variable pair."""
    row = correlations[
        (
            correlations[
                "x"
            ]
            == x
        )
        & (
            correlations[
                "y"
            ]
            == y
        )
    ]

    if row.empty:
        return {
            "pearson_r": None,
            "pearson_p": None,
            "spearman_rho": None,
            "spearman_p": None,
        }

    values = row.iloc[
        0
    ]

    result: dict[
        str,
        float | None,
    ] = {}

    for key in (
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p",
    ):
        value = values[
            key
        ]

        result[
            key
        ] = (
            None
            if pd.isna(
                value
            )
            else float(
                value
            )
        )

    return result


def segment_sensitivity_summary(
    df: pd.DataFrame,
    monthly_all: pd.DataFrame,
    yearly_sensitivity: pd.DataFrame | None = None,
    focus_product: str = DOMINANT_PRODUCT,
) -> dict[str, object]:
    """Quantify how a dominant product affects aggregate trends and correlations."""
    yearly = (
        yearly_sensitivity
        if yearly_sensitivity is not None
        else segment_yearly_summary(
            df,
            focus_product,
        )
    )

    focus_mask = (
        _text_values(
            df[
                "harmonized_product"
            ]
        )
        .eq(
            focus_product
        )
        .fillna(
            False
        )
    )

    without_focus = df.loc[
        ~focus_mask,
        [
            "year_month",
            "complaint_id",
            "is_timely",
            "has_narrative",
        ],
    ]

    monthly_without = monthly_summary(
        without_focus
    )

    total_correlations = monthly_correlations(
        monthly_all
    )

    without_correlations = monthly_correlations(
        monthly_without
    )

    total_trend = linear_time_trend(
        monthly_all
    )

    without_trend = linear_time_trend(
        monthly_without
    )

    first = yearly.iloc[
        0
    ]

    last = yearly.iloc[
        -1
    ]

    total_growth = (
        float(
            last[
                "total_complaints"
            ]
            / first[
                "total_complaints"
            ]
            - 1
        )
        if first[
            "total_complaints"
        ]
        else None
    )

    without_growth = (
        float(
            last[
                "without_focus_product"
            ]
            / first[
                "without_focus_product"
            ]
            - 1
        )
        if first[
            "without_focus_product"
        ]
        else None
    )

    total_slope = float(
        total_trend[
            "monthly_slope"
        ]
    )

    without_slope = float(
        without_trend[
            "monthly_slope"
        ]
    )

    focus_slope = (
        total_slope
        - without_slope
    )

    slope_share = (
        float(
            focus_slope
            / total_slope
        )
        if (
            np.isfinite(
                total_slope
            )
            and total_slope
            != 0
        )
        else None
    )

    pairs = {
        "complaints_vs_timely_response_rate": (
            "complaints",
            "timely_response_rate",
        ),
        "complaints_vs_narrative_share": (
            "complaints",
            "narrative_share",
        ),
        "timely_response_rate_vs_narrative_share": (
            "timely_response_rate",
            "narrative_share",
        ),
    }

    correlation_comparison = {}

    for name, (
        x,
        y,
    ) in pairs.items():
        correlation_comparison[
            name
        ] = {
            "all": _correlation_record(
                total_correlations,
                x,
                y,
            ),
            "without_focus_product": _correlation_record(
                without_correlations,
                x,
                y,
            ),
        }

    return {
        "focus_product": focus_product,
        "first_year": int(
            first[
                "year"
            ]
        ),
        "last_year": int(
            last[
                "year"
            ]
        ),
        "focus_share_first_year": float(
            first[
                "focus_product_share"
            ]
        ),
        "focus_share_last_year": float(
            last[
                "focus_product_share"
            ]
        ),
        "focus_share_change_percentage_points": float(
            (
                last[
                    "focus_product_share"
                ]
                - first[
                    "focus_product_share"
                ]
            )
            * 100
        ),
        "total_complaints_first_year": int(
            first[
                "total_complaints"
            ]
        ),
        "total_complaints_last_year": int(
            last[
                "total_complaints"
            ]
        ),
        "without_focus_complaints_first_year": int(
            first[
                "without_focus_product"
            ]
        ),
        "without_focus_complaints_last_year": int(
            last[
                "without_focus_product"
            ]
        ),
        "total_growth_first_to_last": total_growth,
        "without_focus_growth_first_to_last": without_growth,
        "total_monthly_slope": total_slope,
        "without_focus_monthly_slope": without_slope,
        "focus_monthly_slope": float(
            focus_slope
        ),
        "focus_share_of_total_linear_slope": slope_share,
        "total_trend_r2": float(
            total_trend[
                "r2"
            ]
        ),
        "without_focus_trend_r2": float(
            without_trend[
                "r2"
            ]
        ),
        "correlations": correlation_comparison,
    }
