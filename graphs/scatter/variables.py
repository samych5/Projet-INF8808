from enum import Enum

class Genres(Enum):
    MEN = "Homme"
    WOMEN = "Femme"

class ColX(Enum):
    HOURS_STUDIED = "Hours_Studied"
    ATTENDANCE = "Attendance"

AXES_X: dict[ColX, str] = {
    ColX.HOURS_STUDIED: "Heures d'étude par semaine",
    ColX.ATTENDANCE: "Taux de présence (%)",
}

class SymbolVar(Enum):
    EXTRACURRICULAR_ACTIVITIES = "Parascolaire"
    INTERNET_ACCESS = "Acces_internet"
    LEARNING_DISORDER = "Troubles_apprentissage"

SYMBOL_VAR_LABELS: dict[SymbolVar, str] = {
    SymbolVar.EXTRACURRICULAR_ACTIVITIES: "Activités parascolaires",
    SymbolVar.INTERNET_ACCESS: "Accès internet",
    SymbolVar.LEARNING_DISORDER: "Troubles d'apprentissage",
}
