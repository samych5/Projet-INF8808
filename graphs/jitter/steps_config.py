from .variables import *

class GraphConfig:
    def __init__(
        self,
        col_x : ColX = ColX.TUTORING_SESSIONS,
        visible_gender: list[Genres] = [Genres.MEN, Genres.WOMEN],
        show_legend: bool = True,
        layers : list = [],
        enable_interactions: bool = False
    ):
        self.col_x = col_x.value
        self.visible_genres = [gender.value for gender in visible_gender]
        self.show_legend = show_legend
        self.layers = layers
        self.enable_interactions = enable_interactions

class StepParameters:
    def __init__(self, text: str, graph_config : GraphConfig):
        self.text = text
        self.graph_config = graph_config

STEPS_CONFIG : list[StepParameters] = [
    StepParameters("text 1 test", GraphConfig(col_x=ColX.TUTORING_SESSIONS)),
    StepParameters("text 2", GraphConfig(col_x=ColX.SLEEP_HOURS)),
    StepParameters("text 3", GraphConfig(col_x=ColX.SLEEP_HOURS, visible_gender=[Genres.MEN])),
    StepParameters(text="text 4", graph_config=GraphConfig(enable_interactions=True))
]

DEFAULT_CONFIG : StepParameters = StepParameters("default_text", GraphConfig())

def get_step_graph_config(step: int) -> GraphConfig:
    if(step > len(STEPS_CONFIG) - 1 or step < 0):
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config
