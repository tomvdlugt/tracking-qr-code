from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import Counter

# Create extension instances (unbound)
limiter = Limiter(key_func=get_remote_address, default_limits=["10 per second"], storage_uri="memory://")
clicks = Counter("qr_clicks_total", "Amount of clicks on QR code", ["tag"])
