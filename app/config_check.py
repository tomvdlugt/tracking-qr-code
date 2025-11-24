import os

REQUIRED_ENV_VARS = [
  "TARGET_URL",
  "SECRET_KEY",
  "METRICS_TOKEN",
  "DB_PATH"
]

def validate_env(app):
  """Ensure all required environments are set correctly"""
  missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
  if missing != []:
    app.logger.error(f"Missing env vars: {missing}")
  return missing
