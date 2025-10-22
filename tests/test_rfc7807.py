from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_problem_details_shape_and_header_echo():
    r = client.get("/users/123456")
    assert r.status_code == 404
    assert r.headers.get("content-type").startswith("application/problem+json")
    body = r.json()
    assert {"type", "title", "status", "detail", "instance", "correlation_id"}.issubset(
        body.keys()
    )
    assert r.headers.get("X-Correlation-ID") == body.get("correlation_id")
