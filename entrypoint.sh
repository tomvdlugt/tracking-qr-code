#!/usr/bin/env sh
set -e

# Ensure gunicorn is visible
export PATH="/usr/local/bin:$PATH"

# ---- Prometheus multiprocess dir (shared across workers) ----
if [ -z "$PROM_DIR" ]; then
  PROM_DIR="/data/prometheus"
fi

echo "🔧 PATH is: $PATH"
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

