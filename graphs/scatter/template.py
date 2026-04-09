import os
import base64
from dash import html
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .variables import *


def get_steps_number():
    return len(STEPS_CONFIG)


def _load_img(graph_name: str, index: int) -> str:
    path = os.path.join("assets", "images", f"{graph_name}-{index}.png")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


SCATTER_LABELS = [
    ["Heures d'étude par semaine", "Activités parascolaires"],
    ["Taux de présence (%)", "Activités parascolaires"],
    ["Heures d'étude par semaine", "Activités parascolaires"],
    ["Heures d'étude par semaine", "Activités parascolaires"],
]


def make_text_steps(start_index: int = 1):
    return [
        html.Div(
            className="story-step scatter-step",
            **{"data-step": str(step_index)},
            children=[
                html.Div(
                    className="text-card",
                    children=[
                        html.H3(step_config.title, className="text-card-title"),
                        html.P(step_config.text, className="text-card-paragraph"),
                    ],
                )
            ],
        )
        for step_index, step_config in enumerate(STEPS_CONFIG, start=start_index)
    ]


def make_section(df: DataFrame, start_index: int = 1):
    graph_panels = []
    for i in range(len(STEPS_CONFIG)):
        labels = SCATTER_LABELS[i] if i < len(SCATTER_LABELS) else []
        graph_panels.append(
            html.Div(
                id=f"scatter-img-{start_index + i}",
                style={"display": "none"},
                children=[
                    html.Div(
                        className="graph-labels",
                        children=[
                            html.Div(label, className="graph-label-pill")
                            for label in labels
                        ],
                    ),
                    html.Img(
                        src=_load_img("scatter", i),
                        style={"width": "100%", "height": "100%", "objectFit": "contain"},
                    ),
                ],
            )
        )

    return html.Section(
        id="section-scatter",
        className="story-section scatter-section",
        children=[
            html.Div(
                className="story-text-column",
                children=make_text_steps(start_index),
            ),
            html.Div(
                className="story-graph-column",
                children=[
                    html.Div(
                        className="story-graph-sticky",
                        children=[
                            html.Div(
                                className="graph-panel scatter-panel",
                                children=[
                                    html.Div(
                                        className="graph-panel-inner",
                                        children=graph_panels,
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
        ],
    )