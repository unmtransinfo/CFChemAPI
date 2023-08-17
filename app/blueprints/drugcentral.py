# blueprints/drugcentral.py

from flask import Blueprint
from database.database import database
drugcentral = Blueprint('drugcentral', __name__, url_prefix="/drugcentral")
api = Api(app)

@drugcentral.route('/<mol_id>')
@drugcentral.route('/')
def index(mol_id = None):
    return database.index('drugcentral', mol_id)