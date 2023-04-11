import numpy as np
import pygame as pg
from atom_properties import covalent_radii, atom_color


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


	def reorder_atoms(self):
		self.atoms.sort(key=lambda x: x.vector[0,2], reverse=False)


	def draw(self, screen, magnification, width, height):
		# Drawing bonds.
		for bond in self.bonds:
			x1 = bond.atoms[0].vector[0,0]*magnification+width//2
			y1 = bond.atoms[0].vector[0,1]*magnification+height//2
			x2 = bond.atoms[1].vector[0,0]*magnification+width//2
			y2 = bond.atoms[1].vector[0,1]*magnification+height//2
			pg.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), 5)
		# Drawing atoms.
		for atom in self.atoms:
			x = atom.vector[0,0]*magnification+width//2
			y = atom.vector[0,1]*magnification+height//2
			if atom.element == "H":
				radius = (covalent_radii[atom.element]*magnification*0.4) + atom.vector[0,2]
			else:
				radius = (covalent_radii[atom.element]*magnification*0.3) + atom.vector[0,2]
			pg.draw.circle(screen, atom_color[atom.element], (x, y), radius)
