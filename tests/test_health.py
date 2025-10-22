from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_validation_problem_details_and_correlation_id():
    r = client.post("/tasks", params={"name": ""})
    assert r.status_code == 422
    assert r.headers.get("X-Correlation-ID")
