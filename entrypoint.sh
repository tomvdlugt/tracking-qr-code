#!/usr/bin/env sh
set -e

unset PROMETHEUS_MULTIPROC_DIR

echo "🔍 gunicorn binary at: $(which gunicorn || echo 'NOT FOUND')"

# ---- Start Gunicorn ----
exec /usr/local/bin/gunicorn \
  --workers "${WORKERS:-1}" \
  --threads "${THREADS:-8}" \
  --bind "0.0.0.0:${PORT:-8000}" \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  app.main:app

