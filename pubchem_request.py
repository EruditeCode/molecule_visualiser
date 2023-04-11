import pubchempy as pcp

def make_request():
	while True:
		print("Type molecule name for request:")
		name = input()
		if name == "exit":
			exit()
		else:
			cs = pcp.get_compounds(name, 'name', record_type='3d')

		if len(cs) == 1:
			molecule_dict = {'mol_id':0, 'atoms':[], 'bonds':[]}
			for cmpd in cs:
				molecule_dict['mol_id'] = cmpd.cid
				for atom in cmpd.atoms:
					molecule_dict['atoms'].append([atom.aid, atom.element, atom.x, atom.y, atom.z])
				for bond in cmpd.bonds:
					molecule_dict['bonds'].append([bond.aid1, bond.aid2, bond.order])
			return molecule_dict
		else:
			print(f"{len(cs)} compounds have been found for that given name.")
