import json
from pathlib import Path
from typing import Any

from app.models import EvalReport, EvalSummary, EvaluationTask, TaskRunResult, ToolResult
from app.registry import ToolRegistry, build_default_registry
from app.scoring import score_task


ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR = ROOT / "evals" / "tasks"


def load_tasks(tasks_dir: Path = TASKS_DIR) -> list[EvaluationTask]:
    tasks: list[EvaluationTask] = []
    for path in sorted(tasks_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as file:
            raw: dict[str, Any] = json.load(file)
        tasks.append(EvaluationTask.model_validate(raw))
    return tasks


def run_task(task: EvaluationTask, registry: ToolRegistry) -> TaskRunResult:
    selected_tool = task.expected_tool
    try:
        output = registry.run(selected_tool, task.input)
        tool_result = ToolResult(tool_name=selected_tool, output=output, status="ok")
    except Exception as exc:  # noqa: BLE001 - task reports should preserve failures.
        tool_result = ToolResult(
            tool_name=selected_tool,
            output={"error": str(exc)},
            status="error",
            error=str(exc),
        )

    assertions, score, passed = score_task(task, selected_tool, tool_result)
    return TaskRunResult(
        task_id=task.id,
        title=task.title,
        expected_tool=task.expected_tool,
        selected_tool=selected_tool,
        tool_result=tool_result,
        assertions=assertions,
        score=score,
        passed=passed,
    )


def run_evaluation(
    tasks: list[EvaluationTask] | None = None,
    registry: ToolRegistry | None = None,
) -> EvalReport:
    selected_tasks = tasks if tasks is not None else load_tasks()
    selected_registry = registry if registry is not None else build_default_registry()

    results = [run_task(task, selected_registry) for task in selected_tasks]
    passed_tasks = sum(1 for result in results if result.passed)
    total_tasks = len(results)
    average_score = (
        sum(result.score for result in results) / total_tasks if total_tasks else 0.0
    )

    return EvalReport(
        summary=EvalSummary(
            total_tasks=total_tasks,
            passed_tasks=passed_tasks,
            failed_tasks=total_tasks - passed_tasks,
            average_score=round(average_score, 4),
        ),
        results=results,
    )

