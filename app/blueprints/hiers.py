"""
@author Jack Ringer
Date: 7/10/2024
Description:
HierS Python code.
"""

import json

import pandas as pd
import scaffoldgraph as sg
from flask import Blueprint, request
from loguru import logger

hiers = Blueprint("hiers", __name__, url_prefix="/hiers")


class HierSTopLevel(sg.HierS):
    def _process_no_top_level(self, molecule):
        """Private: Process molecules with no top-level scaffold.
        Modified from original code so that molecules with no top-level
        scaffold are still included in the graph.
        Parameters
        ----------
        molecule : rdkit.Chem.rdchem.Mol
            An rdkit molecule determined to have no top-level scaffold.
        """
        name = molecule.GetProp("_Name")
        logger.info(f"No top level scaffold for molecule: {name}")
        self.graph["num_linear"] = self.graph.get("num_linear", 0) + 1
        self.add_molecule_node(
            molecule,
        )
        return None


def is_valid_scaf(can_smiles: str):
    if len(can_smiles) == 0:
        # empty string given
        return False
    elif can_smiles == "c1ccccc1" or can_smiles == "C1=CC=CC=C1":
        # benzene excluded from scaffolds
        return False
    return True


def get_scafs(network: HierSTopLevel) -> dict[str, list[str]]:
    mol_to_scafs = {}
    for mol_node in network.get_molecule_nodes(data=True):
        mol_name = mol_node[0]
        mol_smiles = mol_node[1]["smiles"]
        mol_to_scafs[mol_smiles] = []
        mol_scaffolds = network.get_scaffolds_for_molecule(mol_name, data=True)
        for scaf_node in mol_scaffolds:
            scaf_smile = scaf_node[0]
            if is_valid_scaf(scaf_smile):
                mol_to_scafs[mol_smiles].append(scaf_smile)
    return mol_to_scafs


@hiers.route("/", methods=["GET"])
def index():
    """
    Return scaffolds for a given list of molecules.
    Scaffolds are derived using the HierS algorithm:
    https://pubs.acs.org/doi/10.1021/jm049032d.
    """
    mol_smiles = request.args.get("smiles", type=str)
    name = request.args.get("name", type=str)
    # setup network
    smiles_dict = {"Smiles": [mol_smiles], "Name": [name]}
    smiles_df = pd.DataFrame.from_dict(smiles_dict)
    network = HierSTopLevel.from_dataframe(smiles_df, ring_cutoff=10)
    # get scaffolds, convert to json for use with API / UI
    mol2scafs = get_scafs(network)
    mol2scafs_json = json.dumps(mol2scafs)
    return mol2scafs_json
