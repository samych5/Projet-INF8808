import plotly.graph_objects as go
import pandas as pd
from hover_template import scatter_eleve

AXES_X = {
    "Hours_Studied": "Heures d'étude par semaine",
    "Attendance":    "Taux de présence (%)",
}

DROPDOWN_OPTIONS = [
    {"label": label, "value": col}
    for col, label in AXES_X.items()
]


def create_figure(df: pd.DataFrame, col_x: str = "Hours_Studied") -> go.Figure:
    label_x = AXES_X.get(col_x, col_x)
    fig = go.Figure()

    COLORS = {"Homme": "#1a6fdb", "Femme": "#ff1493"}

    for genre in ["Homme", "Femme"]:
        color = COLORS[genre]
        for para, symbol, show in [("Oui", "circle", True), ("Non", "circle-open", False)]:
            mask = (df["Genre"] == genre) & (df["Parascolaire"] == para)
            sub  = df[mask]
            fig.add_trace(go.Scatter(
                x=sub[col_x],
                y=sub["Exam_Score"],
                mode="markers",
                name=genre,
                showlegend=show,
                legendgroup=genre,
                marker=dict(
                    color=color,
                    symbol=symbol,
                    size=7,
                    opacity=0.65,
                    line=dict(width=1.4, color=color),
                ),
                hovertemplate=scatter_eleve(label_x, genre, para),
            ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        name="Parascolaire : Oui",
        marker=dict(color="grey", symbol="circle", size=7),
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        name="Parascolaire : Non",
        marker=dict(color="grey", symbol="circle-open", size=7, line=dict(width=1.4)),
    ))

    fig.update_layout(
        xaxis_title=label_x,
        yaxis_title="Note finale",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="DM Sans, Arial", size=13, color="#1a1a1a"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d8d0c0",
            borderwidth=1,
        ),
        margin=dict(l=60, r=20, t=20, b=60),
        transition=dict(duration=350, easing="cubic-in-out"),
        hovermode="closest",
        xaxis=dict(
    tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 44] if col_x == "Hours_Studied" else [60, 65, 70, 75, 80, 85, 90, 95, 100],
),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e8e0d0", zeroline=False, linecolor="#1a1a1a", linewidth=1.5)
    fig.update_yaxes(showgrid=True, gridcolor="#e8e0d0", zeroline=False, linecolor="#1a1a1a", linewidth=1.5)

    return fig