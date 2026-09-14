from app.tools.profile_readme import profile_readme_audit


def test_profile_readme_audit_reports_ready_profile():
    result = profile_readme_audit(
        {
            "profile_id": "candidate-profile-polished",
            "target_project": "agent-reliability-tool-use-eval-lab",
        }
    )

    assert result["ready_for_recruiter"] is True
    assert result["score"] == 6
    assert result["featured_project_present"] is True
    assert result["missing"] == []


def test_profile_readme_audit_reports_missing_proof():
    result = profile_readme_audit(
        {
            "profile_id": "candidate-profile-thin",
            "target_project": "agent-reliability-tool-use-eval-lab",
        }
    )

    assert result["ready_for_recruiter"] is False
    assert "proof_links" in result["missing"]
    assert "metrics" in result["missing"]
    assert "learning_focus" in result["missing"]


def test_profile_readme_audit_requests_profile_id():
    result = profile_readme_audit(
        {"target_project": "agent-reliability-tool-use-eval-lab"}
    )

    assert result["ready_for_recruiter"] is False
    assert result["score"] == 0
    assert result["missing"] == ["profile_id_required"]
