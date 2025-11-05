import os
import shutil
import qrcode

BASE_URL = "https://bestellen.scoutingwateringen.nl/t/"
TAGS = ["facebook", "qr", "website"]
OUTPUT_DIR = "qr-codes"

# Remove the folder completely if it exists
if os.path.exists(OUTPUT_DIR):
    print("removed existing folder")
    shutil.rmtree(OUTPUT_DIR)

# Recreate it fresh
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_qr(tag: str):
    full_url = f"{BASE_URL}{tag}"
    img = qrcode.make(full_url)
    filename = os.path.join(OUTPUT_DIR, f"qr_{tag}.png")
    img.save(filename)
    print(f"Saved {filename} → {full_url}")

if __name__ == "__main__":
    for tag in TAGS:
        generate_qr(tag)
