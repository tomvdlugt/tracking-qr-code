from flask import Flask, redirect
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

load_dotenv()
app = Flask(__name__)
target_url = os.getenv("TARGET_URL")
port = os.getenv("PORT")
c = Counter("qr_clicks_total", "Amount of clicks on QR code", ["tag"])
allowed_tags = {"facebook", "qr", "website"}

@app.route("/t/<tag>")
def track(tag):
  if tag not in allowed_tags:
    print("unkown tag")
  else:
    c.labels(tag=tag).inc()
  return redirect(target_url, code=302)

@app.route("/metrics")
def metrics():
  return generate_latest(), 200, {"content-type": CONTENT_TYPE_LATEST}
