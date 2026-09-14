from collections import Counter
from html import escape

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


def render_planner_comparison_html(
    results: list[PlannerComparisonResult],
) -> str:
    rows = "\n".join(_render_comparison_row(result) for result in results)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Planner Comparison</title>
  <style>
    body {{
      margin: 0;
      background: #f6f7f9;
      color: #16181d;
      font: 15px/1.5 Arial, Helvetica, sans-serif;
    }}

    main {{
      width: min(980px, calc(100vw - 32px));
      margin: 32px auto;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
      letter-spacing: 0;
    }}

    p {{
      margin: 0 0 24px;
      color: #5d6470;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
      border: 1px solid #d9dee7;
      border-radius: 8px;
      overflow: hidden;
    }}

    th,
    td {{
      padding: 12px 14px;
      border-bottom: 1px solid #d9dee7;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      color: #5d6470;
      font-size: 12px;
      text-transform: uppercase;
    }}

    tr:last-child td {{
      border-bottom: 0;
    }}

    code {{
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      padding: 1px 4px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Planner Comparison</h1>
    <p>Same task set, different planner behavior, summarized by score and failure category.</p>
    <table>
      <thead>
        <tr>
          <th>Planner</th>
          <th>Total</th>
          <th>Passed</th>
          <th>Failed</th>
          <th>Avg Score</th>
          <th>Failure Categories</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </main>
</body>
</html>
"""


def _render_comparison_row(result: PlannerComparisonResult) -> str:
    categories = ", ".join(
        f"{escape(name)}: {count}" for name, count in result.failure_categories.items()
    )
    return f"""
        <tr>
          <td><code>{escape(result.planner_name)}</code></td>
          <td>{result.total_tasks}</td>
          <td>{result.passed_tasks}</td>
          <td>{result.failed_tasks}</td>
          <td>{result.average_score:.4f}</td>
          <td>{categories}</td>
        </tr>
"""
