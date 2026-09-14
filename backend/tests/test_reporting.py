from app.reporting import render_eval_report_html, render_runs_index_html
from app.runner import run_evaluation
from app.storage import save_report


def test_render_eval_report_html_contains_summary_and_trace():
    html = render_eval_report_html(run_evaluation())

    assert "<!doctype html>" in html.lower()
    assert "Agent Reliability Eval Report" in html
    assert "repo-health-ready" in html
    assert "Tool Call Trace" in html
    assert "Pass Rate" in html
    assert "Category" in html


def test_render_runs_index_html_contains_saved_run(tmp_path):
    saved = save_report(run_evaluation(), db_path=tmp_path / "runs.sqlite3")

    html = render_runs_index_html([saved])

    assert "Saved Evaluation Runs" in html
    assert f"#{saved.run_id}" in html
    assert "10" in html


def test_render_runs_index_html_handles_empty_state():
    html = render_runs_index_html([])

    assert "No saved runs yet" in html
