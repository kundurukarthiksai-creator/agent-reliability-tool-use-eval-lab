from fastapi import FastAPI
from pydantic import BaseModel

from app.models import EvalReport, ToolDefinition
from app.registry import build_default_registry
from app.runner import run_evaluation


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
