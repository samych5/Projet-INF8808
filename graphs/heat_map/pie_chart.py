import plotly.graph_objects as go
from dash import dcc

from .variables import ID


def make_pie_chart(answer=None):
    fig = create_pie_chart(answer)

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


def create_pie_chart(answer=None):
    labels = ["Oui", "Non"]
    values = [75, 25]

    if answer == "yes":
        colors = ["#1a6fdb", "#ffffff"]
    else:
        colors = ["#ffffff", "#1a6fdb"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0,
                textinfo="label+percent",
                sort=False,
                hoverinfo="skip",
                marker=dict(
                    colors=colors,
                    line=dict(color="#e5e7eb", width=1),
                ),
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        height=200,
        dragmode=False,
    )

    return fig