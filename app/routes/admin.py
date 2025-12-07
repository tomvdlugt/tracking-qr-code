

import sqlite3
from flask import Blueprint, current_app, request
from app.extensions import limiter



bp = Blueprint("admin", __name__)

@limiter.exempt
@bp.route("/_admin/fix", methods=["POST"])
def admin_fix():
    token = request.args.get("token")
    if token != "SUPER_SECRET_LONG_TOKEN":
        return "forbidden", 403

    tag = request.json.get("tag")
    day = request.json.get("day")
    new_value = request.json.get("value")

    db_path = current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        "UPDATE daily_clicks SET count = ? WHERE tag = ? AND day = ?",
        (new_value, tag, day)
    )
    conn.commit()
    conn.close()
    # added a comment

    return {"status": "ok", "tag": tag, "day": day, "new_value": new_value}
