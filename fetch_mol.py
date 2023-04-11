"""
A module to enable a molecule to be found either locally or
remotely from the PubChem database. If it is found remotely
a copy is made locally for redundancy. The data is prepared
and returned in a format viable for the molecule constructor.
"""

import json
import pubchempy as pcp

def fetch_mol():
	while True:
		user_input = input('Please enter the molecule name: ').lower()
		if user_input == "exit":
			exit()
		else:
			mol_data = check_local_database(user_input)
			if mol_data:
				return mol_data
			mol_data = check_remote_database(user_input)
			if mol_data:
				add_to_local_database(user_input, mol_data)
				return mol_data
		print(f'Unfortunately {user_input} could not be found.')

def check_local_database(mol_name):
	with open('molecules.json', 'r') as f:
		database = json.load(f)
	if mol_name in database:
		return database[mol_name]

def check_remote_database(mol_name):
	compounds = pcp.get_compounds(mol_name, 'name', record_type='3d')
	if len(compounds) >= 1:
		molecule_dict = {'mol_id':compounds[0].cid, 'atoms':[], 'bonds':[]}
		for atom in compounds[0].atoms:
			molecule_dict['atoms'].append([atom.aid, atom.element, atom.x, atom.y, atom.z])
		for bond in compounds[0].bonds:
			molecule_dict['bonds'].append([bond.aid1, bond.aid2, bond.order])
		return molecule_dict

def add_to_local_database(mol_name, mol_data):
	with open('molecules.json', 'r') as f:
		database = json.load(f)
		database[mol_name] = mol_data
	with open('molecules.json', 'w') as f:
		json.dump(database, f)
