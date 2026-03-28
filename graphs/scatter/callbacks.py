from dash import clientside_callback, ClientsideFunction, Input, Output, no_update

from .steps_config import STEPS_CONFIG, GraphConfig, get_step_graph_config
from .template import get_steps_number
from .graph import create_figure
from .variables import *

def register_callbacks(app, df, init_step : int):

    ## Displays precalculated graphs
    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_scatter"),
        Output(ID["graph"], "figure", allow_duplicate=True),
        Input("active-step-input", "value"),
        Input(ID["figures-store"], "data"),
        Input(ID["dropdown-x"], "value"),
        Input(ID["dropdown-symbol"], "value"),
        prevent_initial_call=True,
    )

    ## Displays the graphs using the controller
    ## Used for the last step of the section
    @app.callback(
        Output(ID["graph"], "figure", allow_duplicate=True),
        Input("active-step-input", "value"),
        Input(ID["dropdown-x"], "value"),
        Input(ID["dropdown-symbol"], "value"),
        prevent_initial_call=True,
    )
    def update_final_step(active_step, col_x, col_symbol):
        last_step = init_step + get_steps_number() - 1

        if active_step is None or int(active_step) != last_step:
            return no_update

        config = GraphConfig(col_x=ColX(col_x), col_symbol=SymbolVar(col_symbol))
        figure = create_figure(df, config)
        return figure

    @app.callback(
        Output(ID["dropdown-x"], "value"),
        Output(ID["dropdown-symbol"], "value"),
        Input("active-step-input", "value"),
    )
    def update_dropdowns_from_step(active_step):
        step = int(active_step or init_step) - init_step

        if(step >= get_steps_number() or step < 0):
            return no_update, no_update

        config : GraphConfig = get_step_graph_config(step)
        return config.col_x, config.col_symbol

    @app.callback(
        Output(ID["dropdown-x"], "disabled"),
        Output(ID["dropdown-symbol"], "disabled"),
        Input("active-step-input", "value"),
    )
    def toggle_controllers(active_step):
        step = int(active_step or init_step) - init_step

        if step < 0 or step >= len(STEPS_CONFIG):
            return True, True

        step_params : GraphConfig = get_step_graph_config(step)
        enabled = step_params.enable_interactions

        return not enabled, not enabled
