from app.reporting import render_eval_report_html
from app.runner import run_evaluation


def test_render_eval_report_html_contains_summary_and_trace():
    html = render_eval_report_html(run_evaluation())

    assert "<!doctype html>" in html.lower()
    assert "Agent Reliability Eval Report" in html
    assert "repo-health-ready" in html
    assert "Tool Call Trace" in html
    assert "Pass Rate" in html
