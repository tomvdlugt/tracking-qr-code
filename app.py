from flask import Flask, redirect
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
target_url = os.getenv("TARGET_URL")
port = os.getenv("PORT")

@app.route("/t/<tag>")
def track(tag):
  print(tag)
  return redirect(target_url, code=302)


