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
        x_range: list = [-1, 1],
    ):
        if layers is None:
            layers = []

        self.visible_factors = [factor.column for factor in visible_factors]
        self.show_legend = show_legend
        self.show_color_scale = show_color_scale
        self.layers = layers
        self.enable_interactions = enable_interactions
        self.x_range = x_range

        self.factor_brightness = {
            factor.column: True for factor in visible_factors
        }

        if factor_brightness is not None:
            for factor, is_bright in factor_brightness.items():
                self.factor_brightness[factor.column] = is_bright


class StepParameters:
    def __init__(self, text, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG: list[StepParameters] = [
    StepParameters(
        title="",
        text=(
            "Regardons maintenant les impacts en général."
        ),
        graph_config=GraphConfig(
            show_legend=False,
            show_color_scale=False,
            visible_factors=[],
        ),
    ),
    StepParameters(
        title="Qu'est-ce qui fait vraiment la réussite d'un élève ?",
        text=(
            "Pour répondre à cette question, nous avons analysé une multitude de facteurs du cadre de vie à l'effort personnel, "
            "en passant par l'environnement familial. Ce graphique classe ces variables selon leur degré de corrélation avec la note finale : "
            "plus la barre est longue et bleue, plus le facteur a un impact direct sur la performance."
        ),
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
    ),
    StepParameters(
        title="Facteurs liés à l'élève",
        text=(
            "Les données sont sans appel : la présence en cours et les heures étudiées sont les deux leviers les plus puissants pour réussir. "
            "Loin devant le talent inné ou le genre, c'est l'investissement direct de l'élève qui dicte la note finale. "
            "À noter : les activités parascolaires et le sommeil ont un impact quasi nul sur la note, prouvant qu'on peut avoir une vie équilibrée sans sacrifier ses résultats."
        ),
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
    ),
    StepParameters(
        title="Facteurs familiaux",
        text=(
            "Bien que le revenu familial joue un rôle, c'est l'implication des parents qui a l'impact le plus positif dans cette catégorie. "
            "Un parent qui suit le parcours de son enfant aide plus la réussite scolaire que le simple niveau d'études des parents ou le confort financier. "
            "L'accompagnement humain reste une ressource de premier plan."
        ),
        graph_config=GraphConfig(
            visible_factors=[
                Factors.PARENTAL_INVOLVEMENT,
                Factors.FAMILY_INCOME,
                Factors.PARENTAL_EDUCATION_LEVEL,
            ],
            show_legend=True,
            show_color_scale=True,
            x_range=[0, 1],
            factor_brightness={
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.FAMILY_INCOME: True,
                Factors.PARENTAL_EDUCATION_LEVEL: True,
            },
        ),
    ),
    StepParameters(
        title="Facteurs scolaires",
        text=(
            "L'analyse montre que l'accès aux ressources est bien plus déterminant que le prestige de l'école (public ou privé), "
            "dont la corrélation est presque inexistante. En somme, peu importe l'étiquette de l'école, "
            "c'est la qualité des outils mis à disposition de l'élève qui fait la différence."
        ),
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
            x_range=[0, 1],
            factor_brightness={
                Factors.ACCESS_TO_RESOURCES: True,
                Factors.DISTANCE: True,
                Factors.TEACHER_QUALITY: True,
                Factors.INTERNET_ACCESS: True,
                Factors.PEER_INFLUENCE: True,
                Factors.SCHOOL_TYPE: True,
            },
        ),
    ),
    StepParameters(
        title="Synthèse finale",
        text=(
            "En regardant la vue d'ensemble, on s'aperçoit que la réussite scolaire est une pyramide : "
            "la base solide est faite d'assiduité et de travail personnel. "
            "Les facteurs extérieurs (école, parents, revenus) ne sont que des bonus qui viennent affiner le résultat. "
            "C'est une conclusion encourageante : la clé du succès est majoritairement entre les mains de l'élève."
        ),
        graph_config=GraphConfig(
            show_legend=True,
            show_color_scale=True,
            enable_interactions=True,
        ),
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