from enum import Enum


class Factors(Enum):
    PARENTAL_EDUCATION_LEVEL = "Éducation Parents"
    FAMILY_INCOME = "Revenu Familial"
    PARENTAL_INVOLVEMENT = "Implication Parentale"
    ACCESS_TO_RESOURCES = "Accès aux Ressources"
    TEACHER_QUALITY = "Qualité des Enseignants"
    PEER_INFLUENCE = "Influence des Pairs"


class Levels(Enum):
    LOW = ("LOW", "1. Faible / Secondaire")
    MEDIUM = ("MEDIUM", "2. Moyen / Baccalauréat")
    HIGH = ("HIGH", "3. Élevé / Maîtrise et +")

    def __init__(self, key: str, label: str):
        self.key = key
        self.label = label

    def __str__(self):
        return self.label