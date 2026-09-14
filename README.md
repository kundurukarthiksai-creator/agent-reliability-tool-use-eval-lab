# Agent Reliability and Tool-Use Eval Lab

Evaluation lab for AI agents that use tools. The project will run deterministic tool-use tasks, score outputs, expose failures, and produce reproducible reports.

LinkedIn is paused until this project has real proof.

## Current Status

Phase 0 scaffold:

- FastAPI backend
- `/health` route
- unit test
- smoke test script
- architecture and evaluation-methodology stubs

Phase 1 baseline:

- deterministic tool registry
- 3 tools
- 5 starter tasks
- scoring engine
- JSON evaluation report
- `/tools` and `/eval/run` API endpoints

Phase 2 baseline:

- deterministic rule-based agent planner
- tool-call trace in each task result
- CI-safe agent behavior with no external API key

Project hard rules:

- `STEERING.md`
- `.kiro/steering/product.md`
- `.kiro/steering/tech.md`
- `.kiro/steering/quality.md`

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Run Tests

```powershell
.\.venv\Scripts\python -m pytest backend\tests
```

## Run Smoke Test

```powershell
.\.venv\Scripts\python scripts\smoke_test.py
```

## Run Evaluation Report

```powershell
.\.venv\Scripts\python scripts\run_eval.py
```

The report includes the agent plan, selected tool, tool-call trace, assertion results, and score for each task.

## Render HTML Report

```powershell
.\.venv\Scripts\python scripts\render_report.py
```

Sample output:

```text
reports/sample-eval-report.json
reports/sample-eval-report.html
```

## Known Limitations

- The default planner is rule-based, not an LLM planner.
- The eval set is intentionally small while the tool contracts stabilize.
- Reports use synthetic/public-safe fixture data, not private job-search or employer data.
- CI proves deterministic reliability only; it does not claim real-world agent generalization.

## Run API

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Open:

```text
http://127.0.0.1:8000/health
```

Useful routes:

```text
GET  /health
GET  /tools
POST /eval/run
```

## Plan

`D:\KIRO\chatgpt\career\projects\AGENT_RELIABILITY_TOOL_USE_EVAL_LAB_PLAN_2026-09-14.md`
