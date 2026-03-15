import plotly.graph_objects as go
import pandas as pd
import numpy as np
from hover_template import jitter_eleve

AXES_X = {
    "Tutoring_Sessions": "Séances de tutorat",
    "Physical_Activity": "Activité physique (sessions/semaine)",
    "Sleep_Hours":       "Heures de sommeil par nuit",
}

DROPDOWN_OPTIONS = [
    {"label": label, "value": col}
    for col, label in AXES_X.items()
]


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
            hovertemplate=jitter_eleve(label_x, genre),
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

    return fig