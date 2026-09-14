import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.models import EvalRunRecord, EvalSummary  # noqa: E402
from app.run_comparison import compare_eval_runs, render_run_comparison_html  # noqa: E402
from app.runner import run_evaluation  # noqa: E402


def main() -> None:
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    previous_report = run_evaluation().model_copy(deep=True)
    previous_result = previous_report.results[0]
    previous_result.passed = False
    previous_result.score = 0.0
    previous_result.failure_category = "output_assertion"
    previous_report.summary = EvalSummary(
        total_tasks=len(previous_report.results),
        passed_tasks=sum(1 for result in previous_report.results if result.passed),
        failed_tasks=sum(1 for result in previous_report.results if not result.passed),
        average_score=round(
            sum(result.score for result in previous_report.results)
            / len(previous_report.results),
            4,
        ),
    )

    current_report = run_evaluation()
    previous = EvalRunRecord(
        run_id=1,
        created_at="2026-09-14T00:00:00+00:00",
        summary=previous_report.summary,
        report=previous_report,
    )
    current = EvalRunRecord(
        run_id=2,
        created_at="2026-09-14T01:00:00+00:00",
        summary=current_report.summary,
        report=current_report,
    )
    comparison = compare_eval_runs(previous, current)

    json_path = reports_dir / "run-comparison-demo.json"
    html_path = reports_dir / "run-comparison-demo.html"
    json_path.write_text(
        json.dumps(comparison.model_dump(), indent=2),
        encoding="utf-8",
    )
    html_path.write_text(
        render_run_comparison_html(comparison),
        encoding="utf-8",
    )
    print(f"rendered {json_path}")
    print(f"rendered {html_path}")


if __name__ == "__main__":
    main()
