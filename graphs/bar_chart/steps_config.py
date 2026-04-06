from .variables import *


class GraphConfig:
    def __init__(
        self,
        visible_factors: list[Factors] = [
            Factors.ATTENDANCE,
            Factors.HOURS_STUDIED,
            Factors.ACCESS_TO_RESOURCES,
            Factors.TUTORING_SESSIONS,
            Factors.PARENTAL_INVOLVEMENT,
            Factors.FAMILY_INCOME,
            Factors.MOTIVATION,
            Factors.DISTANCE,
            Factors.TEACHER_QUALITY,
            Factors.EXTRACURRICULAR_ACTIVITIES,
            Factors.INTERNET_ACCESS,
            Factors.PEER_INFLUENCE,
            Factors.PARENTAL_EDUCATION_LEVEL,
            Factors.PHYSICAL_ACTIVITY,
            Factors.GENDER,
            Factors.SCHOOL_TYPE,
            Factors.SLEEP_HOURS,
        ],
        show_legend: bool = True,
        show_color_scale: bool = True,
        layers: list = None,
        enable_interactions: bool = False,
        factor_brightness: dict[Factors, bool] | None = None,
    ):
        if layers is None:
            layers = []

        self.visible_factors = [factor.column for factor in visible_factors]
        self.show_legend = show_legend
        self.show_color_scale = show_color_scale
        self.layers = layers
        self.enable_interactions = enable_interactions

        self.factor_brightness = {
            factor.column: True for factor in visible_factors
        }

        if factor_brightness is not None:
            for factor, is_bright in factor_brightness.items():
                self.factor_brightness[factor.column] = is_bright

class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG: list[StepParameters] = [
    StepParameters(
        text="Vue d’ensemble des facteurs influençant la performance scolaire, classés selon leur corrélation avec la note finale.",
        graph_config=GraphConfig(
            show_legend=True,
            show_color_scale=True,
            factor_brightness={
                Factors.ATTENDANCE: True,
                Factors.HOURS_STUDIED: True,
                Factors.TUTORING_SESSIONS: True,
                Factors.MOTIVATION: True,
                Factors.PHYSICAL_ACTIVITY: False,
                Factors.GENDER: False,
                Factors.SLEEP_HOURS: False,
                Factors.EXTRACURRICULAR_ACTIVITIES: False,
            },
        ),
        title="Prévisualisation",
    ),
    StepParameters(
        text="On commence par les facteurs liés à l’élève, comme l’assiduité, les heures d’étude, la motivation ou encore les activités parascolaires.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.ATTENDANCE,
                Factors.HOURS_STUDIED,
                Factors.TUTORING_SESSIONS,
                Factors.MOTIVATION,
                Factors.PHYSICAL_ACTIVITY,
                Factors.GENDER,
                Factors.SLEEP_HOURS,
                Factors.EXTRACURRICULAR_ACTIVITIES,
            ],
            show_legend=True,
            show_color_scale=True,
            factor_brightness={
                Factors.ATTENDANCE: True,
                Factors.HOURS_STUDIED: True,
                Factors.TUTORING_SESSIONS: True,
                Factors.MOTIVATION: True,
                Factors.PHYSICAL_ACTIVITY: False,
                Factors.GENDER: False,
                Factors.SLEEP_HOURS: False,
                Factors.EXTRACURRICULAR_ACTIVITIES: False,
            },
        ),
        title="Facteurs liés à l’élève",
    ),
    StepParameters(
        text="On observe ensuite les facteurs familiaux, comme l’implication parentale, le revenu et le niveau d’éducation des parents.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.PARENTAL_INVOLVEMENT,
                Factors.FAMILY_INCOME,
                Factors.PARENTAL_EDUCATION_LEVEL,
            ],
            show_legend=True,
            show_color_scale=True,
            factor_brightness={
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.FAMILY_INCOME: True,
                Factors.PARENTAL_EDUCATION_LEVEL: True,
            },
        ),
        title="Facteurs familiaux",
    ),
    StepParameters(
        text="Enfin, on regarde les facteurs liés à l’environnement scolaire, comme l’accès aux ressources, la qualité des enseignants, le type d’école ou l’influence des pairs.",
        graph_config=GraphConfig(
            visible_factors=[
                Factors.ACCESS_TO_RESOURCES,
                Factors.DISTANCE,
                Factors.TEACHER_QUALITY,
                Factors.INTERNET_ACCESS,
                Factors.PEER_INFLUENCE,
                Factors.SCHOOL_TYPE,
            ],
            show_legend=True,
            show_color_scale=True,
            factor_brightness={
                Factors.ACCESS_TO_RESOURCES: True,
                Factors.DISTANCE: False,
                Factors.TEACHER_QUALITY: True,
                Factors.INTERNET_ACCESS: False,
                Factors.PEER_INFLUENCE: True,
                Factors.SCHOOL_TYPE: False,
            },
        ),
        title="Facteurs scolaires",
    ),
    StepParameters(
        text="Cette dernière vue redonne une synthèse complète et permet d’explorer librement les variables les plus influentes.",
        graph_config=GraphConfig(
            show_legend=True,
            show_color_scale=True,
            enable_interactions=True,
        ),
        title="Synthèse finale",
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