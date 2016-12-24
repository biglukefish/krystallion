import pygame
import spritesheet
import constants

pygame.init()
screen = pygame.display.set_mode((1500, 800))
ss = spritesheet.SpriteSheet('level_1_assets/level_1_enemies_1.png')


done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	screen.fill(constants.WHITE)

	enemylocs = constants.L_1_ENEMIES_1[34:]

	xloc = 0
	for i in range(len(enemylocs)):
		bob = ss.get_image(enemylocs[i])
		screen.blit(bob, (xloc, 0))
		xloc += 80
	pygame.display.flip()


pygame.quit()