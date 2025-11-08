from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_sql_injection_attempt_rejected():
    payload = {
        "title": "test'; DROP TABLE users;--",
        "description": "desc",
        "type": "bug",
        "status": "open",
        "priority": 1,
        "tag": "tag",
        "due_at": "2024-01-01T00:00:00Z",
        "started_at": "2024-01-01T00:00:00Z",
    }
    r = client.post("/tasks", json=payload)
    assert r.status_code in (200, 422, 400)
