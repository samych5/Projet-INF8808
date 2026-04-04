import plotly.graph_objects as go
from dash import dcc

from .variables import ID


def make_pie_chart():
    fig = create_pie_chart()

    return dcc.Graph(
        id=ID["pie-chart"],
        figure=fig,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "doubleClick": False,
        },
        className="heat-map-pie-chart",
    )


def create_pie_chart():
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Oui", "Non"],
                values=[75, 25],
                hole=0,
                textinfo="label+percent",
                sort=False,
                hoverinfo="skip",
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        height=200,
    )

    return fig