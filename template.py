from dash import html, dcc
from scatter import DROPDOWN_OPTIONS, SYMBOL_VAR_OPTIONS
from jitter import DROPDOWN_OPTIONS as JITTER_OPTIONS


def get_layout():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id="dropdown-scatter-x",
                options=DROPDOWN_OPTIONS,
                value="Hours_Studied",
                clearable=False,
                style={"width": "350px"},
            ),
            dcc.Dropdown(
                id="dropdown-scatter-symbol",
                options=SYMBOL_VAR_OPTIONS,
                value="Parascolaire",
                clearable=False,
                style={"width": "350px"},
            ),
        ], style={"display": "flex", "gap": "20px", "justifyContent": "center", "margin": "20px auto"}),
        dcc.Graph(
            id="graph-scatter",
            config={"displayModeBar": False},
            style={"height": "600px", "width": "900px", "margin": "0 auto"},
        ),
        
        html.Div([
            dcc.Dropdown(
                id="dropdown-jitter-x",
                options=JITTER_OPTIONS,
                value="Tutoring_Sessions",
                clearable=False,
                style={"width": "350px"},
            ),
        ], style={"display": "flex", "justifyContent": "center", "margin": "40px auto 10px auto"}),
        dcc.Graph(
            id="graph-jitter",
            config={"displayModeBar": False},
            style={"height": "600px", "width": "900px", "margin": "0 auto"},
        ),
    ])