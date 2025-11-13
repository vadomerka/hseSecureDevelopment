import pytest
from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_nfr_api_err_not_found_error_contract():
    response = client.get("/tasks/999999")
    assert response.status_code == 404
    body = response.json()
    assert set(body.keys()) >= {
        "type",
        "title",
        "status",
        "detail",
        "instance",
        "correlation_id",
    }
    assert body["title"] == "not_found"
    assert body["status"] == 404
    assert body["type"].startswith("https://example.com/problems/")
    assert body["instance"].startswith("/tasks/")
    assert response.headers["Content-Type"] == "application/problem+json"
    assert "X-Correlation-ID" in response.headers


def test_nfr_dto_validation_returns_422():
    response = client.post("/users", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["status"] == 422
    assert body["title"] == "Unprocessable Entity"
    assert "Request validation failed" in body["detail"]
    assert body["type"].startswith("https://datatracker.ietf.org/")
    assert "correlation_id" in body


@pytest.mark.skip(reason="Требуется тестовая БД с пользователями")
def test_nfr_pii_password_not_exposed():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for user in data:
        assert "password" not in user


@pytest.mark.xfail(reason="NFR: latency threshold not yet implemented")
def test_nfr_latency_under_100ms():
    assert True


@pytest.mark.xfail(reason="NFR: throughput measurement not yet implemented")
def test_nfr_throughput_min_requests_per_sec():
    assert True


@pytest.mark.xfail(reason="NFR: error rate SLO not enforced")
def test_nfr_error_rate_below_threshold():
    assert True


@pytest.mark.xfail(reason="NFR: auth/role audit logging not implemented")
def test_nfr_security_audit_log_on_sensitive_action():
    assert False


@pytest.mark.xfail(
    reason="NFR: availability healthcheck for dependencies not implemented"
)
def test_nfr_dependency_healthchecks():
    assert False
