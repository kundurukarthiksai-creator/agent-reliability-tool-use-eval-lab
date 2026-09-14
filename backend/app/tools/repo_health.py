import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
REPO_FIXTURE = ROOT / "evals" / "fixtures" / "repos.json"


REQUIRED_SIGNALS = [
    "readme",
    "tests",
    "ci",
    "screenshots",
    "known_limitations",
]


def load_repos() -> dict[str, dict[str, Any]]:
    with REPO_FIXTURE.open("r", encoding="utf-8") as file:
        repos: list[dict[str, Any]] = json.load(file)
    return {repo["name"]: repo for repo in repos}


def repo_health_check(payload: dict[str, Any]) -> dict[str, Any]:
    repo_name = payload.get("repo_name")
    repos = load_repos()
    repo = repos.get(repo_name)
    if repo is None:
        return {
            "repo_name": repo_name,
            "ready_for_profile": False,
            "score": 0,
            "missing": ["repo_not_found"],
            "checks": {},
        }

    checks = {signal: bool(repo.get(signal)) for signal in REQUIRED_SIGNALS}
    missing = [name for name, passed in checks.items() if not passed]
    score = sum(1 for passed in checks.values() if passed)

    return {
        "repo_name": repo_name,
        "ready_for_profile": not missing,
        "score": score,
        "max_score": len(REQUIRED_SIGNALS),
        "missing": missing,
        "checks": checks,
        "summary": repo.get("summary", ""),
    }

