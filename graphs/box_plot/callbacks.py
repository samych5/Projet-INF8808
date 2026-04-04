from dash import Input, Output, no_update

from .steps_config import STEPS_CONFIG, GraphConfig, get_step_graph_config
from .graph import create_figure
from .variables import *


def register_callbacks(app, df, init_step: int):

    @app.callback(
        Output(ID["graph"], "figure"),
        Input("active-step-input", "value"),
    )
    def update_graph_from_step(active_step):
        if active_step is None:
            config = get_step_graph_config(0)
            return create_figure(df, config)

        try:
            local_step = int(active_step) - init_step
        except (TypeError, ValueError):
            return no_update

        if local_step < 0 or local_step >= len(STEPS_CONFIG):
            return no_update

        config: GraphConfig = get_step_graph_config(local_step)
        return create_figure(df, config)