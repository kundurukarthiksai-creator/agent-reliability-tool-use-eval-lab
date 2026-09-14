import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
REPORTS_DIR = ROOT / "reports"
ASSETS_DIR = ROOT / "docs" / "assets"
DOCS_DIR = ROOT / "docs"


REPORT_FILES = [
    "dashboard.html",
    "task-catalog.html",
    "sample-eval-report.html",
    "sample-eval-report.json",
    "quality-gate.json",
    "sample-failure-report.html",
    "sample-failure-report.json",
    "failure-catalog.html",
    "failure-catalog.json",
    "planner-comparison.md",
    "planner-comparison.json",
    "run-comparison-demo.html",
    "run-comparison-demo.json",
    "run-trends-demo.html",
    "run-trends-demo.json",
]


def main() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    assets_output = SITE_DIR / "assets"
    docs_output = SITE_DIR / "docs"
    reports_output = SITE_DIR / "reports"
    reports_output.mkdir(parents=True)
    assets_output.mkdir(parents=True)
    docs_output.mkdir(parents=True)

    for filename in REPORT_FILES:
        source = REPORTS_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing report artifact: {source}")
        shutil.copy2(source, reports_output / filename)

    screenshot = ASSETS_DIR / "eval-report.png"
    if screenshot.exists():
        shutil.copy2(screenshot, assets_output / screenshot.name)

    openapi_contract = DOCS_DIR / "openapi.json"
    if not openapi_contract.exists():
        raise FileNotFoundError(f"Missing OpenAPI contract: {openapi_contract}")
    shutil.copy2(openapi_contract, docs_output / openapi_contract.name)

    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (SITE_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    (SITE_DIR / "case-study.html").write_text(render_case_study(), encoding="utf-8")
    (SITE_DIR / "traceability.html").write_text(
        render_traceability_guide(),
        encoding="utf-8",
    )
    (SITE_DIR / "architecture-flow.html").write_text(
        render_architecture_flow(),
        encoding="utf-8",
    )
    print(f"built {SITE_DIR}")


def render_index() -> str:
    links = [
        ("Case Study", "case-study.html", "Read the reviewer-friendly project walkthrough."),
        ("Traceability Guide", "traceability.html", "Follow one task from fixture to planner, trace, and assertions."),
        ("Architecture Flow", "architecture-flow.html", "See how fixtures, planner, tools, scoring, reports, and quality gate connect."),
        ("Dashboard", "reports/dashboard.html", "Start with the portfolio demo index."),
        ("Task Catalog", "reports/task-catalog.html", "Inspect all 38 deterministic tasks."),
        ("Eval Report", "reports/sample-eval-report.html", "Review traces, assertions, and scoring."),
        ("Quality Gate", "reports/quality-gate.json", "See the strict regression gate output."),
        ("Failure Catalog", "reports/failure-catalog.html", "Inspect deliberate failure categories."),
        ("Planner Comparison", "reports/planner-comparison.md", "Compare planners in a compact report."),
        ("Run Comparison", "reports/run-comparison-demo.html", "Review saved-run regression signals."),
        ("Run Trends", "reports/run-trends-demo.html", "Review reliability movement over runs."),
        ("OpenAPI Contract", "docs/openapi.json", "Inspect the FastAPI route schema."),
    ]
    inspection_steps = [
        (
            "reports/sample-eval-report.html",
            "Confirm the report shows 38/38 tasks pass, 8 tools exercised, 38/38 traces, and a passing regression guard.",
        ),
        (
            "reports/task-catalog.html",
            "Check that the task catalog covers the deterministic corpus and tool distribution.",
        ),
        (
            "reports/failure-catalog.html",
            "Review deliberate tool-selection, tool-execution, and output-assertion failures.",
        ),
        (
            "traceability.html",
            "Use the traceability guide to understand how one task becomes auditable evidence.",
        ),
        (
            "architecture-flow.html",
            "Use the architecture flow to understand how fixtures, planner, tools, scoring, reports, and the quality gate connect.",
        ),
        (
            "docs/openapi.json",
            "Inspect the OpenAPI contract for the FastAPI route surface.",
        ),
    ]
    cards = "\n".join(
        f"""
        <a class="card" href="{href}">
          <span>{label}</span>
          <p>{description}</p>
        </a>
        """.strip()
        for label, href, description in links
    )
    inspection_items = "\n".join(
        f"""
        <li>
          <a href="{href}">{description}</a>
        </li>
        """.strip()
        for href, description in inspection_steps
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Lab Demo</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #171a21;
      --muted: #566173;
      --border: #d9e0ea;
      --accent: #0f5db8;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      width: 100%;
      overflow-x: hidden;
    }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    main {{
      width: 100%;
      max-width: 1120px;
      margin: 0 auto;
      padding: 36px 20px 48px;
    }}
    header {{
      display: grid;
      gap: 18px;
      margin-bottom: 28px;
    }}
    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }}
    .summary {{
      max-width: 780px;
      margin: 0;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
      overflow-wrap: anywhere;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 28px 0;
    }}
    .metric, .card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    .metric {{
      padding: 18px;
    }}
    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .metric strong {{
      display: block;
      margin-top: 8px;
      font-size: 28px;
    }}
    h2 {{
      margin: 0;
      font-size: 21px;
      letter-spacing: 0;
    }}
    .inspection {{
      border-bottom: 1px solid var(--border);
      border-top: 1px solid var(--border);
      margin: 28px 0;
      padding: 22px 0;
    }}
    .inspection ol {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px 28px;
      margin: 16px 0 0;
      padding-left: 22px;
    }}
    .inspection li {{
      color: var(--muted);
      line-height: 1.5;
      padding-right: 12px;
    }}
    .inspection a {{
      color: inherit;
      overflow-wrap: anywhere;
      text-decoration-color: rgba(15, 93, 184, .35);
      text-decoration-thickness: 2px;
      text-underline-offset: 3px;
    }}
    .inspection a:hover {{
      color: var(--accent);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .card {{
      min-height: 130px;
      padding: 18px;
      color: inherit;
      text-decoration: none;
      overflow-wrap: anywhere;
    }}
    .card:hover {{
      border-color: var(--accent);
      box-shadow: 0 10px 30px rgba(20, 32, 52, .08);
    }}
    .card span {{
      color: var(--accent);
      font-size: 16px;
      font-weight: 800;
    }}
    .card p {{
      margin: 12px 0 0;
      color: var(--muted);
      line-height: 1.45;
    }}
    .preview {{
      margin-top: 28px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .preview img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    @media (max-width: 840px) {{
      h1 {{ font-size: 29px; }}
      .metrics, .grid, .inspection ol {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 520px) {{
      main {{ max-width: 390px; margin: 0; padding: 28px 16px 40px; }}
      .metrics, .grid, .inspection ol {{ grid-template-columns: 1fr; }}
      .card {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Agent Reliability Eval Lab Demo</h1>
      <p class="summary">Static public demo for a deterministic tool-use evaluation lab. The default path runs without API keys, scores 38 tasks across 8 local tools, and publishes the same reports verified by CI.</p>
    </header>
    <section class="metrics" aria-label="Demo metrics">
      <div class="metric"><span>Tasks</span><strong>38</strong></div>
      <div class="metric"><span>Tools</span><strong>8</strong></div>
      <div class="metric"><span>Pass Rate</span><strong>100%</strong></div>
      <div class="metric"><span>CI Path</span><strong>No Keys</strong></div>
    </section>
    <section class="inspection" aria-label="Reviewer inspection checklist">
      <h2>Reviewer Inspection Checklist</h2>
      <ol>
        {inspection_items}
      </ol>
    </section>
    <section class="grid" aria-label="Demo links">
      {cards}
    </section>
    <section class="preview" aria-label="Report screenshot">
      <img src="assets/eval-report.png" alt="HTML evaluation report screenshot">
    </section>
  </main>
</body>
</html>
"""


def render_architecture_flow() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Lab Architecture Flow</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #171a21;
      --muted: #566173;
      --border: #d9e0ea;
      --accent: #0f5db8;
      --success: #147d43;
    }
    * { box-sizing: border-box; }
    html, body {
      width: 100%;
      overflow-x: hidden;
    }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    main {
      width: 100%;
      max-width: 1120px;
      margin: 0 auto;
      padding: 36px 20px 52px;
    }
    a { color: var(--accent); }
    .back {
      display: inline-block;
      margin-bottom: 22px;
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }
    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .summary {
      max-width: 820px;
      margin: 16px 0 28px;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
    }
    h2 {
      margin: 0 0 14px;
      font-size: 21px;
      letter-spacing: 0;
    }
    p, li {
      color: var(--muted);
      line-height: 1.58;
      overflow-wrap: anywhere;
    }
    code {
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      padding: 1px 4px;
      white-space: normal;
    }
    section {
      border-top: 1px solid var(--border);
      padding: 24px 0;
    }
    .proof {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 0 0 28px;
    }
    .metric, .node {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
    }
    .metric {
      min-height: 104px;
      padding: 18px;
    }
    .metric span {
      color: var(--muted);
      display: block;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .metric strong {
      color: var(--success);
      display: block;
      font-size: 28px;
      margin-top: 8px;
      overflow-wrap: anywhere;
    }
    .proof-note {
      margin: 0;
      max-width: 820px;
    }
    .flow {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }
    .node {
      min-height: 188px;
      padding: 14px;
      position: relative;
    }
    .node span {
      color: var(--accent);
      display: block;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .06em;
      margin-bottom: 9px;
      text-transform: uppercase;
    }
    .node strong {
      display: block;
      font-size: 15px;
      line-height: 1.25;
      overflow-wrap: anywhere;
    }
    .node p {
      font-size: 14px;
      margin: 10px 0 0;
    }
    .split {
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr);
      gap: 28px;
    }
    .plain-list {
      margin: 10px 0 0;
      padding-left: 22px;
    }
    .plain-list li {
      margin: 8px 0;
    }
    @media (max-width: 820px) {
      h1 { font-size: 29px; }
      .proof, .flow, .split { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 520px) {
      main { max-width: 390px; margin: 0; padding: 28px 16px 42px; }
      h1 { font-size: 26px; line-height: 1.15; }
      .summary { font-size: 16px; }
      .proof, .flow, .split { grid-template-columns: 1fr; }
      .metric, .node { min-height: auto; }
    }
  </style>
</head>
<body>
  <main>
    <a class="back" href="index.html">Back to demo</a>
    <h1>Agent Reliability Eval Lab Architecture Flow</h1>
    <p class="summary">A compact map of how deterministic task fixtures become planner decisions, tool traces, scored assertions, quality gates, and public demo evidence.</p>

    <section aria-label="Current Proof">
      <h2>Current Proof</h2>
      <div class="proof">
        <div class="metric"><span>Eval Result</span><strong>38/38</strong></div>
        <div class="metric"><span>Tool Coverage</span><strong>8 tools</strong></div>
        <div class="metric"><span>Launch Cases</span><strong>8 tasks</strong></div>
        <div class="metric"><span>Default Path</span><strong>No Keys</strong></div>
      </div>
      <p class="proof-note">The suite now includes 4 artifact-consistency tasks that check stale public proof markers before they reach reviewers.</p>
    </section>

    <section aria-label="Evaluation Path">
      <h2>Evaluation Path</h2>
      <div class="flow">
        <div class="node"><span>01</span><strong><code>evals/tasks/*.json</code></strong><p>Defines task input, expected tool, and explicit assertions.</p></div>
        <div class="node"><span>02</span><strong><code>RuleBasedAgent</code></strong><p>Selects a tool from task title, description, and structured signals.</p></div>
        <div class="node"><span>03</span><strong><code>ToolRegistry</code></strong><p>Executes one local deterministic tool and records the call trace.</p></div>
        <div class="node"><span>04</span><strong><code>scoring.py</code></strong><p>Checks tool choice, status, exact values, containment, and minimum thresholds.</p></div>
        <div class="node"><span>05</span><strong><code>EvalReport</code></strong><p>Preserves plan, trace, assertions, score, and failure category.</p></div>
        <div class="node"><span>06</span><strong><code>quality-gate.json</code></strong><p>Enforces pass rate, average score, task count, and accepted failure categories.</p></div>
        <div class="node"><span>07</span><strong><code>site/</code></strong><p>Packages checked evidence into the static GitHub Pages demo.</p></div>
      </div>
    </section>

    <section aria-label="Architecture notes">
      <div class="split">
        <div>
          <h2>Why This Matters</h2>
          <p>The public demo is not a hand-written marketing page. It is built from checked artifacts, so broken links, missing proof text, stale task counts, or missing screenshots fail verification before publishing.</p>
          <p>The same path supports local inspection, CI verification, and GitHub Pages review without API keys or paid model calls.</p>
        </div>
        <div>
          <h2>Failure Exits</h2>
          <ul class="plain-list">
            <li><code>tool_selection</code>: planner chose the wrong tool.</li>
            <li><code>tool_execution</code>: selected tool failed at runtime.</li>
            <li><code>output_assertion</code>: tool ran, but output checks failed.</li>
          </ul>
        </div>
      </div>
    </section>
  </main>
</body>
</html>
"""


def render_traceability_guide() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Lab Traceability Guide</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #171a21;
      --muted: #566173;
      --border: #d9e0ea;
      --accent: #0f5db8;
    }
    * { box-sizing: border-box; }
    html, body {
      width: 100%;
      overflow-x: hidden;
    }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    main {
      width: 100%;
      max-width: 960px;
      margin: 0 auto;
      padding: 36px 20px 52px;
    }
    a { color: var(--accent); }
    .back {
      display: inline-block;
      margin-bottom: 22px;
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }
    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .summary {
      max-width: 780px;
      margin: 16px 0 30px;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
    }
    section {
      border-top: 1px solid var(--border);
      padding: 22px 0;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }
    p, li {
      color: var(--muted);
      line-height: 1.58;
      overflow-wrap: anywhere;
    }
    ul, ol {
      margin: 10px 0 0;
      padding-left: 22px;
    }
    code {
      background: #eef2f8;
      border: 1px solid #d7deea;
      border-radius: 4px;
      padding: 1px 4px;
      white-space: normal;
    }
    .path {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      margin-top: 14px;
    }
    .step {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      min-height: 108px;
      padding: 14px;
    }
    .step span {
      color: var(--accent);
      display: block;
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 8px;
      text-transform: uppercase;
    }
    .step p {
      font-size: 14px;
      margin: 0;
    }
    @media (max-width: 820px) {
      h1 { font-size: 29px; }
      .path { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 520px) {
      main { max-width: 390px; margin: 0; padding: 28px 16px 42px; }
      h1 { font-size: 26px; line-height: 1.15; }
      .summary { font-size: 16px; }
      .path { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <a class="back" href="index.html">Back to demo</a>
    <h1>Agent Reliability Eval Lab Traceability Guide</h1>
    <p class="summary">A reviewer guide for following one task from JSON fixture to planner decision, tool call trace, assertions, and final report evidence.</p>

    <section>
      <h2>Audit Path</h2>
      <div class="path" aria-label="Traceability path">
        <div class="step"><span>Task</span><p>Start with one JSON fixture in <code>evals/tasks</code>.</p></div>
        <div class="step"><span>Plan</span><p>Inspect <code>agent_plan</code> for selected tool, matched signals, and rationale.</p></div>
        <div class="step"><span>Trace</span><p>Confirm the selected tool was called and returned <code>ok</code>.</p></div>
        <div class="step"><span>Score</span><p>Check tool selection, status, exact values, containment, and minimum thresholds.</p></div>
        <div class="step"><span>Category</span><p>Use the failure category to understand what broke when a task fails.</p></div>
      </div>
    </section>

    <section>
      <h2>What A Passing Task Proves</h2>
      <ul>
        <li>The planner selected the expected tool.</li>
        <li>The tool call executed successfully.</li>
        <li>The returned structured output matched the task expectations.</li>
        <li>The report kept enough trace data for a reviewer to diagnose the path.</li>
      </ul>
    </section>

    <section>
      <h2>What To Check In The Report</h2>
      <p>In <a href="reports/sample-eval-report.html">the HTML eval report</a>, inspect <code>Expected</code>, <code>Selected</code>, <code>Score</code>, <code>Category</code>, <code>Signals</code>, <code>Assertions</code>, <code>Planner Rationale</code>, and <code>Tool Call Trace</code>.</p>
      <p>The reviewer evidence summary gives aggregate proof. Individual task cards give the audit trail.</p>
    </section>

    <section>
      <h2>Failure Interpretation</h2>
      <ul>
        <li><code>tool_selection</code>: the planner chose the wrong tool.</li>
        <li><code>tool_execution</code>: the selected tool failed at runtime.</li>
        <li><code>output_assertion</code>: the selected tool ran, but output checks failed.</li>
      </ul>
      <p><a href="reports/failure-catalog.html">The failure catalog</a> demonstrates these categories deliberately.</p>
    </section>
  </main>
</body>
</html>
"""


def render_case_study() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Lab Case Study</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #171a21;
      --muted: #566173;
      --border: #d9e0ea;
      --accent: #0f5db8;
    }
    * { box-sizing: border-box; }
    html, body {
      width: 100%;
      overflow-x: hidden;
    }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    main {
      width: 100%;
      max-width: 920px;
      margin: 0 auto;
      padding: 36px 20px 52px;
    }
    a { color: var(--accent); }
    .back {
      display: inline-block;
      margin-bottom: 22px;
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }
    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .summary {
      max-width: 780px;
      margin: 16px 0 30px;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      margin-top: 14px;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }
    p, li {
      color: var(--muted);
      line-height: 1.58;
      overflow-wrap: anywhere;
    }
    a {
      overflow-wrap: anywhere;
    }
    ul, ol {
      margin: 10px 0 0;
      padding-left: 22px;
    }
    strong {
      color: var(--text);
    }
    @media (max-width: 520px) {
      main {
        max-width: 390px;
        margin: 0;
        padding: 28px 16px 42px;
      }
      h1 { font-size: 26px; line-height: 1.15; }
      .summary { font-size: 16px; }
      section { padding: 18px; }
      p, li { font-size: 15px; }
    }
  </style>
</head>
<body>
  <main>
    <a class="back" href="index.html">Back to demo</a>
    <h1>Agent Reliability Eval Lab Case Study</h1>
    <p class="summary">A quick reviewer guide for understanding what the project proves, where to inspect the evidence, and what it intentionally does not claim.</p>

    <section>
      <h2>Why This Project Exists</h2>
      <p>Most agent demos show a fluent answer. This project asks a narrower question: did the agent choose the right tool, call it with structured input, and produce output that can be checked?</p>
      <p>The default path is deterministic and runs without API keys, paid model calls, or private data.</p>
    </section>

    <section>
      <h2>What It Evaluates</h2>
      <ul>
        <li>Tool selection across <strong>38</strong> public-safe tasks.</li>
        <li>Tool-call traces for <strong>8</strong> deterministic local tools.</li>
        <li>Assertion-level scoring for expected fields and values.</li>
        <li>Failure categories for tool selection, tool execution, and output assertions.</li>
        <li>Saved-run comparison and trend views for regression visibility.</li>
      </ul>
    </section>

    <section>
      <h2>How To Inspect It</h2>
      <ol>
        <li><a href="reports/task-catalog.html">Task catalog</a>: coverage and expected tools.</li>
        <li><a href="reports/sample-eval-report.html">Eval report</a>: planner traces, selected tools, assertion results, and score.</li>
        <li><a href="reports/failure-catalog.html">Failure catalog</a>: deliberate failure categories.</li>
        <li><a href="reports/quality-gate.json">Quality gate</a>: the strict regression threshold used by CI.</li>
        <li><a href="docs/openapi.json">OpenAPI contract</a>: route schema for the FastAPI app.</li>
      </ol>
    </section>

    <section>
      <h2>What This Proves</h2>
      <ul>
        <li>The project evaluates tool use instead of only reading final text.</li>
        <li>The reports make failure causes visible.</li>
        <li>CI guards deterministic reliability behavior without secrets.</li>
        <li>Optional LLM planner experiments can be added without replacing the baseline.</li>
      </ul>
    </section>

    <section>
      <h2>Honest Limits</h2>
      <ul>
        <li>The default planner is rule-based.</li>
        <li>Fixtures are synthetic and public-safe.</li>
        <li>CI proves deterministic behavior on this task set, not universal agent reliability.</li>
        <li>Optional LLM planner comparison is manual and disabled by default.</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
