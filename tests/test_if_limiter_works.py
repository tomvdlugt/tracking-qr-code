import os
import sys

import pytest

# Add the project root to the path (so 'app' is importable)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

@pytest.fixture
def app():
    """Create a fresh Flask app instance for each test."""
    app = create_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture
def client(app):
    """Provide a test client for the app."""
    with app.test_client() as client:
        yield client

def test_if_rate_limit_triggers_after_threshold(monkeypatch):
    monkeypatch.setenv("TRACK_ROUTE_LIMIT", "2 per minute")

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    for i in range(3):
        response = client.get("/t/facebook")
        if i < 2:
            assert response.status_code == 302
        else:
            assert response.status_code == 429


def test_health_route_is_not_rate_limited(client):
    for i in range(10):
        response = client.get("/health")
        assert response.status_code == 200, f"Unexpected status {response.status_code} on iteration {i}"

def test_route_specific_limit_overrides_default(monkeypatch, client):
    monkeypatch.setenv("DEFAULT_RATE_LIMIT", "10 per second")  # global default
    monkeypatch.setenv("TRACK_ROUTE_LIMIT", "2 per minute")    # route-specific

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    for i in range(3):
      response = client.get("/t/facebook")
      if i < 2:
        assert response.status_code == 302
      else:
        assert response.status_code == 429

def test_limiter_is_bound_to_app(app):
    assert hasattr(app, "extensions"), "Flask app has no extensions registry"
    assert "limiter" in app.extensions, "limiter extensiosn not found in app.extensions"
    assert app.extensions["limiter"] is not None, "limiter extension is none"
