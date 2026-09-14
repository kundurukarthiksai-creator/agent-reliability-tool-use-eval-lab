from fastapi.testclient import TestClient

from app.main import app


def test_health_route():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "agent-reliability-tool-use-eval-lab",
        "phase": "phase-0-scaffold",
    }

