import logging
import os
import shutil
import sys
from flask import Flask, request
from app.config_check import validate_env
from .config import load_config
from .routes import tracking, metrics, health

def create_app():
    # Validate environment once per worker. If required envs are not there, throw runtime exception
    missing = validate_env()
    if missing:
        raise RuntimeError(f"Missing required environment variables: {','.join(missing)}")

    app = Flask(__name__)
    load_config(app)
    app.url_map.strict_slashes = False
    from .extensions import limiter
    # --- Prometheus multiprocess setup ---
    prom_dir = app.config.get("PROM_DIR") or "/tmp/prometheus-multiproc-dir"
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(prom_dir)
    # Clean old metric files before starting (important!)
    if os.path.exists(prom_dir):
        shutil.rmtree(prom_dir)
    os.makedirs(prom_dir, exist_ok=True)

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

    app.logger.info(f"Flask app initialized on port {os.getenv('PORT')}")

    return app
