from app.models import EvalRunMetadata, EvalSummary
from app.run_trends import build_run_trend, render_run_trend_html


def test_build_run_trend_sorts_runs_and_reports_deltas():
    runs = [
        EvalRunMetadata(
            run_id=2,
            created_at="2026-09-14T01:00:00+00:00",
            summary=EvalSummary(
                total_tasks=15,
                passed_tasks=15,
                failed_tasks=0,
                average_score=1.0,
            ),
        ),
        EvalRunMetadata(
            run_id=1,
            created_at="2026-09-14T00:00:00+00:00",
            summary=EvalSummary(
                total_tasks=15,
                passed_tasks=13,
                failed_tasks=2,
                average_score=0.8667,
            ),
        ),
    ]

    trend = build_run_trend(runs)

    assert trend.run_count == 2
    assert trend.first_run_id == 1
    assert trend.latest_run_id == 2
    assert trend.passed_tasks_delta == 2
    assert trend.failed_tasks_delta == -2
    assert trend.average_score_delta == 0.1333
    assert trend.best_pass_rate == 100.0
    assert trend.worst_pass_rate == 86.7


def test_render_run_trend_html_contains_empty_state():
    html = render_run_trend_html(build_run_trend([]))

    assert "Saved Run Trends" in html
    assert "No saved runs yet" in html
