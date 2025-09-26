from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_user():
    r = client.get("/users/999")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "not_found"


def test_missing_user_arguments_error():
    r = client.post("/users", params={"name": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["detail"][0]["type"] == "missing"


def test_not_found_task():
    r = client.get("/tasks/999")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "not_found"


def test_missing_task_arguments_error():
    r = client.post("/tasks", params={"name": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["detail"][0]["type"] == "missing"
