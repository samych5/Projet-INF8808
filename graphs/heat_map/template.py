from dash import html, dcc
from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .graph import make_initial_graph
from .pie_chart import make_pie_chart
from .variables import ID


def get_steps_number():
    return len(STEPS_CONFIG)


def make_text_steps(start_index: int = 1):
    return [
        html.Div(
            className="story-step heat-map-step",
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


def make_question_block():
    return html.Div(
        id=ID["question-view"],
        className="heat-map-question-view",
        children=[
            html.Div(
                className="heat-map-question-card",
                children=[
                    html.H2(
                        "Penses-tu que la distance entre le domicile et l'école influence la note finale ?",
                        className="heat-map-question-title",
                    ),
                    html.Div(
                        className="heat-map-question-buttons",
                        children=[
                            html.Button("Oui", id=ID["btn-yes"], n_clicks=0, className="heat-map-btn"),
                            html.Button("Non", id=ID["btn-no"], n_clicks=0, className="heat-map-btn"),
                            html.Button("Réinitialiser", id=ID["btn-reset"], n_clicks=0, className="heat-map-btn heat-map-btn-reset", style={"display": "none"}),
                        ],
                    ),
                    html.P(
                        id=ID["question-text"],
                        className="heat-map-question-feedback",
                    ),
                    html.Div(
                        id=ID["pie-wrapper"],
                        className="heat-map-question-pie-wrapper",
                        children=[
                            make_pie_chart(),
                        ],
                    ),
                ],
            )
        ],
    )


def make_result_view(df: DataFrame, start_index: int = 1):
    return html.Div(
        id=ID["result-view"],
        className="heat-map-result-view",
        children=[
            html.Div(
                className="heat-map-content-row",
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
                                        className="graph-panel heat-map-panel",
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
        ],
    )


def make_section(df: DataFrame, start_index: int = 1):
    return html.Section(
        id=ID["section"],
        className="story-section heat-map-section",
        children=[
            dcc.Store(id=ID["answer-store"]),
            make_question_block(),
            make_result_view(df, start_index),
        ],
    )