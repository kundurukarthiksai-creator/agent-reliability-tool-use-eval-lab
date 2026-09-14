import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_FIXTURE = ROOT / "evals" / "fixtures" / "artifact_consistency.json"


FIX_SUGGESTIONS = {
    "architecture-flow": "Link the architecture flow so reviewers can see how fixtures, planner, tools, scoring, reports, and quality gate connect.",
    "current-eval-count": "Refresh public proof text so task-count claims match the current verified eval report.",
    "current-tool-count": "Refresh public proof text so tool-count claims match the current verified registry coverage.",
    "openapi-contract": "Publish or link the OpenAPI contract for the public API surface.",
    "quality-gate-proof": "Show the strict quality-gate result and the command that reproduces it.",
    "traceability-guide": "Link the traceability guide so one task can be audited from fixture to assertion result.",
}


def load_artifact_consistency_fixture() -> dict[str, Any]:
    with ARTIFACT_FIXTURE.open("r", encoding="utf-8") as file:
        payload: dict[str, Any] = json.load(file)
    return {
        "required_markers": payload["required_markers"],
        "artifacts": {item["id"]: item for item in payload["artifacts"]},
    }


def artifact_consistency_audit(payload: dict[str, Any]) -> dict[str, Any]:
    artifact_id = payload.get("artifact_id")

    if not artifact_id:
        return missing_artifact_result(artifact_id, "artifact_id_required")

    fixture = load_artifact_consistency_fixture()
    artifact = fixture["artifacts"].get(artifact_id)
    if artifact is None:
        return missing_artifact_result(artifact_id, "artifact_not_found")

    required_markers = fixture["required_markers"]
    present_markers = set(artifact.get("markers", []))
    matched_required = [
        marker for marker in required_markers if marker in present_markers
    ]
    missing_required = [
        marker for marker in required_markers if marker not in present_markers
    ]
    stale_markers = artifact.get("stale_markers", [])
    consistency_score = round((len(matched_required) / len(required_markers)) * 100)

    return {
        "artifact_id": artifact_id,
        "consistent": not missing_required and not stale_markers,
        "consistency_score": consistency_score,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "stale_markers": stale_markers,
        "recommended_fixes": [
            FIX_SUGGESTIONS.get(marker, f"Refresh public proof marker: {marker}.")
            for marker in missing_required
        ],
        "summary": artifact.get("summary", ""),
    }


def missing_artifact_result(artifact_id: str | None, missing_key: str) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "consistent": False,
        "consistency_score": 0,
        "matched_required": [],
        "missing_required": [missing_key],
        "stale_markers": [],
        "recommended_fixes": [],
        "summary": "A known artifact id is required before public proof consistency can be audited.",
    }
