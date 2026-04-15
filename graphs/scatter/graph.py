import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc

from .steps_config import GraphConfig, get_step_graph_config
from .hover_template import make_hover_component
from .variables import *

COLORS = {Genres.MEN: "#1a6fdb", Genres.WOMEN: "#ff1493"}

SYMBOL_LEGEND_LABELS = {
    SymbolVar.EXTRACURRICULAR_ACTIVITIES: ("Pratique activité parascolaire", "Ne pratique pas"),
    SymbolVar.INTERNET_ACCESS: ("Accès internet", "Pas d'accès internet"),
    SymbolVar.LEARNING_DISORDER: ("Troubles d'apprentissage", "Pas de troubles"),
}

AXES_X_LABELS = {
    ColX.HOURS_STUDIED.value: "Heures d'études",
    ColX.ATTENDANCE.value: "Taux de présence en classe (%)",
}


def make_initial_graph(df: pd.DataFrame):
    return dcc.Graph(
        id=ID["graph"],
        figure=create_figure(df, get_step_graph_config(0)),
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "doubleClick": False,
        },
        className="graph",
    )


def _add_trend_line(fig, df, config):
    x = pd.to_numeric(df[config.col_x], errors="coerce")
    y = pd.to_numeric(df["Exam_Score"], errors="coerce")
    mask = x.notna() & y.notna()
    x = x[mask].to_numpy()
    y = y[mask].to_numpy()

    if len(x) < 2:
        return

    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.array([x.min(), x.max()])
    y_line = slope * x_line + intercept

    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name="Tendance",
        line=dict(color="black", width=2.5),
        showlegend=True,
    ))


def create_figure(df: pd.DataFrame, config: GraphConfig) -> go.Figure:
    label_x = AXES_X_LABELS.get(config.col_x, config.col_x)
    fig = go.Figure()

    col_symbol_enum = next((s for s in SymbolVar if s.value == config.col_symbol), None)
    legend_labels = SYMBOL_LEGEND_LABELS.get(col_symbol_enum, (config.col_symbol + " Oui", config.col_symbol + " Non"))
    label_oui, label_non = legend_labels

    vals = df[config.col_symbol].dropna().unique()
    val_oui = vals[0]
    val_non = vals[1] if len(vals) > 1 else vals[0]

    for genre in Genres:
        if genre.value not in config.visible_genres:
            continue

        color = COLORS[genre]

        for val, opacity, show in [
            (val_oui, 0.65, True),
            (val_non, 0.20, False),
        ]:
            mask = (df["Genre"] == genre.value) & (df[config.col_symbol] == val)
            sub = df[mask]

            fig.add_trace(go.Scatter(
                x=sub[config.col_x],
                y=sub["Exam_Score"],
                mode="markers",
                name=genre.value,
                showlegend=show,
                legendgroup=genre.value,
                marker=dict(
                    color=color,
                    symbol="circle",
                    size=7,
                    opacity=opacity,
                    line=dict(width=1.4, color=color),
                ),
                hovertemplate=make_hover_component(
                    label_x,
                    genre.value,
                    str(val),
                    SYMBOL_VAR_LABELS.get(config.col_symbol)
                ),
            ))

    if config.show_legend:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            name=label_oui,
            marker=dict(color="grey", symbol="circle", size=7, opacity=0.65),
        ))
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            name=label_non,
            marker=dict(color="grey", symbol="circle", size=7, opacity=0.20),
        ))

    _add_trend_line(fig, df, config)

    fig.update_layout(
        title=dict(
            text=config.title_graph,
            x=0.5,
            xanchor="center",
            font=dict(size=15),
        ),
        xaxis_title=label_x,
        yaxis_title="Note finale",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="DM Sans, Arial", size=13, color="#1a1a1a"),
        showlegend=config.show_legend,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d8d0c0",
            borderwidth=1,
        ),
        legend_itemclick=False if not config.enable_interactions else "toggle",
        legend_itemdoubleclick=False if not config.enable_interactions else "toggleothers",
        margin=dict(l=60, r=20, t=60, b=60),
        hovermode="closest",
        xaxis=dict(
            tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 44]
            if config.col_x == ColX.HOURS_STUDIED.value
            else [60, 65, 70, 75, 80, 85, 90, 95, 100],
        ),
        transition=dict(duration=0),
        dragmode=False,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e8e0d0",
        zeroline=False,
        linecolor="#1a1a1a",
        linewidth=1.5
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e8e0d0",
        zeroline=False,
        linecolor="#1a1a1a",
        linewidth=1.5
    )

    return fig