from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)


def test_query_validation():
    response = client.post(
        "/query",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_query_endpoint(monkeypatch):
    def mock_answer_query(question: str):
        return {
            "answer": "Albert Einstein developed the theory of relativity. [Chain 1]",
            "entities": ["Albert Einstein"],
            "evidence": "Einstein --[DEVELOPED]--> theory of relativity",
        }

    monkeypatch.setattr(
        "apps.api.routes.query.answer_query",
        mock_answer_query,
    )

    response = client.post(
        "/query",
        json={
            "question": "What did Albert Einstein develop?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "entities" in data
    assert "evidence" in data
    assert data["entities"] == ["Albert Einstein"]


def test_query_internal_error(monkeypatch):
    def mock_answer_query(question: str):
        raise RuntimeError("database failure")

    monkeypatch.setattr(
        "apps.api.routes.query.answer_query",
        mock_answer_query,
    )

    response = client.post(
        "/query",
        json={
            "question": "Test failure"
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error."