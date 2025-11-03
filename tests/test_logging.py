

import logging

from flask import app

from app import create_app


def test_app_logs_initialized(caplog):
    from app import create_app

    gunicorn_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger.handlers.clear()  # remove stdout-only handlers
    gunicorn_logger.setLevel(logging.INFO)

    with caplog.at_level("INFO"):
        create_app()

    assert "tracking qr code initialized" in caplog.text.lower()



def test_app_logs_request_level_logs(caplog, monkeypatch):
  monkeypatch.setenv("TARGET_URL", "https://example.com")

  app = create_app()
  app.config["testing"] = True
  client = app.test_client()

  with caplog.at_level("INFO", logger="app"):
    client.get("/t/facebook")
    client.get("/t/qr")

  assert "get /t/facebook" in caplog.text.lower()
  assert "get /t/qr" in caplog.text.lower()
