from app.comparison import (
    compare_planners,
    render_planner_comparison_html,
    render_planner_comparison_markdown,
)
from app.models import AgentPlan, EvaluationTask, ToolDefinition


class AlwaysCourseNotesAgent:
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        return AgentPlan(
            selected_tool="course_note_search",
            confidence=0.5,
            rationale="Test planner always chooses course_note_search.",
            matched_signals=["test-comparison"],
        )


def test_compare_planners_reports_good_and_bad_planner_results():
    results = compare_planners(planners={"always_course_notes": AlwaysCourseNotesAgent()})

    result = results[0]

    assert result.planner_name == "always_course_notes"
    assert result.total_tasks == 18
    assert result.failed_tasks > 0
    assert result.failure_categories["tool_selection"] > 0


def test_render_planner_comparison_markdown_contains_table():
    results = compare_planners(planners={"always_course_notes": AlwaysCourseNotesAgent()})

    markdown = render_planner_comparison_markdown(results)

    assert "# Planner Comparison" in markdown
    assert "| Planner | Total | Passed | Failed | Avg Score | Failure Categories |" in markdown
    assert "always_course_notes" in markdown


def test_render_planner_comparison_html_contains_table():
    results = compare_planners(planners={"always_course_notes": AlwaysCourseNotesAgent()})

    html = render_planner_comparison_html(results)

    assert "Planner Comparison" in html
    assert "always_course_notes" in html
    assert "Failure Categories" in html
