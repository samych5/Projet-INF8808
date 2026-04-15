import plotly.graph_objects as go
import pandas as pd
from dash import dcc
import numpy as np

from utils.graph_display import add_layer_to_figure

from .steps_config import GraphConfig, get_step_graph_config
from .hover_template import make_hover_component
from .variables import *

COLORS = {Genres.MEN: "#1a6fdb", Genres.WOMEN: "#ff1493"}


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


def create_figure(df: pd.DataFrame, config: GraphConfig) -> go.Figure:
    col_x = config.col_x
    label_x = AXES_X.get(ColX(config.col_x), col_x)

    fig = go.Figure()

    np.random.seed(42)
    jitter = np.random.uniform(-0.25, 0.25, size=len(df))

    for genre in Genres:
        if genre.value not in config.visible_genres:
            continue

        color = COLORS[genre]
        mask = df["Genre"] == genre.value
        sub = df[mask]
        j = jitter[mask.values]

        fig.add_trace(
            go.Scatter(
                x=sub[col_x] + j,
                y=sub["Exam_Score"],
                mode="markers",
                name=genre.value,
                marker=dict(
                    color=color,
                    size=5,
                    opacity=0.45,
                    line=dict(width=0),
                ),
                hovertemplate=make_hover_component(label_x, genre.value),
            )
        )

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
            itemclick=False if not config.enable_interactions else "toggle",
            itemdoubleclick=False if not config.enable_interactions else "toggleothers",
        ),
        margin=dict(l=60, r=20, t=60, b=60),
        hovermode="closest",
        xaxis=dict(
            tickvals=sorted(df[col_x].dropna().unique().tolist()),
        ),
        transition=dict(duration=0),
        dragmode=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e8e0d0",
        zeroline=False,
        linecolor="#1a1a1a",
        linewidth=1.5,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e8e0d0",
        zeroline=False,
        linecolor="#1a1a1a",
        linewidth=1.5,
    )

    for layer in config.layers:
        layer.apply(fig, df, config)

    return fig