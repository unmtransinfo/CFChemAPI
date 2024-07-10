# blueprints/version.py
# This is the master blueprint directory,
# All new blueprints should be assigned here
from blueprints.bluprint import test_bluprint
from blueprints.hiers import hiers
from flask import Blueprint, current_app

# Set the route prefix based on version
version = Blueprint("version", __name__, url_prefix="/api/v2")


# Test Route
@version.route("/")
def hello():
    """Hello World!
      Returns a greeting to the user!
      ---
    responses:
      200:
        description: Returns the greeting.
      500:
        description: The app is misconfigured, APP_NAME config is missing or broken.
    """
    return f'{current_app.config.get("APP_NAME")} : Hello World!'


# Register routes
version.register_blueprint(test_bluprint)
version.register_blueprint(hiers)
