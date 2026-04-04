from enum import Enum


class Columns(Enum):
    EXAM_SCORE = ("Exam_Score", "Score à l'examen")
    HOURS_STUDIED = ("Hours_Studied", "Heures d'étude")
    ATTENDANCE = ("Attendance", "Présence (%)")
    PREVIOUS_SCORES = ("Previous_Scores", "Scores précédents")
    PHYSICAL_ACTIVITY = ("Physical_Activity", "Activité physique")

    def __init__(self, column: str, label: str):
        self.column = column
        self.label = label


CATEGORICAL_ATTRS = {
    "Gender": ["Female", "Male"],
    "School_Type": ["Public", "Private"],
    "Parental_Involvement": ["Low", "Medium", "High"],
    "Access_to_Resources": ["Low", "Medium", "High"],
    "Extracurricular_Activities": ["No", "Yes"],
    "Motivation_Level": ["Low", "Medium", "High"],
    "Internet_Access": ["No", "Yes"],
    "Family_Income": ["Low", "Medium", "High"],
    "Teacher_Quality": ["Low", "Medium", "High"],
    "Peer_Influence": ["Negative", "Neutral", "Positive"],
    "Learning_Disabilities": ["No", "Yes"],
    "Parental_Education_Level": ["High School", "College", "Postgraduate"],
    "Distance_from_Home": ["Near", "Moderate", "Far"],
    "Sleep_Hours": ["4", "5", "6", "7", "8", "9", "10"],
    "Tutoring_Sessions": ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
}

NUMERIC_ATTRS = [
    "Hours_Studied",
    "Attendance",
    "Previous_Scores",
    "Physical_Activity",
]

LABELS = {
    "Gender": "Genre",
    "School_Type": "Type d'école",
    "Parental_Involvement": "Implication parentale",
    "Access_to_Resources": "Accès aux ressources",
    "Extracurricular_Activities": "Activités extra-scolaires",
    "Motivation_Level": "Motivation",
    "Internet_Access": "Accès internet",
    "Family_Income": "Revenu familial",
    "Teacher_Quality": "Qualité enseignants",
    "Peer_Influence": "Influence des pairs",
    "Learning_Disabilities": "Troubles d'apprentissage",
    "Parental_Education_Level": "Éducation parentale",
    "Distance_from_Home": "Distance domicile-école",
    "Sleep_Hours": "Heures de sommeil",
    "Tutoring_Sessions": "Séances de tutorat",
    "Hours_Studied": "Heures d'étude",
    "Attendance": "Présence (%)",
    "Previous_Scores": "Scores précédents",
    "Physical_Activity": "Activité physique",
    "Exam_Score": "Score à l'examen",
}

PALETTE = [
    "#e07b00", "#3b82f6", "#22c55e", "#ec4899",
    "#a855f7", "#f97316", "#14b8a6", "#eab308",
    "#f87171", "#67e8f9",
]

ID = {
    "graph": "beeswarm-graph",
    "selected-filters-store": "beeswarm-selected-filters-store",
    "filter-page-store": "beeswarm-filter-page-store",
    "filters-container": "beeswarm-filters-container",
    "active-filters-bar": "beeswarm-active-filters-bar",
    "page-label": "beeswarm-page-label",
    "prev-page-btn": "beeswarm-prev-page-btn",
    "next-page-btn": "beeswarm-next-page-btn",
    "reset-all-btn": "beeswarm-reset-all-btn",
}

FILTERS_PER_PAGE = 3