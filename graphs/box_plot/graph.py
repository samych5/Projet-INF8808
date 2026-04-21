import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from utils.graph_display import add_layer_to_figure
from .steps_config import GraphConfig, get_step_graph_config
from .variables import *

MAPPING = {
    "Low": Levels.LOW.label,
    "Negative": Levels.LOW.label,
    "High School": Levels.LOW.label,

    "Medium": Levels.MEDIUM.label,
    "Neutral": Levels.MEDIUM.label,
    "College": Levels.MEDIUM.label,

    "High": Levels.HIGH.label,
    "Positive": Levels.HIGH.label,
    "Postgraduate": Levels.HIGH.label,
}

FEATURES = [
    "Parental_Education_Level",
    "Family_Income",
    "Parental_Involvement",
    "Access_to_Resources",
    "Teacher_Quality",
    "Peer_Influence",
]

ORDER_LEVEL = [level.label for level in Levels]

COLORS = {
    Levels.LOW.label: "#7FB3D5",
    Levels.MEDIUM.label: "#3F8FC4",
    Levels.HIGH.label: "#1F4E79",
}

LEVEL_OFFSETS = {
    Levels.LOW.label: -0.25,
    Levels.MEDIUM.label: 0.0,
    Levels.HIGH.label: 0.25,
}


def make_initial_graph(df: pd.DataFrame):
    return dcc.Graph(
        figure=create_figure(df, get_step_graph_config(0)),
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "doubleClick": False,
        },
        className="graph",
    )


def _format_factor_label(col: str) -> str:
    return (
        col.replace("_", " ")
        .replace("Parental Education Level", "Éducation Parents")
        .replace("Peer Influence", "Influence des Pairs")
        .replace("Family Income", "Revenu Familial")
        .replace("Parental Involvement", "Implication Parentale")
        .replace("Access to Resources", "Accès aux Ressources")
        .replace("Teacher Quality", "Qualité des Enseignants")
    )


def _build_unified_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    data_list = []

    for col in FEATURES:
        if col not in df.columns:
            continue

        temp_df = df[[col, "Exam_Score"]].dropna().copy()
        temp_df["Level"] = temp_df[col].map(MAPPING)
        temp_df["Facteur"] = _format_factor_label(col)
        temp_df = temp_df.dropna(subset=["Level"])

        data_list.append(temp_df[["Facteur", "Level", "Exam_Score"]])

    if not data_list:
        return pd.DataFrame(columns=["Facteur", "Level", "Exam_Score"])

    df_unified = pd.concat(data_list, ignore_index=True)

    facteur_order = [_format_factor_label(col) for col in FEATURES if col in df.columns]

    df_unified["Level"] = pd.Categorical(
        df_unified["Level"],
        categories=ORDER_LEVEL,
        ordered=True,
    )

    df_unified["Facteur"] = pd.Categorical(
        df_unified["Facteur"],
        categories=facteur_order,
        ordered=True,
    )

    return df_unified


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _to_rgba(hex_color: str, alpha: float) -> str:
    r, g, b = _hex_to_rgb(hex_color)
    return f"rgba({r}, {g}, {b}, {alpha})"


def create_figure(df: pd.DataFrame, config: GraphConfig) -> go.Figure:
    df_unified = _build_unified_dataframe(df)
    fig = go.Figure()

    if df_unified.empty:
        fig.update_layout(
            title="Aucune donnée disponible",
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        return fig

    df_plot = df_unified[
        df_unified["Facteur"].isin(config.visible_factors)
        & df_unified["Level"].isin(config.visible_levels)
    ].copy()

    if df_plot.empty:
        fig.update_layout(
            title="Aucune donnée disponible pour cette configuration",
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        return fig

    visible_factor_order = [
        factor
        for factor in df_unified["Facteur"].cat.categories
        if factor in config.visible_factors
    ]

    visible_level_order = [
        level
        for level in ORDER_LEVEL
        if level in config.visible_levels
    ]

    factor_positions = {
        factor: i for i, factor in enumerate(visible_factor_order)
    }

    first_bright_factor = next(
        (f for f in visible_factor_order if config.factor_brightness.get(f, True)),
        visible_factor_order[0]
    )

    for factor in visible_factor_order:
        is_bright = config.factor_brightness.get(factor, True)
        factor_df = df_plot[df_plot["Facteur"] == factor]
        factor_center = factor_positions[factor]

        for level in visible_level_order:
            sub = factor_df[factor_df["Level"] == level]

            if sub.empty:
                continue

            base_color = COLORS[level]

            if is_bright:
                line_color = base_color
                fill_color = _to_rgba(base_color, 0.55)
                point_color = _to_rgba(base_color, 0.95)
            else:
                line_color = _to_rgba("#999999", 0.35)
                fill_color = _to_rgba("#BBBBBB", 0.08)
                point_color = _to_rgba("#AAAAAA", 0.18)

            x_pos = factor_center + LEVEL_OFFSETS[level]
            x_values = [x_pos] * len(sub)

            fig.add_trace(
                go.Box(
                    x=x_values,
                    y=sub["Exam_Score"],
                    name=level,
                    legendgroup=level,
                    showlegend=(factor == first_bright_factor and config.show_legend),
                    width=0.22,
                    marker=dict(
                        color=point_color,
                        size=6,
                    ),
                    line=dict(
                        width=1.3,
                        color=line_color,
                    ),
                    fillcolor=fill_color,
                    boxmean=False,
                    boxpoints="outliers",
                    jitter=0,
                    pointpos=0,
                )
            )

    moyenne_globale = df["Exam_Score"].dropna().mean()

    fig.add_hline(
        y=moyenne_globale,
        line_dash="dash",
        line_color="red",
        opacity=0.6,
    )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Moyenne globale",
            showlegend=True,
        )
    )

    fig.update_layout(
        title=dict(
            text="Synthèse Environnementale : Influence sur la Réussite Scolaire",
            x=0.5,
            xanchor="center",
            font=dict(size=16),
        ),
        yaxis_title="Note à l'examen (%)",
        xaxis_title="",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12, color="#1a1a1a"),
        showlegend=config.show_legend,
        legend=dict(
            title="Niveau Socio-Environnemental",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d8d0c0",
            borderwidth=1,
        ),
        margin=dict(l=60, r=180, t=80, b=90),
        transition=dict(duration=0),
        dragmode=False
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(factor_positions.values()),
        ticktext=visible_factor_order,
        tickangle=15,
        showgrid=False,
        linecolor="#1a1a1a",
        linewidth=1.2,
        range=[-0.6, len(visible_factor_order) - 0.4],
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e8e8e8",
        zeroline=False,
        linecolor="#1a1a1a",
        linewidth=1.2,
    )

    for layer in config.layers:
        add_layer_to_figure(fig, layer)

    return fig