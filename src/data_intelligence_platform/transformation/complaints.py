"""Transform raw CFPB complaint data into an analysis-ready Parquet table."""

from __future__ import annotations

from pathlib import Path

import polars as pl

SOURCE_TO_PROJECT = {
    "Date received": "date_received",
    "Product": "product",
    "Sub-product": "sub_product",
    "Issue": "issue",
    "Consumer complaint narrative": "consumer_narrative",
    "Company": "company",
    "State": "state",
    "Submitted via": "submitted_via",
    "Date sent to company": "date_sent_to_company",
    "Company response to consumer": "company_response",
    "Timely response?": "timely_response",
    "Complaint ID": "complaint_id",
}

EXPECTED_SOURCE_COLUMNS = set(SOURCE_TO_PROJECT)

TAXONOMY_CHANGE_DATE = "2023-08-24"

MISSING_ISSUE_LABEL = "Issue not provided"

LEGACY_CREDIT_REPORTING_PRODUCT = (
    "Credit reporting, credit repair services, "
    "or other personal consumer reports"
)

CREDIT_REPORTING_PRODUCT = (
    "Credit reporting or other personal consumer reports"
)

DEBT_MANAGEMENT_PRODUCT = (
    "Debt or credit management"
)

MONEY_SERVICE_PRODUCT = (
    "Money transfer, virtual currency, or money service"
)

LEGACY_CARD_PRODUCT = (
    "Credit card or prepaid card"
)

CREDIT_CARD_PRODUCT = (
    "Credit card"
)

PREPAID_CARD_PRODUCT = (
    "Prepaid card"
)

PAYDAY_ADVANCE_PRODUCT = (
    "Payday loan, title loan, personal loan, or advance loan"
)

LEGACY_PAYDAY_PRODUCTS = [
    "Payday loan, title loan, or personal loan",
    "Payday loan, personal loan, or title loan",
]

CREDIT_CARD_SUBPRODUCTS = [
    "General-purpose credit card or charge card",
    "Store credit card",
]

PREPAID_CARD_SUBPRODUCTS = [
    "General-purpose prepaid card",
    "Gift card",
    "Payroll card",
    "Government benefit card",
    "Student prepaid card",
]

OLD_CREDIT_INVESTIGATION_ISSUE = (
    "Problem with a credit reporting company's "
    "investigation into an existing problem"
)

CURRENT_CREDIT_INVESTIGATION_ISSUE = (
    "Problem with a company's investigation into an existing problem"
)

PROCESSED_COLUMNS = [
    "complaint_id",
    "date_received",
    "year",
    "month",
    "year_month",
    "quarter",
    "taxonomy_version",
    "product",
    "sub_product",
    "issue",
    "harmonized_product",
    "harmonized_issue",
    "company",
    "state",
    "submitted_via",
    "date_sent_to_company",
    "days_to_company",
    "company_response",
    "timely_response",
    "is_timely",
    "has_narrative",
]


def _clean_text(
    column: str,
) -> pl.Expr:
    """Trim surrounding whitespace while preserving null values."""
    return (
        pl.col(column)
        .cast(
            pl.String,
            strict=False,
        )
        .str.strip_chars()
    )


def _harmonized_product_expr() -> pl.Expr:
    """Return a canonical product classification across CFPB taxonomies.

    Original product values remain unchanged. The additional harmonized field
    maps documented taxonomy moves and revisions onto comparable categories
    for longitudinal exploratory analysis.
    """
    product = pl.col(
        "product"
    )

    sub_product = pl.col(
        "sub_product"
    )

    return (
        pl.when(
            (
                product
                == LEGACY_CREDIT_REPORTING_PRODUCT
            )
            & (
                sub_product
                == "Credit repair services"
            )
        )
        .then(
            pl.lit(
                DEBT_MANAGEMENT_PRODUCT
            )
        )
        .when(
            product
            == LEGACY_CREDIT_REPORTING_PRODUCT
        )
        .then(
            pl.lit(
                CREDIT_REPORTING_PRODUCT
            )
        )
        .when(
            (
                product
                == MONEY_SERVICE_PRODUCT
            )
            & (
                sub_product
                == "Debt settlement"
            )
        )
        .then(
            pl.lit(
                DEBT_MANAGEMENT_PRODUCT
            )
        )
        .when(
            (
                product
                == MONEY_SERVICE_PRODUCT
            )
            & (
                sub_product
                == "Refund anticipation check"
            )
        )
        .then(
            pl.lit(
                PAYDAY_ADVANCE_PRODUCT
            )
        )
        .when(
            product.is_in(
                LEGACY_PAYDAY_PRODUCTS
            )
        )
        .then(
            pl.lit(
                PAYDAY_ADVANCE_PRODUCT
            )
        )
        .when(
            (
                product
                == LEGACY_CARD_PRODUCT
            )
            & sub_product.is_in(
                CREDIT_CARD_SUBPRODUCTS
            )
        )
        .then(
            pl.lit(
                CREDIT_CARD_PRODUCT
            )
        )
        .when(
            (
                product
                == LEGACY_CARD_PRODUCT
            )
            & sub_product.is_in(
                PREPAID_CARD_SUBPRODUCTS
            )
        )
        .then(
            pl.lit(
                PREPAID_CARD_PRODUCT
            )
        )
        .otherwise(
            product
        )
        .alias(
            "harmonized_product"
        )
    )


def _harmonized_issue_expr() -> pl.Expr:
    """Return a cleaned and taxonomy-harmonized analytical issue label.

    Missing source issues remain null in the original ``issue`` field. Only
    the analytical ``harmonized_issue`` field receives the explicit
    ``Issue not provided`` label so missing data are visible in aggregations
    instead of being silently discarded.
    """
    harmonized_product = pl.col(
        "harmonized_product"
    )

    issue = pl.col(
        "issue"
    )

    return (
        pl.when(
            (
                harmonized_product
                == CREDIT_REPORTING_PRODUCT
            )
            & (
                issue
                == OLD_CREDIT_INVESTIGATION_ISSUE
            )
        )
        .then(
            pl.lit(
                CURRENT_CREDIT_INVESTIGATION_ISSUE
            )
        )
        .when(
            (
                harmonized_product
                == DEBT_MANAGEMENT_PRODUCT
            )
            & (
                issue
                == "Unexpected or other fees"
            )
        )
        .then(
            pl.lit(
                "Charged up-front or unexpected fees"
            )
        )
        .when(
            (
                harmonized_product
                == DEBT_MANAGEMENT_PRODUCT
            )
            & (
                issue
                == "Fraud or scam"
            )
        )
        .then(
            pl.lit(
                "Didn't provide services promised"
            )
        )
        .otherwise(
            issue
        )
        .fill_null(
            MISSING_ISSUE_LABEL
        )
        .alias(
            "harmonized_issue"
        )
    )


def build_lazy_transform(
    csv_path: Path,
    *,
    analysis_start: str,
    analysis_end: str,
) -> pl.LazyFrame:
    """Build the lazy transformation query for CFPB complaint data.

    The raw CSV is scanned lazily so projection and date filtering can be
    pushed into the execution plan before the multi-million-row result is
    materialized.
    """
    lf = pl.scan_csv(
        csv_path,
        infer_schema_length=10_000,
        ignore_errors=False,
        null_values=[
            "",
            "N/A",
            "NA",
        ],
        schema_overrides={
            "Complaint ID": pl.String,
        },
    )

    available = set(
        lf.collect_schema()
        .names()
    )

    missing = (
        EXPECTED_SOURCE_COLUMNS
        - available
    )

    if missing:
        raise ValueError(
            "Source data are missing required columns: "
            f"{sorted(missing)}"
        )

    lf = lf.select(
        [
            pl.col(source)
            .alias(target)
            for source, target
            in SOURCE_TO_PROJECT.items()
        ]
    )

    text_columns = [
        "product",
        "sub_product",
        "issue",
        "consumer_narrative",
        "company",
        "state",
        "submitted_via",
        "company_response",
        "timely_response",
        "complaint_id",
    ]

    lf = lf.with_columns(
        pl.col(
            "date_received"
        ).str.to_date(
            strict=False
        ),
        pl.col(
            "date_sent_to_company"
        ).str.to_date(
            strict=False
        ),
        *[
            _clean_text(
                column
            ).alias(
                column
            )
            for column
            in text_columns
        ],
    )

    start = (
        pl.lit(
            analysis_start
        )
        .str.to_date()
    )

    end = (
        pl.lit(
            analysis_end
        )
        .str.to_date()
    )

    taxonomy_change = (
        pl.lit(
            TAXONOMY_CHANGE_DATE
        )
        .str.to_date()
    )

    lf = (
        lf.filter(
            pl.col(
                "date_received"
            ).is_between(
                start,
                end,
                closed="both",
            )
        )
        .with_columns(
            pl.col(
                "date_received"
            )
            .dt.year()
            .alias(
                "year"
            ),
            pl.col(
                "date_received"
            )
            .dt.month()
            .alias(
                "month"
            ),
            pl.col(
                "date_received"
            )
            .dt.truncate(
                "1mo"
            )
            .alias(
                "year_month"
            ),
            (
                pl.col(
                    "date_received"
                )
                .dt.year()
                .cast(
                    pl.String
                )
                + pl.lit(
                    "-Q"
                )
                + pl.col(
                    "date_received"
                )
                .dt.quarter()
                .cast(
                    pl.String
                )
            ).alias(
                "quarter"
            ),
            (
                pl.col(
                    "date_sent_to_company"
                )
                - pl.col(
                    "date_received"
                )
            )
            .dt.total_days()
            .alias(
                "days_to_company"
            ),
            (
                pl.col(
                    "consumer_narrative"
                )
                .is_not_null()
                & (
                    pl.col(
                        "consumer_narrative"
                    )
                    .str.len_chars()
                    > 0
                )
            ).alias(
                "has_narrative"
            ),
            (
                pl.col(
                    "timely_response"
                )
                == "Yes"
            ).alias(
                "is_timely"
            ),
            pl.when(
                pl.col(
                    "date_received"
                )
                < taxonomy_change
            )
            .then(
                pl.lit(
                    "pre_aug_2023"
                )
            )
            .otherwise(
                pl.lit(
                    "aug_2023_or_later"
                )
            )
            .alias(
                "taxonomy_version"
            ),
        )
        .with_columns(
            _harmonized_product_expr(),
        )
        .with_columns(
            _harmonized_issue_expr(),
        )
        .select(
            PROCESSED_COLUMNS
        )
    )

    return lf


def transform_complaints(
    csv_path: Path,
    output_path: Path,
    *,
    analysis_start: str,
    analysis_end: str,
) -> Path:
    """Stream the transformed dataset directly into compressed Parquet."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lf = build_lazy_transform(
        csv_path,
        analysis_start=analysis_start,
        analysis_end=analysis_end,
    )

    # Streaming directly to Parquet prevents the complete transformed dataset
    # from having to reside in memory before it is written.
    lf.sink_parquet(
        output_path,
        compression="zstd",
        statistics=True,
    )

    return output_path
