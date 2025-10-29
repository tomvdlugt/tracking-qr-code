from flask import Blueprint
from app.extensions import limiter

bp = Blueprint("health", __name__)

@bp.route("/")
@limiter.exempt
def index():
    return "<p>QR Tracking redirect service is running</p>", 200

@bp.route("/health")
@limiter.exempt
def health():
    return "OK", 200
