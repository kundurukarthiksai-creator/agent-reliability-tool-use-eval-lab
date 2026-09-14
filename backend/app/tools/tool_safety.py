import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TOOL_SAFETY_FIXTURE = ROOT / "evals" / "fixtures" / "tool_safety.json"


FIX_SUGGESTIONS = {
    "schema": "Document every callable tool with a stable input/output schema.",
    "permission-gate": "Show that each tool declares and enforces required permissions.",
    "audit-log": "Record every allowed and blocked tool-call attempt in an audit log.",
    "approval-gate": "Require explicit human approval for risky or publish-like actions.",
    "dry-run": "Keep write-like demos in dry-run mode unless a real approval path exists.",
    "negative-tests": "Test blocked paths, not only happy-path tool calls.",
    "ci": "Run the safety test suite in CI so the proof stays current.",
    "public-safe-limits": "State public-safe limits clearly and avoid private system claims.",
}


def load_tool_safety_fixture() -> dict[str, Any]:
    with TOOL_SAFETY_FIXTURE.open("r", encoding="utf-8") as file:
        payload: dict[str, Any] = json.load(file)
    return {
        "required_controls": payload["required_controls"],
        "projects": {item["id"]: item for item in payload["projects"]},
    }


def tool_safety_audit(payload: dict[str, Any]) -> dict[str, Any]:
    project_id = payload.get("project_id")

    if not project_id:
        return missing_project_result(project_id, "project_id_required")

    fixture = load_tool_safety_fixture()
    project = fixture["projects"].get(project_id)
    if project is None:
        return missing_project_result(project_id, "project_not_found")

    required_controls = fixture["required_controls"]
    present_controls = set(project.get("controls", []))
    matched_controls = [
        control for control in required_controls if control in present_controls
    ]
    missing_controls = [
        control for control in required_controls if control not in present_controls
    ]
    safety_score = round((len(matched_controls) / len(required_controls)) * 100)

    return {
        "project_id": project_id,
        "safety_ready": not missing_controls and not project.get("risky_gaps", []),
        "safety_score": safety_score,
        "matched_controls": matched_controls,
        "missing_controls": missing_controls,
        "risky_gaps": project.get("risky_gaps", []),
        "recommended_fixes": [
            FIX_SUGGESTIONS.get(control, f"Add missing tool-safety control: {control}.")
            for control in missing_controls
        ],
        "summary": project.get("summary", ""),
    }


def missing_project_result(project_id: str | None, missing_key: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "safety_ready": False,
        "safety_score": 0,
        "matched_controls": [],
        "missing_controls": [missing_key],
        "risky_gaps": [],
        "recommended_fixes": [],
        "summary": "A known project id is required before tool-safety proof can be audited.",
    }
