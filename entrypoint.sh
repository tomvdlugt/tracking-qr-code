#!/usr/bin/env sh
set -e

# Ensure gunicorn is visible
export PATH="/usr/local/bin:$PATH"

# ---- Prometheus multiprocess dir (shared across workers) ----
if [ -z "$PROM_DIR" ]; then
  PROM_DIR="/data/prometheus"
fi
export PROMETHEUS_MULTIPROC_DIR="$PROM_DIR"

mkdir -p "$PROMETHEUS_MULTIPROC_DIR"
rm -f "$PROMETHEUS_MULTIPROC_DIR"/* 2>/dev/null || true

echo "🔧 PATH is: $PATH"
echo "🔍 gunicorn binary at: $(which gunicorn || echo 'NOT FOUND')"

# ---- Start Gunicorn ----
exec /usr/local/bin/gunicorn \
  --workers "${WORKERS:-4}" \
  --bind "0.0.0.0:${PORT:-8000}" \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  app.main:app
