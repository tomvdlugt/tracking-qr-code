import json
import logging
import os
import shutil
import qrcode
from dotenv import load_dotenv

with open("./config.json") as f:
    cfg = json.load(f)

base_url = cfg["BASE_URL"]
tags = cfg["ALLOWED_TAGS"]

print(repr(tags))
print(len(tags))


OUTPUT_DIR = "qr-codes"

# Remove the folder completely if it exists
if os.path.exists(OUTPUT_DIR):
    logging.info("removed existing folder")
    shutil.rmtree(OUTPUT_DIR)

# Recreate it fresh
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_qr(tag: str):
    full_url = f"{base_url}{tag}"
    img = qrcode.make(full_url)
    filename = os.path.join(OUTPUT_DIR, f"qr_{tag}.png")
    img.save(filename)
    logging.info(f"Saved {filename} → {full_url}")

if __name__ == "__main__":
    for tag in tags:
        generate_qr(tag)
