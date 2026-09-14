from typing import Any


REQUIRED_FIELDS = ["company", "role", "event_type"]


STATUS_BY_EVENT = {
    "found": "prospect",
    "saved": "saved",
    "applied": "applied",
    "interview": "interviewing",
    "rejected": "closed",
}


def application_tracker_update(payload: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if not payload.get(field)]
    if missing:
        return {
            "needs_clarification": True,
            "missing_fields": missing,
            "normalized": None,
        }

    event_type = str(payload["event_type"]).lower().strip()
    status = STATUS_BY_EVENT.get(event_type, "needs_review")
    company = str(payload["company"]).strip()
    role = str(payload["role"]).strip()

    return {
        "needs_clarification": False,
        "missing_fields": [],
        "normalized": {
            "company": company,
            "role": role,
            "status": status,
            "source": payload.get("source", "manual"),
            "next_action": payload.get("next_action", "review"),
            "notes": payload.get("notes", ""),
        },
    }

