import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc

from .ids import ID
from .graph_controller import AXES_X
from .hover_template import make_hover_component


def make_graph(df, col_x = "Tutoring_Sessions"):
    return dcc.Graph(
        id=ID["graph"],
        figure=create_figure(df, col_x),
        config={"displayModeBar": False},
        className="graph",
    )

def create_figure(df: pd.DataFrame, col_x: str = "Tutoring_Sessions") -> go.Figure:
    label_x = AXES_X.get(col_x, col_x)
    fig = go.Figure()

    np.random.seed(42)
    jitter = np.random.uniform(-0.25, 0.25, size=len(df))

    for genre, color in [("Homme", "#1a6fdb"), ("Femme", "#ff1493")]:
        mask = df["Genre"] == genre
        sub  = df[mask]
        j    = jitter[mask.values]

        fig.add_trace(go.Scatter(
            x=sub[col_x] + j,
            y=sub["Exam_Score"],
            mode="markers",
            name=genre,
            marker=dict(
                color=color,
                size=5,
                opacity=0.45,
                line=dict(width=0),
            ),
            hovertemplate=make_hover_component(label_x, genre),
        ))

    fig.update_layout(
        xaxis_title=label_x,
        yaxis_title="Note finale",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="DM Sans, Arial", size=13, color="#1a1a1a"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d8d0c0",
            borderwidth=1,
        ),
        margin=dict(l=60, r=20, t=20, b=60),
        hovermode="closest",
        xaxis=dict(
            tickvals=sorted(df[col_x].dropna().unique().tolist()),
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e8e0d0", zeroline=False, linecolor="#1a1a1a", linewidth=1.5)
    fig.update_yaxes(showgrid=True, gridcolor="#e8e0d0", zeroline=False, linecolor="#1a1a1a", linewidth=1.5)

    fig.update_layout(
        transition=dict(duration=0)
    )

    return fig