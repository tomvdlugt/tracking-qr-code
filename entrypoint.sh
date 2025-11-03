#!/bin/sh
# Start Gunicorn with proper stdout/stderr config so Railway shows correct log levels

exec gunicorn \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    -w 4 \
    -b 0.0.0.0:${PORT:-8000} \
    app.main:app
