from dash import html, dcc
from scatter import DROPDOWN_OPTIONS


def get_layout():
    return html.Div([
        dcc.Dropdown(
            id="dropdown-scatter-x",
            options=DROPDOWN_OPTIONS,
            value="Hours_Studied",
            clearable=False,
            style={"width": "400px", "margin": "20px auto 10px auto"},
        ),
        dcc.Graph(
            id="graph-scatter",
            config={"displayModeBar": False},
            style={"height": "600px", "width": "900px", "margin": "0 auto"},
        ),
    ], style={"textAlign": "center"})