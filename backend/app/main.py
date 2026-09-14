from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.comparison import (
    PlannerComparisonResult,
    compare_planners,
    render_planner_comparison_html,
)
from app.models import EvalReport, EvalRunMetadata, EvalRunRecord, ToolDefinition
from app.reporting import render_eval_report_html, render_runs_index_html
from app.registry import build_default_registry
from app.run_comparison import (
    EvalRunComparison,
    compare_eval_runs,
    render_run_comparison_html,
)
from app.runner import run_evaluation
from app.storage import get_latest_run_pair, get_run, list_runs, save_report


class HealthResponse(BaseModel):
    status: str
    service: str
    phase: str


app = FastAPI(
    title="Agent Reliability and Tool-Use Eval Lab",
    version="0.1.0",
    description="Evaluation lab for deterministic tool-use agent tasks.",
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="agent-reliability-tool-use-eval-lab",
        phase="phase-0-scaffold",
    )


@app.get("/tools", response_model=list[ToolDefinition])
async def tools() -> list[ToolDefinition]:
    return build_default_registry().list_tools()


@app.get("/planners/compare", response_model=list[PlannerComparisonResult])
async def compare_default_planners() -> list[PlannerComparisonResult]:
    return compare_planners()


@app.get("/planners/compare.html", response_class=HTMLResponse)
async def compare_default_planners_html() -> HTMLResponse:
    return HTMLResponse(render_planner_comparison_html(compare_planners()))


@app.post("/eval/run", response_model=EvalReport)
async def run_eval() -> EvalReport:
    return run_evaluation()


@app.post("/eval/runs", response_model=EvalRunRecord)
async def create_eval_run() -> EvalRunRecord:
    return save_report(run_evaluation())


@app.get("/eval/runs", response_model=list[EvalRunMetadata])
async def eval_runs() -> list[EvalRunMetadata]:
    return list_runs()


@app.get("/eval/runs.html", response_class=HTMLResponse)
async def eval_runs_html() -> HTMLResponse:
    return HTMLResponse(render_runs_index_html(list_runs()))


@app.get("/eval/runs/compare", response_model=EvalRunComparison)
async def eval_runs_compare() -> EvalRunComparison:
    run_pair = get_latest_run_pair()
    if run_pair is None:
        raise HTTPException(
            status_code=404,
            detail="At least two saved evaluation runs are required.",
        )
    previous, current = run_pair
    return compare_eval_runs(previous, current)


@app.get("/eval/runs/compare.html", response_class=HTMLResponse)
async def eval_runs_compare_html() -> HTMLResponse:
    run_pair = get_latest_run_pair()
    if run_pair is None:
        raise HTTPException(
            status_code=404,
            detail="At least two saved evaluation runs are required.",
        )
    previous, current = run_pair
    comparison = compare_eval_runs(previous, current)
    return HTMLResponse(render_run_comparison_html(comparison))


@app.get("/eval/runs/{run_id}", response_model=EvalRunRecord)
async def eval_run(run_id: int) -> EvalRunRecord:
    record = get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return record


@app.get("/reports/latest.html", response_class=HTMLResponse)
async def latest_html_report() -> HTMLResponse:
    return HTMLResponse(render_eval_report_html(run_evaluation()))
