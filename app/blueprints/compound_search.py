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


def _get_smiles_list(request, limit: int = 1000):
    smiles_list = request.args.get("SMILES", type=str)
    if not smiles_list:
        return abort(400, "No SMILES provided")
    smiles_list = smiles_list.split(",")
    if len(smiles_list) > limit:
        return abort(
            400,
            f"Provided list of SMILES exceeded limit of {limit}. Please provide <= {limit} SMILES at a time.",
        )
    return smiles_list


def _get_associated_scaffolds_from_list(smiles_list: list[str]) -> dict[str, list]:
    """
    Helper function, returns a dictionary mapping SMILES to associated scaffolds + info.
    """
    result = {}

    for smiles in smiles_list:
        # original code uses ring_cutoff=30, hence why using it here
        scaf_res = get_scaffolds_single_mol(smiles, name="", ring_cutoff=30)
        if scaf_res == {}:
            # ignore invalid SMILES
            continue

        scaffolds = scaf_res["scaffolds"]
        scaffold_info_list = []
        for scafsmi in scaffolds:
            scaf_info = BadappleDB.search_scaffold(scafsmi)
            if len(scaf_info) < 1:
                scaf_info = {
                    "scafsmi": scafsmi,
                    "in_db": False,
                }
            else:
                scaf_info = dict(scaf_info[0])
                scaf_info["in_db"] = True
            scaffold_info_list.append(scaf_info)

        result[smiles] = scaffold_info_list
    return result


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
    smiles_list = _get_smiles_list(request)
    result = _get_associated_scaffolds_from_list(smiles_list)
    return jsonify(result)


@compound_search.route("/get_high_scores", methods=["GET"])
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
                "description": "A json object with all compounds and their highest-scoring scaffold + its pscore. If the compound has no scaffolds in the DB a score of 'None' is given."
            },
            400: {"description": "Malformed request error"},
        },
    }
)
def get_high_scores():
    """
    Return highest-scoring scaffold for each molecule.
    """
    smiles_list = _get_smiles_list(request)
    associated_scaffolds = _get_associated_scaffolds_from_list(smiles_list)
    result = []
    for smiles in associated_scaffolds.keys():
        scaffolds = associated_scaffolds[smiles]
        max_scaf_score = -1
        max_scaf_info = {}
        for scaf_info in scaffolds:
            if scaf_info["in_db"]:
                scaf_pscore = scaf_info["pscore"]
                if scaf_pscore is not None and scaf_pscore > max_scaf_score:
                    max_scaf_score = scaf_pscore
                    max_scaf_info = scaf_info
        if max_scaf_score == -1:
            max_scaf_score = None
        result.append(
            {
                "molecule_smiles": smiles,
                "highest_scoring_scaf": max_scaf_info,
            }
        )

    return jsonify(result)
