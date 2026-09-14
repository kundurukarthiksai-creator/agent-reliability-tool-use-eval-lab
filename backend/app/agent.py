import json
from dataclasses import dataclass
from typing import Protocol

from app.models import AgentPlan, EvaluationTask, ToolDefinition


SIGNALS_BY_TOOL = {
    "repo_health_check": [
        "repo",
        "github",
        "portfolio",
        "public proof",
        "profile-ready",
        "promoted publicly",
        "promote",
        "readme",
        "ci",
        "wrapper",
    ],
    "course_note_search": [
        "course",
        "learning",
        "resource",
        "notes",
        "mcp",
        "tool interfaces",
        "structured contracts",
        "contracts",
    ],
    "application_tracker_update": [
        "application",
        "tracker",
        "internship",
        "role",
        "company",
        "applied",
        "saved",
        "interview",
        "rejected",
    ],
    "runbook_lookup": [
        "runbook",
        "incident",
        "triage",
        "on-call",
        "oncall",
        "latency",
        "timeout",
        "ci failure",
        "github actions",
        "workflow",
        "database",
        "persistence",
        "saved runs",
        "escalation",
    ],
    "profile_readme_audit": [
        "profile readme",
        "profile",
        "featured project",
        "proof link",
        "proof links",
        "recruiter",
        "headline",
        "learning focus",
        "contact",
    ],
    "role_readiness_audit": [
        "role readiness",
        "readiness",
        "target role",
        "role fit",
        "fit",
        "evidence gap",
        "missing evidence",
        "ai tools",
        "backend internship",
        "cloud platform",
        "portfolio evidence",
    ],
}


class AgentPlanner(Protocol):
    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        """Return a tool-use plan for one evaluation task."""


@dataclass
class RuleBasedAgent:
    name: str = "rule-based-ci-agent"

    def plan(self, task: EvaluationTask, tools: list[ToolDefinition]) -> AgentPlan:
        available = {tool.name for tool in tools}
        task_text = self._task_text(task)
        scored: list[tuple[int, str, list[str]]] = []

        for tool_name, signals in SIGNALS_BY_TOOL.items():
            if tool_name not in available:
                continue
            matches = [signal for signal in signals if signal in task_text]
            scored.append((len(matches), tool_name, matches))

        scored.sort(key=lambda item: (-item[0], item[1]))
        best_score, selected_tool, matches = scored[0] if scored else (0, "", [])

        if not selected_tool:
            selected_tool = sorted(available)[0]
            rationale = "No registered tool signals were available; selected a fallback tool."
            confidence = 0.0
        elif best_score == 0:
            rationale = "No strong task signals matched; selected the first deterministic fallback."
            confidence = 0.2
        else:
            rationale = (
                "Selected the tool with the strongest deterministic signal match "
                "from the task title, description, and input payload."
            )
            confidence = min(0.95, 0.45 + (best_score * 0.12))

        return AgentPlan(
            selected_tool=selected_tool,
            confidence=round(confidence, 2),
            rationale=rationale,
            matched_signals=matches,
        )

    @staticmethod
    def _task_text(task: EvaluationTask) -> str:
        payload = {
            "title": task.title,
            "description": task.description,
            "input": task.input,
        }
        return json.dumps(payload, sort_keys=True).lower()
