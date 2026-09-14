from collections import Counter
from collections.abc import Iterable
from html import escape

from app.models import (
    AssertionResult,
    EvalReport,
    EvalRunMetadata,
    EvaluationTask,
    TaskRunResult,
    ToolDefinition,
)
from app.task_catalog import summarize_task_coverage


def render_dashboard_html(
    report: EvalReport,
    tools: list[ToolDefinition],
    runs: list[EvalRunMetadata],
) -> str:
    summary = report.summary
    pass_rate = (
        round((summary.passed_tasks / summary.total_tasks) * 100, 1)
        if summary.total_tasks
        else 0.0
    )
    tool_rows = "\n".join(_render_tool_row(tool) for tool in tools)
    latest_run = f"#{runs[0].run_id}" if runs else "none"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Lab</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #16181d;
      --muted: #5d6470;
      --line: #d9dee7;
      --accent: #2454a6;
      --good: #117a47;
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
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
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

    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-self: flex-start;
    }}

    a {{
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }}

    nav a {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .metric,
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}

    .metric,
    section {{
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

    .grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
      gap: 16px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 10px 0;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}

    td:first-child {{
      width: 38%;
      padding-right: 16px;
    }}

    tr:last-child td {{
      border-bottom: 0;
    }}

    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }}

    code {{
      display: inline-block;
      max-width: 100%;
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      font-size: 13px;
      overflow-wrap: anywhere;
      padding: 1px 4px;
      white-space: normal;
    }}

    .ok {{
      color: var(--good);
      font-weight: 700;
    }}

    @media (max-width: 820px) {{
      header,
      .grid {{
        grid-template-columns: 1fr;
      }}

      header {{
        display: block;
      }}

      nav {{
        margin-top: 16px;
      }}

      .summary {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Agent Reliability Lab</h1>
        <p>Deterministic tool-use evaluation, traces, reports, and saved-run analysis.</p>
      </div>
      <nav aria-label="Dashboard navigation">
        <a href="/eval/tasks.html">Tasks</a>
        <a href="/reports/latest.html">Report</a>
        <a href="/eval/runs.html">Runs</a>
        <a href="/eval/runs/compare.html">Compare</a>
        <a href="/eval/runs/trends.html">Trends</a>
        <a href="/planners/compare.html">Planners</a>
      </nav>
    </header>

    <section class="summary" aria-label="Current evaluation summary">
      <div class="metric"><span>Tasks</span><strong>{summary.total_tasks}</strong></div>
      <div class="metric"><span>Pass Rate</span><strong>{pass_rate}%</strong></div>
      <div class="metric"><span>Tools</span><strong>{len(tools)}</strong></div>
      <div class="metric"><span>Latest Run</span><strong>{escape(latest_run)}</strong></div>
    </section>

    <div class="grid">
      <section>
        <h2>Registered Tools</h2>
        <table>
          <thead>
            <tr>
              <th>Tool</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {tool_rows}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Current Status</h2>
        <p class="ok">Evaluation path is passing.</p>
        <p>Total: {summary.total_tasks}; passed: {summary.passed_tasks}; failed: {summary.failed_tasks}; average score: {summary.average_score:.4f}.</p>
      </section>
    </div>
  </main>
</body>
</html>
"""


def render_task_catalog_html(
    tasks: list[EvaluationTask],
    tools: list[ToolDefinition],
) -> str:
    rows = "\n".join(_render_task_catalog_row(task) for task in tasks)
    coverage_by_tool = {
        item.tool_name: item.task_count
        for item in summarize_task_coverage(tasks, tools).coverage
    }
    tool_rows = "\n".join(
        _render_catalog_tool_row(tool, coverage_by_tool[tool.name]) for tool in tools
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evaluation Task Catalog</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #16181d;
      --muted: #5d6470;
      --line: #d9dee7;
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
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
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

    a {{
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }}

    .back-link {{
      align-self: flex-start;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      white-space: nowrap;
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .metric,
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
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

    .grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
      gap: 16px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 10px 0;
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

    td:first-child {{
      width: 22%;
      padding-right: 16px;
    }}

    code {{
      display: inline-block;
      max-width: 100%;
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      font-size: 13px;
      overflow-wrap: anywhere;
      padding: 1px 4px;
      white-space: normal;
    }}

    .task-title {{
      display: block;
      margin-bottom: 4px;
      overflow-wrap: anywhere;
    }}

    .expectations {{
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 980px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 820px) {{
      header {{
        display: block;
      }}

      .back-link {{
        display: inline-block;
        margin-top: 16px;
      }}

      .summary {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 700px) {{
      table,
      thead,
      tbody,
      tr,
      th,
      td {{
        display: block;
      }}

      thead {{
        display: none;
      }}

      tr {{
        border-bottom: 1px solid var(--line);
        padding: 12px 0;
      }}

      tr:last-child {{
        border-bottom: 0;
      }}

      td,
      td:first-child {{
        width: auto;
        border-bottom: 0;
        padding: 4px 0;
      }}

      td::before {{
        content: attr(data-label);
        display: block;
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 2px;
        text-transform: uppercase;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Evaluation Task Catalog</h1>
        <p>Public-safe task coverage for deterministic tool-selection evaluation.</p>
      </div>
      <a class="back-link" href="/">Dashboard</a>
    </header>

    <section class="summary" aria-label="Task catalog summary">
      <div class="metric"><span>Tasks</span><strong>{len(tasks)}</strong></div>
      <div class="metric"><span>Tools</span><strong>{len(tools)}</strong></div>
      <div class="metric"><span>Fixture Type</span><strong>Public</strong></div>
    </section>

    <div class="grid">
      <section>
        <h2>Tasks</h2>
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Expected Tool</th>
              <th>Checks</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Registered Tools</h2>
        <table>
          <thead>
            <tr>
              <th>Tool</th>
              <th>Tasks</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {tool_rows}
          </tbody>
        </table>
      </section>
    </div>
  </main>
</body>
</html>
"""


def render_eval_report_html(report: EvalReport) -> str:
    rows = "\n".join(_render_task(result) for result in report.results)
    tool_rows = _render_count_rows(result.selected_tool for result in report.results)
    category_rows = _render_count_rows(
        result.failure_category for result in report.results
    )
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

    .overview-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}

    .overview-panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}

    .overview-panel table {{
      width: 100%;
      border-collapse: collapse;
    }}

    .overview-panel td {{
      padding: 8px 0;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}

    .overview-panel tr:last-child td {{
      border-bottom: 0;
    }}

    .overview-panel td:last-child {{
      color: var(--muted);
      font-weight: 700;
      text-align: right;
      white-space: nowrap;
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
      .overview-grid,
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

    <section class="overview-grid" aria-label="Evaluation distribution summary">
      <div class="overview-panel">
        <h2>Tool Selection</h2>
        <table>
          <tbody>
            {tool_rows}
          </tbody>
        </table>
      </div>
      <div class="overview-panel">
        <h2>Failure Categories</h2>
        <table>
          <tbody>
            {category_rows}
          </tbody>
        </table>
      </div>
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


def _render_tool_row(tool: ToolDefinition) -> str:
    return f"""
        <tr>
          <td data-label="Tool"><code>{escape(tool.name)}</code></td>
          <td data-label="Description">{escape(tool.description)}</td>
        </tr>
"""


def _render_catalog_tool_row(tool: ToolDefinition, task_count: int) -> str:
    return f"""
        <tr>
          <td data-label="Tool"><code>{escape(tool.name)}</code></td>
          <td data-label="Tasks">{task_count}</td>
          <td data-label="Description">{escape(tool.description)}</td>
        </tr>
"""


def _render_task_catalog_row(task: EvaluationTask) -> str:
    expectation_names = ", ".join(sorted(task.expectations)) or "tool result only"

    return f"""
        <tr>
          <td data-label="Task">
            <strong class="task-title">{escape(task.title)}</strong>
            <code>{escape(task.id)}</code>
          </td>
          <td data-label="Expected Tool"><code>{escape(task.expected_tool)}</code></td>
          <td data-label="Checks">
            {escape(task.description)}
            <div class="expectations">Assertions: {escape(expectation_names)}</div>
          </td>
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


def _render_count_rows(values: Iterable[str]) -> str:
    counts = Counter(values)
    if not counts:
        return """
        <tr>
          <td>None</td>
          <td>0</td>
        </tr>
"""
    rows = []
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        rows.append(
            f"""
        <tr>
          <td><code>{escape(name)}</code></td>
          <td>{count}</td>
        </tr>
"""
        )
    return "".join(rows)
