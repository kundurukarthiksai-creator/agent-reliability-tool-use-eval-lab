from app.tools.launch_readiness import launch_readiness_audit


def test_launch_readiness_reports_ready_project():
    result = launch_readiness_audit({"project_id": "agent-reliability-eval-lab"})

    assert result["launch_ready"] is True
    assert result["readiness_score"] == 100
    assert "openapi-contract" in result["matched_required"]
    assert "no-key-static-demo" in result["matched_required"]
    assert result["missing_required"] == []


def test_launch_readiness_reports_missing_public_evidence():
    result = launch_readiness_audit({"project_id": "agent-demo-no-contract"})

    assert result["launch_ready"] is False
    assert result["readiness_score"] == 75
    assert "openapi-contract" in result["missing_required"]
    assert "failure-catalog" in result["missing_required"]
    assert len(result["recommended_evidence"]) == 2


def test_launch_readiness_requires_project_id():
    result = launch_readiness_audit({})

    assert result["launch_ready"] is False
    assert result["readiness_score"] == 0
    assert result["missing_required"] == ["project_id_required"]


def test_launch_readiness_reports_unknown_project():
    result = launch_readiness_audit({"project_id": "unknown-project"})

    assert result["launch_ready"] is False
    assert result["readiness_score"] == 0
    assert result["missing_required"] == ["project_not_found"]
