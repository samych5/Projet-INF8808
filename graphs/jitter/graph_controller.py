from dash import html, dcc

from .variables import *

DROPDOWN_OPTIONS = [
    {"label": AXES_X[col], "value": col.value}
    for col in ColX
]

def make_controller():
    return html.Div(
        [
            dcc.Dropdown(
                id=ID["dropdown-x"],
                options=DROPDOWN_OPTIONS,
                value=ColX.TUTORING_SESSIONS.value,
                clearable=False,
                searchable=False,
                className="graphs-controller-element",
            ),
        ],
        className="graph-controller jitter-controller",
    )
