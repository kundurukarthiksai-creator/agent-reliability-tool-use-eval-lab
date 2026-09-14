# Project One-Pager

## What This Is

Agent Reliability and Tool-Use Eval Lab is a deterministic evaluation system for tool-using agents. It checks whether a planner chooses the right tool, records the tool call, scores structured output, and turns the result into reviewer-friendly reports.

## Current Proof

- `38/38` deterministic tasks pass.
- `8` local tools are exercised.
- `38/38` tool-call traces are recorded.
- The strict quality gate requires 100% pass rate, 1.0 average score, zero failed tasks, and only passed failure categories.
- The public static demo runs without API keys, paid model calls, or private data.

## Why It Matters

Most agent demos are hard to evaluate because they show final text, not evidence. This project makes the evaluation path inspectable:

- task fixture;
- planner decision;
- selected tool;
- tool-call trace;
- assertion-level score;
- failure category;
- public report.

## Engineering Signals

- FastAPI route surface with OpenAPI export.
- Pydantic models for task, report, storage, comparison, trends, and quality-gate contracts.
- SQLite persistence for saved evaluation runs.
- CI-safe deterministic planner baseline.
- Failure catalog for deliberate `tool_selection`, `tool_execution`, and `output_assertion` failures.
- Static GitHub Pages demo built from checked artifacts.

## What To Inspect First

1. `reports/sample-eval-report.html`
   - Confirm the reviewer evidence summary, traces, assertions, and quality gate.
2. `reports/task-catalog.html`
   - Confirm task coverage across all 8 tools.
3. `traceability.html`
   - Follow one task from fixture to report evidence.
4. `architecture-flow.html`
   - Understand how fixtures, planner, tools, scoring, reports, and static publishing connect.
5. `docs/openapi.json`
   - Inspect the API contract.

## Honest Limits

- The default planner is rule-based.
- Fixtures are synthetic and public-safe.
- CI proves deterministic reliability on this corpus, not universal agent performance.
- Optional OpenAI planner comparison is manual and disabled by default.
