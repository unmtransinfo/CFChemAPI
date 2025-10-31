# blueprints/lincs.py

from typing import Optional

from database.database import database
from flask import Blueprint

lincs = Blueprint("lincs", __name__, url_prefix="/lincs")


@lincs.route("/<mol_id>", methods=["GET"])
@lincs.route("/", methods=["GET"])
def index(mol_id: Optional[int] = None):
    return database.index("lincs", mol_id)
