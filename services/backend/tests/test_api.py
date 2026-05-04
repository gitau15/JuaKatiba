from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_abstains_without_context() -> None:
    response = client.post("/query", json={"question": "What does notice 4556 say?", "tier": "public"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "insufficient_context"
    assert body["answer"] == "INSUFFICIENT_CONTEXT"
    assert body["sources"] == []
