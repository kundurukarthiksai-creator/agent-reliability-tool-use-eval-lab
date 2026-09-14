from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field

from app.models import EvalReport, EvalSummary


FailureCategory = Literal[
    "passed",
    "tool_selection",
    "tool_execution",
    "output_assertion",
]


class QualityGateConfig(BaseModel):
    min_total_tasks: int = 38
    min_pass_rate: float = 1.0
    min_average_score: float = 1.0
    max_failed_tasks: int = 0
    allowed_failure_categories: list[FailureCategory] = Field(
        default_factory=lambda: ["passed"],
    )


class QualityGateCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class QualityGateResult(BaseModel):
    passed: bool
    config: QualityGateConfig
    summary: EvalSummary
    pass_rate: float
    failure_category_counts: dict[str, int]
    failed_task_ids: list[str]
    checks: list[QualityGateCheck]


def evaluate_quality_gate(
    report: EvalReport,
    config: QualityGateConfig | None = None,
) -> QualityGateResult:
    selected_config = config if config is not None else QualityGateConfig()
    summary = report.summary
    pass_rate = (
        summary.passed_tasks / summary.total_tasks if summary.total_tasks else 0.0
    )
    category_counts = Counter(result.failure_category for result in report.results)
    failed_task_ids = [result.task_id for result in report.results if not result.passed]
    disallowed_categories = sorted(
        category
        for category in category_counts
        if category not in selected_config.allowed_failure_categories
    )

    checks = [
        QualityGateCheck(
            name="min_total_tasks",
            passed=summary.total_tasks >= selected_config.min_total_tasks,
            detail=(
                f"total_tasks={summary.total_tasks}; "
                f"required>={selected_config.min_total_tasks}"
            ),
        ),
        QualityGateCheck(
            name="min_pass_rate",
            passed=pass_rate >= selected_config.min_pass_rate,
            detail=(
                f"pass_rate={pass_rate:.4f}; "
                f"required>={selected_config.min_pass_rate:.4f}"
            ),
        ),
        QualityGateCheck(
            name="min_average_score",
            passed=summary.average_score >= selected_config.min_average_score,
            detail=(
                f"average_score={summary.average_score:.4f}; "
                f"required>={selected_config.min_average_score:.4f}"
            ),
        ),
        QualityGateCheck(
            name="max_failed_tasks",
            passed=summary.failed_tasks <= selected_config.max_failed_tasks,
            detail=(
                f"failed_tasks={summary.failed_tasks}; "
                f"allowed<={selected_config.max_failed_tasks}"
            ),
        ),
        QualityGateCheck(
            name="allowed_failure_categories",
            passed=not disallowed_categories,
            detail=(
                "disallowed="
                f"{disallowed_categories}; "
                f"allowed={selected_config.allowed_failure_categories}"
            ),
        ),
    ]

    return QualityGateResult(
        passed=all(check.passed for check in checks),
        config=selected_config,
        summary=summary,
        pass_rate=round(pass_rate, 4),
        failure_category_counts=dict(sorted(category_counts.items())),
        failed_task_ids=failed_task_ids,
        checks=checks,
    )
