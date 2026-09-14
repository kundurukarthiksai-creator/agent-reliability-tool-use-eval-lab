from fastapi.testclient import TestClient

from app.main import app


EXPECTED_PATHS = {
    "/",
    "/health",
    "/tools",
    "/eval/tasks",
    "/eval/tasks/coverage",
    "/eval/run",
    "/eval/runs",
    "/eval/runs/compare",
    "/eval/runs/trends",
    "/reports/latest.html",
}


def test_openapi_contract_exposes_core_routes():
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    spec = response.json()
    assert spec["info"]["title"] == "Agent Reliability and Tool-Use Eval Lab"
    assert spec["info"]["version"] == "0.1.0"
    assert EXPECTED_PATHS.issubset(set(spec["paths"]))
    assert "EvalReport" in spec["components"]["schemas"]
    assert "EvaluationTask" in spec["components"]["schemas"]


def test_eval_run_route_documents_eval_report_response():
    client = TestClient(app)

    response = client.get("/openapi.json")

    spec = response.json()
    eval_run_response = spec["paths"]["/eval/run"]["post"]["responses"]["200"]
    schema_ref = eval_run_response["content"]["application/json"]["schema"]["$ref"]
    assert schema_ref == "#/components/schemas/EvalReport"
