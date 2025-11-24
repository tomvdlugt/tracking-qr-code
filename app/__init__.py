import logging
import os
import shutil
import sys
from flask import Flask, request
from app.config_check import validate_env
from app.persistence import init_db, load_totals_by_tag
from app.routes.errors import register_error_handlers
from app.extensions import clicks
from .config import load_config
from .routes import tracking, metrics, health
from app.config_loader import load_json_config

def create_app():
    app = Flask(__name__)

    #loads public config
    load_json_config("config.json")
    missing = validate_env(app)
    if missing:
        raise RuntimeError(f"Missing required environment variables: {','.join(missing)}")
    load_config(app)
    db_path = app.config.get("DB_PATH", "/data/clicks.db")
    init_db(db_path)



    app.url_map.strict_slashes = False
    from .extensions import limiter

     # restore clicks total
    totals = load_totals_by_tag(app.config["DB_PATH"])
    for tag, total in totals.items():
        if total > 0:
          clicks.labels(tag=tag).inc(total)
        app.logger.info(f"Loaded {total} clicks for tag '{tag}' from DB")

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

    register_error_handlers(app)

    app.logger.info(f"Flask app initialized on port {os.getenv('PORT')}")

    return app
