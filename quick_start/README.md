# Quick Start: Reviewer Proof Path

Goal: give a reviewer the shortest no-key path from clone to proof.

This project is designed to be inspectable without private data, paid model calls,
or API keys. The default planner is deterministic and the sample artifacts are
generated from local fixtures.

## Fastest Public Inspection

Open the live static demo first:

https://kundurukarthiksai-creator.github.io/agent-reliability-tool-use-eval-lab/

Then inspect these public pages:

1. Project one-pager: purpose, current proof, engineering signals, and limits.
2. Eval report: `42/42` passing tasks, `9` local tools, and trace coverage.
3. Task catalog: task ids, expected tools, assertion keys, and coverage.
4. Tool-safety walkthrough: permission gates, approvals, dry-run behavior, audit logs, and negative tests.
5. Architecture flow: how fixtures, planner, tools, scoring, reports, and static demo publishing connect.
6. OpenAPI contract: the route surface exposed by the FastAPI backend.

## Local No-Key Verification

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\check_all.py
```

### macOS/Linux

```bash
python -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python scripts/check_all.py
```

The full check runs:

- backend tests;
- API smoke test;
- deterministic eval;
- strict quality gate;
- report builders;
- schema export;
- OpenAPI export;
- static demo build;
- static demo content/link check.

Expected proof summary:

- `73` backend tests pass;
- eval result is `42/42`;
- `9` local tools are exercised;
- strict quality gate passes;
- static demo check passes.

## Code Inspection Map

Start here if you want to inspect implementation rather than artifacts:

- `backend/app/agent.py`: deterministic planner.
- `backend/app/registry.py`: local tool registry.
- `backend/app/runner.py`: evaluation orchestration and trace recording.
- `backend/app/scoring.py`: assertion-level scoring.
- `evals/tasks/`: deterministic task fixtures.
- `scripts/check_all.py`: one-command verification path.
- `scripts/build_static_demo.py`: GitHub Pages artifact builder.

## Optional API Run

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/reports/latest.html
http://127.0.0.1:8000/openapi.json
```

## Optional LLM Planner

The OpenAI planner comparison is intentionally disabled by default and is not
part of CI. It only runs when environment variables explicitly enable it.

```powershell
$env:EVAL_LAB_ENABLE_OPENAI_PLANNER = "1"
$env:OPENAI_API_KEY = "<your-api-key>"
.\.venv\Scripts\python scripts\compare_openai_planner.py
```

The project does not need this optional path to prove the core eval workflow.
