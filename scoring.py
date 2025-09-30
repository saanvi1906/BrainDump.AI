def score_to_color(score: float) -> str:
    if score < 0.3:
        return "green"
    if score < 0.6:
        return "blue"
    return "red"
