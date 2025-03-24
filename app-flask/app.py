"""Flask app that displays current time in Italian timezone with rate limiting."""

# Import standard
import os
from datetime import datetime

# Import terze parti
import pytz
from flask import Flask
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


@app.route("/")
@limiter.limit("100 per minute")
def hello():
    """Generate greeting message with agent name, version and current time."""
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
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone).isoformat(),
        "version": version.get_version(),
    }


if __name__ == "__main__":
    # Avvio dell'applicazione Flask
    app.run(host="0.0.0.0", port=5000) # nosec B104
