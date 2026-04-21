from enum import Enum


class FactorCategory(Enum):
    STUDENT = "Élève"
    PARENTS = "Parents"
    SCHOOL = "École"


class Factors(Enum):
    # Élève
    ATTENDANCE = ("Attendance", "Présence en cours")
    HOURS_STUDIED = ("Hours_Studied", "Heures étudiées")
    PHYSICAL_ACTIVITY = ("Physical_Activity", "Activité Physique")
    SLEEP_HOURS = ("Sleep_Hours", "Heures de Sommeil")
    TUTORING_SESSIONS = ("Tutoring_Sessions", "Sessions de tutorat")
    GENDER = ("Genre", "Genre")
    MOTIVATION = ("Motivation", "Motivation")
    EXTRACURRICULAR_ACTIVITIES = ("Parascolaire", "Activités parascolaires")

    # Parents
    PARENTAL_INVOLVEMENT = ("Implication_parentale", "Implication Parentale")
    FAMILY_INCOME = ("Revenu", "Revenu Familial")
    PARENTAL_EDUCATION_LEVEL = ("Education_parents", "Éducation Parents")

    # École
    DISTANCE = ("Distance", "Distance")
    SCHOOL_TYPE = ("Type_ecole", "Type d'école")
    TEACHER_QUALITY = ("Qualite_enseignants", "Qualité des Enseignants")
    PEER_INFLUENCE = ("Influence_pairs", "Influence des Pairs")
    ACCESS_TO_RESOURCES = ("Acces_ressources", "Accès aux Ressources")
    INTERNET_ACCESS = ("Acces_internet", "Accès Internet")

    def __init__(self, column_name: str, label: str):
        self.column = column_name
        self.label = label


FACTOR_LABELS = {
    factor.column: factor.label
    for factor in Factors
}


FACTOR_CATEGORIES = {
    # Élève
    Factors.ATTENDANCE.column: FactorCategory.STUDENT,
    Factors.HOURS_STUDIED.column: FactorCategory.STUDENT,
    Factors.PHYSICAL_ACTIVITY.column: FactorCategory.STUDENT,
    Factors.SLEEP_HOURS.column: FactorCategory.STUDENT,
    Factors.TUTORING_SESSIONS.column: FactorCategory.STUDENT,
    Factors.GENDER.column: FactorCategory.STUDENT,
    Factors.MOTIVATION.column: FactorCategory.STUDENT,
    Factors.EXTRACURRICULAR_ACTIVITIES.column: FactorCategory.STUDENT,

    # Parents
    Factors.PARENTAL_INVOLVEMENT.column: FactorCategory.PARENTS,
    Factors.FAMILY_INCOME.column: FactorCategory.PARENTS,
    Factors.PARENTAL_EDUCATION_LEVEL.column: FactorCategory.PARENTS,

    # École
    Factors.DISTANCE.column: FactorCategory.SCHOOL,
    Factors.SCHOOL_TYPE.column: FactorCategory.SCHOOL,
    Factors.TEACHER_QUALITY.column: FactorCategory.SCHOOL,
    Factors.PEER_INFLUENCE.column: FactorCategory.SCHOOL,
    Factors.ACCESS_TO_RESOURCES.column: FactorCategory.SCHOOL,
    Factors.INTERNET_ACCESS.column: FactorCategory.SCHOOL,
}
