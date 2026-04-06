def make_hover_component(label_x: str, genre: str) -> str:
    return (
        f"<b>{genre}</b><br>"
        f"{label_x} : <b>%{{x:.0f}}</b><br>"
        "Note finale : <b>%{y}</b>"
        "<extra></extra>"
    )