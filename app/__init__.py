import logging
import os
import sys
from flask import Flask, request
from app.config_check import validate_env
from .config import load_config
from .extensions import limiter
from .routes import tracking, metrics, health

def create_app():
    # Validate environment once per worker. If required envs are not there, throw runtime exception
    missing = validate_env()
    if missing:
        raise RuntimeError(f"Missing required environment variables: {','.join(missing)}")

    app = Flask(__name__)
    load_config(app)
    app.url_map.strict_slashes = False

    # --- Clean logger setup ---
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    # Optional: also log to stdout if running locally (not under gunicorn)
    if not app.logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        ))
        app.logger.addHandler(handler)

    app.logger.info("Tracking QR code initialized")

    @app.before_request
    def _log_request():
        app.logger.info(f"{request.method} {request.path} from {request.remote_addr}")

    limiter.init_app(app)

    app.register_blueprint(tracking.bp)
    app.register_blueprint(metrics.bp)
    app.register_blueprint(health.bp)


    print(f"Flask app initialized on port {os.getenv('PORT')}")

    return app
