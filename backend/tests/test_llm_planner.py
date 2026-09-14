import pytest

from app.llm_planner import (
    OpenAIPlanner,
    OpenAIPlannerError,
    build_openai_planner_from_env,
)
from app.runner import load_tasks
from app.registry import build_default_registry


class FakeResponsesTransport:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.payload = {}

    def create_response(self, payload):
        self.payload = payload
        return {"output_text": self.output_text}


def test_openai_planner_builds_structured_payload_and_parses_plan():
    transport = FakeResponsesTransport(
        '{"selected_tool":"repo_health_check","confidence":0.84,'
        '"rationale":"The task asks about repo readiness."}'
    )
    planner = OpenAIPlanner(model="test-model", transport=transport)
    task = load_tasks()[0]
    tools = build_default_registry().list_tools()

    plan = planner.plan(task, tools)

    assert plan.selected_tool == "repo_health_check"
    assert plan.confidence == 0.84
    assert plan.matched_signals == ["openai-structured-output"]
    assert transport.payload["model"] == "test-model"
    schema = transport.payload["text"]["format"]["schema"]
    assert schema["properties"]["selected_tool"]["enum"] == [
        "repo_health_check",
        "course_note_search",
        "application_tracker_update",
        "runbook_lookup",
    ]


def test_openai_planner_rejects_unknown_tool():
    transport = FakeResponsesTransport(
        '{"selected_tool":"unknown_tool","confidence":0.9,"rationale":"Bad choice."}'
    )
    planner = OpenAIPlanner(model="test-model", transport=transport)

    with pytest.raises(OpenAIPlannerError, match="unknown tool"):
        planner.plan(load_tasks()[0], build_default_registry().list_tools())


def test_openai_planner_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("EVAL_LAB_ENABLE_OPENAI_PLANNER", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert build_openai_planner_from_env() is None


def test_openai_planner_requires_api_key_when_enabled(monkeypatch):
    monkeypatch.setenv("EVAL_LAB_ENABLE_OPENAI_PLANNER", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(OpenAIPlannerError, match="OPENAI_API_KEY"):
        build_openai_planner_from_env()
