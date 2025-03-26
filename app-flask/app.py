"""Flask app that displays current time in Italian timezone with rate limiting and metrics."""

# Import standard
import os
import time
from datetime import datetime

# Import terze parti
import pytz
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Import moduli interni
import version

app = Flask(__name__)

# Rate limiting configuration - 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

# Italian timezone configuration
timezone = pytz.timezone("Europe/Rome")

# Metrics tracking
start_time = time.time()
request_count = 0
endpoint_counts = {"root": 0, "health_check": 0, "metrics": 0}


@app.route("/")
@limiter.limit("100 per minute")
def hello():
    """Generate greeting message with agent name, version and current time."""
    global request_count
    request_count += 1
    endpoint_counts["root"] += 1
    
    # Get agent name from environment variable or use default
    agent_name = os.getenv("AGENT_NAME", "Flask")
    # Get current time in Italian timezone
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime("%H:%M")
    # Get version from file
    app_version = version.get_version()
    message = f"Ciao, mi chiamo {agent_name} versione {app_version}"
    return f"{message} sono le ore {formatted_time}"


@app.route("/health-check")
@limiter.limit("100 per minute")
def health_check():
    """Provide health status information."""
    global request_count
    request_count += 1
    endpoint_counts["health_check"] += 1
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone).isoformat(),
        "version": version.get_version(),
    }


@app.route("/metrics")
@limiter.limit("100 per minute")
def metrics():
    """Provide application metrics for Prometheus monitoring."""
    global request_count
    request_count += 1
    endpoint_counts["metrics"] += 1
    
    uptime_seconds = time.time() - start_time
    
    # Create metrics in a format Prometheus can understand
    metrics_data = {
        "flask_uptime_seconds": uptime_seconds,
        "flask_request_count": request_count,
        "flask_request_count_by_endpoint": [
            {"endpoint": "/", "count": endpoint_counts["root"]},
            {"endpoint": "/health-check", "count": endpoint_counts["health_check"]},
            {"endpoint": "/metrics", "count": endpoint_counts["metrics"]}
        ],
        "flask_version": version.get_version(),
        "flask_http_request_total": request_count
    }
    
    return jsonify(metrics_data)


if __name__ == "__main__":
    # Avvio dell'applicazione Flask
    app.run(host="0.0.0.0", port=5000) # nosec B104
