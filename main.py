import pygame as pg
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

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule.
		# Drawing bonds.
		for atom in molecule:
			for key in atom.bonds.keys():
				pg.draw.line(screen, (255,255,255), (atom.x+WIDTH//2, atom.y+HEIGHT//2), (molecule[key-1].x+WIDTH//2, molecule[key-1].y+HEIGHT//2), 5)
		# Drawing atoms.
		for atom in molecule:
			pg.draw.circle(screen, (255,255,255), (atom.x+WIDTH//2,atom.y+HEIGHT//2), 10)
		
		pg.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()

