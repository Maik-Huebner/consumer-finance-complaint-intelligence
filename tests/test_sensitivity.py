from __future__ import annotations

import pandas as pd

from data_intelligence_platform.analysis.metrics import (
    DOMINANT_PRODUCT,
    monthly_summary,
    segment_sensitivity_summary,
    segment_yearly_summary,
)
from data_intelligence_platform.analysis.report import (
    _build_sensitivity_section,
)
from data_intelligence_platform.visualization.charts import (
    plot_segment_sensitivity,
)


def _sample_dataframe() -> pd.DataFrame:
    rows = []
    complaint_id = 1

    for month_index in range(
        12
    ):
        year = (
            2022
            if month_index < 6
            else 2023
        )

        month = (
            month_index + 1
            if month_index < 6
            else month_index - 5
        )

        year_month = pd.Timestamp(
            year=year,
            month=month,
            day=1,
        )

        focus_count = (
            5
            + month_index
            * 2
        )

        other_count = (
            8
            + month_index
            // 3
        )

        for index in range(
            focus_count
        ):
            rows.append(
                {
                    "complaint_id": str(
                        complaint_id
                    ),
                    "year": year,
                    "year_month": year_month,
                    "harmonized_product": DOMINANT_PRODUCT,
                    "is_timely": (
                        (
                            index
                            + month_index
                        )
                        % 10
                        != 0
                    ),
                    "has_narrative": (
                        index
                        % 4
                        == 0
                    ),
                }
            )

            complaint_id += 1

        for index in range(
            other_count
        ):
            rows.append(
                {
                    "complaint_id": str(
                        complaint_id
                    ),
                    "year": year,
                    "year_month": year_month,
                    "harmonized_product": "Other product",
                    "is_timely": (
                        (
                            index
                            + month_index
                        )
                        % 7
                        != 0
                    ),
                    "has_narrative": (
                        (
                            index
                            + month_index
                        )
                        % 3
                        == 0
                    ),
                }
            )

            complaint_id += 1

    return pd.DataFrame(
        rows
    )


def test_segment_sensitivity_detects_product_mix_shift():
    df = _sample_dataframe()

    yearly = segment_yearly_summary(
        df
    )

    monthly = monthly_summary(
        df
    )

    sensitivity = segment_sensitivity_summary(
        df,
        monthly,
        yearly_sensitivity=yearly,
    )

    assert (
        yearly[
            "focus_product_share"
        ].iloc[
            -1
        ]
        > yearly[
            "focus_product_share"
        ].iloc[
            0
        ]
    )

    assert (
        sensitivity[
            "focus_share_last_year"
        ]
        > sensitivity[
            "focus_share_first_year"
        ]
    )

    assert (
        sensitivity[
            "without_focus_complaints_first_year"
        ]
        > 0
    )

    assert (
        sensitivity[
            "without_focus_complaints_last_year"
        ]
        > 0
    )

    assert (
        "complaints_vs_narrative_share"
        in sensitivity[
            "correlations"
        ]
    )

    assert (
        "without_focus_product"
        in sensitivity[
            "correlations"
        ][
            "complaints_vs_narrative_share"
        ]
    )


def test_sensitivity_section_explains_aggregation_effect():
    df = _sample_dataframe()

    monthly = monthly_summary(
        df
    )

    sensitivity = segment_sensitivity_summary(
        df,
        monthly,
    )

    text = _build_sensitivity_section(
        sensitivity
    )

    assert (
        "## Sensitivitätsanalyse"
        in text
    )

    assert (
        "Produktmix"
        in text
    )

    assert (
        "Segment- beziehungsweise Kompositionseffekt"
        in text
    )

    assert (
        "nicht vorschnell als Simpson-Paradox"
        in text
    )

    assert (
        "Portfolio-Kennzahlen"
        in text
    )


def test_segment_sensitivity_plot_is_written(
    tmp_path,
):
    df = _sample_dataframe()

    yearly = segment_yearly_summary(
        df
    )

    output_path = (
        tmp_path
        / "sensitivity.png"
    )

    plot_segment_sensitivity(
        yearly,
        output_path,
    )

    assert output_path.exists()

    assert (
        output_path.stat().st_size
        > 0
    )
