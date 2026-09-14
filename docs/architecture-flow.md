# Architecture Flow

This project is designed to make tool-use evaluation inspectable. A reviewer should be able to trace how a task enters the system, how the planner selects a tool, how the tool result is scored, and how that evidence becomes a public report.

## Evaluation Path

1. `evals/tasks/*.json`
   - Each fixture defines the task title, description, structured input, expected tool, and assertions.
2. `RuleBasedAgent`
   - The deterministic planner reads title, description, and input signals, then selects one registered tool.
3. `ToolRegistry`
   - The registry executes one of the local deterministic tools and records the tool-call trace.
4. `scoring.py`
   - The scorer checks expected tool, tool status, exact values, containment rules, and minimum values.
5. `EvalReport`
   - The report preserves the planner decision, trace, assertion outcomes, score, and failure category.
6. `quality-gate.json`
   - The quality gate enforces the required task count, pass rate, average score, and failure-category expectations.
7. `site/`
   - The static demo packages report evidence, task catalog, failure catalog, traceability guide, architecture flow, and OpenAPI contract for GitHub Pages.

## Current Proof

- `38/38` deterministic tasks pass.
- `8` local tools are exercised.
- `8` launch-readiness tasks test reviewer-facing project proof.
- `4` artifact-consistency tasks test stale public proof markers.
- The default path uses no API keys, paid model calls, or private data.

## Why This Matters

The architecture keeps the demo honest. The static page is not a separate story from the code; it is built from checked artifacts. If the eval count, report text, screenshot, links, or required proof markers break, the local checker and CI fail.

## Failure Exits

- `tool_selection`: the planner chose the wrong tool.
- `tool_execution`: the selected tool failed at runtime.
- `output_assertion`: the selected tool ran, but output assertions failed.

Those categories are intentionally narrow so a reviewer can tell whether the problem is planner choice, tool behavior, or result quality.
