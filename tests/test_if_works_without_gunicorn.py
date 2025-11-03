import logging
from app import create_app


def test_if_works_without_gunicorn(monkeypatch):
    fake_logger = logging.getLogger("fake")
    fake_logger.handlers = []
    fake_logger.setLevel(logging.WARNING)

    original_getLogger = logging.getLogger

    # Only fake out gunicorn.error
    def fake_getLogger(name=None):
        if name == "gunicorn.error":
            return fake_logger
        return original_getLogger(name)

    monkeypatch.setattr(logging, "getLogger", fake_getLogger)

    app = create_app()

    # ✅ Should attach fallback StreamHandler when no gunicorn handlers exist
    assert len(app.logger.handlers) > 0
    assert any(isinstance(h, logging.StreamHandler) for h in app.logger.handlers)


def test_create_app_with_gunicorn_logger(monkeypatch):
    fake_handler = logging.StreamHandler()
    fake_logger = logging.getLogger("gunicorn.error")
    fake_logger.handlers = [fake_handler]
    fake_logger.setLevel(logging.ERROR)

    original_getLogger = logging.getLogger

    def fake_getLogger(name=None):
        if name == "gunicorn.error":
            return fake_logger
        return original_getLogger(name)

    monkeypatch.setattr(logging, "getLogger", fake_getLogger)

    app = create_app()

    assert fake_handler in app.logger.handlers
    assert app.logger.level == logging.ERROR
