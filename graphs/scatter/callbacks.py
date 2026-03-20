from dash import Input, Output

from .graph import create_figure
from .ids import ID

def register_callbacks(app, df):

    @app.callback(
        Output(ID["graph"], "figure"),
        Input(ID["dropdown-x"], "value"),
        Input(ID["dropdown-symbol"], "value"),
    )
    def update_scatter(col_x, col_symbol):
        return create_figure(df, col_x, col_symbol)