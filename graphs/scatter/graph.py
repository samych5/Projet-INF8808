import plotly.graph_objects as go
import pandas as pd
from dash import dcc

from .ids import ID
from .graph_controller import AXES_X
from .hover_template import make_hover_component

COLORS = {"Homme": "#1a6fdb", "Femme": "#ff1493"}

SYMBOL_VAR_LABELS = {
    "Parascolaire":          "Parascolaire",
    "Acces_internet":        "Accès internet",
    "Troubles_apprentissage":"Troubles d'apprentissage",
}

def make_graph(
    df: pd.DataFrame,
    col_x: str = "Hours_Studied",
    col_symbol: str = "Parascolaire",
):
    return dcc.Graph(
        id=ID["graph"],
        figure=create_figure(df, col_x, col_symbol),
        config={"displayModeBar": False},
        className="graph",
    )

def create_figure(
    df: pd.DataFrame,
    col_x: str = "Hours_Studied",
    col_symbol: str = "Parascolaire",
    visible_genres: list[str] | None = None,
    show_legend: bool = True,
    layers: list[dict] | None = None,
) -> go.Figure:
    if visible_genres is None:
        visible_genres = ["Homme", "Femme"]

    if layers is None:
        layers = []

    label_x = AXES_X.get(col_x, col_x)
    fig = go.Figure()

    vals = df[col_symbol].dropna().unique()
    val_oui = vals[0]
    val_non = vals[1] if len(vals) > 1 else vals[0]

    for genre in ["Homme", "Femme"]:
        if genre not in visible_genres:
            continue

        color = COLORS[genre]

        for val, symbol, opacity, show in [
            (val_oui, "circle", 0.65, True),
            (val_non, "circle", 0.20, False),
        ]:
            mask = (df["Genre"] == genre) & (df[col_symbol] == val)
            sub = df[mask]

            fig.add_trace(go.Scatter(
                x=sub[col_x],
                y=sub["Exam_Score"],
                mode="markers",
                name=genre,
                showlegend=show,
                legendgroup=genre,
                marker=dict(
                    color=color,
                    symbol=symbol,
                    size=7,
                    opacity=opacity,
                    line=dict(width=1.4, color=color),
                ),
                hovertemplate=make_hover_component(
                    label_x,
                    genre,
                    str(val),
                    SYMBOL_VAR_LABELS.get(col_symbol, col_symbol)
                ),
            ))

    if show_legend:
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
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d8d0c0",
            borderwidth=1,
        ),
        margin=dict(l=60, r=20, t=20, b=60),
        transition=dict(duration=350, easing="cubic-in-out"),
        hovermode="closest",
        xaxis=dict(
            tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 44]
            if col_x == "Hours_Studied"
            else [60, 65, 70, 75, 80, 85, 90, 95, 100],
        ),
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

    for layer in layers:
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
