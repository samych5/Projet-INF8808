import plotly.graph_objects as go
import pandas as pd
from hover_template import scatter_eleve

AXES_X = {
    "Hours_Studied": "Heures d'étude par semaine",
    "Attendance":    "Taux de présence (%)",
}

SYMBOL_VAR_OPTIONS = [
    {"label": "Activités parascolaires", "value": "Parascolaire"},
    {"label": "Accès internet",          "value": "Acces_internet"},
    {"label": "Troubles d'apprentissage","value": "Troubles_apprentissage"},
]

DROPDOWN_OPTIONS = [
    {"label": label, "value": col}
    for col, label in AXES_X.items()
]

COLORS = {"Homme": "#1a6fdb", "Femme": "#ff1493"}

SYMBOL_VAR_LABELS = {
    "Parascolaire":          "Parascolaire",
    "Acces_internet":        "Accès internet",
    "Troubles_apprentissage":"Troubles d'apprentissage",
}


def create_figure(df: pd.DataFrame, col_x: str = "Hours_Studied", col_symbol: str = "Parascolaire") -> go.Figure:
    label_x = AXES_X.get(col_x, col_x)
    fig = go.Figure()

    vals = df[col_symbol].dropna().unique()
    val_oui = vals[0]
    val_non = vals[1] if len(vals) > 1 else vals[0]

    for genre in ["Homme", "Femme"]:
        color = COLORS[genre]
        for val, symbol, opacity, show in [
            (val_oui, "circle", 0.65, True),
            (val_non, "circle", 0.20, False),
        ]:
            mask = (df["Genre"] == genre) & (df[col_symbol] == val)
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
                    opacity=opacity,
                    line=dict(width=1.4, color=color),
                ),
                hovertemplate=scatter_eleve(label_x, genre, str(val), SYMBOL_VAR_LABELS.get(col_symbol, col_symbol)),
            ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        name=str(val_oui),
        marker=dict(color="grey", symbol="circle", size=7, opacity=0.65),
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        name=str(val_non),
        marker=dict(color="grey", symbol="circle", size=7, opacity=0.20),
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