# blueprints/search.py

from database.database import database
from flask import Blueprint, request

search = Blueprint("search", __name__, url_prefix="/search")
from psycopg2 import sql


@search.route("/")
def index():
    """Endpoint returning lincs objects based on search parameter (query)
    This endpoint allows you to return a list of Lincs objects.
    ---
    parameters:
      - name: query
        in: query
        type: string
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
        description: A list of Lincs objects
      400:
        description: Malformed request error
    """

    # Limit the query size
    raw_user_input = request.args.get("query", type=str) or ""
    limit = request.args.get("limit", type=int) or 10
    offset = request.args.get("offset", type=int) or 0
    # Build the query
    user_input = "%" + raw_user_input + "%"
    columns = ["moa", "cansmi", "inchi_key", "lcs_id", "pert_name", "smiles", "target"]
    where_clauses = [
        sql.SQL("{} LIKE %s").format(sql.Identifier(col)) for col in columns
    ]
    query = sql.SQL(
        """
        SELECT * FROM {table}
        WHERE {where_clause}
        LIMIT %s OFFSET %s
    """
    ).format(
        table=sql.Identifier("lincs"), where_clause=sql.SQL(" OR ").join(where_clauses)
    )
    query_vars = [user_input] * len(columns) + [limit, offset]
    searchCollection = database.select(query, query_vars)
    return searchCollection
