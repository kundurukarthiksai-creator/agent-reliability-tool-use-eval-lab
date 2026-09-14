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

1. `site/index.html`
   - Start with the reviewer inspection checklist. It points to the current 42/42 report, task catalog, failure catalog, and OpenAPI contract.
2. `site/project-one-pager.html`
   - Quick recruiter and reviewer scan of purpose, proof, engineering signals, inspection path, and honest limits.
3. `reports/dashboard.html`
   - Entry point for the report, task catalog, saved runs, comparison, trends, and planner comparison.
4. `site/case-study.html`
   - Reviewer-focused explanation of what the project proves, where to inspect evidence, and what the limits are.
5. `site/interview-walkthrough.html`
   - Interview-focused explanation of the problem, design choices, tradeoffs, current proof, and limits.
6. `site/traceability.html`
   - Shows how one task flows from fixture to planner decision, tool trace, assertions, and failure category.
7. `site/architecture-flow.html`
   - Shows how fixtures, planner, tools, scoring, reports, quality gate, and static publishing connect.
8. `reports/task-catalog.html`
   - Shows all 42 deterministic tasks, their expected tools, assertion keys, and tool coverage counts.
9. `reports/sample-eval-report.html`
   - Shows reviewer evidence summary, planner traces, selected tools, scores, assertions, and failure categories.
10. `reports/failure-catalog.html`
   - Shows deliberate `tool_selection`, `tool_execution`, and `output_assertion` failures.
11. `reports/planner-comparison.md`
   - Compares the deterministic planner against a deliberately weak baseline.

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
