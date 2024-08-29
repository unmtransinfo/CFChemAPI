"""
@author Jack Ringer
Date: 8/29/2024
Description:
Generic utilities for processing SMILES strings.
"""

from typing import Optional

from rdkit import Chem


def get_canon_smiles(smiles: str) -> Optional[str]:
    """
    Get (RDKit) canonical SMILES.
    :param str smiles: input SMILES
    :return str: canonical SMILES, or None if invalid SMILES given.
    """
    if not isinstance(smiles, str):
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return Chem.MolToSmiles(mol, canonical=True)
    except Exception:
        return None
