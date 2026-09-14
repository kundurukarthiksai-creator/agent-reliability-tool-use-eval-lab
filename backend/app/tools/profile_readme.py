import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROFILE_FIXTURE = ROOT / "evals" / "fixtures" / "profiles.json"


REQUIRED_PROFILE_SIGNALS = [
    "headline",
    "featured_project",
    "proof_links",
    "metrics",
    "learning_focus",
    "contact",
]


def load_profiles() -> dict[str, dict[str, Any]]:
    with PROFILE_FIXTURE.open("r", encoding="utf-8") as file:
        profiles: list[dict[str, Any]] = json.load(file)
    return {profile["id"]: profile for profile in profiles}


def profile_readme_audit(payload: dict[str, Any]) -> dict[str, Any]:
    profile_id = payload.get("profile_id")
    target_project = payload.get("target_project")

    if not profile_id:
        return {
            "profile_id": profile_id,
            "target_project": target_project,
            "ready_for_recruiter": False,
            "score": 0,
            "max_score": len(REQUIRED_PROFILE_SIGNALS),
            "featured_project_present": False,
            "missing": ["profile_id_required"],
            "checks": {},
            "summary": "A profile id is required before profile README quality can be audited.",
        }

    profile = load_profiles().get(profile_id)
    if profile is None:
        return {
            "profile_id": profile_id,
            "target_project": target_project,
            "ready_for_recruiter": False,
            "score": 0,
            "max_score": len(REQUIRED_PROFILE_SIGNALS),
            "featured_project_present": False,
            "missing": ["profile_not_found"],
            "checks": {},
            "summary": "Profile fixture was not found.",
        }

    featured_projects = profile.get("featured_projects", [])
    proof_links = profile.get("proof_links", [])
    metrics = profile.get("metrics", [])
    learning_focus = profile.get("learning_focus", [])
    featured_project_present = (
        target_project in featured_projects if target_project else bool(featured_projects)
    )
    checks = {
        "headline": bool(profile.get("headline")),
        "featured_project": featured_project_present,
        "proof_links": bool(proof_links),
        "metrics": bool(metrics),
        "learning_focus": bool(learning_focus),
        "contact": bool(profile.get("contact")),
    }
    missing = [name for name, passed in checks.items() if not passed]

    return {
        "profile_id": profile_id,
        "target_project": target_project,
        "ready_for_recruiter": not missing,
        "score": sum(1 for passed in checks.values() if passed),
        "max_score": len(REQUIRED_PROFILE_SIGNALS),
        "featured_project_present": featured_project_present,
        "missing": missing,
        "checks": checks,
        "summary": profile.get("summary", ""),
    }
