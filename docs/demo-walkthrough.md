# Demo Walkthrough

This walkthrough is for a quick public review of the project without needing API keys
or external services.

## One-Command Proof

```powershell
.\.venv\Scripts\python scripts\check_all.py
```

This verifies:

- backend tests;
- API smoke path;
- deterministic eval summary;
- strict quality gate;
- dashboard render;
- task catalog render;
- HTML report render;
- failure demo;
- failure catalog;
- planner comparison;
- saved-run comparison demo;
- saved-run trend demo;
- schema export;
- OpenAPI export;
- static demo build;
- static demo link/content check.

## What To Inspect First

1. `reports/dashboard.html`
   - Entry point for the report, task catalog, saved runs, comparison, trends, and planner comparison.
2. `site/case-study.html`
   - Reviewer-focused explanation of what the project proves, where to inspect evidence, and what the limits are.
3. `reports/task-catalog.html`
   - Shows all 22 deterministic tasks, their expected tools, assertion keys, and tool coverage counts.
4. `reports/sample-eval-report.html`
   - Shows planner traces, selected tools, scores, assertions, and failure categories.
5. `reports/failure-catalog.html`
   - Shows deliberate `tool_selection`, `tool_execution`, and `output_assertion` failures.
6. `reports/planner-comparison.md`
   - Compares the deterministic planner against a deliberately weak baseline.
7. `site/index.html`
   - Local build of the static Pages demo.

## Local API Demo

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/eval/tasks.html
http://127.0.0.1:8000/eval/tasks/coverage
http://127.0.0.1:8000/reports/latest.html
http://127.0.0.1:8000/planners/compare.html
```

## Static Demo

```powershell
.\.venv\Scripts\python scripts\build_static_demo.py
.\.venv\Scripts\python scripts\check_static_demo.py
```

Open:

```text
site/index.html
```

The GitHub Pages workflow builds the same static demo from verified artifacts.

## Reliability Claims

The project demonstrates:

- deterministic tool selection and execution;
- explicit tool-call traces;
- assertion-level scoring;
- separated failure categories;
- saved-run comparison and trend summaries;
- strict quality gate for deterministic regressions;
- JSON schemas for public contracts;
- CI-safe execution without keys or paid model calls.

The optional OpenAI planner adapter is manual and disabled by default. It is not part
of the deterministic demo path.
