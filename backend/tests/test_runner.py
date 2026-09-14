from app.runner import load_tasks, run_evaluation


def test_loads_forty_two_deterministic_tasks():
    tasks = load_tasks()

    assert len(tasks) == 42
    assert {task.expected_tool for task in tasks} == {
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
        "runbook_lookup",
        "profile_readme_audit",
        "role_readiness_audit",
        "launch_readiness_audit",
        "artifact_consistency_audit",
        "tool_safety_audit",
    }


def test_evaluation_report_all_deterministic_tasks_pass():
    report = run_evaluation()

    assert report.summary.total_tasks == 42
    assert report.summary.passed_tasks == 42
    assert report.summary.failed_tasks == 0
    assert report.summary.average_score == 1.0
    assert all(result.passed for result in report.results)
    assert all(result.failure_category == "passed" for result in report.results)
    assert all(result.agent_plan.selected_tool == result.selected_tool for result in report.results)
    assert all(len(result.trace) == 1 for result in report.results)
