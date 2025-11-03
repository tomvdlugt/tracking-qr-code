import os
import sys
import pytest

# Add the project root to the path (so 'app' is importable)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b"OK" in response.data

def test_root_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"QR Tracking" in response.data

def test_metrics_protected_requires_token(client):
    # Without token should return 401 or 403
    response = client.get("/metrics")
    assert response.status_code in (401, 403), f"Expected 401/403, got {response.status_code}"

def test_metrics_route_allows_valid_token(monkeypatch):
    monkeypatch.setenv("METRICS_TOKEN", "secret123")

    # Create a new app so it picks up the env var
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Now pass the correct token in query params
    response = client.get("/metrics?token=secret123")

    assert response.status_code == 200
    assert b"qr_clicks_total" in response.data  # or any metric name you expose


