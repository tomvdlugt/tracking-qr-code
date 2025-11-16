from flask import Blueprint, request, abort, current_app
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from app.extensions import limiter

bp = Blueprint("metrics", __name__)

@bp.route("/metrics")
@limiter.exempt
def metrics():
    token = request.args.get("token")
    metrics_token = current_app.config["METRICS_TOKEN"]
    if metrics_token and token != metrics_token:
        abort(403)

    data = generate_latest(REGISTRY)

     # 🧠 Debug logs
    metric_count = len(list(REGISTRY.collect()))
    current_app.logger.info(f"/metrics called — {metric_count} metric families registered")

    return data, 200, {"Content-Type": CONTENT_TYPE_LATEST}
