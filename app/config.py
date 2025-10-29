import os
from dotenv import load_dotenv

#loads dotenv if present
load_dotenv()

class Config:
  """Base configuration (used by default)"""

  #flask settings
  DEBUG = os.getenv("FLASK_DEBUG", "false").lower == "true"
  TESTING = os.getenv("FLASK_TESTING", "false").lower == "true"
  SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

  #app-specific settings
  TARGET_URL = os.getenv("TARGET_URL", "https://example.com")
  METRICS_TOKEN = os.getenv("METRICS_TOKEN")

  #comma seperated list of allowed tags
  ALLOWED_TAGS = set(
    tag.strip().lower()
    for tag in os.getenv("ALLOWED_TAGS", "facebook, qr, website").split(",")
    if tag.strip()
  )

  # Rate limiting config
  DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "10 per second")
  TRACK_ROUTE_LIMIT = os.getenv("TRACK_ROUTE_LIMIT", "5 per second")

  # Prometheus settings
  METRIC_NAME = os.getenv("PROMETHEUS_METRIC_NAME", "qr_clicks_total")

  # Port (Railway injects PORT automatically)
  PORT = int(os.getenv("PORT", 8000))


class ProductionConfig(Config):
    """Overrides for production"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Overrides for local dev"""
    DEBUG = True


def load_config(app):
    """Applies the proper config class to the Flask app."""
    env = os.getenv("FLASK_ENV", "production").lower()

    if env == "development":
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
