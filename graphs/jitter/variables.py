from enum import Enum

class Genres(Enum):
    MEN = "Homme"
    WOMEN = "Femme"

class ColX(Enum):
    TUTORING_SESSIONS = "Tutoring_Sessions"
    PHYSICAL_ACTIVITY = "Physical_Activity"
    SLEEP_HOURS = "Sleep_Hours"

AXES_X = {
    ColX.TUTORING_SESSIONS: "Séances de tutorat",
    ColX.PHYSICAL_ACTIVITY: "Activité physique (sessions/semaine)",
    ColX.SLEEP_HOURS: "Heures de sommeil par nuit",
}

ID = {
    "graph" : "graph-jitter",
    "dropdown-x" : "dropdown-jitter-x",
    "figures-store": "jitter-figures-store"
}