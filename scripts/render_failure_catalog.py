import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.models import AgentPlan, EvalReport, EvalSummary, EvaluationTask, ToolDefinition  # noqa: E402
from app.registry import build_default_registry  # noqa: E402
from app.reporting import render_eval_report_html  # noqa: E402
from app.runner import load_tasks, run_task  # noqa: E402


class WrongToolAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.99,
            rationale="Failure catalog: intentionally chooses the wrong registered tool.",
            matched_signals=["failure-catalog-tool-selection"],
        )


class MissingToolAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="missing_tool",
            confidence=0.99,
            rationale="Failure catalog: intentionally selects an unregistered tool.",
            matched_signals=["failure-catalog-tool-execution"],
        )


def main() -> None:
    registry = build_default_registry()
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    repo_task = next(task for task in load_tasks() if task.id == "repo-health-ready")
    tool_selection_result = run_task(repo_task, registry, WrongToolAgent())

    tool_execution_task = EvaluationTask(
        id="failure-catalog-tool-execution",
        title="Classify an unregistered tool call",
        description="A synthetic planner selects an unregistered tool.",
        expected_tool="missing_tool",
        input={},
        expectations={},
    )
    tool_execution_result = run_task(tool_execution_task, registry, MissingToolAgent())

    output_assertion_task = EvaluationTask(
        id="failure-catalog-output-assertion",
        title="Classify a wrong supported output",
        description="A synthetic expectation asks for the wrong course note source.",
        expected_tool="course_note_search",
        input={"query": "model evaluation foundations"},
        expectations={"must_equal": {"matches.0.source_id": "not-the-right-note"}},
    )
    output_assertion_result = run_task(output_assertion_task, registry)

    results = [
        tool_selection_result,
        tool_execution_result,
        output_assertion_result,
    ]
    passed_tasks = sum(1 for result in results if result.passed)
    report = EvalReport(
        summary=EvalSummary(
            total_tasks=len(results),
            passed_tasks=passed_tasks,
            failed_tasks=len(results) - passed_tasks,
            average_score=round(
                sum(result.score for result in results) / len(results),
                4,
            ),
        ),
        results=results,
    )

    json_path = reports_dir / "failure-catalog.json"
    html_path = reports_dir / "failure-catalog.html"

    json_path.write_text(json.dumps(report.model_dump(), indent=2), encoding="utf-8")
    html_path.write_text(render_eval_report_html(report), encoding="utf-8")
    print(f"rendered {json_path}")
    print(f"rendered {html_path}")


if __name__ == "__main__":
    main()
