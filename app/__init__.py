from flask import Flask

app = Flask(__name__)

# Secret key for session storage (move to env var in prod)
app.secret_key = "super_secret_key"

# Import routes last to avoid circular import errors
from app import routes
