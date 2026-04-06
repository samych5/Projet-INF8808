import plotly.graph_objects as go
import pandas as pd
from dash import dcc

from .steps_config import GraphConfig, get_step_graph_config
from .hover_template import make_hover_component
from .variables import *

COLORS = {Genres.MEN: "#1a6fdb", Genres.WOMEN: "#ff1493"}

def make_initial_graph(
    df: pd.DataFrame,
):
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

def create_figure(
    df: pd.DataFrame,
    config: GraphConfig,
) -> go.Figure:
    label_x = AXES_X.get(config.col_x)
    fig = go.Figure()

    vals = df[config.col_symbol].dropna().unique()
    val_oui = vals[0]
    val_non = vals[1] if len(vals) > 1 else vals[0]

    for genre in Genres:
        if genre.value not in config.visible_genres:
            continue

        color = COLORS[genre]

        for val, symbol, opacity, show in [
            (val_oui, "circle", 0.65, True),
            (val_non, "circle", 0.20, False),
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
                    symbol=symbol,
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
            name=str(val_oui),
            marker=dict(color="grey", symbol="circle", size=7, opacity=0.65),
        ))
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            name=str(val_non),
            marker=dict(color="grey", symbol="circle", size=7, opacity=0.20),
        ))

    fig.update_layout(
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
        margin=dict(l=60, r=20, t=20, b=60),
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

    # for layer in config.layers:
    #     add_layer_to_figure(fig, layer)

    return fig
