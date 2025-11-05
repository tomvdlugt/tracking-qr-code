#!/usr/bin/env sh
set -e

# ---- Prometheus multiprocess dir (shared across workers) ----
export PROMETHEUS_MULTIPROC_DIR="${PROM_DIR:-/tmp/prometheus-multiproc-dir}"
mkdir -p "$prometheus_multiproc_dir"
# Clear old shard files from previous runs (safe: Prometheus keeps history)
rm -f "$prometheus_multiproc_dir"/* 2>/dev/null || true

# ---- Start Gunicorn ----
# Notes:
#  - access/error logs to stdout/stderr so Railway shows correct levels
#  - WORKERS default 4; tune based on CPU/memory
#  - PORT provided by Railway; fall back to 8000 locally
exec gunicorn \
  --workers "${WORKERS:-4}" \
  --bind "0.0.0.0:${PORT:-8000}" \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  app.main:app
