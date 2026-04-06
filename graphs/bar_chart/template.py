from dash import html, dcc
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .graph import make_initial_graph
from .variables import *

def get_steps_number():
    return len(STEPS_CONFIG)

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
    return html.Section(
        id="section-bar-chart",
        className="story-section bar-chart-section",
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
                                        className="graph-panel-inner",
                                        children=[
                                            make_initial_graph(df),
                                        ],
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
        ],
    )