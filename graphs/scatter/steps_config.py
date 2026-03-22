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
        if(~col_x or ~col_symbol):
            raise(ValueError("col_x and col_symbol need to have a value"))
        return {
            "col_x": col_x,
            "col_symbol": col_symbol,
            "visible_genres": ["Homme", "Femme"],
            "show_legend": True,
            "layers": [],
        }