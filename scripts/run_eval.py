import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.runner import run_evaluation  # noqa: E402


def main():
    report = run_evaluation()
    payload = json.dumps(report.model_dump(), indent=2)
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"{payload}\n", encoding="utf-8")
        print(f"wrote {output_path}")
        return
    print(payload)


if __name__ == "__main__":
    main()
