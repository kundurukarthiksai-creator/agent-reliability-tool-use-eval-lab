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
        |       +--> runbook_lookup
        |
        +--> backend/app/scoring.py
        |
        v
EvalReport JSON
```

API:

- `GET /` renders the dashboard index for report and run-analysis views.
- `GET /tools` lists registered deterministic tools.
- `GET /planners/compare` compares default planner summaries as JSON.
- `GET /planners/compare.html` renders default planner comparison as HTML.
- `GET /eval/tasks` lists deterministic evaluation tasks as JSON.
- `GET /eval/tasks/coverage` summarizes task coverage by expected tool as JSON.
- `GET /eval/tasks.html` renders task coverage as HTML.
- `POST /eval/run` executes all starter tasks and returns an `EvalReport`.
- `POST /eval/runs` executes and saves an eval run to SQLite.
- `GET /eval/runs` lists saved run summaries.
- `GET /eval/runs.html` renders saved run summaries as HTML.
- `GET /eval/runs/compare` compares the latest two saved runs as JSON.
- `GET /eval/runs/compare.html` renders the latest saved-run comparison as HTML.
- `GET /eval/runs/trends` summarizes all saved runs as JSON.
- `GET /eval/runs/trends.html` renders saved-run trend summaries as HTML.
- `GET /eval/runs/{run_id}` returns one saved run and report.
- `GET /reports/latest.html` renders the latest deterministic report as HTML.

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

This keeps the project reliable while creating a real agent loop: plan, execute, trace, score, report. Optional LLM planners are separate planner implementations, not replacements for the baseline.

## Optional OpenAI Planner

```text
EvaluationTask + ToolDefinition[]
      |
      v
OpenAIPlanner -> structured tool-selection JSON -> AgentPlan
```

The OpenAI planner adapter is disabled by default and is not part of CI. It is enabled only when `EVAL_LAB_ENABLE_OPENAI_PLANNER=1` and `OPENAI_API_KEY` are present. The adapter rejects any selected tool that is not already registered locally.

## Reporting

```text
EvalReport JSON -> backend/app/reporting.py -> reports/sample-eval-report.html
```

The HTML report is generated from the same `EvalReport` schema used by the API and CLI. This avoids separate dashboard-only logic and keeps the public artifact reproducible.

The task catalog is generated from the same JSON fixtures that power the runner. It is meant to show coverage quickly: task title, fixture id, expected tool, and assertion keys.

## Persistence

```text
EvalReport -> backend/app/storage.py -> data/eval_runs.sqlite3
```

SQLite stores run metadata and the full report JSON. The database file is intentionally ignored by git.

## Saved-Run Comparison

```text
EvalRunRecord + EvalRunRecord -> backend/app/run_comparison.py -> JSON/HTML delta
```

The comparison view labels task-level movement between the latest two saved runs: unchanged pass, unchanged fail, regression, recovery, score changed, added, or removed. This turns saved reports into a simple reliability trend signal without adding any non-deterministic dependencies.

## Saved-Run Trends

```text
EvalRunMetadata[] -> backend/app/run_trends.py -> JSON/HTML trend summary
```

The trend view summarizes all saved runs by pass-rate, average-score movement, and passed/failed task deltas. It is intentionally metadata-only so trend pages stay cheap and deterministic.
