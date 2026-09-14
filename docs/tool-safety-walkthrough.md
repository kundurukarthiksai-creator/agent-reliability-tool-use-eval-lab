# Agent Reliability Eval Lab Tool-Safety Walkthrough

## Purpose

The tool-safety audit checks whether a public tool-use project shows the controls reviewers should expect before trusting agent-driven tool calls.

## Current Proof

- `42/42` deterministic tasks pass.
- `9` local tools are exercised.
- `tool_safety_audit` covers 4 tasks.
- The current MCP Tool Safety Lab fixture passes with a `100` safety score.

## What The Audit Checks

- Tool schemas are documented.
- Permission gates exist.
- Tool-call attempts are audit logged.
- Risky publish-like paths require human approval.
- Write-like demos use dry-run behavior.
- Negative tests cover blocked paths.
- CI runs the safety checks.
- Public-safe limits are stated.

## Task Cases

- `tool-safety-mcp-lab-ready`: confirms the current MCP lab proof package has all required controls.
- `tool-safety-missing-approval`: catches a publish-like path without an approval boundary.
- `tool-safety-missing-audit`: catches missing observability for allowed and blocked tool calls.
- `tool-safety-missing-project-id`: fails closed when the required project identifier is missing.

## How To Inspect

1. Open `reports/sample-eval-report.html`.
2. Search for `tool_safety_audit`.
3. Confirm selected tool equals expected tool for each tool-safety task.
4. Inspect `matched_controls`, `missing_controls`, and `risky_gaps`.
5. Open `reports/task-catalog.html` to see the four task definitions together.

## Honest Limits

This is a deterministic public proof check over local fixtures. It does not certify a real production integration, execute external writes, or prove full MCP server compliance.
