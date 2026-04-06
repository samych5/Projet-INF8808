from dash import html, dcc

from .variables import *

DROPDOWN_OPTIONS = [
    {"label": AXES_X[col], "value": col.value}
    for col in ColX
]

SYMBOL_VAR_OPTIONS = [
    {"label": SYMBOL_VAR_LABELS[var], "value": var.value}
    for var in SymbolVar
]

def make_controller():
    return html.Div(
        id="scatter-controls",
        children=[
            dcc.Dropdown(
                id=ID["dropdown-x"],
                options=DROPDOWN_OPTIONS,
                value=ColX.HOURS_STUDIED.value,
                clearable=False,
                searchable=False,
                className="graphs-controller-element",
            ),
            dcc.Dropdown(
                id=ID["dropdown-symbol"],
                options=SYMBOL_VAR_OPTIONS,
                value=SymbolVar.EXTRACURRICULAR_ACTIVITIES.value,
                clearable=False,
                searchable=False,
                className="graphs-controller-element",
            ),
        ],
        className="graph-controller",
    )