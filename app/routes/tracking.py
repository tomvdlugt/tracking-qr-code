from flask import Blueprint, app, redirect, request, current_app
from app.extensions import limiter, clicks
import random

bp = Blueprint("tracking", __name__)

@bp.route("/t/", defaults={"tag": None})
@bp.route("/t/<tag>")
@limiter.limit(lambda: current_app.config["TRACK_ROUTE_LIMIT"])
def track(tag):
    tag = (tag or "").lower().strip("/")
    ua = request.headers.get("User-Agent", "").lower()

    # Skip known crawlers and bots
    bots = ["bot", "crawl", "spider", "facebookexternalhit", "whatsapp", "discord"]
    if any(b in ua for b in bots):
        current_app.logger.warn(f"Ignored bot UA: {ua[:80]}")
        return redirect(current_app.config["TARGET_URL"], code=302)

    if tag in current_app.config["ALLOWED_TAGS"]:
        clicks.labels(tag=tag).inc()
        if random.random() < 0.1:
            current_app.log.info(f"Counted tag: {tag}")
    else:
        current_app.log.info(f"Ignored tag: {tag!r}")

    return redirect(current_app.config["TARGET_URL"], code=302)
