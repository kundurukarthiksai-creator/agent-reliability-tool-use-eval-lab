from fastapi.testclient import TestClient

from app.main import app


def test_tools_endpoint_lists_registered_tools():
    client = TestClient(app)

    response = client.get("/tools")

    assert response.status_code == 200
    names = {tool["name"] for tool in response.json()}
    assert names == {
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
    }


def test_eval_run_endpoint_returns_passing_report():
    client = TestClient(app)

    response = client.post("/eval/run")

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"] == {
        "total_tasks": 5,
        "passed_tasks": 5,
        "failed_tasks": 0,
        "average_score": 1.0,
    }
    assert len(payload["results"]) == 5
    assert all("agent_plan" in result for result in payload["results"])
    assert all(result["trace"] for result in payload["results"])
