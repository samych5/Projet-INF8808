import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dcc

from .steps_config import get_step_graph_config
from .variables import (
    FactorCategory,
    FACTOR_LABELS,
    FACTOR_CATEGORIES,
)

TARGET_COLUMN = "Exam_Score"
PALE_BLUE = "rgb(230,240,255)"

CATEGORY_PATTERN = {
    FactorCategory.STUDENT: "",
    FactorCategory.PARENTS: ".",
    FactorCategory.SCHOOL: "/",
}

def _encode_column(df: pd.DataFrame, col: str) -> pd.Series:
    unique_vals = df[col].dropna().unique()

    if len(unique_vals) == 2:
        return df[col].map({unique_vals[0]: 0, unique_vals[1]: 1})

    if set(unique_vals) <= {"Low", "Medium", "High"}:
        return df[col].map({"Low": 1, "Medium": 2, "High": 3})

    return df[col].astype("category").cat.codes


def _compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for col in FACTOR_CATEGORIES:
        if col not in df.columns or col == TARGET_COLUMN:
            continue

        series = df[[col, TARGET_COLUMN]].dropna()

        if series.empty:
            continue

        if pd.api.types.is_numeric_dtype(series[col]):
            corr = series[col].corr(series[TARGET_COLUMN])
        else:
            encoded = _encode_column(series, col)
            corr = encoded.corr(series[TARGET_COLUMN])

        if pd.isna(corr):
            continue

        results.append(
            {
                "variable": col,
                "label": FACTOR_LABELS.get(col, col),
                "category": FACTOR_CATEGORIES[col],
                "impact": corr,
            }
        )

    if not results:
        return pd.DataFrame(columns=["variable", "label", "category", "impact"])

    return pd.DataFrame(results).sort_values("impact", ascending=True)


def _get_diverging_colors(values: pd.Series) -> list[str]:
    if values.empty:
        return []

    max_val = max(abs(values.min()), abs(values.max()))
    colors = []

    for v in values:
        norm = abs(v) / max_val if max_val != 0 else 0
        norm = min(norm, 1) * 0.85

        if v >= 0:
            r = int(230 - 200 * norm)
            g = int(240 - 200 * norm)
            b = 255
        else:
            r = 255
            g = int(240 - 200 * norm)
            b = int(230 - 200 * norm)

        colors.append(f"rgb({r},{g},{b})")

    return colors


def _rgb_to_rgba(rgb_color: str, alpha: float) -> str:
    cleaned = rgb_color.replace("rgb(", "").replace(")", "")
    r, g, b = [part.strip() for part in cleaned.split(",")]
    return f"rgba({r},{g},{b},{alpha})"


def _get_patterns(categories: pd.Series) -> list[str]:
    return [CATEGORY_PATTERN.get(category, "") for category in categories]


def _get_bar_colors(impact_df: pd.DataFrame, config) -> list[str]:
    base_colors = _get_diverging_colors(impact_df["impact"])
    final_colors = []

    for i, (_, row) in enumerate(impact_df.iterrows()):
        variable = row["variable"]

        is_bright = True
        if config is not None and hasattr(config, "factor_brightness"):
            is_bright = config.factor_brightness.get(variable, True)

        if is_bright:
            final_colors.append(base_colors[i])
        else:
            final_colors.append(_rgb_to_rgba(base_colors[i], 0.25))

    return final_colors


def _get_line_colors(impact_df: pd.DataFrame, config) -> list[str]:
    line_colors = []

    for _, row in impact_df.iterrows():
        variable = row["variable"]

        is_bright = True
        if config is not None and hasattr(config, "factor_brightness"):
            is_bright = config.factor_brightness.get(variable, True)

        if is_bright:
            line_colors.append("rgba(0,0,0,0.45)")
        else:
            line_colors.append("rgba(0,0,0,0.15)")

    return line_colors


def _get_text_colors(impact_df: pd.DataFrame, config) -> list[str]:
    text_colors = []

    for _, row in impact_df.iterrows():
        variable = row["variable"]

        is_bright = True
        if config is not None and hasattr(config, "factor_brightness"):
            is_bright = config.factor_brightness.get(variable, True)

        if is_bright:
            text_colors.append("rgba(20,40,80,1)")
        else:
            text_colors.append("rgba(20,40,80,0.35)")

    return text_colors


def _add_colorbar_trace(fig: go.Figure):
    fig.add_trace(
        go.Scatter(
            x=[None, None, None],
            y=[None, None, None],
            mode="markers",
            marker=dict(
                size=10,
                colorscale=[
                    [0, "rgb(180,0,0)"],
                    [0.5, "rgb(230,240,255)"],
                    [1, "rgb(0,50,150)"],
                ],
                cmin=-1,
                cmax=0.75,
                color=[-1, 0, 0.75],
                showscale=True,
                colorbar=dict(
                    title="Corrélation",
                    tickvals=[-1, 0, 0.75],
                    ticktext=[
                        "Fortement négative",
                        "Faible",
                        "Fortement positive",
                    ],
                ),
            ),
            showlegend=False,
            hoverinfo="skip",
        )
    )


def _add_category_legend(fig: go.Figure):
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker=dict(
                color=PALE_BLUE,
                pattern=dict(shape=CATEGORY_PATTERN[FactorCategory.STUDENT]),
            ),
            name=FactorCategory.STUDENT.value,
            showlegend=True,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker=dict(
                color=PALE_BLUE,
                pattern=dict(shape=CATEGORY_PATTERN[FactorCategory.PARENTS]),
            ),
            name=FactorCategory.PARENTS.value,
            showlegend=True,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker=dict(
                color=PALE_BLUE,
                pattern=dict(shape=CATEGORY_PATTERN[FactorCategory.SCHOOL]),
            ),
            name=FactorCategory.SCHOOL.value,
            showlegend=True,
            hoverinfo="skip",
        )
    )


def create_figure(df: pd.DataFrame, config=None) -> go.Figure:
    impact_df = _compute_correlations(df)

    if config is not None and hasattr(config, "visible_factors"):
        impact_df = impact_df[
            impact_df["variable"].isin(config.visible_factors)
        ].copy()

    fig = go.Figure()

    if impact_df.empty:
        fig.update_layout(
            title="Prévisualisation",
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Corrélation avec la note finale",
            yaxis_title="Variables",
        )
        return fig

    colors = _get_bar_colors(impact_df, config)
    line_colors = _get_line_colors(impact_df, config)
    text_colors = _get_text_colors(impact_df, config)
    patterns = _get_patterns(impact_df["category"])

    fig.add_trace(
        go.Bar(
            x=impact_df["impact"],
            y=impact_df["label"],
            orientation="h",
            showlegend=False,
            marker=dict(
                color=colors,
                pattern=dict(
                    shape=patterns,
                    size=6,
                    solidity=0.25,
                ),
                line=dict(
                    color=line_colors,
                    width=0.5,
                ),
            ),
            text=impact_df["impact"].round(2),
            textposition=["outside" for _ in impact_df["impact"]],
            insidetextanchor="middle",
            textfont=dict(color=text_colors),
            hoverinfo="skip"
        )
    )

    if config is None or getattr(config, "show_color_scale", True):
        _add_colorbar_trace(fig)

    if config is None or getattr(config, "show_legend", True):
        _add_category_legend(fig)

    fig.update_layout(
        title="Impact des facteurs sur la performance scolaire",
        xaxis_title="Corrélation avec la note finale",
        yaxis_title="Variables",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=180, r=120, t=80, b=50),
        autosize=True,
        bargap=0.1,
        legend=dict(
            orientation="h",
            y=-0.18,
            yanchor="top",
            x=0.5,
            xanchor="center",
            title="",
            font=dict(size=14),
            itemsizing="constant",
        ),
        transition=dict(duration=0),
        dragmode=False,
    )

    x_range = config.x_range if config is not None and hasattr(config, "x_range") else [-1, 1]
    if x_range == [0, 1]:
        tick_vals = [0, 0.25, 0.5, 0.75, 1]
        tick_text = ["0", "0.25", "0.5", "0.75", "1"]
    else:
        tick_vals = [-1, -0.5, 0, 0.5, 1]
        tick_text = ["-1", "-0.5", "0", "0.5", "1"]

    fig.update_xaxes(
        showgrid=False,
        range=x_range,
        zeroline=True,
        zerolinecolor="rgba(0,0,0,0.25)",
        zerolinewidth=1,
        layer="below traces",
        tickvals=tick_vals,
        ticktext=tick_text,
    )

    fig.update_yaxes(
        showgrid=False,
        automargin=True,
    )

    return fig