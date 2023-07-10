# blueprints/lincs.py

from flask import Blueprint
from database.database import database
lincs = Blueprint('lincs', __name__, url_prefix="/lincs")


@lincs.route('/<mol_id>')
@lincs.route('/')
def index(mol_id = None):
    return database.index('lincs', mol_id)