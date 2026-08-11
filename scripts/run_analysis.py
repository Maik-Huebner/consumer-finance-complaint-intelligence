#!/usr/bin/env python3
"""Run EDA, create analytical tables, figures, and executive reporting."""

from __future__ import annotations

import json

import pandas as pd

from data_intelligence_platform.analysis.metrics import (
    DOMINANT_PRODUCT,
    company_timeliness,
    data_cleaning_summary,
    executive_kpis,
    issue_hotspots,
    linear_time_trend,
    monthly_correlations,
    monthly_summary,
    product_summary,
    product_year_matrix,
    segment_sensitivity_summary,
    segment_yearly_summary,
    taxonomy_audit,
    taxonomy_harmonization_summary,
    yearly_summary,
)
from data_intelligence_platform.analysis.report import (
    write_executive_summary,
)
from data_intelligence_platform.utils.paths import (
    ensure_project_directories,
    load_config,
    resolve_project_path,
)
from data_intelligence_platform.validation.quality import (
    validate_dataframe,
)
from data_intelligence_platform.visualization.charts import (
    plot_issue_hotspots,
    plot_monthly_trend,
    plot_product_mix,
    plot_product_timeliness,
    plot_product_year_heatmap,
    plot_segment_sensitivity,
    write_interactive_dashboard,
)

ANALYSIS_COLUMNS = [
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
]

CATEGORICAL_COLUMNS = [
    "product",
    "issue",
    "harmonized_product",
    "harmonized_issue",
    "taxonomy_version",
    "company",
    "company_response",
    "timely_response",
]


def main() -> None:
    """Execute the complete exploratory analysis workflow."""
    config = load_config()

    ensure_project_directories(
        config
    )

    project = config[
        "project"
    ]

    data = config[
        "data"
    ]

    processed_path = (
        resolve_project_path(
            data[
                "processed_dir"
            ]
        )
        / data[
            "processed_filename"
        ]
    )

    if not processed_path.exists():
        raise FileNotFoundError(
            "Processed data not found: "
            f"{processed_path}. "
            "Run scripts/run_pipeline.py first."
        )

    reports_dir = resolve_project_path(
        data[
            "reports_dir"
        ]
    )

    figures_dir = resolve_project_path(
        data[
            "figures_dir"
        ]
    )

    print(
        "Loading analysis columns from processed Parquet ..."
    )

    df = pd.read_parquet(
        processed_path,
        columns=ANALYSIS_COLUMNS,
        engine="pyarrow",
        dtype_backend="pyarrow",
    )

    df[
        "date_received"
    ] = pd.to_datetime(
        df[
            "date_received"
        ]
    )

    df[
        "date_sent_to_company"
    ] = pd.to_datetime(
        df[
            "date_sent_to_company"
        ]
    )

    df[
        "year_month"
    ] = pd.to_datetime(
        df[
            "year_month"
        ]
    )

    for column in (
        CATEGORICAL_COLUMNS
    ):
        df[
            column
        ] = (
            df[
                column
            ]
            .astype(
                "category"
            )
        )

    memory_mb = (
        df.memory_usage(
            index=True,
            deep=True,
        ).sum()
        / 1024**2
    )

    print(
        f"Loaded {len(df):,} complaints "
        f"using approximately "
        f"{memory_mb:,.1f} MiB."
    )

    print(
        "Running data-quality validation ..."
    )

    quality = validate_dataframe(
        df
    )

    (
        reports_dir
        / "data_quality_report.json"
    ).write_text(
        json.dumps(
            quality.to_dict(),
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        "Calculating data-cleaning and taxonomy audits ..."
    )

    cleaning = data_cleaning_summary(
        df
    )

    taxonomy = taxonomy_harmonization_summary(
        df
    )

    taxonomy_mapping = taxonomy_audit(
        df
    )

    (
        reports_dir
        / "data_cleaning_summary.json"
    ).write_text(
        json.dumps(
            cleaning,
            indent=2,
        ),
        encoding="utf-8",
    )

    (
        reports_dir
        / "taxonomy_harmonization_summary.json"
    ).write_text(
        json.dumps(
            taxonomy,
            indent=2,
        ),
        encoding="utf-8",
    )

    taxonomy_mapping.to_csv(
        reports_dir
        / "taxonomy_harmonization_audit.csv",
        index=False,
    )

    print(
        "Calculating business and EDA metrics ..."
    )

    kpis = executive_kpis(
        df
    )

    yearly = yearly_summary(
        df
    )

    monthly = monthly_summary(
        df,
        project[
            "rolling_window_months"
        ],
    )

    product = product_summary(
        df
    )

    hotspots = issue_hotspots(
        df
    )

    companies = company_timeliness(
        df,
        project[
            "minimum_company_complaints"
        ],
    )

    correlations = monthly_correlations(
        monthly
    )

    trend = linear_time_trend(
        monthly
    )

    matrix = product_year_matrix(
        df,
        project[
            "top_n_products"
        ],
    )

    print(
        "Calculating segment sensitivity analysis ..."
    )

    sensitivity_yearly = segment_yearly_summary(
        df,
        DOMINANT_PRODUCT,
    )

    sensitivity = segment_sensitivity_summary(
        df,
        monthly,
        yearly_sensitivity=sensitivity_yearly,
        focus_product=DOMINANT_PRODUCT,
    )

    print(
        "Writing analytical tables ..."
    )

    kpis.to_csv(
        reports_dir
        / "kpi_summary.csv",
        index=False,
    )

    yearly.to_csv(
        reports_dir
        / "yearly_summary.csv",
        index=False,
    )

    monthly.to_csv(
        reports_dir
        / "monthly_trends.csv",
        index=False,
    )

    product.to_csv(
        reports_dir
        / "product_summary.csv",
        index=False,
    )

    hotspots.to_csv(
        reports_dir
        / "issue_hotspots.csv",
        index=False,
    )

    companies.to_csv(
        reports_dir
        / "company_timeliness.csv",
        index=False,
    )

    correlations.to_csv(
        reports_dir
        / "monthly_correlations.csv",
        index=False,
    )

    (
        reports_dir
        / "linear_trend.json"
    ).write_text(
        json.dumps(
            trend,
            indent=2,
        ),
        encoding="utf-8",
    )

    sensitivity_yearly.to_csv(
        reports_dir
        / "segment_sensitivity_yearly.csv",
        index=False,
    )

    (
        reports_dir
        / "segment_sensitivity_summary.json"
    ).write_text(
        json.dumps(
            sensitivity,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        "Creating static figures and interactive dashboard ..."
    )

    plot_monthly_trend(
        monthly,
        figures_dir
        / "01_monthly_complaints.png",
    )

    plot_product_mix(
        product,
        figures_dir
        / "02_product_mix.png",
        project[
            "top_n_products"
        ],
    )

    plot_product_timeliness(
        product,
        figures_dir
        / "03_timely_response_by_product.png",
        project[
            "top_n_products"
        ],
    )

    plot_issue_hotspots(
        hotspots,
        figures_dir
        / "04_issue_hotspots.png",
        project[
            "top_n_issues"
        ],
    )

    plot_product_year_heatmap(
        matrix,
        figures_dir
        / "05_product_year_heatmap.png",
    )

    plot_segment_sensitivity(
        sensitivity_yearly,
        figures_dir
        / "06_credit_reporting_sensitivity.png",
        focus_label="Credit Reporting",
    )

    write_interactive_dashboard(
        monthly,
        product,
        reports_dir
        / "interactive_dashboard.html",
        sensitivity_yearly=sensitivity_yearly,
        focus_label="Credit Reporting",
    )

    print(
        "Writing executive summary ..."
    )

    write_executive_summary(
        output_path=(
            reports_dir
            / "executive_summary.md"
        ),
        yearly=yearly,
        product=product,
        hotspots=hotspots,
        trend=trend,
        correlations=correlations,
        cleaning=cleaning,
        taxonomy=taxonomy,
        quality_passed=quality.passed,
        sensitivity=sensitivity,
    )

    print(
        "Analysis complete. "
        f"Reports written to {reports_dir}"
    )

    if not quality.passed:
        print(
            "WARNING: Data-quality checks reported findings. "
            "Review data_quality_report.json."
        )


if __name__ == "__main__":
    main()
