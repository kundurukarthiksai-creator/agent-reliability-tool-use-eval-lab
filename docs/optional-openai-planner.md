# Optional OpenAI Planner

The default evaluation path is deterministic and does not call any external model.

An optional OpenAI-backed planner adapter exists for manual experiments where you want
to compare a model-selected tool plan against the CI-safe rule-based planner.

## Why This Is Optional

- CI should remain reproducible without API keys.
- Public sample reports should remain deterministic.
- Model-backed planner behavior can change across time, model versions, prompts, and
  account settings.
- External model calls may cost money.

## Environment Variables

```powershell
$env:EVAL_LAB_ENABLE_OPENAI_PLANNER = "1"
$env:OPENAI_API_KEY = "<your-api-key>"
$env:EVAL_LAB_OPENAI_MODEL = "gpt-4o-mini"
```

`EVAL_LAB_OPENAI_MODEL` is optional. If omitted, the script uses `gpt-4o-mini`.

## Run

```powershell
.\.venv\Scripts\python scripts\compare_openai_planner.py
```

When disabled, the script exits without creating reports.

When enabled, it writes:

- `reports/openai-planner-comparison.json`
- `reports/openai-planner-comparison.md`

Those generated files are intentionally not required by CI.

## Contract

The adapter asks the model to return structured JSON with:

- `selected_tool`
- `confidence`
- `rationale`

The selected tool must be one of the registered local tool names. Unknown tools are
rejected before evaluation.

Reference: OpenAI Structured Outputs documentation:

https://platform.openai.com/docs/guides/structured-outputs
