from datetime import date
import os
import sqlite3

def init_db(db_path):
  folder = os.path.dirname(db_path)
  if folder:
    os.makedirs(folder, exist_ok=True)


  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("PRAGMA journal_mode=WAL;")

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS daily_clicks(
    tag TEXT NOT NULL,
    day TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (tag, day)
  );
  """)

  conn.commit()
  conn.close()

def record_click(tag, db_path="/data/clicks.db"):
  today = date.today().isoformat()

  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute("""
    INSERT INTO daily_clicks(tag, day, count)
    VALUES(?, ?, 1)
    ON CONFLICT(tag, day) DO UPDATE SET count = count + 1;""", (tag, today)
  )

  conn.commit()
  conn.close()

def load_totals_by_tag(db_path):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute("""
    SELECT tag, SUM(count) FROM daily_clicks GROUP BY tag;
  """)

  rows = cursor.fetchall()
  totals = {tag: total for tag, total in rows}
  conn.close()

  return totals



