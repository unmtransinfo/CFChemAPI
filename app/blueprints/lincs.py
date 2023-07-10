# blueprints/lincs.py

from flask import Blueprint, request
from database.database import database
lincs = Blueprint('lincs', __name__, url_prefix="/lincs")


@lincs.route('/')
def index():
    limit = request.args.get('limit', type=int) or 10
    offset = request.args.get('offset', type=int) or 0
    lincsCollection = database.select("""
    SELECT * FROM lincs
    LIMIT %(limit)s
    OFFSET %(offset)s
    """, {'limit': limit, 'offset': offset})
    return lincsCollection