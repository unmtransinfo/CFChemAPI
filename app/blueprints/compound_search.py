"""
@author Jack Ringer
Date: 8/28/2024
Description:
Blueprint for searching Badapple DB for data from compound inputs.
"""

from database.database import BadappleDB
from flasgger import swag_from
from flask import Blueprint, jsonify, request

compound_search = Blueprint("compound_search", __name__, url_prefix="/compound_search")


@compound_search.route("/get_isosmi", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "CID",
                "in": "query",
                "type": "integer",
                "required": True,
                "description": "PubChem CID (Compound ID)",
            },
        ],
        "responses": {
            200: {
                "description": "A json object with the Isomeric SMILES of the CID, or nothing if CID not in DB"
            },
            400: {"description": "Malformed request error"},
        },
    }
)
def get_isosmi():
    """
    Return Isomeric SMILES of a given CID.
    """
    cid = request.args.get("CID", type=int)
    result = BadappleDB.index_compound(cid)
    return jsonify(result)
