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
        margin=dict(l=60, r=20, t=20, b=60),
        hovermode="closest",
        xaxis=dict(
            tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 44]
            if config.col_x ==  ColX.HOURS_STUDIED.value
            else [60, 65, 70, 75, 80, 85, 90, 95, 100],
        ),
        transition=dict(duration=0),
        dragmode=False
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

    for layer in config.layers:
        add_layer_to_figure(fig, layer)

    return fig


def add_layer_to_figure(fig: go.Figure, layer: dict):
    layer_type = layer.get("type")

    if layer_type == "circle":
        fig.add_shape(
            type="circle",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 3),
            ),
            fillcolor=layer.get("fillcolor", "rgba(0,0,0,0)"),
            opacity=layer.get("opacity", 1.0),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "rect":
        fig.add_shape(
            type="rect",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 2),
            ),
            fillcolor=layer.get("fillcolor", "rgba(255,0,0,0.08)"),
            opacity=layer.get("opacity", 1.0),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "line":
        fig.add_shape(
            type="line",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 2),
                dash=layer.get("dash", "solid"),
            ),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "annotation":
        fig.add_annotation(
            x=layer["x"],
            y=layer["y"],
            text=layer["text"],
            showarrow=layer.get("showarrow", True),
            arrowhead=layer.get("arrowhead", 2),
            ax=layer.get("ax", 0),
            ay=layer.get("ay", -40),
            font=layer.get("font", dict(size=13)),
        )

    elif layer_type == "scatter":
        fig.add_trace(go.Scatter(
            x=layer["x"],
            y=layer["y"],
            mode=layer.get("mode", "markers"),
            name=layer.get("name", ""),
            showlegend=layer.get("showlegend", False),
            marker=layer.get("marker", {}),
            line=layer.get("line", {}),
            text=layer.get("text"),
            hoverinfo=layer.get("hoverinfo", "skip"),
        ))
