class Atom:
	def __init__(self, element, x, y, z, bonds):
		self.element = element
		self.x = x
		self.y = y
		self.z = z
		self.bonds = {bond[0]:bond[1] for bond in bonds}