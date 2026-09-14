# Evaluation Methodology

## Principle

The project measures whether an agent uses the correct tool and produces supported structured output. It should not reward fluent hallucination.

## MVP Metrics

- Correct tool selected.
- Required fields present.
- Output schema valid.
- Expected answer matched.
- Unsupported claims flagged.
- Runtime status recorded.

## First Tasks

1. Repo-quality question -> `repo_health_check`
2. Course-note question -> `course_note_search`
3. Job tracker event -> `application_tracker_update`
4. Ambiguous input -> refusal/clarification behavior
5. Final report generation -> structured summary

## Phase 1 Scoring

The Phase 1 runner executes the expected tool directly and scores:

- tool selection;
- exact expected fields;
- list containment;
- minimum numeric thresholds.

This is intentionally deterministic. The later agent loop must earn the right to be interesting by matching this baseline without breaking repeatability.

## Phase 2 Agent Trace

Phase 2 records an `agent_plan` and `trace` for each task:

- `agent_plan` explains which tool the planner selected, confidence, and matched signals.
- `trace` records the actual tool call payload and runtime status.

This separates planner failures from tool failures. Wrong tool selection means the agent failed. Right tool with wrong output means the tool, fixture, or scoring expectation failed. Tool execution errors mean registry/runtime behavior failed.

The CI planner is deterministic on purpose. Future LLM-backed planners should be compared against this baseline instead of replacing it.

## Human-Readable Report

The HTML report shows:

- total tasks, passed tasks, failed tasks, and pass rate;
- expected vs selected tool;
- failure category;
- planner confidence and matched signals;
- assertion-level details;
- tool-call trace status.

This report should make failures understandable without requiring a reader to inspect raw JSON first.

## Saved Runs

Saved runs persist:

- creation timestamp;
- total, passed, and failed task counts;
- average score;
- full report JSON.

The persistence layer does not change scoring. It only records the report produced by the deterministic runner.

## Failure Categories

Each task receives one failure category:

- `passed`: every assertion passed;
- `tool_selection`: the planner chose the wrong tool;
- `tool_execution`: the selected tool raised a runtime error;
- `output_assertion`: the right tool ran, but one or more output assertions failed.

These categories make the report useful for debugging instead of only ranking runs by average score.

## Planner Comparison

Planner comparison runs the same task set against multiple planner implementations and summarizes:

- total tasks;
- passed and failed tasks;
- average score;
- failure-category counts.

The included comparison uses the deterministic default planner and a deliberately weak baseline. Optional LLM-backed planners can be added later, but they should use the same comparison output.
