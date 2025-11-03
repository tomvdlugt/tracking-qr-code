from flask import Blueprint, make_response
from app.extensions import limiter

bp = Blueprint("health", __name__)

@bp.route("/")
@limiter.exempt
def index():
    return no_cache_response("<p>QR Tracking redirect service is running</p>")

@bp.route("/health")
@limiter.exempt
def health():
    return no_cache_response("OK")

def no_cache_response(body, status=200):
    resp = make_response(body, status)
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return resp
