from fastapi import FastAPI

from app.generation import GenerationService
from app.models import QueryRequest, QueryResponse
from app.prompting import normalize_question
from app.retrieval import RetrievalService

app = FastAPI(title="JuaKatiba Backend", version="0.1.0")
retrieval_service = RetrievalService()
generation_service = GenerationService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    question = normalize_question(payload.question)
    retrieved = retrieval_service.search(question=question, tier=payload.tier)
    return generation_service.answer(question=question, tier=payload.tier, context=retrieved)
