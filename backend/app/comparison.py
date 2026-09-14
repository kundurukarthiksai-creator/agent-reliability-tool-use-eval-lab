from collections import Counter

from pydantic import BaseModel

from app.agent import AgentPlanner, RuleBasedAgent
from app.models import EvaluationTask
from app.registry import ToolRegistry, build_default_registry
from app.runner import load_tasks, run_evaluation


class PlannerComparisonResult(BaseModel):
    planner_name: str
    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    average_score: float
    failure_categories: dict[str, int]


def compare_planners(
    planners: dict[str, AgentPlanner] | None = None,
    tasks: list[EvaluationTask] | None = None,
    registry: ToolRegistry | None = None,
) -> list[PlannerComparisonResult]:
    selected_planners = planners if planners is not None else {"rule_based": RuleBasedAgent()}
    selected_tasks = tasks if tasks is not None else load_tasks()
    selected_registry = registry if registry is not None else build_default_registry()

    results: list[PlannerComparisonResult] = []
    for planner_name, planner in selected_planners.items():
        report = run_evaluation(
            tasks=selected_tasks,
            registry=selected_registry,
            agent=planner,
        )
        categories = Counter(result.failure_category for result in report.results)
        results.append(
            PlannerComparisonResult(
                planner_name=planner_name,
                total_tasks=report.summary.total_tasks,
                passed_tasks=report.summary.passed_tasks,
                failed_tasks=report.summary.failed_tasks,
                average_score=report.summary.average_score,
                failure_categories=dict(sorted(categories.items())),
            )
        )
    return results


def render_planner_comparison_markdown(
    results: list[PlannerComparisonResult],
) -> str:
    lines = [
        "# Planner Comparison",
        "",
        "| Planner | Total | Passed | Failed | Avg Score | Failure Categories |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        categories = ", ".join(
            f"{name}: {count}" for name, count in result.failure_categories.items()
        )
        lines.append(
            "| "
            f"{result.planner_name} | "
            f"{result.total_tasks} | "
            f"{result.passed_tasks} | "
            f"{result.failed_tasks} | "
            f"{result.average_score:.4f} | "
            f"{categories} |"
        )
    lines.append("")
    return "\n".join(lines)
