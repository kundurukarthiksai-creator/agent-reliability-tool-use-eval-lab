import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ROLE_FIXTURE = ROOT / "evals" / "fixtures" / "role_readiness.json"


EVIDENCE_SUGGESTIONS = {
    "agent-evaluation": "Show eval tasks, scoring, traces, and failure categories.",
    "api-design": "Show route contracts, schemas, and clear API docs.",
    "case-study": "Add a short reviewer guide explaining proof and limits.",
    "ci": "Show deterministic CI checks that run without secrets.",
    "cloud-deployment": "Add a public no-cost deployment or document the deployment path.",
    "fastapi": "Show FastAPI routes and local run instructions.",
    "observability": "Show logs, traces, dashboards, or regression views.",
    "public-demo": "Link a public demo that works without credentials.",
    "python": "Show tested Python code, not just notebooks or snippets.",
    "tool-use-traces": "Expose selected tools, inputs, and trace status in reports.",
}


def load_role_readiness_fixture() -> dict[str, dict[str, dict[str, Any]]]:
    with ROLE_FIXTURE.open("r", encoding="utf-8") as file:
        payload: dict[str, list[dict[str, Any]]] = json.load(file)
    return {
        "roles": {item["id"]: item for item in payload["roles"]},
        "profiles": {item["id"]: item for item in payload["profiles"]},
    }


def role_readiness_audit(payload: dict[str, Any]) -> dict[str, Any]:
    role_id = payload.get("role_id")
    profile_id = payload.get("profile_id")

    if not role_id:
        return missing_input_result(role_id, profile_id, "role_id_required")
    if not profile_id:
        return missing_input_result(role_id, profile_id, "profile_id_required")

    fixture = load_role_readiness_fixture()
    role = fixture["roles"].get(role_id)
    profile = fixture["profiles"].get(profile_id)

    if role is None:
        return missing_input_result(role_id, profile_id, "role_not_found")
    if profile is None:
        return missing_input_result(role_id, profile_id, "profile_not_found")

    profile_signals = set(profile.get("signals", []))
    required_signals = role.get("required_signals", [])
    preferred_signals = role.get("preferred_signals", [])
    matched_required = [
        signal for signal in required_signals if signal in profile_signals
    ]
    missing_required = [
        signal for signal in required_signals if signal not in profile_signals
    ]
    matched_preferred = [
        signal for signal in preferred_signals if signal in profile_signals
    ]
    missing_preferred = [
        signal for signal in preferred_signals if signal not in profile_signals
    ]

    required_score = (
        len(matched_required) / len(required_signals) if required_signals else 1.0
    )
    preferred_score = (
        len(matched_preferred) / len(preferred_signals) if preferred_signals else 1.0
    )
    readiness_score = round((required_score * 75) + (preferred_score * 25))

    return {
        "role_id": role_id,
        "profile_id": profile_id,
        "ready_for_role": not missing_required,
        "readiness_score": readiness_score,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "recommended_evidence": [
            EVIDENCE_SUGGESTIONS.get(signal, f"Add evidence for {signal}.")
            for signal in missing_required
        ],
        "summary": role.get("summary", ""),
        "profile_summary": profile.get("summary", ""),
    }


def missing_input_result(
    role_id: str | None,
    profile_id: str | None,
    missing_key: str,
) -> dict[str, Any]:
    return {
        "role_id": role_id,
        "profile_id": profile_id,
        "ready_for_role": False,
        "readiness_score": 0,
        "matched_required": [],
        "missing_required": [missing_key],
        "matched_preferred": [],
        "missing_preferred": [],
        "recommended_evidence": [],
        "summary": "A role id and profile id are required before readiness can be audited.",
        "profile_summary": "",
    }
