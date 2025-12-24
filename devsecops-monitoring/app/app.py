import logging
import os
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Log file path
LOG_FILE = os.path.join(os.path.dirname(__file__), "app.log")

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Rate limiter configuration
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

@app.route("/")
def home():
    app.logger.info("User accessed home page")
    return "Hello DevSecOps"

@app.route("/login")
@limiter.limit("5 per minute")
def login():
    app.logger.warning(
        "Failed login attempt from IP %s",
        request.remote_addr
    )
    return "Login failed", 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
