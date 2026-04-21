from dash import html
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .variables import *
from utils.loading_img import load_img
from utils.story_section import (
    get_steps_number as base_get_steps_number,
    make_section_layout,
)

TRANSITION_STEP_INDEX = 1


def get_steps_number():
    return base_get_steps_number(STEPS_CONFIG)


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
                                html.P(
                                    step_config.text,
                                    className="text-card-paragraph boxplot-transition-text",
                                ),
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
                                html.P(step_config.text, className="text-card-paragraph")
                                if isinstance(step_config.text, str)
                                else step_config.text,
                            ],
                        )
                    ],
                )
            )

    return steps


def make_graph_panels(start_index: int = 1):
    graph_panels = []

    for i in range(len(STEPS_CONFIG)):
        class_name = "section-graph-frame active" if i == 0 else "section-graph-frame"
        step_value = str(start_index + i)

        if i == TRANSITION_STEP_INDEX:
            graph_panels.append(
                html.Div(
                    className=class_name,
                    **{"data-step": step_value},
                )
            )
        else:
            graph_panels.append(
                html.Div(
                    className=class_name,
                    **{"data-step": step_value},
                    children=[
                        html.Img(
                            src=load_img("boxplot", i),
                            style={
                                "width": "100%",
                                "height": "100%",
                                "objectFit": "contain",
                            },
                        )
                    ],
                )
            )

    return graph_panels


def make_section(df: DataFrame, start_index: int = 1):
    steps = make_text_steps(start_index)
    graph_panels = make_graph_panels(start_index)

    return make_section_layout(
        steps=steps,
        graph_panels=graph_panels,
        section_id="section-boxplot",
        section_class="boxplot-section",
        data_section="boxplot",
        panel_class="boxplot-panel",
    )