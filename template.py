from dash import html, dcc

from sections import SECTIONS, DEFAULT_STEP


def get_home_section():
    return html.Section(
        id="home-section",
        className="home-section",
        children=[],
    )


def get_story_sections(df):
    """
    Appelle les template.py de chaque graphique
    et retourne la liste complète des sections scrollytelling.
    """
    result = []
    init_step = DEFAULT_STEP

    for section in SECTIONS:
        result.append(section.construction_function(df, init_step))
        init_step += section.get_steps_number()

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