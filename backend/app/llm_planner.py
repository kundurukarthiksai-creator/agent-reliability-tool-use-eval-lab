import json
import os
from dataclasses import dataclass
from typing import Any, Protocol
from urllib import request

from app.models import AgentPlan, EvaluationTask, ToolDefinition


class OpenAIPlannerError(RuntimeError):
    pass


class ResponsesTransport(Protocol):
    def create_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a Responses API payload and return the decoded JSON response."""


@dataclass
class UrlLibResponsesTransport:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    timeout_seconds: float = 30.0

    def create_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        endpoint = f"{self.base_url.rstrip('/')}/responses"
        encoded = json.dumps(payload).encode("utf-8")
        api_request = request.Request(
            endpoint,
            data=encoded,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(api_request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))


@dataclass
class OpenAIPlanner:
    model: str
    transport: ResponsesTransport

    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        tool_names = [tool.name for tool in tools]
        if not tool_names:
            raise OpenAIPlannerError("No tools are available for planner selection.")

        response = self.transport.create_response(
            _build_responses_payload(task=task, tools=tools, model=self.model)
        )
        payload = _extract_json_payload(response)
        selected_tool = str(payload.get("selected_tool", "")).strip()
        if selected_tool not in tool_names:
            raise OpenAIPlannerError(
                f"Planner selected unknown tool '{selected_tool}'. "
                f"Available tools: {', '.join(tool_names)}"
            )

        confidence = float(payload.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))
        rationale = str(payload.get("rationale", "")).strip()

        return AgentPlan(
            selected_tool=selected_tool,
            confidence=round(confidence, 2),
            rationale=rationale or "OpenAI planner returned a structured tool choice.",
            matched_signals=["openai-structured-output"],
        )


def build_openai_planner_from_env() -> OpenAIPlanner | None:
    if os.getenv("EVAL_LAB_ENABLE_OPENAI_PLANNER") != "1":
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIPlannerError(
            "OPENAI_API_KEY is required when EVAL_LAB_ENABLE_OPENAI_PLANNER=1."
        )

    model = os.getenv("EVAL_LAB_OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAIPlanner(
        model=model,
        transport=UrlLibResponsesTransport(api_key=api_key, base_url=base_url),
    )


def _build_responses_payload(
    task: EvaluationTask,
    tools: list[ToolDefinition],
    model: str,
) -> dict[str, Any]:
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [
        {"name": tool.name, "description": tool.description} for tool in tools
    ]
    return {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": (
                    "Choose exactly one registered tool for the evaluation task. "
                    "Use only the provided tool names. Return a concise rationale."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "task": {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "input": task.input,
                        },
                        "tools": tool_descriptions,
                    },
                    sort_keys=True,
                ),
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "tool_selection_plan",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "selected_tool": {"type": "string", "enum": tool_names},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "rationale": {"type": "string"},
                    },
                    "required": ["selected_tool", "confidence", "rationale"],
                },
            }
        },
    }


def _extract_json_payload(response: dict[str, Any]) -> dict[str, Any]:
    output_text = response.get("output_text")
    if isinstance(output_text, str):
        return _loads_object(output_text)

    for item in response.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str):
                return _loads_object(text)

    raise OpenAIPlannerError("OpenAI response did not contain JSON output text.")


def _loads_object(value: str) -> dict[str, Any]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        raise OpenAIPlannerError("OpenAI response was not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise OpenAIPlannerError("OpenAI response JSON must be an object.")
    return payload
