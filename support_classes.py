import numpy as np

class Atom:
	def __init__(self, atom_id, element, x, y, z):
		self.id = atom_id
		self.element = element
		self.fixed_vector = np.matrix([x, y, z])
		self.vector = np.matrix([x, y, z])

class Bond:
	def __init__(self, atom_a, atom_b, bond_order):
		self.atoms = [atom_a, atom_b]
		self.order = bond_order

class Molecule:
	def __init__(self, molecule, name=None):
		self.id = None
		self.name = name if name else None
		self.atoms = []
		self.bonds = []
		self.constructor(molecule)

	def constructor(self, molecule):
		# Log the id from source - PubChem.
		self.id = molecule['mol_id']
		for atom in molecule['atoms']:
			self.atoms.append(Atom(atom[0], atom[1], atom[2], atom[3], atom[4]))
		for bond in molecule['bonds']:
			atom_a, atom_b = self.find_bonding_atoms(bond[0], bond[1])
			self.bonds.append(Bond(atom_a, atom_b, bond[2]))

	def find_bonding_atoms(self, id_a, id_b):
		for atom in self.atoms:
			if atom.id == id_a:
				atom_a = atom
			elif atom.id == id_b:
				atom_b = atom
		return atom_a, atom_b


	def update(self):
		# A function to handle drawing updates...
		pass

	def reorder_atoms(self):
		pass

	def reorder_bonds(self):
		pass
