from fastapi.testclient import TestClient

from app import main as main_module
from app.main import app
from app.storage import get_run, list_runs, save_report


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
        "total_tasks": 10,
        "passed_tasks": 10,
        "failed_tasks": 0,
        "average_score": 1.0,
    }
    assert len(payload["results"]) == 10
    assert all("agent_plan" in result for result in payload["results"])
    assert all(result["trace"] for result in payload["results"])


def test_latest_html_report_endpoint_returns_report_page():
    client = TestClient(app)

    response = client.get("/reports/latest.html")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Agent Reliability Eval Report" in response.text
    assert "Tool Call Trace" in response.text


def test_persisted_eval_run_endpoint_saves_report(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    monkeypatch.setattr(
        main_module,
        "save_report",
        lambda report: save_report(report, db_path=db_path),
    )
    client = TestClient(app)

    response = client.post("/eval/runs")

    assert response.status_code == 200
    payload = response.json()
    assert payload["run_id"] == 1
    assert payload["summary"]["failed_tasks"] == 0


def test_persisted_eval_run_read_endpoints(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    report = main_module.run_evaluation()
    saved = save_report(report, db_path=db_path)
    monkeypatch.setattr(main_module, "list_runs", lambda: list_runs(db_path=db_path))
    monkeypatch.setattr(main_module, "get_run", lambda run_id: get_run(run_id, db_path=db_path))
    client = TestClient(app)

    list_response = client.get("/eval/runs")
    get_response = client.get(f"/eval/runs/{saved.run_id}")
    missing_response = client.get("/eval/runs/999")

    assert list_response.status_code == 200
    assert list_response.json()[0]["run_id"] == saved.run_id
    assert get_response.status_code == 200
    assert get_response.json()["report"]["summary"]["total_tasks"] == 10
    assert missing_response.status_code == 404
