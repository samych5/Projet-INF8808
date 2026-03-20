from server import app
from preprocess import get_data
from template import get_layout

from graphs.scatter.callbacks import register_callbacks as register_scatter_callbacks
from graphs.jitter.callbacks import register_callbacks as register_jitter_callbacks


df = get_data()
app.layout = get_layout(df)

register_scatter_callbacks(app, df)
register_jitter_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)