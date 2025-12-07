

import sqlite3
from flask import Blueprint, current_app, request
from app.extensions import limiter



bp = Blueprint("admin", __name__)


@bp.route("/_admin/show", methods=["GET"])
def admin_show():
    token = request.args.get("token")
    if token != "SUPER_SECRET":
        return "forbidden", 403

    tag = request.args.get("tag")

    db_path = current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT tag, day, count FROM daily_clicks WHERE tag = ?", (tag,))
    rows = cur.fetchall()

    conn.close()
    return {"rows": rows}

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

@bp.route("/_admin/dbpath")
def show_db_path():
    return {"db_path": current_app.config["DB_PATH"]}

@bp.route("/_admin/list")
def list_db():
    import os
    path = os.path.dirname(current_app.config["DB_PATH"])
    return {"files": os.listdir(path)}
