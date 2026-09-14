from typing import Any, Literal

from pydantic import BaseModel, Field


class EvaluationTask(BaseModel):
    id: str
    title: str
    description: str
    expected_tool: str
    input: dict[str, Any] = Field(default_factory=dict)
    expectations: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    name: str
    description: str


class ToolResult(BaseModel):
    tool_name: str
    output: dict[str, Any]
    status: Literal["ok", "error"] = "ok"
    error: str | None = None


class AgentPlan(BaseModel):
    selected_tool: str
    confidence: float
    rationale: str
    matched_signals: list[str] = Field(default_factory=list)


class ToolCallTrace(BaseModel):
    tool_name: str
    payload: dict[str, Any]
    status: Literal["ok", "error"]


class AssertionResult(BaseModel):
    name: str
    passed: bool
    detail: str


class TaskRunResult(BaseModel):
    task_id: str
    title: str
    expected_tool: str
    selected_tool: str
    agent_plan: AgentPlan
    trace: list[ToolCallTrace] = Field(default_factory=list)
    tool_result: ToolResult
    assertions: list[AssertionResult]
    score: float
    passed: bool


class EvalSummary(BaseModel):
    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    average_score: float


class EvalReport(BaseModel):
    summary: EvalSummary
    results: list[TaskRunResult]
