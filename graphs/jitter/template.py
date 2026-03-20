from dash import html
from pandas import DataFrame

from .graph_controller import make_controller
from .graph import make_graph


JITTER_TEXTS = [
    "Texte jitter 1",
    "Texte jitter 2",
    "Texte jitter 3",
]


def make_text_steps():
    return [
        html.Div(
            className="story-step jitter-step",
            children=[
                html.Div(
                    className="text-card",
                    children=[
                        html.H3("Jitter plot", className="text-card-title"),
                        html.P(text, className="text-card-paragraph"),
                    ],
                )
            ],
        )
        for text in JITTER_TEXTS
    ]


def make_section(df: DataFrame):
    return html.Section(
        id="section-jitter",
        className="story-section jitter-section",
        children=[
            html.Div(
                className="story-text-column",
                children=make_text_steps(),
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