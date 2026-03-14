import os
import pandas as pd

_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets", "data", "StudentPerformanceFactors.csv"
)


def get_data() -> pd.DataFrame:
    df = pd.read_csv(_CSV, sep=";")
    df = df.dropna()

    df["Genre"] = df["Gender"].map(
        {"Male": "Homme", "Female": "Femme"}
    )
    df["Parascolaire"] = df["Extracurricular_Activities"].map(
        {"Yes": "Oui", "No": "Non"}
    )
    df["Motivation"] = df["Motivation_Level"].map(
        {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"}
    )
    df["Implication_parentale"] = df["Parental_Involvement"].map(
        {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"}
    )
    df["Revenu"] = df["Family_Income"].map(
        {"Low": "Faible", "Medium": "Moyen", "High": "Élevé"}
    )
    df["Education_parents"] = df["Parental_Education_Level"].map(
        {"High School": "Secondaire", "College": "Collégial",
         "Postgraduate": "Universitaire"}
    )
    df["Qualite_enseignants"] = df["Teacher_Quality"].map(
        {"Low": "Faible", "Medium": "Moyenne", "High": "Élevée"}
    )
    df["Influence_pairs"] = df["Peer_Influence"].map(
        {"Positive": "Positive", "Neutral": "Neutre", "Negative": "Négative"}
    )
    df["Type_ecole"] = df["School_Type"].map(
        {"Public": "Public", "Private": "Privé"}
    )
    df["Distance"] = df["Distance_from_Home"].map(
        {"Near": "Proche", "Moderate": "Modérée", "Far": "Loin"}
    )
    df["Acces_ressources"] = df["Access_to_Resources"].map(
        {"Low": "Faible", "Medium": "Moyen", "High": "Élevé"}
    )
    df["Troubles_apprentissage"] = df["Learning_Disabilities"].map(
        {"Yes": "Oui", "No": "Non"}
    )
    df["Acces_internet"] = df["Internet_Access"].map(
        {"Yes": "Oui", "No": "Non"}
    )

    return df
