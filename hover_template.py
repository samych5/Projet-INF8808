def scatter_eleve(label_x: str, genre: str, val: str, col_symbol_label: str) -> str:
    return (
        f"<b>{genre}</b> · {col_symbol_label} : {val}<br>"
        f"{label_x} : <b>%{{x}}</b><br>"
        "Note finale : <b>%{y}</b>"
        "<extra></extra>"
    )
    
def jitter_eleve(label_x: str, genre: str) -> str:
    return (
        f"<b>{genre}</b><br>"
        f"{label_x} : <b>%{{x:.0f}}</b><br>"
        "Note finale : <b>%{y}</b>"
        "<extra></extra>"
    )