import math
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
		self.free = True

	def check_if_rotatable(self, bonds):
		# NOT AN ACCURATE OR VIABLE CHECK AT PRESENT - CONSIDERATION REQUIRED!
		for bond in bonds:
			if any(atom in self.atoms for atom in bond.atoms) and bond.order > 1:
				self.free = False


class Molecule:
	def __init__(self, molecule, name=None):
		self.id = molecule['mol_id']
		self.name = name if name else None
		self.atoms = []
		self.bonds = []
		self.constructor(molecule)
		self.spin = False

	def constructor(self, molecule):
		for atom in molecule['atoms']:
			self.atoms.append(Atom(atom[0], atom[1], atom[2], atom[3], atom[4]))
		for bond in molecule['bonds']:
			atom_a, atom_b = self.find_bonding_atoms(bond[0], bond[1])
			self.bonds.append(Bond(atom_a, atom_b, bond[2]))
		for bond in self.bonds:
			bond.check_if_rotatable(self.bonds)

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
		also involves handling flags e.g. showing hydrogen atoms,
		multiple bonds or bonds with free rotation.
	"""
	def __init__(self, molecule, screen, width, height):
		self.molecule = molecule
		self.screen = screen
		self.center = (width//2, height//2)

		# Properties and Settings
		self.mag = 100
		self.show_multiple_bonds = False
		self.show_H = True
		self.show_free_rotation = False

	def draw(self):
		if self.show_H:
			available_bonds = self.molecule.bonds.copy()
			available_atoms = self.molecule.atoms.copy()
		else:
			available_bonds = [bond for bond in self.molecule.bonds if bond.atoms[0].element != "H" and bond.atoms[1].element != "H"]
			available_atoms = [atom for atom in self.molecule.atoms if atom.element != "H"]
		
		for atom in available_atoms:
			for i in range(len(available_bonds)-1, -1, -1):
				if atom in available_bonds[i].atoms:
					self.draw_bond(available_bonds[i])
					available_bonds.pop(i)
			self.draw_atom(atom)
		
	def draw_bond(self, bond):
		x1 = bond.atoms[0].vector[0,0]*self.mag+self.center[0]
		y1 = bond.atoms[0].vector[0,1]*self.mag+self.center[1]
		x2 = bond.atoms[1].vector[0,0]*self.mag+self.center[0]
		y2 = bond.atoms[1].vector[0,1]*self.mag+self.center[1]
		if bond.order > 1 and self.show_multiple_bonds:
			if bond.order % 2 != 0:
				pg.draw.line(self.screen, (255,255,255), (x1, y1), (x2, y2), 5)

			bond_spread = bond.order * 5
			r = bond_spread/2
			# HUGE MESSY SECTION - NEEDS TIDYING UP!
			# Line between atoms
			m = (y2 - y1)/(x2 - x1)
			if m != 0:
				c = y1 - (m * x1)
				# Line perpendicular at atom 1...
				m_perp = (-1/m)
				c_perp = y1 - m_perp*x1
				# Need to find two points
				a = 1 + m_perp**2
				b = 2*m_perp*c_perp - 2*x1 - 2*y1*m_perp
				c = c_perp**2 + x1**2 + y1**2 - r**2 - 2*y1*c_perp
				x1_perp_1 = (-b + ((b**2)-4*a*c)**0.5)/(2*a)
				y1_perp_1 = m_perp*x1_perp_1 + c_perp
				x1_perp_2 = (-b - ((b**2)-4*a*c)**0.5)/(2*a)
				y1_perp_2 = m_perp*x1_perp_2 + c_perp

				c_perp = y2 - m_perp*x2
				# Need to find two points
				a = 1 + m_perp**2
				b = 2*m_perp*c_perp - 2*x2 - 2*y2*m_perp
				c = c_perp**2 + x2**2 + y2**2 - r**2 - 2*y2*c_perp
				x2_perp_1 = (-b + ((b**2)-4*a*c)**0.5)/(2*a)
				y2_perp_1 = m_perp*x2_perp_1 + c_perp
				x2_perp_2 = (-b - ((b**2)-4*a*c)**0.5)/(2*a)
				y2_perp_2 = m_perp*x2_perp_2 + c_perp

				pg.draw.line(self.screen, (255,255,255), (x1_perp_1, y1_perp_1), (x2_perp_1, y2_perp_1), 5)
				pg.draw.line(self.screen, (255,255,255), (x1_perp_2, y1_perp_2), (x2_perp_2, y2_perp_2), 5)

		else:
			if self.show_free_rotation and bond.free:
				pg.draw.line(self.screen, (255,0,0), (x1, y1), (x2, y2), 5)
			else:
				pg.draw.line(self.screen, (255,255,255), (x1, y1), (x2, y2), 5)

	def draw_atom(self, atom):
		x = atom.vector[0,0]*self.mag+self.center[0]
		y = atom.vector[0,1]*self.mag+self.center[1]
		num = 0.4 if (atom.element == "H") else 0.3
		radius = (covalent_radii[atom.element]*self.mag*num) + atom.vector[0,2]
		pg.draw.circle(self.screen, atom_color[atom.element], (x, y), radius)
