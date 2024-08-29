"""
@author Jack Ringer
Date: 8/29/2024
Description:
Blueprint for searching Badapple DB for data from scaffold inputs.
"""

from database.database import BadappleDB
from flasgger import swag_from
from flask import Blueprint, jsonify, request

scaffold_search = Blueprint("scaffold_search", __name__, url_prefix="/scaffold_search")


@scaffold_search.route("/get_scaffold_info", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "SMILES",
                "in": "query",
                "type": "string",
                "required": True,
                "description": "SMILES of scaffold",
            },
        ],
        "responses": {
            200: {
                "description": "A json object with the scaffold's canonicalized SMILES (from DB), pscore, prank, and in_drug info. Nothing if scaffold not in DB"
            },
            400: {"description": "Malformed request error (likely invalid SMILES)"},
        },
    }
)
def get_scaffold_info():
    """
    Return information about a given scaffold from the DB.
    """
    scaf_smiles = request.args.get("SMILES", type=str)
    # canonicalize given SMILES using RDKit
    result = BadappleDB.search_scaffold(scaf_smiles)
    return jsonify(result)
