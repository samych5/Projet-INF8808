from dash import clientside_callback, ClientsideFunction, Input, Output, no_update

from .steps_config import STEPS_CONFIG, GraphConfig, get_step_graph_config
from .template import get_steps_number
from .graph import create_figure
from .variables import *

def register_callbacks(app, df, init_step: int):

    ## Displays precalculated graphs
    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_scatter"),
        Output(ID["graph"], "figure", allow_duplicate=True),
        Input("active-step-input", "value"),
        Input(ID["figures-store"], "data"),
        Input(ID["dropdown-x"], "value"),
        prevent_initial_call=True,
    )

    ## Displays the graph using the controller (last step only)
    @app.callback(
        Output(ID["graph"], "figure", allow_duplicate=True),
        Input("active-step-input", "value"),
        Input(ID["dropdown-x"], "value"),
        prevent_initial_call=True,
    )
    def update_final_step(active_step, col_x):
        last_step = init_step + get_steps_number() - 1

        if active_step is None or int(active_step) != last_step:
            return no_update

        local_step = last_step - init_step

        step_config = get_step_graph_config(local_step)
        step_config.col_x = col_x

        figure = create_figure(df, step_config)
        return figure

    @app.callback(
        Output(ID["dropdown-x"], "value"),
        Input("active-step-input", "value"),
    )
    def update_dropdowns_from_step(active_step):
        step = int(active_step or init_step) - init_step

        if step >= get_steps_number() or step < 0:
            return no_update

        config: GraphConfig = get_step_graph_config(step)
        return config.col_x

    @app.callback(
        Output(ID["dropdown-x"], "disabled"),
        Input("active-step-input", "value"),
    )
    def toggle_controllers(active_step):
        step = int(active_step or init_step) - init_step

        if step < 0 or step >= len(STEPS_CONFIG):
            return True

        step_params: GraphConfig = get_step_graph_config(step)
        enabled = step_params.enable_interactions

        return not enabled