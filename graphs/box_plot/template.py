import os
import base64
from dash import html
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .variables import *

TRANSITION_STEP_INDEX = 1


def get_steps_number():
    return len(STEPS_CONFIG)


def _load_img(graph_name: str, index: int) -> str:
    path = os.path.join("assets", "images", f"{graph_name}-{index}.png")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def make_text_steps(start_index: int = 1):
    steps = []
    for i, step_config in enumerate(STEPS_CONFIG):
        step_index = start_index + i

        if i == TRANSITION_STEP_INDEX:
            steps.append(
                html.Div(
                    className="story-step boxplot-step boxplot-transition-step",
                    **{"data-step": str(step_index)},
                    children=[
                        html.Div(
                            className="text-card boxplot-transition-card",
                            children=[
                                html.P(step_config.text, className="text-card-paragraph boxplot-transition-text"),
                            ],
                        )
                    ],
                )
            )
        else:
            steps.append(
                html.Div(
                    className="story-step boxplot-step",
                    **{"data-step": str(step_index)},
                    children=[
                        html.Div(
                            className="text-card",
                            children=[
                                html.H3(step_config.title, className="text-card-title"),
                                html.P(step_config.text, className="text-card-paragraph") if isinstance(step_config.text, str) else step_config.text,
                            ],
                        )
                    ],
                )
            )
    return steps


def make_section(df: DataFrame, start_index: int = 1):
    graph_panels = []
    for i in range(len(STEPS_CONFIG)):
        if i == TRANSITION_STEP_INDEX:
            graph_panels.append(
                html.Div(
                    id=f"boxplot-img-{start_index + i}",
                    style={"display": "none"},
                )
            )
        else:
            graph_panels.append(
                html.Div(
                    id=f"boxplot-img-{start_index + i}",
                    style={"display": "none"},
                    children=[
                        html.Img(
                            src=_load_img("boxplot", i),
                            style={"width": "100%", "height": "100%", "objectFit": "contain"},
                        )
                    ],
                )
            )

    return html.Section(
        id="section-boxplot",
        className="story-section boxplot-section",
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
                                className="graph-panel boxplot-panel",
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