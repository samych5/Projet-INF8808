from dash import html
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
    def __init__(self, text, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG: list[StepParameters] = [
    StepParameters(
        title="",
        text="Nous allons maintenant nous intéresser aux facteurs environnementaux qui peuvent influencer la réussite scolaire.",
        graph_config=GraphConfig(
            factor_brightness={
                Factors.PARENTAL_EDUCATION_LEVEL: False,
                Factors.FAMILY_INCOME: False,
                Factors.PARENTAL_INVOLVEMENT: False,
                Factors.ACCESS_TO_RESOURCES: False,
                Factors.TEACHER_QUALITY: False,
                Factors.PEER_INFLUENCE: False,
            },
        ),
    ),

    StepParameters(
        title="Comment interpréter ce graphique ?",
        text=html.Ul([
            html.Li("La boîte représente la majorité des résultats. Plus elle est haute, plus les valeurs sont élevées."),
            html.Li("La ligne au centre correspond à la valeur typique (la médiane). Elle indique où se situe le milieu des données."),
            html.Li("Les barres (moustaches) montrent l'étendue des résultats, du plus bas au plus élevé."),
            html.Li("Les points autour représentent des résultats inhabituels, très différents de la majorité."),
        ]),
        graph_config=GraphConfig(
            factor_brightness={
                Factors.PARENTAL_EDUCATION_LEVEL: True,
                Factors.FAMILY_INCOME: True,
                Factors.PARENTAL_INVOLVEMENT: True,
                Factors.ACCESS_TO_RESOURCES: True,
                Factors.TEACHER_QUALITY: True,
                Factors.PEER_INFLUENCE: True,
            },
        ),
    ),

    StepParameters(
    title="Facteurs familiaux",
    text=html.Ul([
        html.Li("Les élèves dont les parents ont un niveau d'éducation plus élevé obtiennent légèrement de meilleures notes."),
        html.Li("On observe une tendance similaire pour le revenu familial et l’implication parentale : des niveaux plus élevés de revenu et d’implication sont associés à de meilleures performances."),
        html.Li("La différence existe, mais elle reste modérée : les groupes se chevauchent beaucoup."),
    ]),
    graph_config=GraphConfig(
        visible_factors=[
            Factors.PARENTAL_EDUCATION_LEVEL,
            Factors.FAMILY_INCOME,
            Factors.PARENTAL_INVOLVEMENT,
            Factors.ACCESS_TO_RESOURCES,
            Factors.TEACHER_QUALITY,
            Factors.PEER_INFLUENCE,
        ],
        factor_brightness={
            Factors.PARENTAL_EDUCATION_LEVEL: True,
            Factors.FAMILY_INCOME: True,
            Factors.PARENTAL_INVOLVEMENT: True,
            Factors.ACCESS_TO_RESOURCES: False,
            Factors.TEACHER_QUALITY: False,
            Factors.PEER_INFLUENCE: False,
        },
    ),
),

    StepParameters(
    title="Encadrement scolaire",
    text=html.Ul([
        html.Li("Les élèves ayant un meilleur accès aux ressources et bénéficiant d’enseignants de meilleure qualité obtiennent légèrement de meilleures notes."),
        html.Li("La différence existe, mais elle reste modérée : les groupes se chevauchent beaucoup."),
        html.Li("L'influence des pairs a peu d'impact."),
    ]),
    graph_config=GraphConfig(
        visible_factors=[
            Factors.PARENTAL_EDUCATION_LEVEL,
            Factors.FAMILY_INCOME,
            Factors.PARENTAL_INVOLVEMENT,
            Factors.ACCESS_TO_RESOURCES,
            Factors.TEACHER_QUALITY,
            Factors.PEER_INFLUENCE,
        ],
        factor_brightness={
            Factors.PARENTAL_EDUCATION_LEVEL: False,
            Factors.FAMILY_INCOME: False,
            Factors.PARENTAL_INVOLVEMENT: False,
            Factors.ACCESS_TO_RESOURCES: True,
            Factors.TEACHER_QUALITY: True,
            Factors.PEER_INFLUENCE: True,
        },
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