"""
@author Jack Ringer
Date: 8/28/2024
Description:
Blueprint for searching Badapple DB for data from compound inputs.
"""

from database.database import BadappleDB
from flasgger import swag_from
from flask import Blueprint, abort, jsonify, request
from utils.scaffold_utils import get_scaffolds_single_mol

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


@compound_search.route("/get_associated_scaffolds", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "SMILES",
                "in": "query",
                "type": "string",
                "required": True,
                "description": "List of compound SMILES, comma-separated. Invalid SMILES are ignored.",
            },
        ],
        "responses": {
            200: {
                "description": "A json object with all compounds and their associated scaffolds + their information. Note that if a scaffold is not present in the DB it will have an empty list instead of info."
            },
            400: {"description": "Malformed request error"},
        },
    }
)
def get_associated_scaffolds():
    """
    Return associated scaffolds + info on each.
    """
    smiles_list = request.args.get("SMILES", type=str)
    if not smiles_list:
        return abort(400, "No SMILES provided")

    smiles_list = smiles_list.split(",")
    result = {"scaffolds_info": []}

    for smiles in smiles_list:
        # original code uses ring_cutoff=30, hence why using it here
        scaf_res = get_scaffolds_single_mol(smiles, name="", ring_cutoff=30)
        if scaf_res == {}:
            # ignore invalid SMILES
            continue

        scaffolds = scaf_res["scaffolds"]
        scaffold_info = {
            "molecule_smiles": smiles,
            "scaffolds": [],
        }
        for scafsmi in scaffolds:
            scaf_info = BadappleDB.search_scaffold(scafsmi)
            if len(scaf_info) < 1:
                scaf_info = {
                    "scafsmi": scafsmi,
                    "pscore": None,
                    "prank": None,
                    "in_drug": None,
                    "in_db": False,
                }
            else:
                scaf_info = dict(scaf_info[0])
                scaf_info["in_db"] = True
            scaffold_info["scaffolds"].append(scaf_info)

        result["scaffolds_info"].append(scaffold_info)

    return jsonify(result)
