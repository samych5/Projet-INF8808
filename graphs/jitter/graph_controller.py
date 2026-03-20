from dash import html, dcc

from .ids import ID

AXES_X = {
    "Tutoring_Sessions": "Séances de tutorat",
    "Physical_Activity": "Activité physique (sessions/semaine)",
    "Sleep_Hours":       "Heures de sommeil par nuit",
}

DROPDOWN_OPTIONS = [
    {"label": label, "value": col}
    for col, label in AXES_X.items()
]

def make_controller():
    return html.Div(
        [
            dcc.Dropdown(
                id=ID["dropdown-x"],
                options=DROPDOWN_OPTIONS,
                value="Tutoring_Sessions",
                clearable=False,
                className="graphs-controller-element",
            ),
        ],
        className="graph-controller jitter-controller",
    )