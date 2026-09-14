# Quality Steering

## Required Checks

Before committing meaningful changes:

```powershell
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python scripts\smoke_test.py
.\.venv\Scripts\python scripts\run_eval.py
```

## Test Expectations

- New tools need unit tests and at least one eval task.
- New planners need tests that prove they do not read answer-key fields as shortcuts.
- New API endpoints need smoke or endpoint tests.
- Scoring changes need both passing and failing examples when practical.

## Failure Policy

Failures should be visible in:

- assertion details;
- selected tool vs expected tool;
- tool output;
- agent plan;
- trace status.

Do not hide a failed task behind a broad average score.

## Documentation Expectations

Update docs when changing:

- report schema;
- evaluation methodology;
- planner behavior;
- tool contracts;
- public setup steps.
