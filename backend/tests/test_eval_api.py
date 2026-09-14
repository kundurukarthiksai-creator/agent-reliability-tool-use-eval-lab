from fastapi.testclient import TestClient

from app import main as main_module
from app.main import app
from app.storage import get_latest_run_pair, get_run, list_runs, save_report


def test_tools_endpoint_lists_registered_tools():
    client = TestClient(app)

    response = client.get("/tools")

    assert response.status_code == 200
    names = {tool["name"] for tool in response.json()}
    assert names == {
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
        "runbook_lookup",
        "profile_readme_audit",
        "role_readiness_audit",
        "launch_readiness_audit",
    }


def test_dashboard_endpoint_returns_navigation_page():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Agent Reliability Lab" in response.text
    assert "/eval/tasks.html" in response.text
    assert "/planners/compare.html" in response.text


def test_eval_task_catalog_endpoints_return_public_task_coverage():
    client = TestClient(app)

    json_response = client.get("/eval/tasks")
    coverage_response = client.get("/eval/tasks/coverage")
    html_response = client.get("/eval/tasks.html")

    assert json_response.status_code == 200
    tasks = json_response.json()
    assert len(tasks) == 30
    assert tasks[0]["id"] == "repo-health-ready"
    assert {task["expected_tool"] for task in tasks} == {
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
        "runbook_lookup",
        "profile_readme_audit",
        "role_readiness_audit",
        "launch_readiness_audit",
    }
    assert coverage_response.status_code == 200
    assert coverage_response.json() == {
        "total_tasks": 30,
        "coverage": [
            {"tool_name": "repo_health_check", "task_count": 6},
            {"tool_name": "course_note_search", "task_count": 5},
            {"tool_name": "application_tracker_update", "task_count": 4},
            {"tool_name": "runbook_lookup", "task_count": 3},
            {"tool_name": "profile_readme_audit", "task_count": 4},
            {"tool_name": "role_readiness_audit", "task_count": 4},
            {"tool_name": "launch_readiness_audit", "task_count": 4},
        ],
    }
    assert html_response.status_code == 200
    assert html_response.headers["content-type"].startswith("text/html")
    assert "Evaluation Task Catalog" in html_response.text
    assert "repo-health-ready" in html_response.text


def test_planner_comparison_endpoints_return_default_comparison():
    client = TestClient(app)

    json_response = client.get("/planners/compare")
    html_response = client.get("/planners/compare.html")

    assert json_response.status_code == 200
    assert json_response.json()[0]["planner_name"] == "rule_based"
    assert json_response.json()[0]["passed_tasks"] == 30
    assert html_response.status_code == 200
    assert html_response.headers["content-type"].startswith("text/html")
    assert "Planner Comparison" in html_response.text


def test_eval_run_endpoint_returns_passing_report():
    client = TestClient(app)

    response = client.post("/eval/run")

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"] == {
        "total_tasks": 30,
        "passed_tasks": 30,
        "failed_tasks": 0,
        "average_score": 1.0,
    }
    assert len(payload["results"]) == 30
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
    assert get_response.json()["report"]["summary"]["total_tasks"] == 30
    assert missing_response.status_code == 404


def test_saved_runs_html_endpoint(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    saved = save_report(main_module.run_evaluation(), db_path=db_path)
    monkeypatch.setattr(main_module, "list_runs", lambda: list_runs(db_path=db_path))
    client = TestClient(app)

    response = client.get("/eval/runs.html")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Saved Evaluation Runs" in response.text
    assert f"#{saved.run_id}" in response.text


def test_saved_run_comparison_endpoints(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    save_report(main_module.run_evaluation(), db_path=db_path)
    save_report(main_module.run_evaluation(), db_path=db_path)
    monkeypatch.setattr(
        main_module,
        "get_latest_run_pair",
        lambda: get_latest_run_pair(db_path=db_path),
    )
    client = TestClient(app)

    json_response = client.get("/eval/runs/compare")
    html_response = client.get("/eval/runs/compare.html")

    assert json_response.status_code == 200
    assert json_response.json()["previous_run_id"] == 1
    assert json_response.json()["current_run_id"] == 2
    assert html_response.status_code == 200
    assert html_response.headers["content-type"].startswith("text/html")
    assert "Saved Run Comparison" in html_response.text


def test_saved_run_comparison_requires_two_runs(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    save_report(main_module.run_evaluation(), db_path=db_path)
    monkeypatch.setattr(
        main_module,
        "get_latest_run_pair",
        lambda: get_latest_run_pair(db_path=db_path),
    )
    client = TestClient(app)

    response = client.get("/eval/runs/compare")

    assert response.status_code == 404


def test_saved_run_trend_endpoints(monkeypatch, tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    save_report(main_module.run_evaluation(), db_path=db_path)
    save_report(main_module.run_evaluation(), db_path=db_path)
    monkeypatch.setattr(main_module, "list_runs", lambda: list_runs(db_path=db_path))
    client = TestClient(app)

    json_response = client.get("/eval/runs/trends")
    html_response = client.get("/eval/runs/trends.html")

    assert json_response.status_code == 200
    assert json_response.json()["run_count"] == 2
    assert json_response.json()["latest_run_id"] == 2
    assert html_response.status_code == 200
    assert html_response.headers["content-type"].startswith("text/html")
    assert "Saved Run Trends" in html_response.text
