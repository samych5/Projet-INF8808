from .variables import *

class GraphConfig:
    def __init__(
        self,
        visible_factors: list[Factors] = [
            Factors.PARENTAL_EDUCATION_LEVEL,
            Factors.FAMILY_INCOME,
            Factors.PARENTAL_INVOLVEMENT,
            Factors.ACCESS_TO_RESOURCES,
            Factors.TEACHER_QUALITY,
            Factors.PEER_INFLUENCE,
        ],
        visible_levels: list[Levels] = [
            Levels.LOW,
            Levels.MEDIUM,
            Levels.HIGH,
        ],
        show_legend: bool = True,
        layers: list = None,
        enable_interactions: bool = False,
        factor_brightness: dict[Factors, bool] | None = None,
    ):
        if layers is None:
            layers = []

        self.visible_factors = [factor.value for factor in visible_factors]
        self.visible_levels = [level.label for level in visible_levels]
        self.show_legend = show_legend
        self.layers = layers
        self.enable_interactions = enable_interactions

        self.factor_brightness = {
            factor.value: True for factor in visible_factors
        }

        if factor_brightness is not None:
            for factor, is_bright in factor_brightness.items():
                self.factor_brightness[factor.value] = is_bright

class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG: list[StepParameters] = [
    StepParameters(
        text="Vue d’ensemble des facteurs environnementaux influençant la note d’examen.",
        graph_config=GraphConfig(
            factor_brightness={
                Factors.PARENTAL_EDUCATION_LEVEL: True,
                Factors.FAMILY_INCOME: True,
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.ACCESS_TO_RESOURCES: True,
                Factors.TEACHER_QUALITY: True,
                Factors.PEER_INFLUENCE: False,
            },
        ),
        title="Synthèse environnementale",
    ),
    StepParameters(
        text="Vue d’ensemble des facteurs environnementaux influençant la note d’examen.",
        graph_config=GraphConfig(
            show_legend=True,
            factor_brightness={
                Factors.PARENTAL_EDUCATION_LEVEL: True,
                Factors.FAMILY_INCOME: True,
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.ACCESS_TO_RESOURCES: False,
                Factors.TEACHER_QUALITY: False,
                Factors.PEER_INFLUENCE: True,
            },
        ),
        title="Synthèse environnementale",
    ),
    StepParameters(
        text="On commence par observer l’effet du milieu familial à travers l’éducation des parents et le revenu familial.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.PARENTAL_EDUCATION_LEVEL,
                Factors.FAMILY_INCOME,
            ],
            visible_levels=[Levels.LOW, Levels.MEDIUM, Levels.HIGH],
            show_legend=True,
            factor_brightness={
                Factors.PARENTAL_EDUCATION_LEVEL: True,
                Factors.FAMILY_INCOME: True,
            },
        ),
        title="Milieu familial",
    ),
    StepParameters(
        text="Ici, on se concentre sur l’implication parentale et l’accès aux ressources.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.PARENTAL_INVOLVEMENT,
                Factors.ACCESS_TO_RESOURCES,
            ],
            visible_levels=[Levels.LOW, Levels.MEDIUM, Levels.HIGH],
            show_legend=True,
            factor_brightness={
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.ACCESS_TO_RESOURCES: False,
            },
        ),
        title="Encadrement scolaire",
    ),
    StepParameters(
        text="Enfin, on termine avec la qualité des enseignants et l’influence des pairs.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.TEACHER_QUALITY,
                Factors.PEER_INFLUENCE,
            ],
            visible_levels=[Levels.LOW, Levels.MEDIUM, Levels.HIGH],
            show_legend=True,
            enable_interactions=True,
            factor_brightness={
                Factors.TEACHER_QUALITY: True,
                Factors.PEER_INFLUENCE: True,
            },
        ),
        title="Dernière étape",
    ),
]


DEFAULT_CONFIG: StepParameters = StepParameters(
    "default_text",
    GraphConfig(),
    title="default_title",
)


def get_step_graph_config(step: int) -> GraphConfig:
    if step > len(STEPS_CONFIG) - 1 or step < 0:
        return DEFAULT_CONFIG.graph_config
    return STEPS_CONFIG[step].graph_config