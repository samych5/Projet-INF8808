from dash import html
from pandas import DataFrame

from .graph_controller import make_scatter_controller
from .graph import make_graph


SCATTER_TEXTS = [
    "Texte scatter 1",
    "Texte scatter 2",
]

def get_steps_number():
    return len(SCATTER_TEXTS)

def make_text_steps(start_index : int = 1):
    return [
        html.Div(
            className="story-step scatter-step",
            **{"data-step": str(step_index)},
            children=[
                html.Div(
                    className="text-card",
                    children=[
                        html.H3("Scatter plot", className="text-card-title"),
                        html.P(text, className="text-card-paragraph"),
                    ],
                )
            ],
        )
        for step_index, text in enumerate(SCATTER_TEXTS, start=start_index)
    ]


def make_section(df: DataFrame, start_index : int = 1):
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
                                        children=[
                                            make_scatter_controller(),
                                            make_graph(df),
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