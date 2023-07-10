# blueprints/drugcentral.py

from flask import Blueprint, request
from database.database import database
drugcentral = Blueprint('drugcentral', __name__, url_prefix="/drugcentral")


@drugcentral.route('/')
def index():
    limit = request.args.get('limit', type=int) or 10
    offset = request.args.get('offset', type=int) or 0
    drugcentralCollection = database.select("""
    SELECT * FROM drugcentral
    LIMIT %(limit)s
    OFFSET %(offset)s
    """, {'limit': limit, 'offset': offset})
    return drugcentralCollection