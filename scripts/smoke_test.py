import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.main import app  # noqa: E402


def main():
    client = TestClient(app)
    response = client.get("/health")
    response.raise_for_status()

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "agent-reliability-tool-use-eval-lab"

    dashboard_response = client.get("/")
    dashboard_response.raise_for_status()
    assert "Agent Reliability Lab" in dashboard_response.text

    eval_response = client.post("/eval/run")
    eval_response.raise_for_status()
    report = eval_response.json()
    assert report["summary"]["total_tasks"] == 30
    assert report["summary"]["failed_tasks"] == 0

    html_response = client.get("/reports/latest.html")
    html_response.raise_for_status()
    assert "Agent Reliability Eval Report" in html_response.text

    runs_html_response = client.get("/eval/runs.html")
    runs_html_response.raise_for_status()
    assert "Saved Evaluation Runs" in runs_html_response.text

    first_saved_run = client.post("/eval/runs")
    first_saved_run.raise_for_status()
    second_saved_run = client.post("/eval/runs")
    second_saved_run.raise_for_status()

    run_comparison_response = client.get("/eval/runs/compare")
    run_comparison_response.raise_for_status()
    comparison = run_comparison_response.json()
    assert comparison["current_run_id"] > comparison["previous_run_id"]

    run_comparison_html_response = client.get("/eval/runs/compare.html")
    run_comparison_html_response.raise_for_status()
    assert "Saved Run Comparison" in run_comparison_html_response.text

    run_trends_response = client.get("/eval/runs/trends")
    run_trends_response.raise_for_status()
    assert run_trends_response.json()["run_count"] >= 2

    run_trends_html_response = client.get("/eval/runs/trends.html")
    run_trends_html_response.raise_for_status()
    assert "Saved Run Trends" in run_trends_html_response.text

    comparison_response = client.get("/planners/compare")
    comparison_response.raise_for_status()
    assert comparison_response.json()[0]["planner_name"] == "rule_based"

    comparison_html_response = client.get("/planners/compare.html")
    comparison_html_response.raise_for_status()
    assert "Planner Comparison" in comparison_html_response.text

    print("smoke test passed")


if __name__ == "__main__":
    main()
