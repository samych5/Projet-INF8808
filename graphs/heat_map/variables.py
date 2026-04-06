from enum import Enum


class DistanceCategory(Enum):
    NEAR = ("Proche", "Proche")
    MODERATE = ("Modérée", "Modérée")
    FAR = ("Loin", "Loin")

    def __init__(self, column_value: str, label: str):
        self.value_db = column_value
        self.label = label


class SchoolType(Enum):
    PUBLIC = ("Public", "Public")
    PRIVATE = ("Privé", "Privé")

    def __init__(self, column_value: str, label: str):
        self.value_db = column_value
        self.label = label


class Columns(Enum):
    DISTANCE = ("Distance", "Distance")
    SCHOOL_TYPE = ("Type_ecole", "Type d'école")
    EXAM_SCORE = ("Exam_Score", "Note finale (%)")

    def __init__(self, column_name: str, label: str):
        self.column = column_name
        self.label = label


DISTANCE_ORDER = [
    DistanceCategory.NEAR.value_db,
    DistanceCategory.MODERATE.value_db,
    DistanceCategory.FAR.value_db,
]

DISTANCE_LABELS = {
    DistanceCategory.NEAR.value_db: DistanceCategory.NEAR.label,
    DistanceCategory.MODERATE.value_db: DistanceCategory.MODERATE.label,
    DistanceCategory.FAR.value_db: DistanceCategory.FAR.label,
}

SCHOOL_TYPE_ORDER = [
    SchoolType.PUBLIC.value_db,
    SchoolType.PRIVATE.value_db,
]

SCHOOL_TYPE_LABELS = {
    SchoolType.PUBLIC.value_db: SchoolType.PUBLIC.label,
    SchoolType.PRIVATE.value_db: SchoolType.PRIVATE.label,
}

ID = {
    "graph": "graph-heat-map",
    "figures-store": "heat-map-figures-store",

    "section": "section-heat-map",
    "question-view": "heat-map-question-view",
    "result-view": "heat-map-result-view",

    "answer-store": "heat-map-answer-store",

    "btn-yes": "heat-map-btn-yes",
    "btn-no": "heat-map-btn-no",

    "pie-chart": "heat-map-pie-chart",
    "pie-wrapper": "heat-map-pie-wrapper",
    "question-text": "heat-map-question-text",
}