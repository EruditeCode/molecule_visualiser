import pygame as pg
import math
import numpy as np
from molecules import methane, benzene, paracetamol, penicillin, azulene
from geometric_functions import rotate_y, rotate_x, recenter_molecule
from support_classes import Molecule, Molecule_Renderer


def main():
	pg.init()
	WIDTH, HEIGHT = 900, 600
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	bg = pg.Surface((WIDTH, HEIGHT))
	bg.fill((130,150,150))

	# Load molecule using molecule class.
	molecule = Molecule(azulene, 'Azulene')
	molecule_renderer = Molecule_Renderer(molecule, screen, WIDTH, HEIGHT)

	# Flags and Placeholders
	r_start, r_end = False, False
	r_pos = None
	
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
				if event.button == 3:
					position = pg.mouse.get_pos()
					position = ((position[0]-WIDTH//2)/molecule_renderer.mag, (position[1]-HEIGHT//2)/molecule_renderer.mag)
					recenter_molecule(position, molecule)
			if event.type == pg.MOUSEWHEEL:
				molecule_renderer.mag += event.y

		# Update molecule position.
		if r_start:
			temp_pos = pg.mouse.get_pos()
			dx = r_pos[0]-temp_pos[0]
			dy = r_pos[1]-temp_pos[1]
			
			angle = math.pi * (dy / HEIGHT)
			for atom in molecule.atoms:
				atom.vector = rotate_x(-angle, atom.fixed_vector)
			
			angle = math.pi * (dx / WIDTH)
			for atom in molecule.atoms:
				atom.vector = rotate_y(angle, atom.vector)
			
			if r_end:
				for atom in molecule.atoms:
					atom.fixed_vector = atom.vector.copy()
				r_start, r_end = False, False
				r_pos = None


		# Update molecule position, orientation etc.
		molecule.reorder_atoms()

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule using the molecule renderer.
		molecule_renderer.draw()
		
		pg.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()

