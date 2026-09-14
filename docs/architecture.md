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

## Phase 2 Baseline

```text
EvaluationTask
      |
      v
RuleBasedAgent planner
      |
      v
selected tool -> ToolRegistry -> ToolCallTrace -> Scoring -> EvalReport JSON
```

The runner now evaluates the agent-selected tool instead of copying `expected_tool`. The first planner is deterministic and CI-safe: it reads the task title, description, and input payload, then chooses a registered tool through signal matching.

This keeps the project reliable while creating a real agent loop: plan, execute, trace, score, report. Optional LLM planners can be added later as another planner implementation, not as a replacement for the baseline.

## Reporting

```text
EvalReport JSON -> backend/app/reporting.py -> reports/sample-eval-report.html
```

The HTML report is generated from the same `EvalReport` schema used by the API and CLI. This avoids separate dashboard-only logic and keeps the public artifact reproducible.
