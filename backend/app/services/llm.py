CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end it all", "self harm",
    "hurt myself", "can't go on", "ending my life"
]

POS = {"confident","progress","okay","good","better","improve","win","focus"}
NEG = {"overwhelmed","anxious","fail","tired","stuck","panic","hopeless","procrastinate","exhausted"}

def _detect_crisis(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in CRISIS_KEYWORDS)

def _score_text(text: str) -> float:
    t = text.lower()
    pos = sum(1 for w in POS if w in t)
    neg = sum(1 for w in NEG if w in t)
    if pos == 0 and neg == 0:
        return 0.5
    s = (pos - neg) / max(1, pos + neg)
    return max(0.0, min(1.0, 0.5 + 0.5*s))

async def generate_bundle(prompt: str, history_snippets: list[str] | None = None) -> dict:
    crisis = _detect_crisis(prompt)
    score = _score_text(prompt)

    if crisis:
        return {
            "action_plan": "Pause tasks and reach out to someone you trust.",
            "wellness_tip": "If in danger, call local emergency services. In the U.S., dial or text 988.",
            "motivation": "You matter. Help is available and you deserve support.",
            "stress_score": score,
            "crisis": True
        }

    plan = (
        "1) 10-minute brain dump.\n"
        "2) Choose ONE tiny next step (≤10 min).\n"
        "3) 25-minute focus timer.\n"
        "4) 3-minute break.\n"
        "5) Log what worked."
    )
    tip = "Stand up, roll shoulders, sip water, take 6 slow breaths."
    mot = "You’ve handled hard days before — today is about momentum, not perfection."
    return {
        "action_plan": plan,
        "wellness_tip": tip,
        "motivation": mot,
        "stress_score": score,
        "crisis": False
    }
