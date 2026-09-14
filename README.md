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

## Run API

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Open:

```text
http://127.0.0.1:8000/health
```

## Plan

`D:\KIRO\chatgpt\career\projects\AGENT_RELIABILITY_TOOL_USE_EVAL_LAB_PLAN_2026-09-14.md`

