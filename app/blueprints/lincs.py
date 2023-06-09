# blueprints/lincs.py

from flask import Blueprint

lincs = Blueprint('lincs', __name__, url_prefix="/lincs")

lincsCollection = ['1', '2', '3']

@lincs.route('/')
def index():
    return lincsCollection