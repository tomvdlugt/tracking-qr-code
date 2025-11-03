import os
import sys

# Add the project root to the path (so 'app' is importable)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

def test_if_right_config_is_set_development(monkeypatch):
  monkeypatch.setenv("FLASK_ENV", "development")

  app = create_app()

  assert app.config["DEBUG"] is True
  assert app.config["TESTING"] is False

def test_if_right_config_is_set_prod(monkeypatch):
  monkeypatch.setenv("FLASK_ENV", "production")
  app = create_app()

  assert app.config["DEBUG"] is False
  assert app.config["TESTING"] is False

def test_if_environments_properly_propagate_into_config(monkeypatch):
  monkeypatch.setenv("TARGET_URL", "test_target_url")
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PORT", "9000")

  app = create_app()

  assert app.config["TARGET_URL"] == "test_target_url"
  assert app.config["SECRET_KEY"] == "test_secret_key"
  assert app.config["PORT"] == 9000





