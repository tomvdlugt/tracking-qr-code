
import os
import sys
# Add the project root to the path (so 'app' is importable)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.config_check import validate_env

def test_valide_env_missing(monkeypatch):
  monkeypatch.delenv("SECRET_KEY", raising=False)
  missing=validate_env()

  assert "SECRET_KEY" in missing

def test_all_env_present(monkeypatch):
  monkeypatch.setenv("SECRET_KEY", "test_secret")
  monkeypatch.setenv("ALLOWED_TAGS", "test_allowed_tags")
  monkeypatch.setenv("METRICS_TOKEN", "test_metrics_token")
  monkeypatch.setenv("TARGET_URL", "test_target_url")

  missing = validate_env()

  assert missing == []

def test_multiple_env_missing(monkeypatch):
  monkeypatch.delenv("SECRET_KEY", raising=False)
  monkeypatch.delenv("ALLOWED_TAGS", raising=False)

  missing=validate_env()

  assert missing == ["SECRET_KEY", "ALLOWED_TAGS"]



