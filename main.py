import pygame as pg
import math
import numpy as np
from molecules import benzene, methane, covalent_radii, atom_color
from class_Atom import Atom


def main():
	pg.init()
	WIDTH, HEIGHT = 900, 600
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	bg = pg.Surface((WIDTH, HEIGHT))
	bg.fill((20,20,20))

	# Load molecule using atom class.
	molecule = []
	for atom in methane:
		molecule.append(Atom(atom[0], atom[1], atom[2], atom[3], atom[4]))

	MAG = 100
	r_start = False
	r_pos = None
	r_end = False
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1 and not r_start:
					r_start, r_pos = True, pg.mouse.get_pos()
			if event.type == pg.MOUSEBUTTONUP:
				if event.button == 1 and r_start:
					r_end = True
			if event.type == pg.MOUSEWHEEL:
				MAG += event.y

		# Update molecule position.
		if r_start:
			temp_pos = pg.mouse.get_pos()
			dx = r_pos[0]-temp_pos[0]
			dy = r_pos[1]-temp_pos[1]
			
			angle = math.pi * (dy / HEIGHT)
			for atom in molecule:
				atom.vector = rotate_x(-angle, atom.fixed_vector)
			
			angle = math.pi * (dx / WIDTH)
			for atom in molecule:
				atom.vector = rotate_y(angle, atom.vector)
			if r_end:
				for atom in molecule:
					atom.fixed_vector = atom.vector.copy()
				# Reset flags...
				r_start, r_end = False, False
				r_pos = None


		# Prior to displaying, order atoms in molecule by z-position.

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule.
		# Drawing bonds.
		for atom in molecule:
			for key in atom.bonds.keys():
				x1 = atom.vector[0].item(0)*MAG+WIDTH//2
				y1 = atom.vector[0].item(1)*MAG+HEIGHT//2
				x2 = molecule[key-1].vector[0].item(0)*MAG+WIDTH//2
				y2 = molecule[key-1].vector[0].item(1)*MAG+HEIGHT//2
				pg.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), 5)
		# Drawing atoms.
		for atom in molecule:
			x = atom.vector[0].item(0)*MAG+WIDTH//2
			y = atom.vector[0].item(1)*MAG+HEIGHT//2
			radius = MAG//5+atom.vector[0].item(2)*MAG//20
			pg.draw.circle(screen, (255,255,255), (x, y), radius) #12
		
		pg.display.update()
		clock.tick(60)


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


if __name__ == "__main__":
	main()

