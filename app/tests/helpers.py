"""
@author Jack Ringer
Date: 12/16/2025
Description:
Helper functions for tests
"""


def validate_keys(d: dict, expected_keys: list):
    # returned value should contain all expected_keys
    assert set(expected_keys).issubset(d.keys())


def validate_drugcentral_keys(d: dict):
    """Validate keys returned from drugcentral endpoint"""
    expected_keys = [
        "cansmi",
        "cas_reg_no",
        "formula",
        "id",
        "inchi",
        "inchikey",
        "mol_id",
        "molweight",
        "name",
        "smiles",
    ]
    validate_keys(d, expected_keys)
