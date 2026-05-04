ABSTENTION_TOKEN = "INSUFFICIENT_CONTEXT"


def normalize_question(question: str) -> str:
    return " ".join(question.strip().split())


def choose_tone(tier: str) -> str:
    if tier == "enterprise":
        return "Use precise legal language and preserve statutory references."
    return "Use plain, simple English and avoid legal jargon."
