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


class Molecule_Renderer:
	"""
		This class is responsible for all drawing action which
		also involves handling flags e.g. show hydrogen atoms,
		show bonds with free rotation, draw space filling model...
		many more to add
	"""
	def __init__(self, molecule, screen, width, height):
		self.molecule = molecule
		self.screen = screen
		self.center = (width//2, height//2)

		# Properties
		self.mag = 100
		self.show_H = True
		self.show_free_rotation = False

	def draw(self, magnification):
		# Have to draw any bonds connected to an atom before drawing the atom.
		available_bonds = self.molecule.bonds.copy()
		for atom in self.molecule.atoms:
			for i in range(len(available_bonds)-1, -1, -1):
				if atom in available_bonds[i].atoms:
					self.draw_bond(available_bonds[i], magnification)
					available_bonds.pop(i)
			self.draw_atom(atom, magnification)

	def draw_bond(self, bond, magnification):
		x1 = bond.atoms[0].vector[0,0]*magnification+self.center[0]
		y1 = bond.atoms[0].vector[0,1]*magnification+self.center[1]
		x2 = bond.atoms[1].vector[0,0]*magnification+self.center[0]
		y2 = bond.atoms[1].vector[0,1]*magnification+self.center[1]
		pg.draw.line(self.screen, (255,255,255), (x1, y1), (x2, y2), 5)

	def draw_atom(self, atom, magnification):
		x = atom.vector[0,0]*magnification+self.center[0]
		y = atom.vector[0,1]*magnification+self.center[1]
		num = 0.4 if (atom.element == "H") else 0.3
		radius = (covalent_radii[atom.element]*magnification*num) + atom.vector[0,2]
		pg.draw.circle(self.screen, atom_color[atom.element], (x, y), radius)
