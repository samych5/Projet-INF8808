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
        text="Cette heat map montre la note finale moyenne selon le type d'école et la distance entre le domicile et l'école.",
        graph_config=GraphConfig(),
    ),
]


DEFAULT_CONFIG = GraphConfig()


def get_step_graph_config(step: int) -> GraphConfig:
    if 0 <= step < len(STEPS_CONFIG):
        return STEPS_CONFIG[step].graph_config
    return DEFAULT_CONFIG