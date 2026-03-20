from dash import html, dcc

from .ids import ID

AXES_X = {
    "Hours_Studied": "Heures d'étude par semaine",
    "Attendance":    "Taux de présence (%)",
}

SYMBOL_VAR_OPTIONS = [
    {"label": "Activités parascolaires", "value": "Parascolaire"},
    {"label": "Accès internet",          "value": "Acces_internet"},
    {"label": "Troubles d'apprentissage","value": "Troubles_apprentissage"},
]

DROPDOWN_OPTIONS = [
    {"label": label, "value": col}
    for col, label in AXES_X.items()
]

def make_scatter_controller():
    return html.Div(
        id="scatter-controls",
        children=[
            dcc.Dropdown(
                id=ID["dropdown-x"],
                options=DROPDOWN_OPTIONS,
                value="Hours_Studied",
                clearable=False,
                className="graphs-controller-element",
            ),
            dcc.Dropdown(
                id=ID["dropdown-symbol"],
                options=SYMBOL_VAR_OPTIONS,
                value="Parascolaire",
                clearable=False,
                className="graphs-controller-element",
            ),
        ],
        className="graph-controller",
    )