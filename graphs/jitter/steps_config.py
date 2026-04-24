from utils.layers import BaseLayer
from .variables import *

class GraphConfig:
    def __init__(
        self,
        col_x: ColX = ColX.TUTORING_SESSIONS,
        visible_gender: list[Genres] = [Genres.MEN, Genres.WOMEN],
        show_legend: bool = True,
        layers: list[BaseLayer] = [],
        enable_interactions: bool = False,
        title_graph: str = "",
    ):
        self.col_x = col_x.value
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
        "Bien qu'utile pour débloquer des concepts précis, l'impact statistique du tutorat plafonne rapidement chez les hommes comme chez les femmes, suggérant qu'il ne peut se substituer à un travail personnel de fond.",
        GraphConfig(
            col_x=ColX.TUTORING_SESSIONS,
            layers=[],
            title_graph="Impact du tutorat",
        ),
        title="Tutorat",
    ),
    StepParameters(
        "Bien qu'essentiel à la santé mentale et physique, le temps de repos ne montre pas de lien statistique significatif avec la performance brute chez les hommes comme chez les femmes, indiquant que l'efficacité du travail prime sur la simple récupération.",
        GraphConfig(
            col_x=ColX.SLEEP_HOURS,
            layers=[],
            title_graph="Impact des heures de sommeil",
        ),
        title="Sommeil",
    ),
    StepParameters(
        "Si le sport est indispensable à l'équilibre de vie de l'élève, son impact sur les résultats académiques est quasi nul chez les hommes comme chez les femmes, confirmant une indépendance entre performance cognitive scolaire et forme physique.",
        GraphConfig(
            col_x=ColX.PHYSICAL_ACTIVITY,
            layers=[],
            title_graph="Impact de l'activité physique",
        ),
        title="Activité physique",
    ),
]

DEFAULT_CONFIG: StepParameters = StepParameters("default_text", GraphConfig(), title="default_title")

def get_step_graph_config(step: int) -> GraphConfig:
    if step > len(STEPS_CONFIG) - 1 or step < 0:
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config