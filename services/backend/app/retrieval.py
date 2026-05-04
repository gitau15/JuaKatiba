from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    text: str
    notice_id: str
    date: str


class RetrievalService:
    """Placeholder retrieval service.

    TODO: wire this to Qdrant hybrid search (dense + sparse + payload filters).
    """

    def search(self, question: str, tier: str) -> list[RetrievedChunk]:
        _ = (question, tier)
        return []
