import logging
import sys
from flask import Flask, request

from app.config_check import validate_env
from .config import load_config
from .extensions import limiter
from .routes import tracking, metrics, health

def create_app():
    validate_env()
    app = Flask(__name__)
    load_config(app)
    app.url_map.strict_slashes = False

    # configuration for logging
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s %(message)s")

    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Tracking qr code initialized")

    # Log each request (middleware)
    @app.before_request
    def log_request():
        app.logger.info(
            f"Request: {request.method} {request.path} from {request.remote_addr}"
        )

    # Initialize extensions
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(tracking.bp)
    app.register_blueprint(metrics.bp)
    app.register_blueprint(health.bp)

    return app
