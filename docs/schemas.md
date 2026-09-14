# Schemas

JSON schemas are generated from Pydantic models so tool contracts stay close to the application code.

Regenerate:

```powershell
.\.venv\Scripts\python scripts\export_schemas.py
```

Generated schemas:

- `docs/schemas/evaluation-task.schema.json`
- `docs/schemas/eval-report.schema.json`
- `docs/schemas/eval-run-record.schema.json`
- `docs/schemas/eval-run-comparison.schema.json`
- `docs/schemas/planner-comparison-result.schema.json`

These schemas describe:

- eval task fixture format;
- report output format;
- persisted run record format;
- saved run comparison format;
- planner comparison summary format.
