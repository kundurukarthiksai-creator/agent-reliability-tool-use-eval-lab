from app.models import AgentPlan, EvaluationTask, ToolDefinition
from app.quality_gate import QualityGateConfig, evaluate_quality_gate
from app.runner import load_tasks, run_evaluation


class WrongToolAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.99,
            rationale="Test planner intentionally chooses the wrong tool.",
            matched_signals=["quality-gate-test"],
        )


def test_quality_gate_passes_clean_default_report():
    result = evaluate_quality_gate(run_evaluation())

    assert result.passed
    assert result.pass_rate == 1.0
    assert result.failure_category_counts == {"passed": 18}
    assert result.failed_task_ids == []
    assert all(check.passed for check in result.checks)


def test_quality_gate_fails_on_failed_task():
    task = next(task for task in load_tasks() if task.id == "repo-health-ready")
    report = run_evaluation(tasks=[task], agent=WrongToolAgent())
    result = evaluate_quality_gate(report)

    assert not result.passed
    assert result.failed_task_ids == ["repo-health-ready"]
    assert result.failure_category_counts == {"tool_selection": 1}
    assert any(
        check.name == "allowed_failure_categories" and not check.passed
        for check in result.checks
    )


def test_quality_gate_can_be_relaxed_for_diagnostic_reports():
    task = next(task for task in load_tasks() if task.id == "repo-health-ready")
    report = run_evaluation(tasks=[task], agent=WrongToolAgent())
    config = QualityGateConfig(
        min_total_tasks=1,
        min_pass_rate=0.0,
        min_average_score=0.0,
        max_failed_tasks=1,
        allowed_failure_categories=["tool_selection"],
    )

    result = evaluate_quality_gate(report, config)

    assert result.passed
