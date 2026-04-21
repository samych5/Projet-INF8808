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
            "Cette carte de chaleur montre la note finale moyenne selon le type d'école et la distance entre le domicile et l'école. "
            "Les données montrent que la proximité du domicile est un facteur clé de succès : plus un élève habite près de son établissement, "
            "meilleure est sa note finale, qu'il soit dans le secteur public ou privé. "
            "S'il existe bien une tendance montrant que la proximité favorise légèrement les résultats, il faut garder en tête que les écarts constatés sont très faibles. "
            "Le succès d'un élève ne se joue pas uniquement sur son adresse postale. Le type d'école et la distance sont des facteurs d'influence, "
            "mais ils ne sont pas les seuls moteurs de la réussite scolaire, qui reste globalement constante dans tous les scénarios présentés."
        ),
        graph_config=GraphConfig(),
    ),
]


DEFAULT_CONFIG = GraphConfig()


def get_step_graph_config(step: int) -> GraphConfig:
    if 0 <= step < len(STEPS_CONFIG):
        return STEPS_CONFIG[step].graph_config
    return DEFAULT_CONFIG