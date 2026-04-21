import os
import base64

def load_img(graph_name: str, index: int) -> str:
    path = os.path.join("assets", "images", "graphs", f"{graph_name}-{index}.png")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"