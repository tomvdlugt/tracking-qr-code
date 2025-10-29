from flask import Flask
from .config import load_config
from .extensions import limiter, clicks
from .routes import tracking, metrics, health

def create_app():
    app = Flask(__name__)
    load_config(app)
    app.url_map.strict_slashes = False

    # Initialize extensions
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(tracking.bp)
    app.register_blueprint(metrics.bp)
    app.register_blueprint(health.bp)

    return app
