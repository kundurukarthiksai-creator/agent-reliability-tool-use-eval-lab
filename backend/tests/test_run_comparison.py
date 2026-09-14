from app.models import EvalRunRecord, EvalSummary
from app.run_comparison import compare_eval_runs, render_run_comparison_html
from app.runner import run_evaluation


def test_compare_eval_runs_reports_recovery():
    previous_report = run_evaluation().model_copy(deep=True)
    current_report = run_evaluation()
    previous_result = previous_report.results[0]
    previous_result.passed = False
    previous_result.score = 0.0
    previous_result.failure_category = "output_assertion"
    total_tasks = len(previous_report.results)
    previous_report.summary = EvalSummary(
        total_tasks=total_tasks,
        passed_tasks=total_tasks - 1,
        failed_tasks=1,
        average_score=round((total_tasks - 1) / total_tasks, 4),
    )

    previous = EvalRunRecord(
        run_id=1,
        created_at="2026-09-14T00:00:00+00:00",
        summary=previous_report.summary,
        report=previous_report,
    )
    current = EvalRunRecord(
        run_id=2,
        created_at="2026-09-14T01:00:00+00:00",
        summary=current_report.summary,
        report=current_report,
    )

    comparison = compare_eval_runs(previous, current)

    assert comparison.previous_run_id == 1
    assert comparison.current_run_id == 2
    assert comparison.passed_tasks_delta == 1
    assert comparison.failed_tasks_delta == -1
    assert comparison.average_score_delta > 0
    assert comparison.status_counts["recovery"] == 1


def test_render_run_comparison_html_contains_task_status():
    first_report = run_evaluation()
    second_report = run_evaluation()
    first = EvalRunRecord(
        run_id=1,
        created_at="2026-09-14T00:00:00+00:00",
        summary=first_report.summary,
        report=first_report,
    )
    second = EvalRunRecord(
        run_id=2,
        created_at="2026-09-14T01:00:00+00:00",
        summary=second_report.summary,
        report=second_report,
    )

    html = render_run_comparison_html(compare_eval_runs(first, second))

    assert "Saved Run Comparison" in html
    assert "unchanged_pass" in html
    assert "#1" in html
    assert "#2" in html
