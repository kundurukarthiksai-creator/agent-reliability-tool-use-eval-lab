import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.models import AgentPlan, EvaluationTask, ToolDefinition  # noqa: E402
from app.reporting import render_eval_report_html  # noqa: E402
from app.runner import load_tasks, run_evaluation  # noqa: E402


class DeliberatelyWrongAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.99,
            rationale=(
                "Failure demo: intentionally picks the wrong tool so the report "
                "shows tool-selection and assertion failures."
            ),
            matched_signals=["failure-demo"],
        )


def main() -> None:
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    task = next(task for task in load_tasks() if task.id == "repo-health-ready")
    report = run_evaluation(tasks=[task], agent=DeliberatelyWrongAgent())

    json_path = reports_dir / "sample-failure-report.json"
    html_path = reports_dir / "sample-failure-report.html"

    json_path.write_text(
        json.dumps(report.model_dump(), indent=2),
        encoding="utf-8",
    )
    html_path.write_text(render_eval_report_html(report), encoding="utf-8")
    print(f"rendered {json_path}")
    print(f"rendered {html_path}")


if __name__ == "__main__":
    main()
