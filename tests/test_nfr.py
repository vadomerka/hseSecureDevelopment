import statistics
from time import perf_counter

from fastapi.testclient import TestClient

from task_app.main import app

client = TestClient(app)


def test_nfr_latency_under_150ms():
    samples_ms: list[float] = []
    for _ in range(5):
        start = perf_counter()
        resp = client.get("/health")
        elapsed_ms = (perf_counter() - start) * 1000
        samples_ms.append(elapsed_ms)
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    assert statistics.mean(samples_ms) < 150
    assert max(samples_ms) < 250


def test_nfr_throughput_min_requests_per_sec():
    iterations = 40
    start = perf_counter()
    for _ in range(iterations):
        resp = client.get("/health")
        assert resp.status_code == 200
    elapsed = perf_counter() - start
    assert elapsed > 0
    requests_per_sec = iterations / elapsed
    assert requests_per_sec >= 25


def test_nfr_error_rate_below_threshold():
    endpoints = ["/health", "/tasks", "/users"]
    total = 0
    failures = 0
    for _ in range(5):
        for path in endpoints:
            resp = client.get(path)
            total += 1
            if resp.status_code >= 500:
                failures += 1
            else:
                assert resp.status_code in (200, 404)
    error_rate = failures / total
    assert error_rate <= 0.01


def test_nfr_security_audit_log_on_sensitive_action():
    first = client.get("/tasks/99999")
    second = client.get("/tasks/99998")
    assert first.status_code == 404
    assert second.status_code == 404

    cid_header_1 = first.headers.get("X-Correlation-ID")
    cid_header_2 = second.headers.get("X-Correlation-ID")
    assert cid_header_1
    assert cid_header_2
    assert cid_header_1 != cid_header_2

    body1 = first.json()
    body2 = second.json()
    assert body1["correlation_id"] == cid_header_1
    assert body2["correlation_id"] == cid_header_2


def test_nfr_dependency_healthchecks():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}

    tasks = client.get("/tasks")
    users = client.get("/users")
    assert tasks.status_code == 200
    assert users.status_code == 200
    assert isinstance(tasks.json(), list)
    assert isinstance(users.json(), list)
