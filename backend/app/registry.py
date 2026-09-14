from collections.abc import Callable
from typing import Any

from app.models import ToolDefinition
from app.tools.application_tracker import application_tracker_update
from app.tools.course_notes import course_note_search
from app.tools.repo_health import repo_health_check


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolDefinition, ToolHandler]] = {}

    def register(
        self,
        name: str,
        description: str,
        handler: ToolHandler,
    ) -> None:
        self._tools[name] = (ToolDefinition(name=name, description=description), handler)

    def list_tools(self) -> list[ToolDefinition]:
        return [definition for definition, _ in self._tools.values()]

    def run(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            available = ", ".join(sorted(self._tools))
            raise KeyError(f"Unknown tool '{name}'. Available tools: {available}")
        _, handler = self._tools[name]
        return handler(payload)


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        "repo_health_check",
        "Checks whether a repo has basic public-proof signals.",
        repo_health_check,
    )
    registry.register(
        "course_note_search",
        "Searches curated course notes and returns source-backed snippets.",
        course_note_search,
    )
    registry.register(
        "application_tracker_update",
        "Normalizes a job-application event into tracker-ready fields.",
        application_tracker_update,
    )
    return registry

