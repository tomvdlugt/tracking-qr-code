from flask import Flask, redirect
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

load_dotenv()
app = Flask(__name__)
app.url_map.strict_slashes = False
target_url = os.getenv("TARGET_URL")
port = os.getenv("PORT")
c = Counter("qr_clicks_total", "Amount of clicks on QR code", ["tag"])
allowed_tags = {"facebook", "qr", "website"}

@app.route("/t/")
def track_missing():
    print("Missing tag in request")
    return "Missing tag", 400


@app.route("/t/<tag>")
def track(tag):
  print(f"Tag received: '{tag}' | Allowed: {tag in allowed_tags}")
  tag = tag.lower().strip("/")
  if tag not in allowed_tags:
    return "unkown tag"
  else:
    c.labels(tag=tag).inc()
  return redirect(target_url, code=302)


@app.route("/metrics")
def metrics():
  return generate_latest(), 200, {"content-type": CONTENT_TYPE_LATEST}

@app.route("/")
def index():
    return "<p>QR Tracking redirect service is running </p>"


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))  # Railway injects PORT
    app.run(host="0.0.0.0", port=port)
