from dataclasses import dataclass, field

from app.models import IngestNoticeRequest, QueryFilters


@dataclass
class RetrievedChunk:
    text: str
    notice_id: str
    date: str
    ministry: str
    notice_type: str
    entities_org: list[str] = field(default_factory=list)


class RetrievalService:
    """In-memory retrieval with lightweight hybrid scoring + payload filtering."""

    def __init__(self) -> None:
        self._notices: list[RetrievedChunk] = []

    def ingest(self, notice: IngestNoticeRequest) -> None:
        existing_ids = {n.notice_id for n in self._notices}
        if notice.notice_id in existing_ids:
            return
        self._notices.append(
            RetrievedChunk(
                text=notice.text,
                notice_id=notice.notice_id,
                date=notice.date,
                ministry=notice.ministry,
                notice_type=notice.notice_type,
                entities_org=notice.entities_org,
            )
        )

    def search(self, question: str, tier: str, filters: QueryFilters | None = None) -> list[RetrievedChunk]:
        _ = tier
        filtered = [n for n in self._notices if self._match_filters(n, filters)]
        ranked = sorted(filtered, key=lambda n: self._score(question, n), reverse=True)
        return [n for n in ranked if self._score(question, n) > 0][:5]

    @staticmethod
    def _match_filters(chunk: RetrievedChunk, filters: QueryFilters | None) -> bool:
        if filters is None:
            return True
        if filters.notice_id and chunk.notice_id != filters.notice_id:
            return False
        if filters.org and filters.org.lower() not in {o.lower() for o in chunk.entities_org}:
            return False
        if filters.min_date and chunk.date < filters.min_date:
            return False
        return True

    @staticmethod
    def _score(question: str, chunk: RetrievedChunk) -> int:
        q = question.lower()
        score = 0
        if chunk.notice_id.lower() in q:
            score += 3
        for token in q.split():
            if token in chunk.text.lower():
                score += 1
        return score
