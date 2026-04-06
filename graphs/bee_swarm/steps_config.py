class GraphConfig:
    def __init__(self, title: str = "Essaim d’abeille interactif"):
        self.title = title


class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG = [
    StepParameters(
        title="Essaim d’abeille interactif",
        text=(
            "Ci-dessous, vous trouverez un graphique interactif dans lequel chaque point représente un élève. "
            "Les filtres permettent de mettre en lumière les élèves correspondant à certaines caractéristiques, "
            "afin de situer plus facilement votre enfant par rapport à l’ensemble du jeu de données."
        ),
        graph_config=GraphConfig(),
    ),
]


def get_step_graph_config(step: int) -> GraphConfig:
    return STEPS_CONFIG[0].graph_config