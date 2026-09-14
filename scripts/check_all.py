import subprocess
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


COMMANDS = [
    ("tests", [sys.executable, "-m", "pytest", "backend/tests", "-q"], False),
    ("smoke", [sys.executable, "scripts/smoke_test.py"], False),
    ("eval-json", [sys.executable, "scripts/run_eval.py"], True),
    (
        "sample-json",
        [sys.executable, "scripts/run_eval.py", "reports/sample-eval-report.json"],
        False,
    ),
    ("dashboard", [sys.executable, "scripts/render_dashboard.py"], False),
    ("task-catalog", [sys.executable, "scripts/render_task_catalog.py"], False),
    ("html-report", [sys.executable, "scripts/render_report.py"], False),
    ("failure-demo", [sys.executable, "scripts/render_failure_demo.py"], False),
    ("failure-catalog", [sys.executable, "scripts/render_failure_catalog.py"], False),
    ("planner-comparison", [sys.executable, "scripts/compare_planners.py"], False),
    ("run-comparison-demo", [sys.executable, "scripts/render_run_comparison_demo.py"], False),
    ("run-trends-demo", [sys.executable, "scripts/render_run_trends_demo.py"], False),
    ("schemas", [sys.executable, "scripts/export_schemas.py"], False),
]


def main() -> None:
    for name, command, summarize_json in COMMANDS:
        print(f"\n== {name} ==", flush=True)
        if summarize_json:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            summary = payload["summary"]
            print(
                "total={total_tasks} passed={passed_tasks} "
                "failed={failed_tasks} average={average_score}".format(**summary),
                flush=True,
            )
        else:
            subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
