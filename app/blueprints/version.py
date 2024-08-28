# blueprints/version.py
# This is the master blueprint directory,
# All new blueprints should be assigned here
from blueprints.compound_search import compound_search
from blueprints.hiers import hiers
from flasgger import swag_from
from flask import Blueprint, current_app

# Set the route prefix based on version
version = Blueprint("version", __name__, url_prefix="/api/v1")


# Test Route
@version.route("/")
@swag_from(
    {
        "responses": {
            200: {"description": "Returns the greeting."},
            500: {
                "description": "The app is misconfigured, APP_NAME config is missing or broken."
            },
        }
    }
)
def hello():
    """
    Hello World!
    Returns a greeting to the user!
    """
    return f'{current_app.config.get("APP_NAME")} : Hello World!'


# Register routes
version.register_blueprint(hiers)
version.register_blueprint(compound_search)
