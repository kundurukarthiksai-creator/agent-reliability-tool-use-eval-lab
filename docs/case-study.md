# Case Study

## Why This Project Exists

Most agent demos show a fluent answer. This project asks a narrower question: did the agent choose the right tool, call it with structured input, and produce output that can be checked?

The default path is intentionally deterministic. It runs without API keys or paid model calls so the core reliability claims can be verified in CI and by any reviewer cloning the repo.

## What It Evaluates

- Tool selection across 22 public-safe tasks.
- Tool-call traces for 5 deterministic local tools.
- Assertion-level scoring for expected fields and values.
- Failure categories for tool selection, tool execution, and output assertions.
- Saved-run comparison and trend views for regression visibility.

## How To Inspect It

Start with the static demo landing page, then inspect:

1. Task catalog: coverage and expected tools.
2. Eval report: planner traces, selected tools, assertion results, and score.
3. Failure catalog: deliberate failure categories.
4. Quality gate: the strict regression threshold used by CI.
5. OpenAPI contract: route schema for the FastAPI app.

## What This Proves

- The project can evaluate tool use instead of only reading final text.
- The reports make failure causes visible.
- CI can guard deterministic reliability behavior without secrets.
- Optional LLM planner experiments can be added without replacing the baseline.

## Honest Limits

- The default planner is rule-based.
- Fixtures are synthetic and public-safe.
- CI proves deterministic behavior on this task set, not universal agent reliability.
- Optional LLM planner comparison is manual and disabled by default.
