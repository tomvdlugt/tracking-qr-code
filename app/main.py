from app import create_app
import os

from app.config_loader import load_json_config

 #loads public config
load_json_config("config.json")
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
