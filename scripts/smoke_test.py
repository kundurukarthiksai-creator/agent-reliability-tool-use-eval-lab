import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.main import app  # noqa: E402


def main():
    client = TestClient(app)
    response = client.get("/health")
    response.raise_for_status()

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "agent-reliability-tool-use-eval-lab"

    print("smoke test passed")


if __name__ == "__main__":
    main()

