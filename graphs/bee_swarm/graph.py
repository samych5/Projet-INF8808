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


def compute_y(df: pd.DataFrame, step: float = 7.0) -> np.ndarray:
    df_reset = df.reset_index(drop=True)
    y = np.zeros(len(df_reset))

    for _, group in df_reset.groupby("Exam_Score", sort=True):
        indices = group.index.tolist()
        for k, idx in enumerate(indices):
            if k == 0:
                y[idx] = 0
            else:
                level = (k + 1) // 2
                sign = 1 if k % 2 == 1 else -1
                y[idx] = sign * level * step

    return y


def compute_x(df: pd.DataFrame, jitter_strength: float = 0.12) -> np.ndarray:
    rng = np.random.default_rng(42)
    x = df["Exam_Score"].astype(float).to_numpy().copy()

    for _, group in df.groupby("Exam_Score", sort=True):
        indices = group.index.to_numpy()
        x[indices] += rng.uniform(-jitter_strength, jitter_strength, size=len(indices))

    return x


def make_hover(df: pd.DataFrame) -> list[str]:
    return (
        "<b>Score à l'examen : " + df["Exam_Score"].astype(str) + "</b><br>"
        + "Heures d'étude : " + df["Hours_Studied"].astype(str) + "<br>"
        + "Présence : " + df["Attendance"].astype(str) + "%<br>"
        + "Scores précédents : " + df["Previous_Scores"].astype(str) + "<br>"
        + "Heures de sommeil : " + df["Sleep_Hours"].astype(str) + "<br>"
        + "Type d'école : " + df["School_Type"].astype(str) + "<br>"
        + "Genre : " + df["Gender"].astype(str)
    ).tolist()


def build_match_mask(df: pd.DataFrame, selected_filters: dict) -> np.ndarray:
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


def get_filter_display_value(filter_key: str, value) -> str:
    filter_meta = FILTERS[filter_key]

    if filter_meta["type"] == "categorical":
        labels_map = filter_meta.get("labels", {})
        return labels_map.get(value, str(value))

    return str(value)


def get_active_filters_text(selected_filters: dict) -> list[str]:
    items: list[str] = []

    for filter_key in FILTER_KEYS:
        if filter_key not in selected_filters:
            continue

        filter_value = selected_filters[filter_key]
        if not filter_value:
            continue

        filter_meta = FILTERS[filter_key]
        label = filter_meta["label"]

        if filter_meta["type"] == "categorical":
            display_values = [get_filter_display_value(filter_key, value) for value in filter_value]
            items.append(f"{label} : {', '.join(display_values)}")
        else:
            items.append(f"{label} : {filter_value[0]} à {filter_value[1]}")

    return items


def create_figure(df: pd.DataFrame, selected_filters: dict | None = None) -> go.Figure:
    df_plot = df.reset_index(drop=True)

    if selected_filters is None:
        selected_filters = {}

    x_positions = compute_x(df_plot, jitter_strength=0.12)
    y_positions = compute_y(df_plot, step=7.0)
    hover = make_hover(df_plot)
    highlight_mask = build_match_mask(df_plot, selected_filters)

    mean_all = df_plot["Exam_Score"].mean()
    mean_filtered = df_plot.loc[highlight_mask, "Exam_Score"].mean() if highlight_mask.any() else None

    background_trace = go.Scatter(
        x=x_positions,
        y=y_positions,
        mode="markers",
        showlegend=False,
        marker=dict(
            color="#d1d5db",
            size=4,
            opacity=0.26,
            line=dict(width=0),
        ),
        text=hover,
        hovertemplate="%{text}<extra></extra>",
    )

    highlight_trace = go.Scatter(
        x=x_positions[highlight_mask],
        y=y_positions[highlight_mask],
        mode="markers",
        showlegend=False,
        marker=dict(
            color="#5cc16a",
            size=5,
            opacity=0.96,
            line=dict(width=0.7, color="white"),
        ),
        text=np.array(hover)[highlight_mask].tolist(),
        hovertemplate="%{text}<extra></extra>",
    )

    legend_global = go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        name="Moyenne globale",
        line=dict(color="#dc2626", width=2.5, dash="dash"),
        showlegend=True,
        hoverinfo="skip",
    )

    legend_filtered = go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        name="Moyenne filtrée",
        line=dict(color="#111111", width=2.5, dash="dash"),
        showlegend=True,
        hoverinfo="skip",
    )

    fig = go.Figure(data=[background_trace, highlight_trace, legend_global, legend_filtered])

    y_min = float(np.min(y_positions)) - 8
    y_max = float(np.max(y_positions)) + 8

    offset_top = (y_max - y_min) * 0.12
    offset_bottom = (y_max - y_min) * 0.12

    annotations = [
        dict(
            x=mean_all,
            y=-0.06,
            xref="x",
            yref="paper",
            text=f"{mean_all:.1f}",
            showarrow=False,
            font=dict(color="white", size=11),
            bgcolor="#dc2626",
            bordercolor="#dc2626",
            borderpad=4,
        )
    ]

    if mean_filtered is not None:
        annotations.append(
            dict(
                x=mean_filtered,
                y=1.06,
                xref="x",
                yref="paper",
                text=f"{mean_filtered:.1f}",
                showarrow=False,
                font=dict(color="white", size=11),
                bgcolor="#111111",
                bordercolor="#111111",
                borderpad=4,
            )
        )

    shapes = [
        dict(
            type="line",
            x0=mean_all,
            x1=mean_all,
            y0=y_min,
            y1=y_max,
            line=dict(color="#dc2626", width=2.5, dash="dash"),
            layer="above",
        )
    ]

    if mean_filtered is not None:
        shapes.append(
            dict(
                type="line",
                x0=mean_filtered,
                x1=mean_filtered,
                y0=y_min,
                y1=y_max,
                line=dict(color="#111111", width=2.5, dash="dash"),
                layer="above",
            )
        )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        autosize=False,
        height=540,
        margin=dict(l=50, r=20, t=70, b=70),
        title=dict(
            text="Distribution des scores à l'examen",
            font=dict(size=18, color="#e07b00"),
            x=0.0,
            xanchor="left",
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
            range=[y_min, y_max],
        ),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#e2e5ec",
            font=dict(size=12, color="#1a1d26"),
        ),
        dragmode=False,
        shapes=shapes,
        legend=dict(
            x=0.98,
            y=0.97,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#d1d5db",
            borderwidth=1,
            font=dict(size=11, color="#1f2937"),
        ),
        annotations=annotations
    )

    return fig


def make_initial_graph(df: pd.DataFrame):
    return dcc.Graph(
        id=ID["graph"],
        figure=create_figure(df, {}),
        config={"displayModeBar": False},
        className="beeswarm-graph",
        style={"height": "540px"},
    )