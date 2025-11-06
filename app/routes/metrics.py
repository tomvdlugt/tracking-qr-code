from flask import Blueprint, request, abort, current_app
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, multiprocess
from app.extensions import limiter

bp = Blueprint("metrics", __name__)

@bp.route("/metrics")
@limiter.exempt
def metrics():
    token = request.args.get("token")
    metrics_token = current_app.config["METRICS_TOKEN"]
    if metrics_token and token != metrics_token:
        abort(403)

    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)

     # 🧠 Debug logs
    metric_count = len(list(registry.collect()))
    current_app.logger.info(f"/metrics called — {metric_count} metric families registered")
    current_app.logger.info(f"PROMETHEUS_MULTIPROC_DIR={os.getenv('PROMETHEUS_MULTIPROC_DIR')}")

    return data, 200, {"Content-Type": CONTENT_TYPE_LATEST}
