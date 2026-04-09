import math

import pandas as pd
from dash import dcc, html

from .steps_config import STEPS_CONFIG
from .graph import FILTERS, FILTER_KEYS, get_active_filters_text, make_initial_graph
from .variables import FILTERS_PER_PAGE, ID

def get_steps_number():
    return len(STEPS_CONFIG)

def _get_numeric_bounds(df: pd.DataFrame, filter_key: str) -> tuple[int, int]:
    series = pd.to_numeric(df[filter_key], errors="coerce").dropna()
    return int(series.min()), int(series.max())


def _make_numeric_marks(min_value: int, max_value: int) -> dict[int, str]:
    if max_value <= min_value:
        return {min_value: str(min_value)}

    steps = 4
    values = sorted({int(round(min_value + i * (max_value - min_value) / steps)) for i in range(steps + 1)})
    return {value: str(value) for value in values}


def make_filter_card(df: pd.DataFrame, filter_key: str, selected_filters: dict):
    filter_meta = FILTERS[filter_key]
    current_value = selected_filters.get(filter_key)

    if filter_meta["type"] == "categorical":
        if current_value is None:
            current_value = []

        options = [
            {"label": filter_meta["labels"].get(value, value), "value": value}
            for value in filter_meta["values"]
        ]

        control = dcc.Checklist(
            id={"type": "beeswarm-categorical-filter", "index": filter_key},
            options=options,
            value=current_value,
            className="beeswarm-checklist",
            inputClassName="beeswarm-checklist-input",
            labelClassName="beeswarm-checklist-label",
        )
    else:
        min_value, max_value = _get_numeric_bounds(df, filter_key)

        if current_value is None:
            current_value = [min_value, max_value]

        control = html.Div(
            className="beeswarm-slider-wrapper",
            children=[
                html.Div(
                    className="beeswarm-slider-values",
                    children=f"{current_value[0]} à {current_value[1]}",
                ),
                dcc.RangeSlider(
                    id={"type": "beeswarm-numeric-filter", "index": filter_key},
                    min=min_value,
                    max=max_value,
                    step=1,
                    value=current_value,
                    marks=_make_numeric_marks(min_value, max_value),
                    allowCross=False,
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ],
        )

    return html.Div(
        className="beeswarm-filter-card",
        children=[
            html.Div(
                className="beeswarm-filter-card-header",
                children=[
                    html.H3(filter_meta["label"], className="beeswarm-filter-title"),
                    html.Button(
                        "Réinitialiser",
                        id={"type": "beeswarm-reset-single", "index": filter_key},
                        n_clicks=0,
                        className="beeswarm-reset-single-btn",
                    ),
                ],
            ),
            control,
        ],
    )


def make_filters_page(df: pd.DataFrame, page_index: int, selected_filters: dict):
    start = page_index * FILTERS_PER_PAGE
    end = start + FILTERS_PER_PAGE
    page_filter_keys = FILTER_KEYS[start:end]

    return [make_filter_card(df, filter_key, selected_filters) for filter_key in page_filter_keys]


def make_active_filters_summary(selected_filters: dict):
    texts = get_active_filters_text(selected_filters)

    if not texts:
        return [
            html.Span("Filtres actifs :", className="active-filters-title"),
            html.Span("Aucun filtre appliqué", className="active-filters-empty"),
        ]

    chips = []
    for filter_key, filter_value in selected_filters.items():
        if not filter_value:
            continue

        label = FILTERS[filter_key]["label"]
        if FILTERS[filter_key]["type"] == "categorical":
            values_text = ", ".join(FILTERS[filter_key]["labels"].get(value, str(value)) for value in filter_value)
        else:
            values_text = f"{filter_value[0]} à {filter_value[1]}"

        chips.append(
            html.Div(
                className="active-filter-chip",
                children=[
                    html.Span(f"{label} : {values_text}", className="active-filter-chip-text"),
                    html.Button(
                        "×",
                        id={"type": "beeswarm-remove-chip", "index": filter_key},
                        n_clicks=0,
                        className="active-filter-chip-remove",
                    ),
                ],
            )
        )

    return [html.Span("Filtres actifs :", className="active-filters-title"), *chips]

def make_section(df: pd.DataFrame, init_step : int = 1):
    total_pages = math.ceil(len(FILTER_KEYS) / FILTERS_PER_PAGE)
    step_config = STEPS_CONFIG[0]

    return html.Div(
        className="beeswarm-section",
        children=[
            dcc.Store(id=ID["selected-filters-store"], data={}),
            dcc.Store(id=ID["filter-page-store"], data=0),

            html.Div(
                className="beeswarm-top-text",
                children=[
                    html.Div(
                        className="text-card",
                        children=[
                            html.H3(step_config.title, className="text-card-title"),
                            html.P(
                                step_config.text,
                                className="text-card-paragraph",
                            ),
                        ],
                    )
                ],
            ),

            html.Div(
                className="beeswarm-layout",
                children=[
                    html.Div(
                        className="beeswarm-left-panel",
                        children=[
                            make_initial_graph(df),
                            html.Div(
                                id=ID["active-filters-bar"],
                                className="active-filters-bar",
                                children=make_active_filters_summary({}),
                            ),
                        ],
                    ),
                    html.Div(
                        className="beeswarm-right-panel",
                        children=[
                            html.Div(
                                className="beeswarm-panel-header",
                                children=[
                                    html.Button("←", id=ID["prev-page-btn"], n_clicks=0, className="beeswarm-page-nav-btn"),
                                    html.Div(id=ID["page-label"], className="beeswarm-page-label", children=f"Filtres 1 / {total_pages}"),
                                    html.Button("→", id=ID["next-page-btn"], n_clicks=0, className="beeswarm-page-nav-btn"),
                                ],
                            ),
                            html.Button(
                                "Réinitialiser tous les filtres",
                                id=ID["reset-all-btn"],
                                n_clicks=0,
                                className="beeswarm-reset-all-btn",
                            ),
                            html.Div(
                                id=ID["filters-container"],
                                className="beeswarm-filters-container",
                                children=make_filters_page(df, 0, {}),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
