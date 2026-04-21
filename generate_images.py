import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from preprocess import get_data
from graphs.scatter.graph import create_figure as scatter_fig
from graphs.scatter.steps_config import STEPS_CONFIG as SCATTER_STEPS

from graphs.jitter.graph import create_figure as jitter_fig
from graphs.jitter.steps_config import STEPS_CONFIG as JITTER_STEPS

from graphs.box_plot.graph import create_figure as boxplot_fig
from graphs.box_plot.steps_config import STEPS_CONFIG as BOXPLOT_STEPS

from graphs.bar_chart.graph import create_figure as barchart_fig
from graphs.bar_chart.steps_config import STEPS_CONFIG as BARCHART_STEPS

OUTPUT_DIR = os.path.join("assets", "images", "graphs")

if os.path.exists(OUTPUT_DIR):
    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Erreur suppression {file_path}: {e}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = get_data()

GRAPHS = [
    ("scatter", scatter_fig, SCATTER_STEPS),
    ("jitter", jitter_fig, JITTER_STEPS),
    ("boxplot", boxplot_fig, BOXPLOT_STEPS),
    ("barchart", barchart_fig, BARCHART_STEPS),
]

for graph_name, create_figure, steps in GRAPHS:
    print(f"Génération {graph_name}...")
    for i, step_params in enumerate(steps):
        print(f"  Image {i+1}/{len(steps)}...")
        fig = create_figure(df, step_params.graph_config)
        path = os.path.join(OUTPUT_DIR, f"{graph_name}-{i}.png")
        fig.write_image(path, format="png", width=1200, height=700, scale=2)
        print(f"  Sauvegardé : {path}")

print("Toutes les images générées !")