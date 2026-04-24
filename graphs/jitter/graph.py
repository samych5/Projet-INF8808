import plotly.graph_objects as go
import pandas as pd
import numpy as np

from .steps_config import GraphConfig
from .variables import *

POINT_COLOR = "rgba(140, 140, 140, 0.55)"
TREND_COLORS = {
    Genres.MEN: "#4da6ff",
    Genres.WOMEN: "#ff1493",
}


def _add_trend_line(
    fig,
    sub_df: pd.DataFrame,
    x_col: str,
    color: str,
    name: str,
    dash: str = "solid",
):
    if len(sub_df) < 2:
        return

    x = sub_df[x_col].astype(float).to_numpy()
    y = sub_df["Exam_Score"].astype(float).to_numpy()

    coef = np.polyfit(x, y, 1)
    poly = np.poly1d(coef)

    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = poly(x_line)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name=name,
            line=dict(
                color=color,
                width=4,
                dash=dash,
            ),
            hoverinfo="skip",
            showlegend=True,
        )
    )


def create_figure(df: pd.DataFrame, config: GraphConfig) -> go.Figure:
    col_x = config.col_x
    label_x = AXES_X.get(ColX(config.col_x), col_x)

    fig = go.Figure()

    np.random.seed(42)
    jitter = np.random.uniform(-0.25, 0.25, size=len(df))

    # Tous les points en gris
    fig.add_trace(
        go.Scatter(
            x=df[col_x] + jitter,
            y=df["Exam_Score"],
            mode="markers",
            name="Élèves",
            marker=dict(
                color=POINT_COLOR,
                size=5,
                opacity=0.55,
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=True,
        )
    )

    # Courbe de tendance Femmes dessinée en premier
    femmes = df[df["Genre"] == Genres.WOMEN.value].dropna(
        subset=[col_x, "Exam_Score"]
    )
    _add_trend_line(
        fig,
        femmes,
        col_x,
        TREND_COLORS[Genres.WOMEN],
        "Tendance - Femmes",
        dash="solid",
    )

    # Courbe de tendance Hommes dessinée après, donc au-dessus
    hommes = df[df["Genre"] == Genres.MEN.value].dropna(
        subset=[col_x, "Exam_Score"]
    )
    _add_trend_line(
        fig,
        hommes,
        col_x,
        TREND_COLORS[Genres.MEN],
        "Tendance - Hommes",
        dash="dash",
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
        ),
        legend_itemclick=False if not config.enable_interactions else "toggle",
        legend_itemdoubleclick=False if not config.enable_interactions else "toggleothers",
        margin=dict(l=60, r=20, t=60, b=60),
        hovermode="closest",
        xaxis=dict(
            tickvals=sorted(df[col_x].dropna().unique().tolist()),
        ),
        transition=dict(duration=0),
        dragmode=False,
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

    return fig