from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.models import EvalReport, EvalRunMetadata, EvalRunRecord, ToolDefinition
from app.reporting import render_eval_report_html
from app.registry import build_default_registry
from app.runner import run_evaluation
from app.storage import get_run, list_runs, save_report


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


@app.post("/eval/run", response_model=EvalReport)
async def run_eval() -> EvalReport:
    return run_evaluation()


@app.post("/eval/runs", response_model=EvalRunRecord)
async def create_eval_run() -> EvalRunRecord:
    return save_report(run_evaluation())


@app.get("/eval/runs", response_model=list[EvalRunMetadata])
async def eval_runs() -> list[EvalRunMetadata]:
    return list_runs()


@app.get("/eval/runs/{run_id}", response_model=EvalRunRecord)
async def eval_run(run_id: int) -> EvalRunRecord:
    record = get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return record


@app.get("/reports/latest.html", response_class=HTMLResponse)
async def latest_html_report() -> HTMLResponse:
    return HTMLResponse(render_eval_report_html(run_evaluation()))
