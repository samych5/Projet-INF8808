from dash import Input, Output, no_update, ctx

from .steps_config import get_step_graph_config
from .graph import create_figure
from .pie_chart import create_pie_chart
from .variables import ID


def register_callbacks(app, df, init_step: int):

    @app.callback(
        Output(ID["answer-store"], "data"),
        Input(ID["btn-yes"], "n_clicks"),
        Input(ID["btn-no"], "n_clicks"),
        Input(ID["btn-reset"], "n_clicks"),
        prevent_initial_call=True,
    )
    def store_answer(yes_clicks, no_clicks, reset_clicks):
        triggered_id = ctx.triggered_id

        if triggered_id == ID["btn-yes"]:
            return "yes"

        if triggered_id == ID["btn-no"]:
            return "no"

        if triggered_id == ID["btn-reset"]:
            return None

        return no_update

    @app.callback(
        Output(ID["question-view"], "style"),
        Output(ID["result-view"], "style"),
        Input(ID["answer-store"], "data"),
    )
    def toggle_views(answer):
        if answer is None:
            return {"display": "flex"}, {"display": "none"}

        return {"display": "flex"}, {"display": "block"}

    @app.callback(
        Output(ID["btn-yes"], "style"),
        Output(ID["btn-no"], "style"),
        Output(ID["btn-reset"], "style"),
        Input(ID["answer-store"], "data"),
    )
    def update_button_styles(answer):
        default_style = {
            "padding": "12px 24px",
            "border": "none",
            "borderRadius": "12px",
            "cursor": "pointer",
            "backgroundColor": "#ececec",
            "color": "black",
        }

        selected_style = {
            "padding": "12px 24px",
            "border": "none",
            "borderRadius": "12px",
            "cursor": "pointer",
            "backgroundColor": "black",
            "color": "white",
        }

        hidden_style = {"display": "none"}

        reset_style = {
            "padding": "12px 24px",
            "border": "none",
            "borderRadius": "12px",
            "cursor": "pointer",
            "backgroundColor": "#ececec",
            "color": "black",
        }

        if answer is None:
            return default_style, default_style, hidden_style

        if answer == "yes":
            return selected_style, hidden_style, reset_style

        if answer == "no":
            return hidden_style, selected_style, reset_style

        return default_style, default_style, hidden_style

    @app.callback(
        Output(ID["question-text"], "children"),
        Input(ID["answer-store"], "data"),
    )
    def update_question_text(answer):
        if answer is None:
            return ""

        if answer == "yes":
            return "C'est aussi le cas de 75 % des parents, mais cela ne représente pas la réalité. Voici comment 100 parents d'élèves ont répondu à cette même question :"

        return "Pourtant, seulement 25 % des parents pensent cela. Voici comment 100 parents d'élèves ont répondu à cette même question :"

    @app.callback(
        Output(ID["pie-wrapper"], "style"),
        Input(ID["answer-store"], "data"),
    )
    def toggle_pie_wrapper(answer):
        if answer is None:
            return {"display": "none"}

        return {"display": "flex", "justifyContent": "center"}

    @app.callback(
        Output(ID["graph"], "figure"),
        Input(ID["answer-store"], "data"),
    )
    def update_graph(answer):
        config = get_step_graph_config(0)
        return create_figure(df, config)

    @app.callback(
        Output(ID["pie-chart"], "figure"),
        Input(ID["answer-store"], "data"),
    )
    def update_pie_chart(answer):
        return create_pie_chart(answer)