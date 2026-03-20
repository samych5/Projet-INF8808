from dash import Input, Output

from .graph import create_figure
from .ids import ID


def register_callbacks(app, df):
    @app.callback(
        Output(ID["graph"],      "figure"),
        Input(ID["dropdown-x"],  "value"),
    )
    def update_jitter(col_x):
        return create_figure(df, col_x)
