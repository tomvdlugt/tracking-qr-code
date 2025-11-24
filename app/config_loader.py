
import json
import os


def load_json_config(file_path="config.json"):
  if not os.path.exists(file_path):
    return

  with open(file_path) as f:
    data = json.load(f)

  for key, value in data.items():
    if os.getenv(key) is None:
      if isinstance(value, list):
        os.environ[key] = ",".join(value)
      else:
        os.environ[key] = str(value)
