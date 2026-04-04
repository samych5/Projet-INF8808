import math

from dash import Input, Output, State, ctx, no_update
from dash.dependencies import ALL

from .graph import FILTERS, FILTER_KEYS, create_figure
from .template import make_active_filters_summary, make_filters_page
from .variables import FILTERS_PER_PAGE, ID


def _normalize_selected_filters(selected_filters: dict | None) -> dict:
    if not selected_filters:
        return {}

    clean_filters: dict = {}

    for filter_key, filter_value in selected_filters.items():
        if filter_key not in FILTERS:
            continue

        filter_meta = FILTERS[filter_key]

        if filter_meta["type"] == "categorical":
            if filter_value:
                clean_filters[filter_key] = list(filter_value)
        else:
            if filter_value and len(filter_value) == 2:
                clean_filters[filter_key] = [filter_value[0], filter_value[1]]

    return clean_filters


def register_callbacks(app, df, init_step = 0):
    total_pages = math.ceil(len(FILTER_KEYS) / FILTERS_PER_PAGE)

    @app.callback(
        Output(ID["filter-page-store"], "data"),
        Input(ID["prev-page-btn"], "n_clicks"),
        Input(ID["next-page-btn"], "n_clicks"),
        State(ID["filter-page-store"], "data"),
        prevent_initial_call=True,
    )
    def update_filter_page(_, __, current_page):
        triggered = ctx.triggered_id
        current_page = int(current_page or 0)

        if triggered == ID["prev-page-btn"]:
            return max(0, current_page - 1)

        if triggered == ID["next-page-btn"]:
            return min(total_pages - 1, current_page + 1)

        return current_page

    @app.callback(
        Output(ID["filters-container"], "children"),
        Output(ID["page-label"], "children"),
        Input(ID["filter-page-store"], "data"),
        Input(ID["selected-filters-store"], "data"),
    )
    def render_filters_container(page_index, selected_filters):
        page_index = int(page_index or 0)
        selected_filters = _normalize_selected_filters(selected_filters)
        return (
            make_filters_page(df, page_index, selected_filters),
            f"Filtres {page_index + 1} / {total_pages}",
        )

    @app.callback(
        Output(ID["selected-filters-store"], "data"),
        Input({"type": "beeswarm-categorical-filter", "index": ALL}, "value"),
        Input({"type": "beeswarm-numeric-filter", "index": ALL}, "value"),
        Input({"type": "beeswarm-reset-single", "index": ALL}, "n_clicks"),
        Input({"type": "beeswarm-remove-chip", "index": ALL}, "n_clicks"),
        Input(ID["reset-all-btn"], "n_clicks"),
        State({"type": "beeswarm-categorical-filter", "index": ALL}, "id"),
        State({"type": "beeswarm-numeric-filter", "index": ALL}, "id"),
        State(ID["selected-filters-store"], "data"),
        prevent_initial_call=True,
    )
    def update_selected_filters(
        categorical_values,
        numeric_values,
        _reset_single_clicks,
        _remove_chip_clicks,
        reset_all_clicks,
        categorical_ids,
        numeric_ids,
        selected_filters,
    ):
        _ = reset_all_clicks
        selected_filters = _normalize_selected_filters(selected_filters)
        triggered = ctx.triggered_id

        if triggered == ID["reset-all-btn"]:
            return {}

        if isinstance(triggered, dict) and triggered.get("type") in {"beeswarm-reset-single", "beeswarm-remove-chip"}:
            filter_key = triggered["index"]
            if filter_key in selected_filters:
                selected_filters.pop(filter_key)
            return selected_filters

        if isinstance(triggered, dict) and triggered.get("type") == "beeswarm-categorical-filter":
            filter_key = triggered["index"]
            for comp_id, value in zip(categorical_ids, categorical_values):
                if comp_id["index"] == filter_key:
                    if value:
                        selected_filters[filter_key] = value
                    elif filter_key in selected_filters:
                        selected_filters.pop(filter_key)
                    break
            return selected_filters

        if isinstance(triggered, dict) and triggered.get("type") == "beeswarm-numeric-filter":
            filter_key = triggered["index"]
            for comp_id, value in zip(numeric_ids, numeric_values):
                if comp_id["index"] == filter_key:
                    min_value = int(df[filter_key].min())
                    max_value = int(df[filter_key].max())

                    if value and value != [min_value, max_value]:
                        selected_filters[filter_key] = value
                    elif filter_key in selected_filters:
                        selected_filters.pop(filter_key)
                    break
            return selected_filters

        return selected_filters

    @app.callback(
        Output(ID["graph"], "figure"),
        Output(ID["active-filters-bar"], "children"),
        Input(ID["selected-filters-store"], "data"),
    )
    def update_graph_and_summary(selected_filters):
        selected_filters = _normalize_selected_filters(selected_filters)
        figure = create_figure(df, selected_filters)
        summary = make_active_filters_summary(selected_filters)
        return figure, summary