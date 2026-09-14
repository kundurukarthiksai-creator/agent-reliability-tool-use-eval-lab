from app.tools.artifact_consistency import artifact_consistency_audit


def test_artifact_consistency_reports_current_public_proof():
    result = artifact_consistency_audit({"artifact_id": "eval-lab-current-proof"})

    assert result["consistent"] is True
    assert result["consistency_score"] == 100
    assert "current-eval-count" in result["matched_required"]
    assert "architecture-flow" in result["matched_required"]
    assert result["missing_required"] == []
    assert result["stale_markers"] == []


def test_artifact_consistency_reports_stale_count_claims():
    result = artifact_consistency_audit({"artifact_id": "eval-lab-stale-counts"})

    assert result["consistent"] is False
    assert result["consistency_score"] == 67
    assert "current-eval-count" in result["missing_required"]
    assert "current-tool-count" in result["missing_required"]
    assert "old-eval-count" in result["stale_markers"]


def test_artifact_consistency_reports_missing_contract_and_gate():
    result = artifact_consistency_audit({"artifact_id": "eval-lab-docs-only"})

    assert result["consistent"] is False
    assert result["consistency_score"] == 67
    assert "quality-gate-proof" in result["missing_required"]
    assert "openapi-contract" in result["missing_required"]
    assert len(result["recommended_fixes"]) == 2


def test_artifact_consistency_requires_artifact_id():
    result = artifact_consistency_audit({})

    assert result["consistent"] is False
    assert result["consistency_score"] == 0
    assert result["missing_required"] == ["artifact_id_required"]
