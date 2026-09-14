from app.registry import build_default_registry


def test_default_registry_contains_mvp_tools():
    registry = build_default_registry()

    tool_names = {tool.name for tool in registry.list_tools()}

    assert tool_names == {
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
        "runbook_lookup",
        "profile_readme_audit",
        "role_readiness_audit",
        "launch_readiness_audit",
        "artifact_consistency_audit",
        "tool_safety_audit",
    }
