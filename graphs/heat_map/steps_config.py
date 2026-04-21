class GraphConfig:
    def __init__(self, title: str = "Lien entre le type d'école, la distance et la note finale"):
        self.title = title


class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG = [
    StepParameters(
        title="Résultat",
        text=(
            "Cette carte de chaleur présente la note finale moyenne selon le type d’école et la distance entre le domicile et l’établissement. "
            "On observe une légère tendance indiquant que les élèves qui habitent plus près de leur école obtiennent des résultats un peu plus élevés, "
            "que ce soit dans le secteur public ou privé. Cependant, les écarts observés restent très faibles (environ 1 %), ce qui n’est pas suffisant "
            "pour conclure à une différence réelle ou significative sur le plan statistique. Autrement dit, même si la proximité semble associée à de "
            "meilleurs résultats, cette relation demeure limitée et doit être interprétée avec prudence. Cela dit, sur le plan logique et dans la réalité "
            "quotidienne, il est donc valable de vouloir réduire le temps de transport, la fatigue et créer potentiellement plus de temps disponible pour "
            "étudier ou se reposer en plaçant son enfant dans une école plus proche de la maison. Cependant, ces éléments, distance et type d’école, ne "
            "suffisent pas à expliquer à eux seuls les performances académiques, qui dépendent d’un ensemble de facteurs beaucoup plus larges."
        ),
        graph_config=GraphConfig(),
    ),
]


DEFAULT_CONFIG = GraphConfig()


def get_step_graph_config(step: int) -> GraphConfig:
    if 0 <= step < len(STEPS_CONFIG):
        return STEPS_CONFIG[step].graph_config
    return DEFAULT_CONFIG