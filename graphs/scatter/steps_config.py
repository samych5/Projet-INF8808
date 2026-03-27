from .graph import create_figure


def get_step_config(step: int, col_x: str = "", col_symbol: str = "") -> dict:
    if step <= 0:
        return {
            "col_x": "Hours_Studied",
            "col_symbol": "Parascolaire",
            "visible_genres": ["Homme"],
            "show_legend": False,
            "layers": [],
        }

    elif step == 1:
        return {
            "col_x": "Hours_Studied",
            "col_symbol": "Parascolaire",
            "visible_genres": ["Homme", "Femme"],
            "show_legend": True,
            "layers": [],
        }

    else:
        if( not col_x or not col_symbol):
            raise(ValueError("col_x and col_symbol need to have a value"))
        return {
            "col_x": col_x,
            "col_symbol": col_symbol,
            "visible_genres": ["Homme", "Femme"],
            "show_legend": True,
            "layers": [],
        }


def precompute_scatter_story_figures(df, init_step: int):
    store = {}

    for local_step in [0, 1]:
        global_step = str(init_step + local_step)
        config = get_step_config(local_step)
        fig = create_figure(df, **config)
        store[global_step] = {
            "__default__": fig.to_plotly_json()
        }

    return store