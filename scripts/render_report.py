import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.reporting import render_eval_report_html  # noqa: E402
from app.runner import run_evaluation  # noqa: E402


def main() -> None:
    output_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else ROOT / "reports" / "sample-eval-report.html"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_eval_report_html(run_evaluation()),
        encoding="utf-8",
    )
    print(f"rendered {output_path}")


if __name__ == "__main__":
    main()
