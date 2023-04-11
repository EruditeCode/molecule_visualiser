"""
Geometric functions for molecule manipulation.
"""

import numpy as np
import math

def rotate_y(angle, vector):
	rotate_by = np.matrix([[math.cos(angle), 0, math.sin(angle)],
				[0, 1, 0], 
				[-math.sin(angle), 0, math.cos(angle)]])
	result = np.matmul(vector, rotate_by)
	return result

def rotate_x(angle, vector):
	rotate_by = np.matrix([[1, 0, 0],
				[0, math.cos(angle), -math.sin(angle)], 
				[0, math.sin(angle), math.cos(angle)]])
	result = np.matmul(vector, rotate_by)
	return result

def recenter_molecule(position, molecule):
	sub_matrix = np.matrix([position[0], position[1], 0])
	for atom in molecule.atoms:
		atom.vector = atom.vector - sub_matrix
		atom.fixed_vector = atom.vector.copy()
