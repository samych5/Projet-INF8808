import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from .variables import ID

FILTERS = {
    "Gender": {
        "type": "categorical",
        "label": "Genre",
        "values": ["Male", "Female"],
        "labels": {"Male": "Homme", "Female": "Femme"},
    },
    "School_Type": {
        "type": "categorical",
        "label": "Type d'école",
        "values": ["Public", "Private"],
        "labels": {"Public": "Public", "Private": "Privé"},
    },
    "Parental_Involvement": {
        "type": "categorical",
        "label": "Implication parentale",
        "values": ["Low", "Medium", "High"],
        "labels": {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"},
    },
    "Access_to_Resources": {
        "type": "categorical",
        "label": "Accès aux ressources",
        "values": ["Low", "Medium", "High"],
        "labels": {"Low": "Faible", "Medium": "Moyen", "High": "Élevé"},
    },
    "Extracurricular_Activities": {
        "type": "categorical",
        "label": "Activités parascolaires",
        "values": ["No", "Yes"],
        "labels": {"No": "Non", "Yes": "Oui"},
    },
    "Motivation_Level": {
        "type": "categorical",
        "label": "Motivation",
        "values": ["Low", "Medium", "High"],
        "labels": {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"},
    },
    "Internet_Access": {
        "type": "categorical",
        "label": "Accès internet",
        "values": ["No", "Yes"],
        "labels": {"No": "Non", "Yes": "Oui"},
    },
    "Family_Income": {
        "type": "categorical",
        "label": "Revenu familial",
        "values": ["Low", "Medium", "High"],
        "labels": {"Low": "Faible", "Medium": "Moyen", "High": "Élevé"},
    },
    "Teacher_Quality": {
        "type": "categorical",
        "label": "Qualité des enseignants",
        "values": ["Low", "Medium", "High"],
        "labels": {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"},
    },
    "Peer_Influence": {
        "type": "categorical",
        "label": "Influence des pairs",
        "values": ["Negative", "Neutral", "Positive"],
        "labels": {"Negative": "Négative", "Neutral": "Neutre", "Positive": "Positive"},
    },
    "Learning_Disabilities": {
        "type": "categorical",
        "label": "Troubles d'apprentissage",
        "values": ["No", "Yes"],
        "labels": {"No": "Non", "Yes": "Oui"},
    },
    "Parental_Education_Level": {
        "type": "categorical",
        "label": "Éducation parentale",
        "values": ["High School", "College", "Postgraduate"],
        "labels": {
            "High School": "Secondaire",
            "College": "Collégial",
            "Postgraduate": "Universitaire",
        },
    },
    "Distance_from_Home": {
        "type": "categorical",
        "label": "Distance domicile-école",
        "values": ["Near", "Moderate", "Far"],
        "labels": {"Near": "Proche", "Moderate": "Modérée", "Far": "Loin"},
    },
    "Sleep_Hours": {
        "type": "numeric",
        "label": "Heures de sommeil",
    },
    "Hours_Studied": {
        "type": "numeric",
        "label": "Heures d'étude",
    },
    "Attendance": {
        "type": "numeric",
        "label": "Présence (%)",
    },
    "Previous_Scores": {
        "type": "numeric",
        "label": "Scores précédents",
    },
    "Tutoring_Sessions": {
        "type": "numeric",
        "label": "Séances de tutorat",
    },
    "Physical_Activity": {
        "type": "numeric",
        "label": "Activité physique",
    },
}

FILTER_KEYS = list(FILTERS.keys())


def compute_y(df: pd.DataFrame, step: float = 5.5):
    df_reset = df.reset_index(drop=True)
    y = np.zeros(len(df_reset))

    for score, group in df_reset.groupby("Exam_Score"):
        indices = group.index.tolist()
        for k, idx in enumerate(indices):
            col = k // 2 if k % 2 == 0 else -(k // 2 + 1)
            y[idx] = col * step

    return y


def make_hover(df: pd.DataFrame):
    return (
        "<b>Score à l'examen : " + df["Exam_Score"].astype(str) + "</b><br>"
        + "Heures d'étude : " + df["Hours_Studied"].astype(str) + "<br>"
        + "Présence : " + df["Attendance"].astype(str) + "%<br>"
        + "Scores précédents : " + df["Previous_Scores"].astype(str) + "<br>"
        + "Heures de sommeil : " + df["Sleep_Hours"].astype(str) + "<br>"
        + "Type d'école : " + df["School_Type"].astype(str) + "<br>"
        + "Genre : " + df["Gender"].astype(str)
    ).tolist()


def build_match_mask(df: pd.DataFrame, selected_filters: dict):
    mask = np.ones(len(df), dtype=bool)

    for col, selected_value in selected_filters.items():
        if col not in FILTERS:
            continue

        filter_type = FILTERS[col]["type"]

        if filter_type == "categorical":
            if not selected_value:
                continue
            mask &= df[col].astype(str).isin([str(v) for v in selected_value]).to_numpy()

        elif filter_type == "numeric":
            if not selected_value or len(selected_value) != 2:
                continue

            min_val, max_val = selected_value
            numeric_series = pd.to_numeric(df[col], errors="coerce")
            mask &= numeric_series.between(min_val, max_val).fillna(False).to_numpy()

    return mask


def create_figure(df: pd.DataFrame, selected_filters: dict | None = None):
    df_plot = df.reset_index(drop=True)
    y_positions = compute_y(df_plot)
    hover = make_hover(df_plot)

    if selected_filters is None:
        selected_filters = {}

    highlight_mask = build_match_mask(df_plot, selected_filters)

    background_trace = go.Scatter(
        x=df_plot["Exam_Score"],
        y=y_positions,
        mode="markers",
        showlegend=False,
        marker=dict(
            color="#d1d5db",
            size=5,
            opacity=0.28,
            line=dict(width=0),
        ),
        text=hover,
        hovertemplate="%{text}<extra></extra>",
    )

    highlight_trace = go.Scatter(
        x=df_plot.loc[highlight_mask, "Exam_Score"],
        y=y_positions[highlight_mask],
        mode="markers",
        showlegend=False,
        marker=dict(
            color="#22c55e",
            size=6,
            opacity=0.95,
            line=dict(width=0),
        ),
        text=np.array(hover)[highlight_mask].tolist(),
        hovertemplate="%{text}<extra></extra>",
    )

    fig = go.Figure(data=[background_trace, highlight_trace])

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        autosize=False,
        height=620,
        margin=dict(l=50, r=30, t=55, b=55),
        title=dict(
            text="Distribution des scores à l'examen",
            font=dict(size=18, color="#e07b00"),
        ),
        xaxis=dict(
            title=dict(text="Score à l'examen"),
            gridcolor="#e2e5ec",
            linecolor="#e2e5ec",
            zeroline=False,
        ),
        yaxis=dict(
            visible=False,
            zeroline=False,
            showgrid=False,
        ),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#e2e5ec",
            font=dict(size=12, color="#1a1d26"),
        ),
    )

    return fig


def make_initial_graph(df: pd.DataFrame):
    return dcc.Graph(
        id=ID["graph"],
        figure=create_figure(df, {}),
        config={"displayModeBar": False},
        className="beeswarm-graph",
        style={"height": "620px"},
    )
