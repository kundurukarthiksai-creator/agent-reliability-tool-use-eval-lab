import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNBOOK_FIXTURE = ROOT / "evals" / "fixtures" / "runbooks.json"


def load_runbooks() -> list[dict[str, Any]]:
    with RUNBOOK_FIXTURE.open("r", encoding="utf-8") as file:
        return json.load(file)


def runbook_lookup(payload: dict[str, Any]) -> dict[str, Any]:
    service = str(payload.get("service", "")).lower().strip()
    symptom = str(payload.get("symptom", "")).lower().strip()
    query = " ".join(part for part in [service, symptom] if part)
    if not query:
        return {
            "query": "",
            "matches": [],
            "match_count": 0,
            "needs_clarification": True,
        }

    matches: list[dict[str, Any]] = []
    query_terms = [term for term in query.replace("-", " ").split() if len(term) > 2]

    for runbook in load_runbooks():
        haystack = " ".join(
            [
                runbook["service"],
                runbook["title"],
                runbook["severity"],
                " ".join(runbook["symptoms"]),
                " ".join(runbook["steps"]),
                runbook["escalation"],
            ]
        ).lower()
        score = sum(1 for term in query_terms if term in haystack)
        if service and service == runbook["service"]:
            score += 3
        if score:
            matches.append(
                {
                    "runbook_id": runbook["id"],
                    "service": runbook["service"],
                    "title": runbook["title"],
                    "severity": runbook["severity"],
                    "score": score,
                    "steps": runbook["steps"],
                    "escalation": runbook["escalation"],
                }
            )

    matches.sort(key=lambda item: (-item["score"], item["runbook_id"]))
    return {
        "query": query,
        "matches": matches[:3],
        "match_count": len(matches),
        "needs_clarification": False,
    }
