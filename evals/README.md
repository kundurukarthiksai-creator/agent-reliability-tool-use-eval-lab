# Evaluation Tasks

This folder contains deterministic evaluation fixtures and tasks.

## Fixtures

- `fixtures/repos.json`: public-proof signals for sample repositories.
- `fixtures/course_notes.json`: small course-note corpus for source-backed retrieval.

## Tasks

Each task is a JSON object with:

- `id`
- `title`
- `description`
- `expected_tool`
- `input`
- `expectations`

The Phase 1 runner executes the expected tool directly, then scores the output. A later agent loop will have to choose the tool itself; the current runner establishes the deterministic baseline first.

