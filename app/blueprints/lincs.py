# blueprints/lincs.py

from flask import Blueprint
from database.database import database
lincs = Blueprint('lincs', __name__, url_prefix="/lincs")


@lincs.route('/')
def index():
    lincsCollection = database.select("""
    SELECT * FROM lincs LIMIT 10
    """)
    return lincsCollection