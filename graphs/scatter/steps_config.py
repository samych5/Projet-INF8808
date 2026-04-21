from utils.layers import LinearTrendLayer, BaseLayer

from .variables import *

class GraphConfig:
    def __init__(
        self,
        col_x: ColX = ColX.HOURS_STUDIED,
        col_symbol: SymbolVar = SymbolVar.EXTRACURRICULAR_ACTIVITIES,
        visible_gender: list[Genres] = [Genres.MEN, Genres.WOMEN],
        show_legend: bool = True,
        layers: list[BaseLayer] = [],
        enable_interactions: bool = False,
        title_graph: str = "",
    ):
        self.col_x = col_x.value
        self.col_symbol = col_symbol.value
        self.visible_genres = [gender.value for gender in visible_gender]
        self.show_legend = show_legend
        self.layers = layers
        self.enable_interactions = enable_interactions
        self.title_graph = title_graph


class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG: list[StepParameters] = [
    StepParameters(
        "Les données confirment que les heures consacrées à l'étude ne sont pas seulement un soutien, mais un réel levier ayant un fort impact sur la réussite finale.",
        GraphConfig(
            col_x=ColX.HOURS_STUDIED,
            title_graph="Impact des heures d'études et pratique d'activités parascolaires",
            layers=[LinearTrendLayer()],
        ),
        title="Heures d'études.",
    ),
    StepParameters(
        "L'analyse montre que la présence constante en classe demeure un facteur ayant un impact positif sur les résultats scolaires.",
        GraphConfig(
            col_x=ColX.ATTENDANCE,
            title_graph="Impact de la présence en classe et la pratique d'activités parascolaires",
            layers=[LinearTrendLayer()],
        ),
        title="Présence en classe",
    ),
]

DEFAULT_CONFIG: StepParameters = StepParameters("default_text", GraphConfig(), title="default_title")

def get_step_graph_config(step: int) -> GraphConfig:
    if step > len(STEPS_CONFIG) - 1 or step < 0:
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config