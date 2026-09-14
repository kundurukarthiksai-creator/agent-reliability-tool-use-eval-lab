import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.agent import RuleBasedAgent  # noqa: E402
from app.comparison import compare_planners, render_planner_comparison_markdown  # noqa: E402
from app.llm_planner import build_openai_planner_from_env  # noqa: E402


def main() -> None:
    openai_planner = build_openai_planner_from_env()
    if openai_planner is None:
        print(
            "OpenAI planner comparison skipped. "
            "Set EVAL_LAB_ENABLE_OPENAI_PLANNER=1 and OPENAI_API_KEY to run it."
        )
        return

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    results = compare_planners(
        planners={
            "rule_based": RuleBasedAgent(),
            "openai_llm": openai_planner,
        }
    )

    json_path = reports_dir / "openai-planner-comparison.json"
    markdown_path = reports_dir / "openai-planner-comparison.md"
    json_path.write_text(
        json.dumps([result.model_dump() for result in results], indent=2),
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_planner_comparison_markdown(results),
        encoding="utf-8",
    )
    print(f"rendered {json_path}")
    print(f"rendered {markdown_path}")


if __name__ == "__main__":
    main()
