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


def test_ingest_and_query_returns_grounded_answer() -> None:
    client.post(
        "/ingest",
        json={
            "notice_id": "4556",
            "date": "2023-03-17",
            "ministry": "ICT",
            "notice_type": "Appointment",
            "text": "This notice appoints committee members and outlines responsibilities in telecommunications.",
            "entities_org": ["Safaricom"],
        },
    )

    response = client.post("/query", json={"question": "What does notice 4556 say?", "tier": "public"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "4556" in body["answer"]
    assert body["sources"][0]["notice_id"] == "4556"


def test_filter_by_org() -> None:
    client.post(
        "/ingest",
        json={
            "notice_id": "8001",
            "date": "2024-01-10",
            "ministry": "Finance",
            "notice_type": "Directive",
            "text": "This directive concerns tax procedures.",
            "entities_org": ["KRA"],
        },
    )

    response = client.post(
        "/query",
        json={"question": "tax procedures", "tier": "public", "filters": {"org": "KRA"}},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
