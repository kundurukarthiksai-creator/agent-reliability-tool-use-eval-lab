from html import escape

from pydantic import BaseModel

from app.models import EvalRunMetadata


class RunTrendPoint(BaseModel):
    run_id: int
    created_at: str
    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    average_score: float
    pass_rate: float


class EvalRunTrend(BaseModel):
    run_count: int
    first_run_id: int | None
    latest_run_id: int | None
    passed_tasks_delta: int
    failed_tasks_delta: int
    average_score_delta: float
    best_pass_rate: float | None
    worst_pass_rate: float | None
    points: list[RunTrendPoint]


def build_run_trend(runs: list[EvalRunMetadata]) -> EvalRunTrend:
    points = [_to_point(run) for run in sorted(runs, key=lambda item: item.run_id)]
    if not points:
        return EvalRunTrend(
            run_count=0,
            first_run_id=None,
            latest_run_id=None,
            passed_tasks_delta=0,
            failed_tasks_delta=0,
            average_score_delta=0.0,
            best_pass_rate=None,
            worst_pass_rate=None,
            points=[],
        )

    first = points[0]
    latest = points[-1]
    pass_rates = [point.pass_rate for point in points]
    return EvalRunTrend(
        run_count=len(points),
        first_run_id=first.run_id,
        latest_run_id=latest.run_id,
        passed_tasks_delta=latest.passed_tasks - first.passed_tasks,
        failed_tasks_delta=latest.failed_tasks - first.failed_tasks,
        average_score_delta=round(latest.average_score - first.average_score, 4),
        best_pass_rate=max(pass_rates),
        worst_pass_rate=min(pass_rates),
        points=points,
    )


def render_run_trend_html(trend: EvalRunTrend) -> str:
    rows = "\n".join(_render_point(point) for point in trend.points)
    if not rows:
        rows = """
        <tr>
          <td colspan="7">No saved runs yet. Use <code>POST /eval/runs</code> to save one.</td>
        </tr>
        """

    latest = f"#{trend.latest_run_id}" if trend.latest_run_id is not None else "n/a"
    best = _format_rate(trend.best_pass_rate)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Saved Run Trends</title>
  <style>
    body {{
      margin: 0;
      background: #f6f7f9;
      color: #16181d;
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
      color: #5d6470;
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .metric,
    table {{
      background: #ffffff;
      border: 1px solid #d9dee7;
      border-radius: 8px;
    }}

    .metric {{
      padding: 16px;
    }}

    .metric span {{
      display: block;
      color: #5d6470;
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
    <h1>Saved Run Trends</h1>
    <p>Reliability movement across all saved evaluation runs.</p>

    <section class="summary" aria-label="Run trend summary">
      <div class="metric"><span>Runs</span><strong>{trend.run_count}</strong></div>
      <div class="metric"><span>Latest</span><strong>{latest}</strong></div>
      <div class="metric"><span>Passed Delta</span><strong>{_format_delta(trend.passed_tasks_delta)}</strong></div>
      <div class="metric"><span>Best Pass Rate</span><strong>{best}</strong></div>
    </section>

    <table>
      <thead>
        <tr>
          <th>Run</th>
          <th>Created</th>
          <th>Total</th>
          <th>Passed</th>
          <th>Failed</th>
          <th>Avg Score</th>
          <th>Pass Rate</th>
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


def _to_point(run: EvalRunMetadata) -> RunTrendPoint:
    total = run.summary.total_tasks
    pass_rate = round((run.summary.passed_tasks / total) * 100, 1) if total else 0.0
    return RunTrendPoint(
        run_id=run.run_id,
        created_at=run.created_at,
        total_tasks=total,
        passed_tasks=run.summary.passed_tasks,
        failed_tasks=run.summary.failed_tasks,
        average_score=run.summary.average_score,
        pass_rate=pass_rate,
    )


def _render_point(point: RunTrendPoint) -> str:
    return f"""
        <tr>
          <td><code>#{point.run_id}</code></td>
          <td>{escape(point.created_at)}</td>
          <td>{point.total_tasks}</td>
          <td>{point.passed_tasks}</td>
          <td>{point.failed_tasks}</td>
          <td>{point.average_score:.4f}</td>
          <td>{point.pass_rate:.1f}%</td>
        </tr>
"""


def _format_delta(value: float | int) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value}"


def _format_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"
