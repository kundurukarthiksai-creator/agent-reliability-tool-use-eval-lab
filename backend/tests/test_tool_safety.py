from app.tools.tool_safety import tool_safety_audit


def test_tool_safety_reports_current_mcp_lab_ready():
    result = tool_safety_audit({"project_id": "mcp-tool-safety-lab"})

    assert result["safety_ready"] is True
    assert result["safety_score"] == 100
    assert "permission-gate" in result["matched_controls"]
    assert "approval-gate" in result["matched_controls"]
    assert result["missing_controls"] == []
    assert result["risky_gaps"] == []


def test_tool_safety_flags_missing_approval_gate():
    result = tool_safety_audit({"project_id": "agent-tools-no-approval"})

    assert result["safety_ready"] is False
    assert result["safety_score"] == 88
    assert "approval-gate" in result["missing_controls"]
    assert "publish-like action lacks approval boundary" in result["risky_gaps"]


def test_tool_safety_flags_missing_audit_log():
    result = tool_safety_audit({"project_id": "agent-tools-no-audit"})

    assert result["safety_ready"] is False
    assert result["safety_score"] == 88
    assert "audit-log" in result["missing_controls"]
    assert "tool calls are not observable after execution" in result["risky_gaps"]


def test_tool_safety_requires_project_id():
    result = tool_safety_audit({})

    assert result["safety_ready"] is False
    assert result["safety_score"] == 0
    assert result["missing_controls"] == ["project_id_required"]
