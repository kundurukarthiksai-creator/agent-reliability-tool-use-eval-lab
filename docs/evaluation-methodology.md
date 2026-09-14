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

