from dash import Input, Output, no_update

from .steps_config import get_step_config
from .template import get_steps_number
from .graph import create_figure
from .ids import ID

def register_callbacks(app, df, init_step : int):

    @app.callback(
        Output(ID["graph"], "figure"),
        Input("active-step-input", "value"),
        Input(ID["dropdown-x"], "value"),
        Input(ID["dropdown-symbol"], "value"),
    )
    def update_scatter(active_step, col_x, col_symbol):
        step = int(active_step or init_step) - init_step

        if(step > get_steps_number()):
            return no_update

        config = get_step_config(step, col_x, col_symbol)
        return create_figure(df, **config)

    @app.callback(
        Output(ID["dropdown-x"], "value"),
        Output(ID["dropdown-symbol"], "value"),
        Input("active-step-input", "value"),
    )
    def update_dropdowns_from_step(active_step):
        step = int(active_step or init_step) - init_step

        if(step >= get_steps_number() or step < 0):
            return no_update, no_update

        config = get_step_config(step)
        return config["col_x"], config["col_symbol"]
