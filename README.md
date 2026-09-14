# Agent Reliability and Tool-Use Eval Lab

[![CI](https://github.com/kundurukarthiksai-creator/agent-reliability-tool-use-eval-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/kundurukarthiksai-creator/agent-reliability-tool-use-eval-lab/actions/workflows/ci.yml)

Deterministic evaluation lab for tool-using AI agents. It runs structured tasks, asks an agent planner to choose a tool, records the tool-call trace, scores the result, and produces JSON plus HTML reports.

The default path is intentionally CI-safe: no API keys, no paid model calls, and no private data.

![HTML evaluation report screenshot](docs/assets/eval-report.png)

## What It Proves

- An agent can be evaluated on tool choice, not just final text.
- Tool calls are visible through traces.
- Failures are diagnosable at assertion level.
- Reports are reproducible from local fixtures.
- Run history can be persisted to SQLite.

## Current Features

- FastAPI backend.
- Deterministic rule-based planner.
- Tool registry with 5 local tools.
- 22 starter evaluation tasks.
- Assertion-level scoring.
- Strict quality gate for deterministic eval regressions.
- JSON report output.
- HTML report renderer and report API route.
- Task catalog API and HTML view.
- Deliberate failure demo for wrong tool selection.
- SQLite persistence for saved runs.
- Saved-run comparison API and HTML view.
- Saved-run trend summary API and HTML view.
- Optional OpenAI planner comparison, disabled by default.
- GitHub Actions CI.

## Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Run tests:

```powershell
.\.venv\Scripts\python -m pytest backend\tests -q
```

Run full local verification:

```powershell
.\.venv\Scripts\python scripts\check_all.py
```

Run the evaluation:

```powershell
.\.venv\Scripts\python scripts\run_eval.py
```

Check the strict quality gate:

```powershell
.\.venv\Scripts\python scripts\check_quality_gate.py --output reports\quality-gate.json
```

Render sample reports:

```powershell
.\.venv\Scripts\python scripts\render_dashboard.py
.\.venv\Scripts\python scripts\render_task_catalog.py
.\.venv\Scripts\python scripts\render_report.py
.\.venv\Scripts\python scripts\render_failure_demo.py
.\.venv\Scripts\python scripts\render_failure_catalog.py
.\.venv\Scripts\python scripts\compare_planners.py
.\.venv\Scripts\python scripts\render_run_comparison_demo.py
.\.venv\Scripts\python scripts\render_run_trends_demo.py
.\.venv\Scripts\python scripts\export_schemas.py
```

Optional OpenAI planner comparison:

```powershell
$env:EVAL_LAB_ENABLE_OPENAI_PLANNER = "1"
$env:OPENAI_API_KEY = "<your-api-key>"
.\.venv\Scripts\python scripts\compare_openai_planner.py
```

Run the API:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Open:

```text
http://127.0.0.1:8000/reports/latest.html
```

## API Routes

```text
GET  /
GET  /health
GET  /tools
GET  /planners/compare
GET  /planners/compare.html
GET  /eval/tasks
GET  /eval/tasks/coverage
GET  /eval/tasks.html
POST /eval/run
POST /eval/runs
GET  /eval/runs
GET  /eval/runs.html
GET  /eval/runs/compare
GET  /eval/runs/compare.html
GET  /eval/runs/trends
GET  /eval/runs/trends.html
GET  /eval/runs/{run_id}
GET  /reports/latest.html
```

## Sample Artifacts

```text
reports/dashboard.html
reports/task-catalog.html
reports/quality-gate.json
reports/sample-eval-report.json
reports/sample-eval-report.html
reports/sample-failure-report.json
reports/sample-failure-report.html
reports/failure-catalog.json
reports/failure-catalog.html
reports/planner-comparison.json
reports/planner-comparison.md
reports/run-comparison-demo.json
reports/run-comparison-demo.html
reports/run-trends-demo.json
reports/run-trends-demo.html
```

The dashboard links the report, run history, run comparison, trends, and planner comparison views.
The task catalog shows all deterministic task fixtures and the expected tool for each task.
The quality gate fails when deterministic eval results drop below configured pass-rate, score, task-count, or failure-category thresholds.
The failure sample intentionally chooses the wrong tool so the report shows how planner failures appear.
The failure catalog demonstrates `tool_selection`, `tool_execution`, and `output_assertion` categories.
The planner comparison shows the default planner against a deliberately weak baseline.
The run comparison demo shows how saved runs surface regressions and recoveries.
The run trends demo shows reliability movement across several saved runs.

## Project Layout

```text
backend/app/
  agent.py       deterministic planner
  registry.py    tool registry
  runner.py      evaluation orchestration
  scoring.py     assertion scoring
  reporting.py   HTML report rendering
  storage.py     SQLite persistence
  tools/         local deterministic tools
evals/
  tasks/         JSON evaluation tasks
  fixtures/      public-safe synthetic fixtures
reports/         generated sample outputs
docs/            architecture and methodology notes
```

## Known Limitations

- The default planner is rule-based, not an LLM planner.
- OpenAI planner comparison is manual and disabled unless environment variables are set.
- The starter eval set is small while tool contracts stabilize.
- Fixtures are synthetic/public-safe examples.
- CI proves deterministic behavior, not broad real-world agent generalization.
- Saved-run comparison needs at least two persisted runs.

## Roadmap

- Add more tools and harder task fixtures.
- Expand optional planner adapters while keeping CI deterministic.
- Add a lightweight docs/demo deployment if it can stay free of secrets and recurring cost.

## Docs

- `STEERING.md`
- `docs/architecture.md`
- `docs/evaluation-methodology.md`
- `docs/commands.md`
- `docs/demo-walkthrough.md`
- `docs/schemas.md`
- `docs/optional-openai-planner.md`
- `docs/github-metadata.md`
