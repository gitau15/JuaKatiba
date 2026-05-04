from app.models import QueryResponse, Source
from app.prompting import ABSTENTION_TOKEN, choose_tone
from app.retrieval import RetrievedChunk


class GenerationService:
    """Guardrail-first generation scaffold.

    For now this only returns abstention when no context is available.
    """

    def answer(self, question: str, tier: str, context: list[RetrievedChunk]) -> QueryResponse:
        _ = (question, choose_tone(tier))

        if not context:
            return QueryResponse(answer=ABSTENTION_TOKEN, status="insufficient_context", sources=[])

        return QueryResponse(
            answer="Answer generation not implemented yet.",
            status="ok",
            sources=[Source(notice_id=c.notice_id, date=c.date) for c in context],
        )
