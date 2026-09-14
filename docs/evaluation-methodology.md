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
