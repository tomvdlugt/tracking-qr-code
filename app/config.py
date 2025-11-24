import os
from dotenv import load_dotenv

from load_config import load_json_config

#loads public config
load_json_config("config.json")
#loads dotenv if present
load_dotenv()

class Config:
  """Base configuration (used by default)"""
  def __init__(self):
    #flask settings
    self.DEBUG = os.getenv("FLASK_DEBUG", "false").lower == "true"
    self.TESTING = os.getenv("FLASK_TESTING", "false").lower == "true"
    self.SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    #app-specific settings
    self.TARGET_URL = os.getenv("TARGET_URL", "https://example.com")
    self.METRICS_TOKEN = os.getenv("METRICS_TOKEN")

    #comma seperated list of allowed tags
    self.ALLOWED_TAGS = set(
      tag.strip().lower()
      for tag in os.getenv("ALLOWED_TAGS", "facebook, qr, website").split(",")
      if tag.strip()
    )

    # Rate limiting config
    self.DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "10 per second")
    self.TRACK_ROUTE_LIMIT = os.getenv("TRACK_ROUTE_LIMIT", "5 per second")

    # Prometheus settings
    self.METRIC_NAME = os.getenv("PROMETHEUS_METRIC_NAME", "qr_clicks_total")
    self.PROM_DIR = os.getenv("PROM_DIR")

    # Port (Railway injects PORT automatically)
    self.PORT = int(os.getenv("PORT", 8000))

    #Database
    self.DB_PATH = os.getenv("DB_PATH")


class ProductionConfig(Config):
    def __init__(self):
       super().__init__()
       self.DEBUG = False
       self.TESTING = False

class DevelopmentConfig(Config):
    """Overrides for local dev"""
    def __init__(self):
       super().__init__()
       self.DEBUG = True

def load_config(app):
    """Applies the proper config class to the Flask app."""
    env = os.getenv("FLASK_ENV", "production").lower()
    config = DevelopmentConfig() if env == "development" else ProductionConfig()
    app.config.from_mapping({
        key: value for key, value in config.__dict__.items() if key.isupper()
    })

