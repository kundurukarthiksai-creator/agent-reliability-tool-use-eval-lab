# Traceability Guide

This guide explains how to inspect one evaluation result from task fixture to planner decision, tool execution, assertions, and public report output.

## Inspection Flow

1. Start with one JSON task in `evals/tasks/`.
2. Confirm the task has an `expected_tool`, structured `input`, and explicit `expectations`.
3. Run the deterministic planner through the normal evaluation path.
4. Inspect the `agent_plan` to see which tool was selected, why it was selected, and which signals matched.
5. Inspect the `trace` to confirm the selected tool was actually called and returned `ok`.
6. Inspect assertion rows to see whether tool selection, tool status, exact values, list containment, and minimum values passed.
7. Inspect the failure category when a task fails.

## What A Passing Task Proves

A passing task proves all of the following for that fixture:

- the planner selected the expected tool;
- the tool call executed successfully;
- the returned structured output matched the task expectations;
- the result kept enough trace data for a reviewer to diagnose the path.

It does not prove broad agent generalization. The project intentionally separates deterministic public proof from optional model-backed planner experiments.

## What To Check In The HTML Report

In `reports/sample-eval-report.html`, inspect:

- `Expected` vs `Selected`;
- `Score`;
- `Category`;
- `Signals`;
- `Assertions`;
- `Planner Rationale`;
- `Tool Call Trace`.

The reviewer evidence summary at the top gives the aggregate proof. Individual task cards give the audit trail.

## Failure Interpretation

Failure categories are intentionally narrow:

- `tool_selection`: the planner chose the wrong tool;
- `tool_execution`: the selected tool failed at runtime;
- `output_assertion`: the selected tool ran, but output checks failed.

The failure catalog demonstrates these categories deliberately so reviewers can see how the lab behaves when something breaks.
