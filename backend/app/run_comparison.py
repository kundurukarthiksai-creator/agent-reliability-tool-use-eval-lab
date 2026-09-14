from collections import Counter
from html import escape
from typing import Literal

from pydantic import BaseModel

from app.models import EvalRunRecord, TaskRunResult


TaskChangeStatus = Literal[
    "unchanged_pass",
    "unchanged_fail",
    "regression",
    "recovery",
    "score_changed",
    "added",
    "removed",
]


class RunTaskComparison(BaseModel):
    task_id: str
    title: str
    status: TaskChangeStatus
    previous_passed: bool | None
    current_passed: bool | None
    previous_score: float | None
    current_score: float | None
    score_delta: float | None
    previous_category: str | None
    current_category: str | None


class EvalRunComparison(BaseModel):
    previous_run_id: int
    current_run_id: int
    previous_created_at: str
    current_created_at: str
    total_tasks_delta: int
    passed_tasks_delta: int
    failed_tasks_delta: int
    average_score_delta: float
    status_counts: dict[str, int]
    task_comparisons: list[RunTaskComparison]


def compare_eval_runs(
    previous: EvalRunRecord,
    current: EvalRunRecord,
) -> EvalRunComparison:
    previous_by_id = {result.task_id: result for result in previous.report.results}
    current_by_id = {result.task_id: result for result in current.report.results}

    task_comparisons = [
        _compare_task(previous_by_id.get(task_id), current_by_id.get(task_id))
        for task_id in sorted(previous_by_id.keys() | current_by_id.keys())
    ]
    status_counts = Counter(change.status for change in task_comparisons)

    return EvalRunComparison(
        previous_run_id=previous.run_id,
        current_run_id=current.run_id,
        previous_created_at=previous.created_at,
        current_created_at=current.created_at,
        total_tasks_delta=(
            current.summary.total_tasks - previous.summary.total_tasks
        ),
        passed_tasks_delta=(
            current.summary.passed_tasks - previous.summary.passed_tasks
        ),
        failed_tasks_delta=(
            current.summary.failed_tasks - previous.summary.failed_tasks
        ),
        average_score_delta=round(
            current.summary.average_score - previous.summary.average_score,
            4,
        ),
        status_counts=dict(sorted(status_counts.items())),
        task_comparisons=task_comparisons,
    )


def render_run_comparison_html(comparison: EvalRunComparison) -> str:
    rows = "\n".join(_render_task_delta(row) for row in comparison.task_comparisons)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Saved Run Comparison</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #16181d;
      --muted: #5d6470;
      --line: #d9dee7;
      --good: #117a47;
      --bad: #b42318;
      --accent: #2454a6;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 15px/1.5 Arial, Helvetica, sans-serif;
    }}

    main {{
      width: min(1080px, calc(100vw - 32px));
      margin: 32px auto;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
      letter-spacing: 0;
    }}

    p {{
      margin: 0 0 24px;
      color: var(--muted);
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .metric,
    table {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}

    .metric {{
      padding: 16px;
    }}

    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }}

    .metric strong {{
      display: block;
      margin-top: 6px;
      font-size: 24px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
    }}

    th,
    td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}

    th {{
      color: var(--muted);
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

    .regression {{
      color: var(--bad);
      font-weight: 700;
    }}

    .recovery {{
      color: var(--good);
      font-weight: 700;
    }}

    @media (max-width: 760px) {{
      .summary {{
        grid-template-columns: 1fr;
      }}

      table {{
        display: block;
        overflow-x: auto;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>Saved Run Comparison</h1>
    <p>Latest saved run compared against the previous saved run.</p>

    <section class="summary" aria-label="Run comparison summary">
      <div class="metric"><span>Previous Run</span><strong>#{comparison.previous_run_id}</strong></div>
      <div class="metric"><span>Current Run</span><strong>#{comparison.current_run_id}</strong></div>
      <div class="metric"><span>Passed Delta</span><strong>{_format_delta(comparison.passed_tasks_delta)}</strong></div>
      <div class="metric"><span>Avg Score Delta</span><strong>{_format_delta(comparison.average_score_delta)}</strong></div>
    </section>

    <table>
      <thead>
        <tr>
          <th>Task</th>
          <th>Status</th>
          <th>Previous</th>
          <th>Current</th>
          <th>Score Delta</th>
          <th>Category</th>
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


def _compare_task(
    previous: TaskRunResult | None,
    current: TaskRunResult | None,
) -> RunTaskComparison:
    title = (current or previous).title if current or previous else "unknown"
    task_id = (current or previous).task_id if current or previous else "unknown"
    score_delta = (
        round(current.score - previous.score, 4)
        if current is not None and previous is not None
        else None
    )

    return RunTaskComparison(
        task_id=task_id,
        title=title,
        status=_classify_change(previous, current, score_delta),
        previous_passed=previous.passed if previous is not None else None,
        current_passed=current.passed if current is not None else None,
        previous_score=previous.score if previous is not None else None,
        current_score=current.score if current is not None else None,
        score_delta=score_delta,
        previous_category=previous.failure_category if previous is not None else None,
        current_category=current.failure_category if current is not None else None,
    )


def _classify_change(
    previous: TaskRunResult | None,
    current: TaskRunResult | None,
    score_delta: float | None,
) -> TaskChangeStatus:
    if previous is None:
        return "added"
    if current is None:
        return "removed"
    if previous.passed and not current.passed:
        return "regression"
    if not previous.passed and current.passed:
        return "recovery"
    if (
        previous.passed == current.passed
        and score_delta == 0
        and previous.failure_category == current.failure_category
    ):
        return "unchanged_pass" if current.passed else "unchanged_fail"
    return "score_changed"


def _render_task_delta(change: RunTaskComparison) -> str:
    status_class = (
        "regression"
        if change.status == "regression"
        else "recovery" if change.status == "recovery" else ""
    )
    category = (
        f"{_format_category(change.previous_category)} -> "
        f"{_format_category(change.current_category)}"
        if change.previous_category != change.current_category
        else _format_category(change.current_category)
    )
    return f"""
        <tr>
          <td><code>{escape(change.task_id)}</code><br>{escape(change.title)}</td>
          <td class="{status_class}">{escape(change.status)}</td>
          <td>{_format_passed(change.previous_passed)} / {_format_score(change.previous_score)}</td>
          <td>{_format_passed(change.current_passed)} / {_format_score(change.current_score)}</td>
          <td>{_format_optional_delta(change.score_delta)}</td>
          <td>{category}</td>
        </tr>
"""


def _format_delta(value: float | int) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value}"


def _format_optional_delta(value: float | None) -> str:
    return "n/a" if value is None else _format_delta(value)


def _format_score(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f}"


def _format_passed(value: bool | None) -> str:
    if value is None:
        return "n/a"
    return "passed" if value else "failed"


def _format_category(value: str | None) -> str:
    return "n/a" if value is None else escape(value)
