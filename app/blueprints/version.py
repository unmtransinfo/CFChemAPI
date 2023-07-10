# blueprints/version.py
# This is the master blueprint directory,
# All new blueprints should be assigned here
from flask import Blueprint, current_app
from blueprints.lincs import lincs
from blueprints.drugcentral import drugcentral
# Set the route prefix based on version
version = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

# Test Route
@version.route('/')
def hello():
	return f'{current_app.config.get("APP_NAME")} : Hello World!'

# Register routes
version.register_blueprint(lincs)
version.register_blueprint(drugcentral)