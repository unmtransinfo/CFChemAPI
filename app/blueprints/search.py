# blueprints/search.py

from database.database import database
from flask import Blueprint, request
from utils.request_processing import int_check

search = Blueprint("search", __name__, url_prefix="/search")
from psycopg2 import sql


@search.route("/", methods=["GET"])
def index():
    # Limit the query size
    raw_user_input = request.args.get("query", type=str) or ""
    limit = int_check(request, "limit", 0, 1000, default_val=10)
    offset = int_check(request, "offset", 0, default_val=0)
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
