from fastapi import FastAPI
from pydantic import BaseModel


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

