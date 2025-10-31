# blueprints/drugcentral.py

from typing import Optional

from database.database import database
from flask import Blueprint

drugcentral = Blueprint("drugcentral", __name__, url_prefix="/drugcentral")


@drugcentral.route("/<mol_id>", methods=["GET"])
@drugcentral.route("/", methods=["GET"])
def index(mol_id: Optional[int] = None):
    return database.index("drugcentral", mol_id)
