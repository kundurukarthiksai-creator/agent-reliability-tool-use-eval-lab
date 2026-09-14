# Commands

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## One-Command Local Verification

```powershell
.\.venv\Scripts\python scripts\check_all.py
```

This runs:

- backend tests;
- API smoke test;
- normal eval JSON;
- dashboard renderer;
- task catalog renderer;
- HTML report renderer;
- failure demo renderer;
- failure catalog renderer;
- planner comparison renderer.
- run comparison demo renderer.
- run trends demo renderer.

## Individual Commands

```powershell
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python scripts\smoke_test.py
.\.venv\Scripts\python scripts\run_eval.py
.\.venv\Scripts\python scripts\run_eval.py reports\sample-eval-report.json
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

## API

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

Useful pages:

```text
http://127.0.0.1:8000/reports/latest.html
http://127.0.0.1:8000/
http://127.0.0.1:8000/eval/tasks.html
http://127.0.0.1:8000/eval/runs.html
http://127.0.0.1:8000/eval/runs/compare.html
http://127.0.0.1:8000/eval/runs/trends.html
http://127.0.0.1:8000/planners/compare.html
```
