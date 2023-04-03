import pygame as pg
import math
import numpy as np
from molecules import benzene, methane
from class_Atom import Atom

# Need to magnify the coordinates when viewing...
MAG = 100

def main():
	pg.init()
	WIDTH, HEIGHT = 900, 600
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	bg = pg.Surface((WIDTH, HEIGHT))
	bg = pg.transform.scale(bg, (WIDTH, HEIGHT))

	# Load molecule using atom class.
	molecule = []
	for atom in benzene:
		molecule.append(Atom(atom[0], atom[1]*MAG, atom[2]*MAG, atom[3]*MAG, atom[4]))

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


		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule.
		# Drawing bonds.
		for atom in molecule:
			for key in atom.bonds.keys():
				pg.draw.line(screen, (255,255,255), (atom.vector[0].item(0)+WIDTH//2, atom.vector[0].item(1)+HEIGHT//2), (molecule[key-1].vector[0].item(0)+WIDTH//2, molecule[key-1].vector[0].item(1)+HEIGHT//2), 5)
		# Drawing atoms.
		for atom in molecule:
			pg.draw.circle(screen, (255,255,255), (atom.vector[0].item(0)+WIDTH//2,atom.vector[0].item(1)+HEIGHT//2), 10)
		
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

