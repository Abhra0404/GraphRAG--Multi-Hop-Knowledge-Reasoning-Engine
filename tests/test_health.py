from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "services" in data

    assert "postgres" in data["services"]
    assert "neo4j" in data["services"]
    assert "qdrant" in data["services"]