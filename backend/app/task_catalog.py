from collections import Counter

from app.models import EvaluationTask, TaskCatalogSummary, ToolDefinition, ToolTaskCoverage


def summarize_task_coverage(
    tasks: list[EvaluationTask],
    tools: list[ToolDefinition],
) -> TaskCatalogSummary:
    task_counts = Counter(task.expected_tool for task in tasks)
    coverage = [
        ToolTaskCoverage(tool_name=tool.name, task_count=task_counts.get(tool.name, 0))
        for tool in tools
    ]
    return TaskCatalogSummary(total_tasks=len(tasks), coverage=coverage)
