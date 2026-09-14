from app.tools.role_readiness import role_readiness_audit


def test_role_readiness_reports_ai_tools_ready_profile():
    result = role_readiness_audit(
        {
            "role_id": "ai-tools-backend-internship",
            "profile_id": "eval-lab-portfolio",
        }
    )

    assert result["ready_for_role"] is True
    assert result["readiness_score"] == 100
    assert result["missing_required"] == []
    assert "agent-evaluation" in result["matched_required"]
    assert "case-study" in result["matched_preferred"]


def test_role_readiness_reports_cloud_gaps():
    result = role_readiness_audit(
        {
            "role_id": "cloud-platform-internship",
            "profile_id": "eval-lab-portfolio",
        }
    )

    assert result["ready_for_role"] is False
    assert result["readiness_score"] == 70
    assert "cloud-deployment" in result["missing_required"]
    assert "observability" in result["missing_required"]
    assert result["recommended_evidence"]


def test_role_readiness_requires_role_id():
    result = role_readiness_audit({"profile_id": "eval-lab-portfolio"})

    assert result["ready_for_role"] is False
    assert result["readiness_score"] == 0
    assert result["missing_required"] == ["role_id_required"]


def test_role_readiness_requires_profile_id():
    result = role_readiness_audit({"role_id": "ai-tools-backend-internship"})

    assert result["ready_for_role"] is False
    assert result["readiness_score"] == 0
    assert result["missing_required"] == ["profile_id_required"]
