import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
LAUNCH_FIXTURE = ROOT / "evals" / "fixtures" / "launch_readiness.json"


EVIDENCE_SUGGESTIONS = {
    "ci-quality-gate": "Show a CI-backed quality gate with the same command reviewers can run locally.",
    "eval-report": "Link a current eval report with task-level traces and scores.",
    "failure-catalog": "Show deliberate failure modes so reviewers can see what the system catches.",
    "honest-limits": "Document what is deterministic, what is optional, and what is not claimed.",
    "no-key-static-demo": "Publish a static demo that works without API keys or account setup.",
    "openapi-contract": "Export and link an OpenAPI contract for the public API surface.",
    "readme-inspection-path": "Put a short reviewer inspection path near the top of the README.",
    "task-catalog": "Expose the task catalog and tool coverage so the corpus is auditable.",
}


def load_launch_readiness_fixture() -> dict[str, Any]:
    with LAUNCH_FIXTURE.open("r", encoding="utf-8") as file:
        payload: dict[str, Any] = json.load(file)
    return {
        "required_signals": payload["required_signals"],
        "projects": {item["id"]: item for item in payload["projects"]},
    }


def launch_readiness_audit(payload: dict[str, Any]) -> dict[str, Any]:
    project_id = payload.get("project_id")

    if not project_id:
        return missing_project_result(project_id, "project_id_required")

    fixture = load_launch_readiness_fixture()
    project = fixture["projects"].get(project_id)
    if project is None:
        return missing_project_result(project_id, "project_not_found")

    required_signals = fixture["required_signals"]
    project_signals = set(project.get("signals", []))
    matched_required = [
        signal for signal in required_signals if signal in project_signals
    ]
    missing_required = [
        signal for signal in required_signals if signal not in project_signals
    ]
    readiness_score = round((len(matched_required) / len(required_signals)) * 100)

    return {
        "project_id": project_id,
        "launch_ready": not missing_required,
        "readiness_score": readiness_score,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "recommended_evidence": [
            EVIDENCE_SUGGESTIONS.get(signal, f"Add public launch evidence for {signal}.")
            for signal in missing_required
        ],
        "summary": project.get("summary", ""),
    }


def missing_project_result(project_id: str | None, missing_key: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "launch_ready": False,
        "readiness_score": 0,
        "matched_required": [],
        "missing_required": [missing_key],
        "recommended_evidence": [],
        "summary": "A known project id is required before launch readiness can be audited.",
    }
