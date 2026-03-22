from dash import html, dcc

from graphs.scatter.template import make_section as make_scatter_section, get_steps_number as scatter_steps
from graphs.jitter.template import make_section as make_jitter_section, get_steps_number as jitter_steps


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
    et retourne la liste complète des sections scrollytelling.
    """
    result = []
    init_step = 1

    sections = [
        {"function": make_scatter_section, "n_steps": scatter_steps},
        {"function": make_jitter_section, "n_steps": jitter_steps},
    ]

    for section in sections:
        result.append(section["function"](df, init_step))
        init_step += section["n_steps"]()

    return result


def get_layout(df):
    """
    Layout principal de l'application Dash.
    """
    return html.Div(
        id="page-container",
        className="page-container",
        children=[
            dcc.Input(
                id="active-step-input",
                type="text",
                value="0",
                style={"display": "none"},
            ),
            dcc.Store(id="active-step", data=0),

            get_home_section(),

            html.Main(
                id="story-container",
                className="story-container",
                children=get_story_sections(df),
            ),
        ],
    )