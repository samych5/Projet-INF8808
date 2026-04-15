import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from .steps_config import get_step_graph_config
from .variables import (
    ID,
    Columns,
    DISTANCE_ORDER,
    DISTANCE_LABELS,
    SCHOOL_TYPE_ORDER,
    SCHOOL_TYPE_LABELS,
)


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


def _prepare_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    school_col = Columns.SCHOOL_TYPE.column
    distance_col = Columns.DISTANCE.column
    score_col = Columns.EXAM_SCORE.column

    data = df[[school_col, distance_col, score_col]].dropna().copy()

    grouped = (
        data.groupby([school_col, distance_col])[score_col]
        .mean()
        .reset_index()
    )

    pivot = grouped.pivot(
        index=school_col,
        columns=distance_col,
        values=score_col,
    )

    pivot = pivot.reindex(index=SCHOOL_TYPE_ORDER, columns=DISTANCE_ORDER)

    return pivot


def _get_z_text(z_values):
    text = []
    for row in z_values:
        text_row = []
        for val in row:
            if pd.isna(val):
                text_row.append("")
            else:
                text_row.append(f"{val:.1f}")
        text.append(text_row)
    return text


def create_figure(df: pd.DataFrame, config=None) -> go.Figure:
    pivot = _prepare_heatmap_data(df)

    x_values = [DISTANCE_LABELS[col] for col in pivot.columns]
    y_values = [SCHOOL_TYPE_LABELS[idx] for idx in pivot.index]
    z_values = pivot.values
    text_values = _get_z_text(z_values)

    zmin = 60
    zmax = 70

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=z_values,
            x=x_values,
            y=y_values,
            text=text_values,
            texttemplate="%{text}",
            colorscale="Blues",
            zmin=zmin,
            zmax=zmax,
            xgap=2,
            ygap=2,
            colorbar=dict(
                title=Columns.EXAM_SCORE.label,
                thickness=18,
                len=0.9,
            ),
            hovertemplate=(
                "Type d'école : %{y}<br>"
                "Distance : %{x}<br>"
                "Note finale moyenne : %{z:.1f}%<extra></extra>"
            ),
        )
    )

    title = "Lien entre le type d'école, la distance et la note finale"
    if config is not None and getattr(config, "title", None):
        title = config.title

    fig.update_layout(
        title=title,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=90, r=60, t=70, b=70),
        transition=dict(duration=0),
        dragmode=False,
    )

    fig.update_xaxes(
        title_text=Columns.DISTANCE.label,
        showgrid=False,
    )

    fig.update_yaxes(
        title_text=Columns.SCHOOL_TYPE.label,
        showgrid=False,
        autorange="reversed",
    )

    return fig