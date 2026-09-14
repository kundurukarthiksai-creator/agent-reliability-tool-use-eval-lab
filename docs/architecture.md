# Architecture

## Goal

Run deterministic tool-use evaluation tasks and produce reproducible reliability reports.

## Phase 0

```text
FastAPI app
  /health

Tests
  backend/tests/test_health.py

Smoke
  scripts/smoke_test.py
```

## Planned Phase 1

```text
Task definitions -> Runner -> Tool registry -> Scoring -> JSON report
```

No LLM dependency should be required for CI. LLM-backed agent behavior comes later and stays optional.

## Phase 1 Baseline

```text
evals/tasks/*.json
        |
        v
backend/app/runner.py
        |
        +--> backend/app/registry.py
        |       |
        |       +--> repo_health_check
        |       +--> course_note_search
        |       +--> application_tracker_update
        |
        +--> backend/app/scoring.py
        |
        v
EvalReport JSON
```

API:

- `GET /tools` lists registered deterministic tools.
- `POST /eval/run` executes all starter tasks and returns an `EvalReport`.

CLI:

- `scripts/run_eval.py` prints the JSON report.
