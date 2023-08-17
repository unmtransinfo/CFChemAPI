# blueprints/drugcentral.py

from flask import Blueprint
from database.database import database
drugcentral = Blueprint('drugcentral', __name__, url_prefix="/drugcentral")


@drugcentral.route('/<mol_id>')
@drugcentral.route('/')
def index(mol_id = None):
    # Create an array of searchable fields
    # These fields can be matched to allow for save 'AsIs' passing through the query
    searchable = [
        
    ]
    return database.index('drugcentral', mol_id)