from dash import Input, Output
from server import app
from preprocess import get_data
from template import get_layout
from scatter import create_figure as scatter_figure

df = get_data()
app.layout = get_layout()

@app.callback(
    Output("graph-scatter", "figure"),
    Input("dropdown-scatter-x", "value"),
)
def update_scatter(col_x):
    return scatter_figure(df, col_x)

if __name__ == "__main__":
    app.run(debug=True)