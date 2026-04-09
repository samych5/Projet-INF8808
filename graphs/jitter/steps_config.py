from .layers import BaseLayer, LinearTrendLayer
from .variables import *

class GraphConfig:
    def __init__(
        self,
        col_x : ColX = ColX.TUTORING_SESSIONS,
        visible_gender: list[Genres] = [Genres.MEN, Genres.WOMEN],
        show_legend: bool = True,
        layers : list[BaseLayer] = [],
        enable_interactions: bool = False
    ):
        self.col_x = col_x.value
        self.visible_genres = [gender.value for gender in visible_gender]
        self.show_legend = show_legend
        self.layers = layers
        self.enable_interactions = enable_interactions

class StepParameters:
    def __init__(self, text: str, graph_config : GraphConfig, title: str ):
        self.text = text
        self.graph_config = graph_config
        self.title = title

STEPS_CONFIG : list[StepParameters] = [
    StepParameters("Un soutien utile, mais dont l'impact positif plafonne rapidement malgré l'investissement.", GraphConfig(col_x=ColX.TUTORING_SESSIONS), title="Le tutorat a un petit impact."),
    StepParameters("Un facteur vital pour l'équilibre, mais sans lien statistique avec la performance académique.", GraphConfig(col_x=ColX.TUTORING_SESSIONS, layers=[LinearTrendLayer()]), title="Le sommeil n'a pas d'impact."),
    StepParameters("Essentiel pour la santé, mais sans incidence mesurable sur la moyenne finale.", GraphConfig(col_x=ColX.PHYSICAL_ACTIVITY, layers=[LinearTrendLayer()]), title="L'activité physique n'a pas d'impact. "),
]

DEFAULT_CONFIG : StepParameters = StepParameters("default_text", GraphConfig(), title="default_title")

def get_step_graph_config(step: int) -> GraphConfig:
    if(step > len(STEPS_CONFIG) - 1 or step < 0):
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config
