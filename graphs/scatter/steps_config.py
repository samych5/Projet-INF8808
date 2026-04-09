from .variables import *

class GraphConfig:
    def __init__(
        self,
        col_x : ColX = ColX.HOURS_STUDIED,
        col_symbol : SymbolVar = SymbolVar.EXTRACURRICULAR_ACTIVITIES,
        visible_gender: list[Genres] = [Genres.MEN, Genres.WOMEN],
        show_legend: bool = True,
        layers : list = [],
        enable_interactions: bool = False
    ):
        self.col_x = col_x.value
        self.col_symbol = col_symbol.value
        self.visible_genres = [gender.value for gender in visible_gender]
        self.show_legend = show_legend
        self.layers = layers
        self.enable_interactions = enable_interactions

class StepParameters:
    def __init__(self, text: str, graph_config : GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title

STEPS_CONFIG : list[StepParameters] = [
    StepParameters("L'investissement personnel est le levier ayant l'impact le plus direct sur la réussite.", GraphConfig(col_x=ColX.HOURS_STUDIED), title="L'étude a un fort impact."),
    StepParameters("L'assiduité en classe demeure le facteur de stabilité le plus fiable pour les notes.", GraphConfig(col_x=ColX.ATTENDANCE), title="La présence a un fort impact."),
]

DEFAULT_CONFIG : StepParameters = StepParameters("default_text", GraphConfig(), title="default_title")

def get_step_graph_config(step: int) -> GraphConfig:
    if(step > len(STEPS_CONFIG) - 1 or step < 0):
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config
