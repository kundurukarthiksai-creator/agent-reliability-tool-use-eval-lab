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

