from typing import Any

from app.models import AssertionResult, EvaluationTask, ToolResult


def read_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            if index >= len(current):
                return None
            current = current[index]
        else:
            return None
    return current


def score_task(
    task: EvaluationTask,
    selected_tool: str,
    tool_result: ToolResult,
) -> tuple[list[AssertionResult], float, bool]:
    assertions: list[AssertionResult] = []

    assertions.append(
        AssertionResult(
            name="tool_selection",
            passed=selected_tool == task.expected_tool,
            detail=f"expected={task.expected_tool}; selected={selected_tool}",
        )
    )
    assertions.append(
        AssertionResult(
            name="tool_status",
            passed=tool_result.status == "ok",
            detail=f"status={tool_result.status}; error={tool_result.error!r}",
        )
    )

    output = tool_result.output
    expectations = task.expectations

    for path, expected in expectations.get("must_equal", {}).items():
        actual = read_path(output, path)
        assertions.append(
            AssertionResult(
                name=f"must_equal:{path}",
                passed=actual == expected,
                detail=f"expected={expected!r}; actual={actual!r}",
            )
        )

    for path, expected_value in expectations.get("must_contain", {}).items():
        actual = read_path(output, path)
        passed = isinstance(actual, list) and expected_value in actual
        assertions.append(
            AssertionResult(
                name=f"must_contain:{path}",
                passed=passed,
                detail=f"expected list to contain {expected_value!r}; actual={actual!r}",
            )
        )

    for path, minimum in expectations.get("min_value", {}).items():
        actual = read_path(output, path)
        passed = isinstance(actual, int | float) and actual >= minimum
        assertions.append(
            AssertionResult(
                name=f"min_value:{path}",
                passed=passed,
                detail=f"expected >= {minimum!r}; actual={actual!r}",
            )
        )

    passed_count = sum(1 for assertion in assertions if assertion.passed)
    score = passed_count / len(assertions) if assertions else 0.0
    passed = all(assertion.passed for assertion in assertions)
    return assertions, score, passed


def classify_failure(
    assertions: list[AssertionResult],
    tool_result: ToolResult,
) -> str:
    if tool_result.status == "error":
        return "tool_execution"
    if all(assertion.passed for assertion in assertions):
        return "passed"
    if any(
        assertion.name == "tool_selection" and not assertion.passed
        for assertion in assertions
    ):
        return "tool_selection"
    return "output_assertion"
