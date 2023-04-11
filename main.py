import pygame as pg
import math
import numpy as np
from molecules import methane, benzene, paracetamol, penicillin, azulene
from geometric_functions import rotate_y, rotate_x, recenter_molecule
from atom_properties import covalent_radii, atom_color
from support_classes import Molecule


def main():
	pg.init()
	WIDTH, HEIGHT = 900, 600
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	bg = pg.Surface((WIDTH, HEIGHT))
	bg.fill((130,150,150))

	# Load molecule using molecule class.
	molecule = Molecule(azulene, 'Azulene')

	mag = 100
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
					position = ((position[0]-WIDTH//2)/mag, (position[1]-HEIGHT//2)/mag)
					recenter_molecule(position, molecule)
			if event.type == pg.MOUSEWHEEL:
				mag += event.y

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


		# Prior to displaying, order atoms in molecule by z-position.
		molecule.atoms.sort(key=lambda x: x.vector[0].item(2), reverse=False)

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule.
		# Drawing bonds.
		for bond in molecule.bonds:
			x1 = bond.atoms[0].vector[0,0]*mag+WIDTH//2
			y1 = bond.atoms[0].vector[0,1]*mag+HEIGHT//2
			x2 = bond.atoms[1].vector[0,0]*mag+WIDTH//2
			y2 = bond.atoms[1].vector[0,1]*mag+HEIGHT//2
			pg.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), 5)
		# Drawing atoms.
		for atom in molecule.atoms:
			x = atom.vector[0,0]*mag+WIDTH//2
			y = atom.vector[0,1]*mag+HEIGHT//2
			if atom.element == "H":
				radius = (covalent_radii[atom.element]*mag*0.4) + (atom.vector[0].item(2))
			else:
				radius = (covalent_radii[atom.element]*mag*0.3) + (atom.vector[0].item(2))
			pg.draw.circle(screen, atom_color[atom.element], (x, y), radius)
		
		pg.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()

