"""Static and interactive visualizations for the complaint EDA."""

from __future__ import annotations

from pathlib import Path
from textwrap import fill

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib.colors import LogNorm
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import FuncFormatter, PercentFormatter

sns.set_theme(
    style="whitegrid",
    context="talk",
)

PRODUCT_DISPLAY_NAMES = {
    "Credit reporting or other personal consumer reports": (
        "Credit Reporting"
    ),
    "Debt collection": (
        "Debt Collection"
    ),
    "Credit card": (
        "Credit Card"
    ),
    "Checking or savings account": (
        "Checking / Savings"
    ),
    "Money transfer, virtual currency, or money service": (
        "Money Transfer / Virtual Currency"
    ),
    "Mortgage": (
        "Mortgage"
    ),
    "Vehicle loan or lease": (
        "Vehicle Loan / Lease"
    ),
    "Student loan": (
        "Student Loan"
    ),
    "Payday loan, title loan, personal loan, or advance loan": (
        "Payday / Title / Personal Loan"
    ),
    "Prepaid card": (
        "Prepaid Card"
    ),
    "Debt or credit management": (
        "Debt / Credit Management"
    ),
}


def _save(
    fig: plt.Figure,
    path: Path,
) -> None:
    """Save a tight, high-resolution figure and close it."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )


def _format_integer_de(
    value: float | int,
) -> str:
    """Format an integer value with German thousands separators."""
    return (
        f"{float(value):,.0f}"
        .replace(
            ",",
            ".",
        )
    )


def _format_compact_number_de(
    value: float,
    _position: object | None = None,
) -> str:
    """Format large chart-axis values without scientific notation."""
    absolute = abs(
        value
    )

    if absolute >= 1_000_000:
        number = (
            f"{value / 1_000_000:.1f}"
            .replace(
                ".",
                ",",
            )
            .rstrip(
                "0"
            )
            .rstrip(
                ","
            )
        )

        return (
            f"{number} Mio."
        )

    if absolute >= 1_000:
        number = (
            f"{value / 1_000:.0f}"
        )

        return (
            f"{number} Tsd."
        )

    return _format_integer_de(
        value
    )


def _display_product_name(
    value: object,
) -> str:
    """Return a concise chart-only label without changing source data."""
    if pd.isna(
        value
    ):
        return (
            "Produkt nicht angegeben"
        )

    text = str(
        value
    )

    return PRODUCT_DISPLAY_NAMES.get(
        text,
        text,
    )


def _prepare_top_product_rows(
    product: pd.DataFrame,
    top_n: int,
    *,
    sort_by: str,
    ascending: bool,
) -> pd.DataFrame:
    """Return exactly the top-N volume products without unused categories."""
    top = (
        product.sort_values(
            "complaints",
            ascending=False,
        )
        .head(
            top_n
        )
        .copy()
    )

    top[
        "product"
    ] = (
        top[
            "product"
        ]
        .astype(
            "string"
        )
        .fillna(
            "Produkt nicht angegeben"
        )
        .astype(
            object
        )
    )

    top[
        sort_by
    ] = pd.to_numeric(
        top[
            sort_by
        ],
        errors="coerce",
    )

    return (
        top.sort_values(
            sort_by,
            ascending=ascending,
        )
        .reset_index(
            drop=True
        )
    )


def _weighted_portfolio_rate(
    product: pd.DataFrame,
) -> float:
    """Calculate the complaint-weighted portfolio timely-response rate."""
    complaints = pd.to_numeric(
        product[
            "complaints"
        ],
        errors="coerce",
    )

    rates = pd.to_numeric(
        product[
            "timely_response_rate"
        ],
        errors="coerce",
    )

    valid = (
        complaints.notna()
        & rates.notna()
        & (
            complaints
            > 0
        )
    )

    if not valid.any():
        return float(
            "nan"
        )

    return float(
        (
            complaints[
                valid
            ]
            * rates[
                valid
            ]
        ).sum()
        / complaints[
            valid
        ].sum()
    )


def plot_monthly_trend(
    monthly: pd.DataFrame,
    path: Path,
) -> None:
    """Plot monthly complaint counts and the full-window rolling average."""
    fig, ax = plt.subplots(
        figsize=(
            13,
            6,
        )
    )

    ax.plot(
        monthly[
            "year_month"
        ],
        monthly[
            "complaints"
        ],
        alpha=0.45,
        label="Monatliche Beschwerden",
    )

    ax.plot(
        monthly[
            "year_month"
        ],
        monthly[
            "rolling_complaints"
        ],
        linewidth=2.5,
        label="Rollierender 12-Monats-Durchschnitt",
    )

    ax.set(
        title="Entwicklung der veröffentlichten CFPB-Beschwerden",
        xlabel="Monat",
        ylabel="Anzahl Beschwerden",
    )

    if not monthly.empty:
        ax.set_xlim(
            monthly[
                "year_month"
            ].min(),
            monthly[
                "year_month"
            ].max(),
        )

    ax.xaxis.set_major_locator(
        MonthLocator(
            bymonth=[
                1,
                7,
            ]
        )
    )

    ax.xaxis.set_major_formatter(
        DateFormatter(
            "%Y-%m"
        )
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            _format_compact_number_de
        )
    )

    ax.legend()

    sns.despine(
        ax=ax
    )

    _save(
        fig,
        path,
    )


def plot_product_mix(
    product: pd.DataFrame,
    path: Path,
    top_n: int = 10,
) -> None:
    """Plot the highest-volume harmonized financial products."""
    top = _prepare_top_product_rows(
        product,
        top_n,
        sort_by="complaints",
        ascending=False,
    )

    fig, ax = plt.subplots(
        figsize=(
            12,
            7,
        )
    )

    order = top[
        "product"
    ].tolist()

    sns.barplot(
        data=top,
        x="complaints",
        y="product",
        order=order,
        ax=ax,
    )

    maximum = float(
        top[
            "complaints"
        ].max()
    )

    for patch, value in zip(
        ax.patches,
        top[
            "complaints"
        ],
        strict=True,
    ):
        ax.text(
            float(
                value
            )
            + maximum
            * 0.012,
            patch.get_y()
            + patch.get_height()
            / 2,
            _format_integer_de(
                value
            ),
            va="center",
            fontsize=10,
        )

    ax.set_xlim(
        0,
        maximum
        * 1.14,
    )

    ax.xaxis.set_major_formatter(
        FuncFormatter(
            _format_compact_number_de
        )
    )

    ax.set(
        title=f"Top {len(top)} Finanzprodukte nach Beschwerdevolumen",
        xlabel="Anzahl Beschwerden",
        ylabel="",
    )

    sns.despine(
        ax=ax
    )

    _save(
        fig,
        path,
    )


def plot_product_timeliness(
    product: pd.DataFrame,
    path: Path,
    top_n: int = 10,
) -> None:
    """Plot timely-response rates as a dot plot for high-volume products."""
    top = _prepare_top_product_rows(
        product,
        top_n,
        sort_by="timely_response_rate",
        ascending=True,
    )

    portfolio_rate = _weighted_portfolio_rate(
        product
    )

    fig, ax = plt.subplots(
        figsize=(
            12,
            7,
        )
    )

    y_positions = list(
        range(
            len(
                top
            )
        )
    )

    ax.scatter(
        top[
            "timely_response_rate"
        ],
        y_positions,
        s=90,
        zorder=3,
    )

    for y_position, rate in zip(
        y_positions,
        top[
            "timely_response_rate"
        ],
        strict=True,
    ):
        rate_value = float(
            rate
        )

        if rate_value >= 0.98:
            text_x = (
                rate_value
                - 0.003
            )

            horizontal_alignment = (
                "right"
            )

        else:
            text_x = (
                rate_value
                + 0.003
            )

            horizontal_alignment = (
                "left"
            )

        label = (
            f"{rate_value:.1%}"
            .replace(
                ".",
                ",",
            )
        )

        ax.text(
            text_x,
            y_position,
            label,
            va="center",
            ha=horizontal_alignment,
            fontsize=10,
        )

    if not pd.isna(
        portfolio_rate
    ):
        portfolio_label = (
            f"{portfolio_rate:.1%}"
            .replace(
                ".",
                ",",
            )
        )

        ax.axvline(
            portfolio_rate,
            linestyle="--",
            linewidth=1.6,
            label=(
                "Portfolio-Durchschnitt: "
                f"{portfolio_label}"
            ),
        )

    minimum_rate = float(
        top[
            "timely_response_rate"
        ].min()
    )

    lower_limit = max(
        0.0,
        minimum_rate
        - 0.05,
    )

    ax.set_xlim(
        lower_limit,
        1.005,
    )

    ax.set_yticks(
        y_positions,
        labels=top[
            "product"
        ].tolist(),
    )

    ax.invert_yaxis()

    ax.xaxis.set_major_formatter(
        PercentFormatter(
            xmax=1.0,
            decimals=0,
        )
    )

    ax.grid(
        axis="y",
        visible=False,
    )

    ax.set(
        title=(
            f"Timely-Response-Rate der Top {len(top)} Finanzprodukte\n"
            "Auswahl nach Beschwerdevolumen"
        ),
        xlabel="Timely-Response-Rate",
        ylabel="",
    )

    ax.legend(
        loc="lower right"
    )

    sns.despine(
        ax=ax
    )

    _save(
        fig,
        path,
    )


def plot_issue_hotspots(
    hotspots: pd.DataFrame,
    path: Path,
    top_n: int = 15,
) -> None:
    """Plot the largest harmonized product-issue combinations."""
    top = (
        hotspots.head(
            top_n
        )
        .copy()
    )

    product_labels = (
        top[
            "product"
        ]
        .astype(
            "string"
        )
        .fillna(
            "Produkt nicht angegeben"
        )
        .map(
            _display_product_name
        )
    )

    issue_labels = (
        top[
            "issue"
        ]
        .astype(
            "string"
        )
        .fillna(
            "Issue nicht angegeben"
        )
        .map(
            lambda value: fill(
                str(
                    value
                ),
                width=48,
            )
        )
    )

    top[
        "label"
    ] = (
        product_labels
        .astype(
            "string"
        )
        .str.cat(
            issue_labels,
            sep=" — ",
        )
        .astype(
            object
        )
    )

    top[
        "complaints"
    ] = pd.to_numeric(
        top[
            "complaints"
        ],
        errors="coerce",
    )

    top = (
        top.sort_values(
            "complaints",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )

    fig, ax = plt.subplots(
        figsize=(
            14,
            10,
        )
    )

    order = top[
        "label"
    ].tolist()

    sns.barplot(
        data=top,
        x="complaints",
        y="label",
        order=order,
        ax=ax,
    )

    maximum = float(
        top[
            "complaints"
        ].max()
    )

    for patch, value in zip(
        ax.patches,
        top[
            "complaints"
        ],
        strict=True,
    ):
        ax.text(
            float(
                value
            )
            + maximum
            * 0.01,
            patch.get_y()
            + patch.get_height()
            / 2,
            _format_integer_de(
                value
            ),
            va="center",
            fontsize=9,
        )

    ax.set_xlim(
        0,
        maximum
        * 1.14,
    )

    ax.xaxis.set_major_formatter(
        FuncFormatter(
            _format_compact_number_de
        )
    )

    ax.tick_params(
        axis="y",
        labelsize=10,
    )

    ax.set(
        title=(
            f"Top {len(top)} Produkt-Issue-Hotspots "
            "nach Beschwerdevolumen"
        ),
        xlabel="Anzahl Beschwerden",
        ylabel="",
    )

    sns.despine(
        ax=ax
    )

    _save(
        fig,
        path,
    )


def plot_product_year_heatmap(
    matrix: pd.DataFrame,
    path: Path,
) -> None:
    """Plot yearly complaint volume with a logarithmic color scale."""
    numeric_matrix = (
        matrix.apply(
            pd.to_numeric,
            errors="coerce",
        )
        .astype(
            "float64"
        )
    )

    display_matrix = numeric_matrix.copy()

    display_matrix.index = [
        _display_product_name(
            value
        )
        for value in display_matrix.index
    ]

    annotations = (
        display_matrix.apply(
            lambda column: column.map(
                _format_integer_de
            )
        )
    )

    positive_values = (
        display_matrix.where(
            display_matrix
            > 0
        )
        .stack()
        .astype(
            "float64"
        )
    )

    norm = None

    plot_matrix = (
        display_matrix.copy()
    )

    if not positive_values.empty:
        minimum = float(
            positive_values.min()
        )

        maximum = float(
            positive_values.max()
        )

        plot_matrix = (
            display_matrix.clip(
                lower=max(
                    minimum,
                    1.0,
                )
            )
        )

        if maximum > minimum:
            norm = LogNorm(
                vmin=max(
                    minimum,
                    1.0,
                ),
                vmax=maximum,
            )

    fig, ax = plt.subplots(
        figsize=(
            12,
            8,
        )
    )

    heatmap = sns.heatmap(
        plot_matrix,
        norm=norm,
        annot=annotations,
        fmt="",
        ax=ax,
        cbar_kws={
            "label": (
                "Anzahl Beschwerden "
                "(logarithmische Farbskala)"
            )
        },
    )

    colorbar = (
        heatmap.collections[
            0
        ]
        .colorbar
    )

    if colorbar is not None:
        colorbar.ax.yaxis.set_major_formatter(
            FuncFormatter(
                _format_compact_number_de
            )
        )

        colorbar.update_ticks()

    ax.set(
        title=(
            "Beschwerdevolumen nach Finanzprodukt und Jahr\n"
            "Farbskala logarithmisch, Zellwerte absolut"
        ),
        xlabel="Jahr",
        ylabel="Finanzprodukt",
    )

    ax.tick_params(
        axis="y",
        rotation=0,
    )

    _save(
        fig,
        path,
    )


def plot_segment_sensitivity(
    yearly: pd.DataFrame,
    path: Path,
    focus_label: str = "Credit Reporting",
) -> None:
    """Visualize the dominant-product sensitivity analysis by year."""
    fig, ax = plt.subplots(
        figsize=(
            12,
            7,
        )
    )

    ax.plot(
        yearly[
            "year"
        ],
        yearly[
            "total_complaints"
        ],
        marker="o",
        linewidth=2.5,
        label="Gesamtportfolio",
    )

    ax.plot(
        yearly[
            "year"
        ],
        yearly[
            "focus_product_complaints"
        ],
        marker="o",
        linewidth=2.5,
        label=focus_label,
    )

    ax.plot(
        yearly[
            "year"
        ],
        yearly[
            "without_focus_product"
        ],
        marker="o",
        linewidth=2.5,
        label=f"Portfolio ohne {focus_label}",
    )

    for _, row in yearly.iterrows():
        share = (
            f"{row['focus_product_share']:.1%}"
            .replace(
                ".",
                ",",
            )
        )

        ax.annotate(
            share,
            (
                row[
                    "year"
                ],
                row[
                    "focus_product_complaints"
                ],
            ),
            xytext=(
                0,
                12,
            ),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            bbox={
                "boxstyle": "round,pad=0.15",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.8,
            },
        )

    ax.set(
        title=(
            "Sensitivitätsanalyse: Einfluss von Credit Reporting "
            "auf das Beschwerdewachstum"
        ),
        xlabel="Jahr",
        ylabel="Anzahl Beschwerden",
    )

    ax.set_xticks(
        yearly[
            "year"
        ]
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            _format_compact_number_de
        )
    )

    ax.legend()

    sns.despine(
        ax=ax
    )

    _save(
        fig,
        path,
    )


def write_interactive_dashboard(
    monthly: pd.DataFrame,
    product: pd.DataFrame,
    output_path: Path,
    sensitivity_yearly: pd.DataFrame | None = None,
    focus_label: str = "Credit Reporting",
) -> None:
    """Write a standalone German HTML dashboard with Plotly charts."""
    line = px.line(
        monthly,
        x="year_month",
        y=[
            "complaints",
            "rolling_complaints",
        ],
        title=(
            "Monatliches Beschwerdevolumen "
            "und rollierender 12-Monats-Durchschnitt"
        ),
        labels={
            "value": "Anzahl Beschwerden",
            "year_month": "Monat",
            "variable": "Kennzahl",
        },
    )

    line.for_each_trace(
        lambda trace: trace.update(
            name={
                "complaints": "Monatliche Beschwerden",
                "rolling_complaints": (
                    "Rollierender 12-Monats-Durchschnitt"
                ),
            }.get(
                trace.name,
                trace.name,
            )
        )
    )

    bar_data = _prepare_top_product_rows(
        product,
        10,
        sort_by="complaints",
        ascending=True,
    )

    bar = px.bar(
        bar_data,
        x="complaints",
        y="product",
        orientation="h",
        hover_data={
            "complaint_share": ":.1%",
            "timely_response_rate": ":.1%",
            "narrative_share": ":.1%",
        },
        title=(
            "Top 10 Finanzprodukte nach "
            "Beschwerdevolumen"
        ),
        labels={
            "complaints": "Anzahl Beschwerden",
            "product": "Finanzprodukt",
            "complaint_share": "Beschwerdeanteil",
            "timely_response_rate": "Timely-Response-Rate",
            "narrative_share": "Narrative-Anteil",
        },
    )

    dashboard_parts = [
        (
            "<!doctype html>"
            "<html lang='de'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<meta name='viewport' "
            "content='width=device-width, initial-scale=1'>"
            "<title>"
            "Consumer Finance Complaint Intelligence"
            "</title>"
            "</head>"
            "<body>"
        ),
        (
            "<h1>"
            "Consumer Finance Complaint Intelligence"
            "</h1>"
        ),
        (
            "<p>"
            "Interaktives exploratives Dashboard für den "
            "konfigurierten CFPB-Analysezeitraum."
            "</p>"
        ),
        (
            "<p>"
            "Die dargestellten Beschwerdewerte sind nicht um "
            "Unternehmensgröße, Kundenbestand, Marktanteil oder "
            "Produkt-Exposure normalisiert."
            "</p>"
        ),
        line.to_html(
            full_html=False,
            include_plotlyjs="cdn",
        ),
        bar.to_html(
            full_html=False,
            include_plotlyjs=False,
        ),
    ]

    if (
        sensitivity_yearly is not None
        and not sensitivity_yearly.empty
    ):
        sensitivity_long = (
            sensitivity_yearly[
                [
                    "year",
                    "total_complaints",
                    "focus_product_complaints",
                    "without_focus_product",
                ]
            ]
            .rename(
                columns={
                    "total_complaints": "Gesamtportfolio",
                    "focus_product_complaints": focus_label,
                    "without_focus_product": (
                        f"Portfolio ohne {focus_label}"
                    ),
                }
            )
            .melt(
                id_vars="year",
                var_name="Segment",
                value_name="Beschwerden",
            )
        )

        sensitivity_figure = px.line(
            sensitivity_long,
            x="year",
            y="Beschwerden",
            color="Segment",
            markers=True,
            title=(
                "Sensitivitätsanalyse des "
                "Beschwerdewachstums"
            ),
            labels={
                "year": "Jahr",
                "Beschwerden": "Anzahl Beschwerden",
            },
        )

        dashboard_parts.extend(
            [
                (
                    "<h2>"
                    "Sensitivitätsanalyse"
                    "</h2>"
                ),
                (
                    "<p>"
                    "Die Segmentkontrolle zeigt, wie stark das "
                    "dominante Credit-Reporting-Segment die "
                    "aggregierte Portfolioentwicklung prägt."
                    "</p>"
                ),
                sensitivity_figure.to_html(
                    full_html=False,
                    include_plotlyjs=False,
                ),
            ]
        )

    dashboard_parts.append(
        "</body></html>"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        "\n".join(
            dashboard_parts
        ),
        encoding="utf-8",
    )
