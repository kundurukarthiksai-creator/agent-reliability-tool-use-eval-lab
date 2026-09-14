# Technical Steering

## Stack

- Python
- FastAPI
- Pydantic
- pytest
- JSON eval fixtures first
- SQLite only when persistence is needed

## Architecture Rules

- Keep `backend/app/runner.py` responsible for orchestration.
- Keep tool implementations small and deterministic under `backend/app/tools`.
- Keep scoring logic in `backend/app/scoring.py`.
- Keep planner implementations separate from the runner.
- Keep fixtures under `evals/fixtures` and tasks under `evals/tasks`.

## Agent Rules

- The default planner must be deterministic.
- LLM planners must be optional and disabled by default.
- LLM planners must produce the same report schema as deterministic planners.
- Never require external credentials for unit tests, smoke tests, or CI.

## Data Rules

- Do not store real private job applications, resume material, or employer-confidential data in public fixtures.
- Use synthetic or public-safe data in sample reports.
- Treat Amazon internship details as private context unless explicitly converted into public-safe wording.
