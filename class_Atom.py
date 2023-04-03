import numpy as np

class Atom:
	def __init__(self, element, x, y, z, bonds):
		self.element = element
		# Can manipulate this vector to render the image in different dimensions.
		self.vector = np.matrix([x, y, z])
		print(self.vector)
		self.bonds = {bond[0]:bond[1] for bond in bonds}