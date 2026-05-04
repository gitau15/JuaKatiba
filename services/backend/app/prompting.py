ABSTENTION_TOKEN = "INSUFFICIENT_CONTEXT"


PUBLIC_TONE = "Use plain, simple English and avoid legal jargon."
ENTERPRISE_TONE = "Use precise legal language and preserve statutory references."


def normalize_question(question: str) -> str:
    return " ".join(question.strip().split())


def choose_tone(tier: str) -> str:
    if tier == "enterprise":
        return ENTERPRISE_TONE
    return PUBLIC_TONE
