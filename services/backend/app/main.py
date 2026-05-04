from fastapi import FastAPI

from app.generation import GenerationService
from app.models import IngestNoticeRequest, QueryRequest, QueryResponse
from app.prompting import normalize_question
from app.retrieval import RetrievalService

app = FastAPI(title="JuaKatiba Backend", version="0.2.0")
retrieval_service = RetrievalService()
generation_service = GenerationService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(payload: IngestNoticeRequest) -> dict[str, str]:
    retrieval_service.ingest(payload)
    return {"status": "ingested", "notice_id": payload.notice_id}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    question = normalize_question(payload.question)
    retrieved = retrieval_service.search(question=question, tier=payload.tier, filters=payload.filters)
    return generation_service.answer(question=question, tier=payload.tier, context=retrieved)
