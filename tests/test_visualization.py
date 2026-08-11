from __future__ import annotations

import pandas as pd

from data_intelligence_platform.visualization.charts import (
    _prepare_top_product_rows,
    plot_issue_hotspots,
    plot_product_timeliness,
    plot_product_year_heatmap,
)


def test_issue_hotspot_plot_accepts_categorical_dimensions(
    tmp_path,
):
    """Categorical analysis dimensions must remain plottable."""
    hotspots = pd.DataFrame(
        {
            "product": pd.Categorical(
                [
                    "Credit reporting",
                    "Debt collection",
                ]
            ),
            "issue": pd.Categorical(
                [
                    "Incorrect information",
                    "Attempts to collect debt",
                ]
            ),
            "complaints": [
                1500,
                900,
            ],
        }
    )

    output_path = (
        tmp_path
        / "issue_hotspots.png"
    )

    plot_issue_hotspots(
        hotspots,
        output_path,
        top_n=2,
    )

    assert output_path.exists()

    assert (
        output_path.stat().st_size
        > 0
    )


def test_heatmap_accepts_arrow_backed_numeric_values(
    tmp_path,
):
    """Arrow-backed pivot values and zero cells must remain plottable."""
    matrix = pd.DataFrame(
        {
            2022: pd.array(
                [
                    1500,
                    0,
                ],
                dtype="int64[pyarrow]",
            ),
            2023: pd.array(
                [
                    1750,
                    1100,
                ],
                dtype="int64[pyarrow]",
            ),
            2024: pd.array(
                [
                    2100,
                    1350,
                ],
                dtype="int64[pyarrow]",
            ),
            2025: pd.array(
                [
                    2450,
                    1600,
                ],
                dtype="int64[pyarrow]",
            ),
        },
        index=[
            "Credit reporting",
            "Debt collection",
        ],
    )

    output_path = (
        tmp_path
        / "product_year_heatmap.png"
    )

    plot_product_year_heatmap(
        matrix,
        output_path,
    )

    assert output_path.exists()

    assert (
        output_path.stat().st_size
        > 0
    )


def test_top_product_plot_data_limits_unused_categories():
    """Top-N plotting data must not retain unused categorical levels."""
    product_names = [
        f"Product {index}"
        for index in range(
            1,
            12,
        )
    ]

    product = pd.DataFrame(
        {
            "product": pd.Categorical(
                product_names,
                categories=[
                    *product_names,
                    "Unused category",
                ],
            ),
            "complaints": [
                1100,
                1000,
                900,
                800,
                700,
                600,
                500,
                400,
                300,
                200,
                100,
            ],
            "timely_response_rate": [
                0.99,
                0.98,
                0.97,
                0.96,
                0.95,
                0.94,
                0.93,
                0.92,
                0.91,
                0.90,
                0.89,
            ],
        }
    )

    top = _prepare_top_product_rows(
        product,
        10,
        sort_by="complaints",
        ascending=False,
    )

    assert len(
        top
    ) == 10

    assert (
        top[
            "product"
        ]
        .nunique()
        == 10
    )

    assert (
        "Product 11"
        not in set(
            top[
                "product"
            ]
        )
    )

    assert (
        "Unused category"
        not in set(
            top[
                "product"
            ]
        )
    )

    assert not isinstance(
        top[
            "product"
        ].dtype,
        pd.CategoricalDtype,
    )


def test_timeliness_plot_accepts_categorical_products(
    tmp_path,
):
    """Timeliness plotting must work after limiting categorical products."""
    product_names = [
        f"Product {index}"
        for index in range(
            1,
            12,
        )
    ]

    product = pd.DataFrame(
        {
            "product": pd.Categorical(
                product_names,
                categories=[
                    *product_names,
                    "Unused category",
                ],
            ),
            "complaints": [
                1100,
                1000,
                900,
                800,
                700,
                600,
                500,
                400,
                300,
                200,
                100,
            ],
            "timely_response_rate": [
                0.999,
                0.995,
                0.990,
                0.985,
                0.980,
                0.975,
                0.970,
                0.965,
                0.960,
                0.955,
                0.950,
            ],
        }
    )

    output_path = (
        tmp_path
        / "timeliness.png"
    )

    plot_product_timeliness(
        product,
        output_path,
        top_n=10,
    )

    assert output_path.exists()

    assert (
        output_path.stat().st_size
        > 0
    )
