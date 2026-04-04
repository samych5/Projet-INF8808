from dash import html
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .graph import make_initial_graph
from .graph_controller import make_controller
from .variables import ID


def get_steps_number():
    return len(STEPS_CONFIG)


def make_section(df: DataFrame, start_index: int = 1):
    step_config = STEPS_CONFIG[0]

    return html.Section(
        id=ID["section"],
        className="story-section beeswarm-section",
        children=[
            html.Div(
                className="beeswarm-intro-wrapper",
                children=[
                    html.Div(
                        className="text-card beeswarm-intro-card",
                        children=[
                            html.H3(step_config.title, className="text-card-title"),
                            html.P(step_config.text, className="text-card-paragraph"),
                        ],
                    )
                ],
            ),
            html.Div(
                className="beeswarm-content-row",
                children=[
                    html.Div(
                        className="beeswarm-graph-wrapper",
                        children=[make_initial_graph(df)],
                    ),
                    html.Div(
                        className="beeswarm-controller-wrapper",
                        children=[make_controller(df)],
                    ),
                ],
            ),
        ],
    )