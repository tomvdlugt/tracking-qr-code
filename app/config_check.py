import os

REQUIRED_ENV_VARS = [
  "TARGET_URL",
  "SECRET_KEY",
  "METRICS_TOKEN",
  "ALLOWED_TAGS",
]

def validate_env():
  """Ensure all required environments are set correctly"""
  missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
  return missing
