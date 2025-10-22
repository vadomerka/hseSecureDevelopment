from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_not_found_user():
    r = client.get("/users/999")
    assert r.status_code == 404
    assert r.headers.get("content-type").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 404
    assert body["title"] == "not_found"
    assert "correlation_id" in body


def test_missing_user_arguments_error():
    r = client.post("/users", params={"name": ""})
    assert r.status_code == 422
    assert r.headers.get("content-type").startswith("application/problem+json")
    body = r.json()
    assert body["title"] == "Unprocessable Entity"
    assert body["status"] == 422
    assert "correlation_id" in body


def test_not_found_task():
    r = client.get("/tasks/999")
    assert r.status_code == 404
    assert r.headers.get("content-type").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 404
    assert body["title"] == "not_found"


def test_missing_task_arguments_error():
    r = client.post("/tasks", params={"name": ""})
    assert r.status_code == 422
    assert r.headers.get("content-type").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 422
