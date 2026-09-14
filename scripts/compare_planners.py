import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.agent import RuleBasedAgent  # noqa: E402
from app.comparison import compare_planners, render_planner_comparison_markdown  # noqa: E402
from app.models import AgentPlan, EvaluationTask, ToolDefinition  # noqa: E402


class AlwaysCourseNotesAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.5,
            rationale="Baseline comparison planner that always chooses course_note_search.",
            matched_signals=["always-course-notes"],
        )


def main() -> None:
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    results = compare_planners(
        planners={
            "rule_based": RuleBasedAgent(),
            "always_course_notes": AlwaysCourseNotesAgent(),
        }
    )

    json_path = reports_dir / "planner-comparison.json"
    markdown_path = reports_dir / "planner-comparison.md"
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
