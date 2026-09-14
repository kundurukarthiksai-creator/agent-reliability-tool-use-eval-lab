from app.registry import build_default_registry
from app.runner import load_tasks
from app.task_catalog import summarize_task_coverage


def test_summarize_task_coverage_counts_tasks_by_registered_tool():
    summary = summarize_task_coverage(load_tasks(), build_default_registry().list_tools())

    assert summary.total_tasks == 18
    assert {item.tool_name: item.task_count for item in summary.coverage} == {
        "repo_health_check": 6,
        "course_note_search": 5,
        "application_tracker_update": 4,
        "runbook_lookup": 3,
    }
