import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.models import EvalRunMetadata, EvalSummary  # noqa: E402
from app.run_trends import build_run_trend, render_run_trend_html  # noqa: E402


def main() -> None:
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    trend = build_run_trend(
        [
            _metadata(1, "2026-09-14T00:00:00+00:00", 28, 2, 0.9333),
            _metadata(2, "2026-09-14T01:00:00+00:00", 29, 1, 0.9667),
            _metadata(3, "2026-09-14T02:00:00+00:00", 30, 0, 1.0),
        ]
    )

    json_path = reports_dir / "run-trends-demo.json"
    html_path = reports_dir / "run-trends-demo.html"
    json_path.write_text(
        json.dumps(trend.model_dump(), indent=2),
        encoding="utf-8",
    )
    html_path.write_text(render_run_trend_html(trend), encoding="utf-8")
    print(f"rendered {json_path}")
    print(f"rendered {html_path}")


def _metadata(
    run_id: int,
    created_at: str,
    passed_tasks: int,
    failed_tasks: int,
    average_score: float,
) -> EvalRunMetadata:
    return EvalRunMetadata(
        run_id=run_id,
        created_at=created_at,
        summary=EvalSummary(
            total_tasks=passed_tasks + failed_tasks,
            passed_tasks=passed_tasks,
            failed_tasks=failed_tasks,
            average_score=average_score,
        ),
    )


if __name__ == "__main__":
    main()
