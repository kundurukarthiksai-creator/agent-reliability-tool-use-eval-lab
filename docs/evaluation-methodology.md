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
- planner confidence and matched signals;
- assertion-level details;
- tool-call trace status.

This report should make failures understandable without requiring a reader to inspect raw JSON first.
