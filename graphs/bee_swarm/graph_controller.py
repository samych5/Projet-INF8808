from dash import html, dcc

from .graph import FILTERS, FILTER_KEYS
from .variables import ID

FILTERS_PER_PAGE = 3


def _make_numeric_marks(min_val: int, max_val: int):
    if min_val == max_val:
        return {min_val: str(min_val)}

    middle = int(round((min_val + max_val) / 2))
    return {
        min_val: str(min_val),
        middle: str(middle),
        max_val: str(max_val),
    }


def make_filter_block(column_name: str, config: dict, df):
    if config["type"] == "categorical":
        options = [
            {
                "label": config["labels"].get(value, value),
                "value": value,
            }
            for value in config["values"]
        ]

        component = dcc.Checklist(
            id={"type": "beeswarm-filter-categorical", "column": column_name},
            options=options,
            value=[],
            labelStyle={"display": "block", "marginBottom": "8px"},
        )

    else:
        numeric_series = df[column_name].dropna()
        min_val = int(numeric_series.min())
        max_val = int(numeric_series.max())

        component = dcc.RangeSlider(
            id={"type": "beeswarm-filter-numeric", "column": column_name},
            min=min_val,
            max=max_val,
            step=1,
            value=[min_val, max_val],
            marks=_make_numeric_marks(min_val, max_val),
            allowCross=False,
            tooltip={"placement": "bottom", "always_visible": False},
        )

    return html.Div(
        id={"type": "beeswarm-filter-block", "column": column_name},
        className="beeswarm-filter-block",
        children=[
            html.H4(config["label"], className="beeswarm-filter-title"),
            component,
        ],
    )


def make_controller(df):
    n_pages = (len(FILTER_KEYS) + FILTERS_PER_PAGE - 1) // FILTERS_PER_PAGE

    return html.Div(
        id=ID["filters-panel"],
        className="beeswarm-filters-panel",
        children=[
            dcc.Store(id=ID["filters-page-store"], data=0),

            html.Div(
                className="beeswarm-filters-header",
                children=[
                    html.Button("←", id=ID["filters-prev-btn"], n_clicks=0, className="beeswarm-page-btn"),
                    html.Div(
                        f"Page 1 / {n_pages}",
                        id=ID["filters-page-label"],
                        className="beeswarm-page-label",
                    ),
                    html.Button("→", id=ID["filters-next-btn"], n_clicks=0, className="beeswarm-page-btn"),
                ],
            ),

            html.Div(
                className="beeswarm-filters-grid",
                children=[
                    make_filter_block(column_name, FILTERS[column_name], df)
                    for column_name in FILTER_KEYS
                ],
            ),
        ],
    )