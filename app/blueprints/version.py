# blueprints/version.py
# This is the master blueprint directory,
# All new blueprints should be assigned here
from blueprints.drugcentral import drugcentral
from blueprints.lincs import lincs
from blueprints.search import search
from flask import Blueprint


def register_routes(app, version_url_prefix: str):
    version = Blueprint("version", __name__, url_prefix=version_url_prefix)
    version.register_blueprint(lincs)
    version.register_blueprint(drugcentral)
    version.register_blueprint(search)
    app.register_blueprint(version)
