from server import app
from preprocess import get_data
from template import get_layout

from sections import SECTIONS, DEFAULT_STEP

server = app.server

df = get_data()
app.layout = get_layout(df)

def register_callbacks(df):
    init_step = DEFAULT_STEP

    for section in SECTIONS:
        section["callback"](app, df, init_step)
        init_step += section["n_steps"]()

register_callbacks(df)

if __name__ == "__main__":
    app.run(debug=True)