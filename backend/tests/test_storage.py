from app.runner import run_evaluation
from app.storage import get_run, list_runs, save_report


def test_save_list_and_get_eval_run(tmp_path):
    db_path = tmp_path / "runs.sqlite3"
    report = run_evaluation()

    saved = save_report(report, db_path=db_path)
    runs = list_runs(db_path=db_path)
    loaded = get_run(saved.run_id, db_path=db_path)

    assert saved.run_id == 1
    assert runs[0].run_id == saved.run_id
    assert runs[0].summary.total_tasks == 10
    assert loaded is not None
    assert loaded.report.summary.failed_tasks == 0


def test_get_run_returns_none_for_missing_run(tmp_path):
    assert get_run(999, db_path=tmp_path / "runs.sqlite3") is None
