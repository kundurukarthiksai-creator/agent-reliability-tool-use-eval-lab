import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
NOTES_FIXTURE = ROOT / "evals" / "fixtures" / "course_notes.json"


def load_notes() -> list[dict[str, Any]]:
    with NOTES_FIXTURE.open("r", encoding="utf-8") as file:
        return json.load(file)


def course_note_search(payload: dict[str, Any]) -> dict[str, Any]:
    query = str(payload.get("query", "")).lower().strip()
    if not query:
        return {"query": query, "matches": [], "match_count": 0, "needs_clarification": True}

    terms = [term for term in query.split() if len(term) > 2]
    matches: list[dict[str, Any]] = []

    for note in load_notes():
        haystack = " ".join(
            [
                note.get("title", ""),
                " ".join(note.get("tags", [])),
                note.get("content", ""),
            ]
        ).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            matches.append(
                {
                    "source_id": note["id"],
                    "title": note["title"],
                    "score": score,
                    "snippet": note["content"][:180],
                }
            )

    matches.sort(key=lambda item: item["score"], reverse=True)
    return {
        "query": query,
        "matches": matches[:3],
        "match_count": len(matches),
        "needs_clarification": False,
    }

