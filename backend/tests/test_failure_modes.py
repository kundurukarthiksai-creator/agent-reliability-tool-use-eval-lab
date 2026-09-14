from app.models import AgentPlan, EvaluationTask, ToolDefinition
from app.registry import build_default_registry
from app.runner import load_tasks, run_evaluation, run_task


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
    assert result.failure_category == "tool_selection"
    assert any(
        assertion.name == "tool_selection" and not assertion.passed
        for assertion in result.assertions
    )


class MissingToolAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="missing_tool",
            confidence=0.99,
            rationale="Test planner intentionally selects an unregistered tool.",
            matched_signals=["test-tool-execution"],
        )


def test_unregistered_tool_is_reported_as_tool_execution_failure():
    task = EvaluationTask(
        id="missing-tool",
        title="Trigger an unregistered tool",
        description="Synthetic failure-mode task.",
        expected_tool="missing_tool",
        input={},
        expectations={},
    )

    result = run_task(task, build_default_registry(), MissingToolAgent())

    assert not result.passed
    assert result.failure_category == "tool_execution"
    assert result.tool_result.status == "error"
    assert any(
        assertion.name == "tool_status" and not assertion.passed
        for assertion in result.assertions
    )


def test_wrong_output_is_reported_as_output_assertion_failure():
    task = EvaluationTask(
        id="wrong-output",
        title="Find model evaluation foundations notes",
        description="A user asks which learning resource supports model evaluation foundations.",
        expected_tool="course_note_search",
        input={"query": "model evaluation foundations"},
        expectations={"must_equal": {"matches.0.source_id": "not-the-right-note"}},
    )

    result = run_task(task, build_default_registry())

    assert not result.passed
    assert result.failure_category == "output_assertion"
    assert result.tool_result.status == "ok"
