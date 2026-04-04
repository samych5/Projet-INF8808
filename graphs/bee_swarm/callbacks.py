from dash import Input, Output, ALL, State, ctx, no_update

from .graph import create_figure, FILTERS, FILTER_KEYS
from .graph_controller import FILTERS_PER_PAGE
from .variables import ID


def register_callbacks(app, df, init_step: int):

    @app.callback(
        Output(ID["filters-page-store"], "data"),
        Input(ID["filters-prev-btn"], "n_clicks"),
        Input(ID["filters-next-btn"], "n_clicks"),
        State(ID["filters-page-store"], "data"),
        prevent_initial_call=True,
    )
    def update_filters_page(prev_clicks, next_clicks, current_page):
        current_page = current_page or 0
        n_pages = (len(FILTER_KEYS) + FILTERS_PER_PAGE - 1) // FILTERS_PER_PAGE

        triggered_id = ctx.triggered_id

        if triggered_id == ID["filters-prev-btn"]:
            return max(0, current_page - 1)

        if triggered_id == ID["filters-next-btn"]:
            return min(n_pages - 1, current_page + 1)

        return no_update

    @app.callback(
        Output(ID["filters-page-label"], "children"),
        Input(ID["filters-page-store"], "data"),
    )
    def update_page_label(current_page):
        current_page = current_page or 0
        n_pages = (len(FILTER_KEYS) + FILTERS_PER_PAGE - 1) // FILTERS_PER_PAGE
        return f"Page {current_page + 1} / {n_pages}"

    @app.callback(
        Output({"type": "beeswarm-filter-block", "column": ALL}, "style"),
        Input(ID["filters-page-store"], "data"),
    )
    def update_filter_blocks_visibility(current_page):
        current_page = current_page or 0

        start = current_page * FILTERS_PER_PAGE
        end = start + FILTERS_PER_PAGE
        visible_keys = set(FILTER_KEYS[start:end])

        styles = []
        for column_name in FILTER_KEYS:
            if column_name in visible_keys:
                styles.append({"display": "block"})
            else:
                styles.append({"display": "none"})
        return styles

    @app.callback(
        Output(ID["graph"], "figure"),
        Input({"type": "beeswarm-filter-categorical", "column": ALL}, "value"),
        Input({"type": "beeswarm-filter-numeric", "column": ALL}, "value"),
    )
    def update_graph(all_categorical_values, all_numeric_values):
        selected_filters = {}

        categorical_keys = [key for key in FILTER_KEYS if FILTERS[key]["type"] == "categorical"]
        numeric_keys = [key for key in FILTER_KEYS if FILTERS[key]["type"] == "numeric"]

        for i, column_name in enumerate(categorical_keys):
            selected_filters[column_name] = all_categorical_values[i] if i < len(all_categorical_values) else []

        for i, column_name in enumerate(numeric_keys):
            selected_filters[column_name] = all_numeric_values[i] if i < len(all_numeric_values) else []

        return create_figure(df, selected_filters)