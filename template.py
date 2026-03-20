from dash import html, dcc

from graphs.scatter.template import make_section as make_scatter_section
from graphs.jitter.template import make_section as make_jitter_section


def get_home_section():
    return html.Section(
        id="home-section",
        className="home-section",
        children=[
            html.Div(
                className="home-overlay",
                children=[
                    html.H1("Titre du site", className="home-title"),
                    html.P(
                        "Texte random",
                        className="home-subtitle",
                    ),
                ],
            )
        ],
    )


def get_story_sections(df):
    """
    Appelle les template.py de chaque graphique
    et retourne la liste des sections scrollytelling.
    """
    return [
        make_scatter_section(df),
        make_jitter_section(df),
    ]


def get_layout(df):
    """
    Layout principal de l'application Dash.
    """
    return html.Div(
        id="page-container",
        className="page-container",
        children=[
            dcc.Store(id="active-step", data=0),
            dcc.Store(id="active-graph", data="scatter"),

            get_home_section(),

            html.Main(
                id="story-container",
                className="story-container",
                children=get_story_sections(df),
            ),
        ],
    )