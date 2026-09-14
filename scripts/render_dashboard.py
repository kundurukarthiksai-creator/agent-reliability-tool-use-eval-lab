import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.reporting import render_dashboard_html  # noqa: E402
from app.registry import build_default_registry  # noqa: E402
from app.runner import run_evaluation  # noqa: E402


def main() -> None:
    output_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else ROOT / "reports" / "dashboard.html"
    )
    registry = build_default_registry()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_dashboard_html(
            report=run_evaluation(registry=registry),
            tools=registry.list_tools(),
            runs=[],
        ),
        encoding="utf-8",
    )
    print(f"rendered {output_path}")


if __name__ == "__main__":
    main()
