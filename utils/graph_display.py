import plotly.graph_objects as go

def add_layer_to_figure(fig: go.Figure, layer: dict):
    layer_type = layer.get("type")

    if layer_type == "circle":
        fig.add_shape(
            type="circle",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 3),
            ),
            fillcolor=layer.get("fillcolor", "rgba(0,0,0,0)"),
            opacity=layer.get("opacity", 1.0),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "rect":
        fig.add_shape(
            type="rect",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 2),
            ),
            fillcolor=layer.get("fillcolor", "rgba(255,0,0,0.08)"),
            opacity=layer.get("opacity", 1.0),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "line":
        fig.add_shape(
            type="line",
            x0=layer["x0"],
            x1=layer["x1"],
            y0=layer["y0"],
            y1=layer["y1"],
            xref=layer.get("xref", "x"),
            yref=layer.get("yref", "y"),
            line=dict(
                color=layer.get("line_color", "red"),
                width=layer.get("line_width", 2),
                dash=layer.get("dash", "solid"),
            ),
            layer=layer.get("layer", "above"),
        )

    elif layer_type == "annotation":
        fig.add_annotation(
            x=layer["x"],
            y=layer["y"],
            text=layer["text"],
            showarrow=layer.get("showarrow", True),
            arrowhead=layer.get("arrowhead", 2),
            ax=layer.get("ax", 0),
            ay=layer.get("ay", -40),
            font=layer.get("font", dict(size=13)),
        )

    elif layer_type == "scatter":
        fig.add_trace(go.Scatter(
            x=layer["x"],
            y=layer["y"],
            mode=layer.get("mode", "markers"),
            name=layer.get("name", ""),
            showlegend=layer.get("showlegend", False),
            marker=layer.get("marker", {}),
            line=layer.get("line", {}),
            text=layer.get("text"),
            hoverinfo=layer.get("hoverinfo", "skip"),
        ))
