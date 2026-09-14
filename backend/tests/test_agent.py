from app.agent import RuleBasedAgent
from app.models import EvaluationTask
from app.registry import build_default_registry


def test_agent_selects_tool_from_task_text_not_expected_tool():
    task = EvaluationTask(
        id="semantic-selection",
        title="Find relevant learning notes",
        description="A user asks which MCP resource explains structured contracts.",
        expected_tool="repo_health_check",
        input={"query": "MCP structured contracts"},
    )

    plan = RuleBasedAgent().plan(task, build_default_registry().list_tools())

    assert plan.selected_tool == "course_note_search"
    assert "mcp" in plan.matched_signals


def test_agent_selects_application_tracker_for_job_event():
    task = EvaluationTask(
        id="application-event",
        title="Normalize a saved internship application",
        description="A user saved a backend internship role and needs a tracker-ready update.",
        expected_tool="course_note_search",
        input={
            "company": "Northstar Systems",
            "role": "Backend Engineering Intern",
            "event_type": "saved",
        },
    )

    plan = RuleBasedAgent().plan(task, build_default_registry().list_tools())

    assert plan.selected_tool == "application_tracker_update"


def test_agent_selects_runbook_lookup_for_incident_triage():
    task = EvaluationTask(
        id="incident-runbook",
        title="Find the CI failure runbook",
        description="A user needs incident triage steps for a GitHub Actions workflow failure.",
        expected_tool="course_note_search",
        input={"service": "ci", "symptom": "schema export workflow failed"},
    )

    plan = RuleBasedAgent().plan(task, build_default_registry().list_tools())

    assert plan.selected_tool == "runbook_lookup"
    assert "runbook" in plan.matched_signals


def test_agent_selects_profile_readme_audit_for_profile_review():
    task = EvaluationTask(
        id="profile-readme-review",
        title="Audit profile README recruiter readiness",
        description="A user asks if a featured project and proof links are visible enough for recruiters.",
        expected_tool="repo_health_check",
        input={
            "profile_id": "candidate-profile-polished",
            "target_project": "agent-reliability-tool-use-eval-lab",
        },
    )

    plan = RuleBasedAgent().plan(task, build_default_registry().list_tools())

    assert plan.selected_tool == "profile_readme_audit"
    assert "profile readme" in plan.matched_signals


def test_agent_selects_role_readiness_for_target_role_fit():
    task = EvaluationTask(
        id="role-readiness-review",
        title="Audit role readiness for an AI tools backend internship",
        description="A user asks whether portfolio evidence fits a target role and wants missing evidence gaps called out.",
        expected_tool="repo_health_check",
        input={
            "role_id": "ai-tools-backend-internship",
            "profile_id": "eval-lab-portfolio",
        },
    )

    plan = RuleBasedAgent().plan(task, build_default_registry().list_tools())

    assert plan.selected_tool == "role_readiness_audit"
    assert "role readiness" in plan.matched_signals
