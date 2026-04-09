from dash import Dash

app = Dash(
    __name__,
    title="Performance scolaire · INF8808",
    suppress_callback_exceptions=True,
)

server = app.server