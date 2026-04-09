class GraphConfig:
    def __init__(self, title: str = "Essaim d'abeille interactif"):
        self.title = title


class StepParameters:
    def __init__(self, text: str, graph_config: GraphConfig, title: str):
        self.text = text
        self.graph_config = graph_config
        self.title = title


STEPS_CONFIG = [
    StepParameters(
        title="À vous de jouer : Devenez l'analyste !",
        text=(
            "Les statistiques nous donnent une tendance, mais la réalité est souvent plus nuancée. "
            "C'est maintenant à votre tour d'explorer ces données ! "
            "Utilisez les filtres à votre disposition sur la droite pour créer vos propres scénarios : "
            "Modifiez, comparez et observez en temps réel comment les élèves qui répondent à ces critères performent. "
            "C'est l'occasion de tester vos propres hypothèses et de voir quels facteurs font pencher la balance !"
        ),
        graph_config=GraphConfig(),
    ),
]


def get_step_graph_config(step: int) -> GraphConfig:
    return STEPS_CONFIG[0].graph_config