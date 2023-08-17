# blueprints/drugcentral.py

from flask import Blueprint
from database.database import database
drugcentral = Blueprint('drugcentral', __name__, url_prefix="/drugcentral")

@drugcentral.route('/<mol_id>')
@drugcentral.route('/')
def index(mol_id = None):
    """Endpoint returning a list of Drugcentral objects
    This endpoint allows you to return a list of Drugcentral objects.
    Optionally, you can pass an integer for the mol_id to select an individual record.
    ---
    parameters:
      - name: mol_id
        in: path
        type: int
        required: false
      - name: limit
        in: query
        type: int
        default: 10
        required: false
      - name: offset
        in: query
        type: int
        default: 0
        required: false
    responses:
      200:
        description: A list of Drugcentral objects
      400:
        description: Malformed request error
    """
    return database.index('drugcentral', mol_id)