# Use a small Python base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app (expects app.py in this folder)
COPY . .

# The app listens on 8000 (avoid macOS AirPlay on 5000)
EXPOSE 8000

# Run with gunicorn in the container
# Make sure your Flask app object is named "app" in app.py
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
