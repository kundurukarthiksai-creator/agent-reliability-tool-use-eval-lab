# Evaluation Tasks

This folder contains deterministic evaluation fixtures and tasks.

## Fixtures

- `fixtures/repos.json`: public-proof signals for sample repositories.
- `fixtures/course_notes.json`: small course-note corpus for source-backed retrieval.
- `fixtures/profiles.json`: synthetic profile README readiness signals.
- `fixtures/role_readiness.json`: synthetic target-role and portfolio signal fixtures.
- `fixtures/launch_readiness.json`: synthetic public launch evidence signals.
- `fixtures/artifact_consistency.json`: synthetic public proof artifact markers.

## Tasks

The current focused corpus has 42 tasks, including happy-path checks and adversarial cases for noisy wording, missing required fields, no-match retrieval, unverified repositories, missing repository fixtures, incident runbook lookup, profile README readiness, target-role readiness, public launch readiness, artifact consistency, and tool-safety proof.

Each task is a JSON object with:

- `id`
- `title`
- `description`
- `expected_tool`
- `input`
- `expectations`

The runner asks the deterministic planner to choose a tool from the task title, description, and input payload. The selected tool is then scored against `expected_tool` and the output expectations.

The `expected_tool` field is an answer key for scoring. Planner implementations should not read it when choosing a tool.
