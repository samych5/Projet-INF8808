import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .variables import AXES_X

class BaseLayer:
    def apply(self, fig, df, config):
        raise NotImplementedError

class LinearTrendLayer(BaseLayer):
    def apply(self, fig, df, config):
        visible_df = df[df["Genre"].isin(config.visible_genres)].copy()

        x = pd.to_numeric(visible_df[config.col_x], errors="coerce")
        y = pd.to_numeric(visible_df["Exam_Score"], errors="coerce")

        mask = x.notna() & y.notna()
        x = x[mask]
        y = y[mask]

        if len(x) < 2:
            return

        slope, intercept = np.polyfit(x, y, 1)

        x_line = np.array([x.min(), x.max()])
        y_line = slope * x_line + intercept

        fig.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Tendance (lin.)",
            line=dict(color="black", width=3),
        ))