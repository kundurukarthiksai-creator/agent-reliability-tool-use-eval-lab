import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.runner import run_evaluation  # noqa: E402


def main():
    report = run_evaluation()
    print(json.dumps(report.model_dump(), indent=2))


if __name__ == "__main__":
    main()

