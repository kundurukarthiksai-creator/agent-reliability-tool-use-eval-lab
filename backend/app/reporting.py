from html import escape

from app.models import AssertionResult, EvalReport, EvalRunMetadata, TaskRunResult


def render_eval_report_html(report: EvalReport) -> str:
    rows = "\n".join(_render_task(result) for result in report.results)
    summary = report.summary
    pass_rate = (
        round((summary.passed_tasks / summary.total_tasks) * 100, 1)
        if summary.total_tasks
        else 0.0
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Report</title>
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
      width: min(1120px, calc(100vw - 32px));
      margin: 32px auto;
    }}

    header {{
      margin-bottom: 24px;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
      letter-spacing: 0;
    }}

    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }}

    p {{
      margin: 0;
      color: var(--muted);
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .metric,
    .task {{
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

    .task {{
      margin-bottom: 14px;
      overflow: hidden;
    }}

    .task-header {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
    }}

    .task-title {{
      min-width: 0;
    }}

    .task-title strong {{
      display: block;
      overflow-wrap: anywhere;
    }}

    .badge {{
      align-self: flex-start;
      border-radius: 999px;
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      white-space: nowrap;
    }}

    .passed {{
      background: var(--good);
    }}

    .failed {{
      background: var(--bad);
    }}

    .task-body {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr);
      gap: 16px;
      padding: 16px;
    }}

    dl {{
      display: grid;
      grid-template-columns: 110px minmax(0, 1fr);
      gap: 6px 12px;
      margin: 0;
    }}

    dt {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }}

    dd {{
      margin: 0;
      overflow-wrap: anywhere;
    }}

    code {{
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      padding: 1px 4px;
    }}

    ul {{
      margin: 0;
      padding-left: 18px;
    }}

    li {{
      margin-bottom: 6px;
    }}

    @media (max-width: 760px) {{
      .summary,
      .task-body {{
        grid-template-columns: 1fr;
      }}

      .task-header {{
        flex-direction: column;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Agent Reliability Eval Report</h1>
      <p>Deterministic tool-use evaluation with planner traces and assertion-level scoring.</p>
    </header>

    <section class="summary" aria-label="Evaluation summary">
      <div class="metric"><span>Total Tasks</span><strong>{summary.total_tasks}</strong></div>
      <div class="metric"><span>Passed</span><strong>{summary.passed_tasks}</strong></div>
      <div class="metric"><span>Failed</span><strong>{summary.failed_tasks}</strong></div>
      <div class="metric"><span>Pass Rate</span><strong>{pass_rate}%</strong></div>
    </section>

    <section aria-label="Task results">
      {rows}
    </section>
  </main>
</body>
</html>
"""


def render_runs_index_html(runs: list[EvalRunMetadata]) -> str:
    rows = "\n".join(_render_run_row(run) for run in runs)
    if not rows:
        rows = """
        <tr>
          <td colspan="5">No saved runs yet. Use <code>POST /eval/runs</code> to save one.</td>
        </tr>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Saved Evaluation Runs</title>
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

    a {{
      color: #2454a6;
      font-weight: 700;
      text-decoration: none;
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
    <h1>Saved Evaluation Runs</h1>
    <p>SQLite-backed run history for deterministic agent evaluation reports.</p>
    <table>
      <thead>
        <tr>
          <th>Run</th>
          <th>Created</th>
          <th>Total</th>
          <th>Passed</th>
          <th>Failed</th>
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


def _render_run_row(run: EvalRunMetadata) -> str:
    return f"""
        <tr>
          <td><a href="/eval/runs/{run.run_id}">#{run.run_id}</a></td>
          <td>{escape(run.created_at)}</td>
          <td>{run.summary.total_tasks}</td>
          <td>{run.summary.passed_tasks}</td>
          <td>{run.summary.failed_tasks}</td>
        </tr>
"""


def _render_task(result: TaskRunResult) -> str:
    status_class = "passed" if result.passed else "failed"
    status_label = "Passed" if result.passed else "Failed"
    assertions = "\n".join(_render_assertion(assertion) for assertion in result.assertions)
    signals = ", ".join(result.agent_plan.matched_signals) or "none"

    return f"""
<article class="task">
  <div class="task-header">
    <div class="task-title">
      <strong>{escape(result.title)}</strong>
      <p>{escape(result.task_id)}</p>
    </div>
    <span class="badge {status_class}">{status_label}</span>
  </div>
  <div class="task-body">
    <dl>
      <dt>Expected</dt>
      <dd><code>{escape(result.expected_tool)}</code></dd>
      <dt>Selected</dt>
      <dd><code>{escape(result.selected_tool)}</code></dd>
      <dt>Score</dt>
      <dd>{result.score:.2f}</dd>
      <dt>Category</dt>
      <dd>{escape(result.failure_category)}</dd>
      <dt>Confidence</dt>
      <dd>{result.agent_plan.confidence:.2f}</dd>
      <dt>Signals</dt>
      <dd>{escape(signals)}</dd>
    </dl>
    <div>
      <h2>Assertions</h2>
      <ul>{assertions}</ul>
      <h2>Planner Rationale</h2>
      <p>{escape(result.agent_plan.rationale)}</p>
      <h2>Tool Call Trace</h2>
      <p><code>{escape(result.trace[0].tool_name if result.trace else "none")}</code> returned <code>{escape(result.tool_result.status)}</code>.</p>
    </div>
  </div>
</article>
"""


def _render_assertion(assertion: AssertionResult) -> str:
    marker = "pass" if assertion.passed else "fail"
    return (
        f"<li><strong>{escape(marker)}</strong> "
        f"{escape(assertion.name)}: {escape(assertion.detail)}</li>"
    )
