from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_user_rejects_invalid_email():
    r = client.post(
        "/users",
        json={"name": "bad", "email": "not-an-email", "password": "password123"},
    )
    assert r.status_code == 422


def test_user_rejects_short_password():
    r = client.post(
        "/users", json={"name": "A", "email": "a@example.com", "password": "123"}
    )
    assert r.status_code == 422


def test_task_rejects_long_title():
    long_title = "x" * 101
    payload = {
        "title": long_title,
        "description": "desc",
        "type": "bug",
        "status": "open",
        "priority": 1,
        "tag": "tag",
        "due_at": "2024-01-01T00:00:00Z",
        "started_at": "2024-01-01T00:00:00Z",
    }
    r = client.post("/tasks", json=payload)
    assert r.status_code == 422
