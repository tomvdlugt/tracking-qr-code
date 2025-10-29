FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Railway injects $PORT automatically
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT:-8000}", "app.main:app"]
