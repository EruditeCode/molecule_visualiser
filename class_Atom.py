import numpy as np

class Atom:
	def __init__(self, element, x, y, z, bonds):
		self.element = element
		self.fixed_vector = np.matrix([x, y, z])
		self.vector = np.matrix([x, y, z])
		self.bonds = {bond[0]:bond[1] for bond in bonds}
