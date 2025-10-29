from flask import Blueprint, request, abort, current_app
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.extensions import limiter

bp = Blueprint("metrics", __name__)

@bp.route("/metrics")
@limiter.exempt
def metrics():
    token = request.args.get("token")
    metrics_token = current_app.config["METRICS_TOKEN"]
    if metrics_token and token != metrics_token:
        abort(403)
    return generate_latest(), 200, {"content-type": CONTENT_TYPE_LATEST}
