import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.comparison import PlannerComparisonResult  # noqa: E402
from app.models import EvalReport, EvalRunRecord, EvaluationTask, TaskCatalogSummary  # noqa: E402
from app.run_comparison import EvalRunComparison  # noqa: E402
from app.run_trends import EvalRunTrend  # noqa: E402


SCHEMAS = {
    "evaluation-task.schema.json": EvaluationTask,
    "eval-report.schema.json": EvalReport,
    "eval-run-record.schema.json": EvalRunRecord,
    "eval-run-comparison.schema.json": EvalRunComparison,
    "eval-run-trend.schema.json": EvalRunTrend,
    "planner-comparison-result.schema.json": PlannerComparisonResult,
    "task-catalog-summary.schema.json": TaskCatalogSummary,
}


def main() -> None:
    schema_dir = ROOT / "docs" / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)

    for filename, model in SCHEMAS.items():
        path = schema_dir / filename
        path.write_text(
            json.dumps(model.model_json_schema(), indent=2),
            encoding="utf-8",
        )
        print(f"exported {path}")


if __name__ == "__main__":
    main()
