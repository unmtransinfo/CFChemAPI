"""
@author Jack Ringer
Date: 8/29/2024
Description:
Functions related to getting scaffolds from input molecule(s).
"""

import pandas as pd
import scaffoldgraph as sg
from loguru import logger


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


def get_mol2scaf_dict(network: HierSTopLevel) -> dict[str, list[str]]:
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


def get_scaffolds_single_mol(mol_smiles: str, name: str, ring_cutoff: int):
    # setup network
    smiles_dict = {"Smiles": [mol_smiles], "Name": [name]}
    smiles_df = pd.DataFrame.from_dict(smiles_dict)
    network = HierSTopLevel.from_dataframe(smiles_df, ring_cutoff=ring_cutoff)
    # get scaffolds, convert to json for use with API / UI
    mol2scafs = get_mol2scaf_dict(network)
    if len(mol2scafs.keys()) < 1:
        return {}  # likely invalid Smiles
    # indexing [0] bc we only have 1 input molecule
    result = {
        "molecule_cansmi": list(mol2scafs.keys())[0],
        "scaffolds": list(mol2scafs.values())[0],
    }
    return result
