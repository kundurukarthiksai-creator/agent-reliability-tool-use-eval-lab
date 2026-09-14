import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.models import EvalReport  # noqa: E402
from app.quality_gate import QualityGateConfig, evaluate_quality_gate  # noqa: E402
from app.runner import run_evaluation  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail when deterministic eval results fall below reliability gates.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional EvalReport JSON file. If omitted, a fresh evaluation is run.",
    )
    parser.add_argument("--output", type=Path, help="Optional path for gate JSON.")
    parser.add_argument("--min-total-tasks", type=int, default=26)
    parser.add_argument("--min-pass-rate", type=float, default=1.0)
    parser.add_argument("--min-average-score", type=float, default=1.0)
    parser.add_argument("--max-failed-tasks", type=int, default=0)
    parser.add_argument(
        "--allow-failure-category",
        action="append",
        dest="allowed_failure_categories",
        choices=["passed", "tool_selection", "tool_execution", "output_assertion"],
        help="Allowed failure category. Repeat to allow more than one.",
    )
    return parser


def load_report(path: Path | None) -> EvalReport:
    if path is None:
        return run_evaluation()
    return EvalReport.model_validate_json(path.read_text(encoding="utf-8"))


def main() -> None:
    args = build_parser().parse_args()
    config = QualityGateConfig(
        min_total_tasks=args.min_total_tasks,
        min_pass_rate=args.min_pass_rate,
        min_average_score=args.min_average_score,
        max_failed_tasks=args.max_failed_tasks,
        allowed_failure_categories=args.allowed_failure_categories or ["passed"],
    )
    result = evaluate_quality_gate(load_report(args.report), config)
    payload = json.dumps(result.model_dump(), indent=2)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{payload}\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(payload)

    if not result.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
