from dash import html, dcc
from pandas import DataFrame

from .steps_config import STEPS_CONFIG, get_step_graph_config, GraphConfig
from .graph_controller import make_controller
from .graph import create_figure, make_initial_graph
from .variables import *

def get_steps_number():
    return len(STEPS_CONFIG)

def make_text_steps(start_index : int = 1):
    return [
        html.Div(
            className="story-step jitter-step",
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

def precompute_story_figures(df, init_step: int, n_steps: int):
    store = {}

    for local_step in range(n_steps - 1):
        config : GraphConfig = get_step_graph_config(local_step)
        fig = create_figure(df, config)
        global_step = str(init_step + local_step)
        store[global_step] = {
            "__default__": fig.to_plotly_json()
        }

    return store

def make_section(df: DataFrame, start_index : int = 1):

    precomputed_figures = precompute_story_figures(df, start_index, get_steps_number())

    return html.Section(
        id="section-jitter",
        className="story-section jitter-section",
        children=[
            dcc.Store(id=ID["figures-store"],data=precomputed_figures),

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
                                className="graph-panel jitter-panel",
                                children=[
                                    html.Div(
                                        className="graph-panel-inner",
                                        children=[
                                            make_controller(),
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