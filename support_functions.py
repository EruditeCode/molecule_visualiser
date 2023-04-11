from pubchem_request import make_request
from molecules import methane, benzene, paracetamol, penicillin, azulene

# The get molecule function can be updated to automatically check the local repo before making a request...
# if a new molecule is requested can be added to the local repo thus reducing load on the pubchem database...

# Split this to a specific file for get molecule which can also be used to see the local stored molecules...

def get_molecule():
	while True:
		print("Would you like to get molecule data from a local repository (1) or the PubChem database (2)?")
		choice = input()
		if choice == "1":
			molecule = local_request()
			return molecule
		elif choice == "2":
			molecule = make_request()
			return molecule
		elif choice == "exit":
			exit()
		else:
			print("Invalid response, type 'exit' to close.")

def local_request():
	# This is a poor implementation, will be fixed later!
	print("Type molecule name for request:")
	name = input()
	if name == "exit":
		exit()
	else:
		if name == "methane":
			return methane
		elif name == "benzene":
			return benzene
		elif name == "paracetamol":
			return paracetamol
		elif name == "penicillin":
			return penicillin
		elif name == "azulene":
			return azulene
