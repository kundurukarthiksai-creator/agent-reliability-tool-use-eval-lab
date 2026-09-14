from app.reporting import (
    render_dashboard_html,
    render_eval_report_html,
    render_runs_index_html,
    render_task_catalog_html,
)
from app.registry import build_default_registry
from app.runner import load_tasks, run_evaluation
from app.storage import save_report


def test_render_eval_report_html_contains_summary_and_trace():
    html = render_eval_report_html(run_evaluation())

    assert "<!doctype html>" in html.lower()
    assert "Agent Reliability Eval Report" in html
    assert "repo-health-ready" in html
    assert "Tool Call Trace" in html
    assert "Pass Rate" in html
    assert "Category" in html


def test_render_dashboard_html_contains_navigation_and_tools():
    registry = build_default_registry()
    html = render_dashboard_html(
        report=run_evaluation(registry=registry),
        tools=registry.list_tools(),
        runs=[],
    )

    assert "Agent Reliability Lab" in html
    assert "/reports/latest.html" in html
    assert "/eval/runs/trends.html" in html
    assert "runbook_lookup" in html
    assert "18" in html


def test_render_task_catalog_html_contains_tool_coverage_counts():
    registry = build_default_registry()

    html = render_task_catalog_html(load_tasks(), registry.list_tools())

    assert "Evaluation Task Catalog" in html
    assert "repo-health-ready" in html
    assert "repo_health_check" in html
    assert 'data-label="Tasks">6</td>' in html


def test_render_runs_index_html_contains_saved_run(tmp_path):
    saved = save_report(run_evaluation(), db_path=tmp_path / "runs.sqlite3")

    html = render_runs_index_html([saved])

    assert "Saved Evaluation Runs" in html
    assert f"#{saved.run_id}" in html
    assert "18" in html


def test_render_runs_index_html_handles_empty_state():
    html = render_runs_index_html([])

    assert "No saved runs yet" in html
