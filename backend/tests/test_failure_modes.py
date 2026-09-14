from app.models import AgentPlan, EvaluationTask, ToolDefinition
from app.runner import load_tasks, run_evaluation


class WrongToolAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.99,
            rationale="Test planner intentionally chooses the wrong tool.",
            matched_signals=["test-failure"],
        )


def test_wrong_tool_selection_is_reported_as_failed_task():
    task = next(task for task in load_tasks() if task.id == "repo-health-ready")
    report = run_evaluation(tasks=[task], agent=WrongToolAgent())
    result = report.results[0]

    assert report.summary.total_tasks == 1
    assert report.summary.failed_tasks == 1
    assert result.selected_tool == "course_note_search"
    assert result.expected_tool == "repo_health_check"
    assert not result.passed
    assert any(
        assertion.name == "tool_selection" and not assertion.passed
        for assertion in result.assertions
    )
