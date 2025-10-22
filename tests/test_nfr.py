import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
