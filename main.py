import pygame as pg
from molecules import benzene

# Need to magnify the coordinates when viewing...
MAGNIFICATION = 100

def main():
	pg.init()
	WIDTH, HEIGHT = 900, 600
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	bg = pg.Surface((WIDTH, HEIGHT))
	bg = pg.transform.scale(bg, (WIDTH, HEIGHT))

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the molecule...
		for atom in benzene:
			pg.draw.circle(screen, (255,255,255), (atom[1]*MAGNIFICATION+WIDTH//2,atom[2]*MAGNIFICATION+HEIGHT//2), 10)
		
		pg.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()

