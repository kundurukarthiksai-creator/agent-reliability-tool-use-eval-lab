import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from app.models import EvalReport, EvalRunMetadata, EvalRunRecord, EvalSummary


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "eval_runs.sqlite3"


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS eval_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            total_tasks INTEGER NOT NULL,
            passed_tasks INTEGER NOT NULL,
            failed_tasks INTEGER NOT NULL,
            average_score REAL NOT NULL,
            report_json TEXT NOT NULL
        )
        """
    )
    connection.commit()


def save_report(report: EvalReport, db_path: Path = DB_PATH) -> EvalRunRecord:
    created_at = datetime.now(UTC).isoformat()
    payload = json.dumps(report.model_dump())

    with connect(db_path) as connection:
        init_db(connection)
        cursor = connection.execute(
            """
            INSERT INTO eval_runs (
                created_at,
                total_tasks,
                passed_tasks,
                failed_tasks,
                average_score,
                report_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                report.summary.total_tasks,
                report.summary.passed_tasks,
                report.summary.failed_tasks,
                report.summary.average_score,
                payload,
            ),
        )
        connection.commit()
        run_id = int(cursor.lastrowid)

    return EvalRunRecord(
        run_id=run_id,
        created_at=created_at,
        summary=report.summary,
        report=report,
    )


def list_runs(db_path: Path = DB_PATH) -> list[EvalRunMetadata]:
    with connect(db_path) as connection:
        init_db(connection)
        rows = connection.execute(
            """
            SELECT
                id,
                created_at,
                total_tasks,
                passed_tasks,
                failed_tasks,
                average_score
            FROM eval_runs
            ORDER BY id DESC
            """
        ).fetchall()

    return [_metadata_from_row(row) for row in rows]


def get_run(run_id: int, db_path: Path = DB_PATH) -> EvalRunRecord | None:
    with connect(db_path) as connection:
        init_db(connection)
        row = connection.execute(
            """
            SELECT
                id,
                created_at,
                total_tasks,
                passed_tasks,
                failed_tasks,
                average_score,
                report_json
            FROM eval_runs
            WHERE id = ?
            """,
            (run_id,),
        ).fetchone()

    if row is None:
        return None

    report = EvalReport.model_validate(json.loads(row["report_json"]))
    return EvalRunRecord(
        run_id=int(row["id"]),
        created_at=str(row["created_at"]),
        summary=_summary_from_row(row),
        report=report,
    )


def _metadata_from_row(row: sqlite3.Row) -> EvalRunMetadata:
    return EvalRunMetadata(
        run_id=int(row["id"]),
        created_at=str(row["created_at"]),
        summary=_summary_from_row(row),
    )


def _summary_from_row(row: sqlite3.Row) -> EvalSummary:
    return EvalSummary(
        total_tasks=int(row["total_tasks"]),
        passed_tasks=int(row["passed_tasks"]),
        failed_tasks=int(row["failed_tasks"]),
        average_score=float(row["average_score"]),
    )
