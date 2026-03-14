def scatter_eleve(label_x: str, genre: str, para: str) -> str:
    return (
        f"<b>{genre}</b> · Parascolaire : {para}<br>"
        f"{label_x} : <b>%{{x}}</b><br>"
        "Note finale : <b>%{y}</b>"
        "<extra></extra>"
    )

