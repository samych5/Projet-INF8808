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


def make_text_steps(start_index: int = 1):
    return [
        html.Div(
            className="story-step boxplot-step",
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
    graph_panels = [
        html.Div(
            className="section-graph-frame active" if i == 0 else "section-graph-frame",
            **{"data-step": str(start_index + i)},
            children=[
                html.Img(
                    src=_load_img("barchart", i),
                    style={
                        "width": "100%",
                        "height": "100%",
                        "objectFit": "contain",
                    },
                )
            ],
        )
        for i in range(len(STEPS_CONFIG))
    ]

    return html.Section(
        id="section-bar-chart",
        className="story-section bar-chart-section",
        **{"data-section": "barchart"},
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
                                className="graph-panel bar-chart-panel",
                                children=[
                                    html.Div(
                                        className="graph-panel-inner section-graph-stack",
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