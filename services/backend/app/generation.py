import re
from pathlib import Path

from app.models import QueryResponse, Source
from app.prompting import ABSTENTION_TOKEN, choose_tone
from app.retrieval import RetrievedChunk


NOTICE_PATTERN = re.compile(r"NOTICE\s+NO\.?\s*(\d+)", re.IGNORECASE)


class GenerationService:
    """Guardrail-first generation with citation validation and enterprise audit logging."""

    def __init__(self, audit_log_path: str = "audit/flagged.log") -> None:
        self.audit_log_path = Path(audit_log_path)

    def answer(self, question: str, tier: str, context: list[RetrievedChunk]) -> QueryResponse:
        _ = choose_tone(tier)

        if not context:
            return QueryResponse(answer=ABSTENTION_TOKEN, status="insufficient_context", sources=[])

        answer = self._compose_answer(question, context)

        if not self._is_grounded(answer, context):
            self._persist_flag(tier=tier, question=question, answer=answer)
            return QueryResponse(
                answer=ABSTENTION_TOKEN,
                status="blocked",
                sources=[],
                reason="hallucinated_citation",
            )

        return QueryResponse(
            answer=answer,
            status="ok",
            sources=[Source(notice_id=c.notice_id, date=c.date) for c in context],
        )

    def _compose_answer(self, question: str, context: list[RetrievedChunk]) -> str:
        _ = question
        primary = context[0]
        summary = primary.text[:200].strip()
        return f"Based on Gazette Notice No. {primary.notice_id} ({primary.date}): {summary}"

    @staticmethod
    def _is_grounded(answer: str, context: list[RetrievedChunk]) -> bool:
        cited_ids = set(NOTICE_PATTERN.findall(answer))
        if not cited_ids:
            return True
        context_ids = {c.notice_id for c in context}
        return cited_ids.issubset(context_ids)

    def _persist_flag(self, tier: str, question: str, answer: str) -> None:
        if tier != "enterprise":
            return
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"question={question}\tanswer={answer}\n")
