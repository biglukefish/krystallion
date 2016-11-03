"""Krystallion features my wife running around and
shooting stuff."""

import pygame
from constants import *
import camera
from player import Player

screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Krystallion")
background_image = pygame.image.load('Level_01_Tile_Map.bmp').convert()
level_width = background_image.get_width
level_height = background_image.get_height
offset_tuple = (0, 0)

clock = pygame.time.Clock()

pygame.init()

ticker = 0
fps = 0



#program starts here
def main():
	
	#create our heroine and plop her in the center of the screen
	krystal = Player()
	krystal.rect.x = STARTING_POSITION_X
	krystal.rect.y = STARTING_POSITION_Y

	bg_image_x_coord = 0
	bg_image_y_coord = 0
	
	#create camera
	camera_shifter = camera.Camera(level_width, level_height)

	#add krystal to a list containing all sprites
	all_sprite_list = pygame.sprite.Group()
	all_sprite_list.add(krystal)
	# all_sprite_list.add(platform_sprite_list)

	last_move = ''

	#prepare main game loop
	done = False

	pygame.mixer.music.load('Retro Reggae.ogg')
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.mixer.music.play(loops = -1)


	#---------main program loop
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			#process user input for playing the game	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					krystal.move_left()
					last_move = 'left'
					krystal.facing = 'left'
					krystal.running = True
				if event.key == pygame.K_RIGHT:
					krystal.move_right()
					last_move = 'right'
					krystal.facing = 'right'
					krystal.running = True
				if event.key == pygame.K_UP:
					krystal.jump()
					last_move = 'jump'
				# elif event.key == pygame.K_SPACE:  <---  save for later when fire function is created
				# 	krystal.fire()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					krystal.stop()
					last_move = 'stop'
					krystal.running = False
				if event.key == pygame.K_RIGHT:
					krystal.stop()
					last_move = 'stop'
					krystal.running = False
				

		#-----------main game loops



		#-----------game logic


		krystal.update()


		#-----------draw functions

		offset_tuple = camera_shifter.apply(krystal)

		screen.blit(background_image, offset_tuple)

		screen.blit(krystal.image, (krystal.rect.x + offset_tuple[0], krystal.rect.y + offset_tuple[1]))


		print "FPS= " + str(round(clock.get_fps()))


		#update the display
		pygame.display.flip()

		#set refresh
		clock.tick(40)

	pygame.quit()  

if __name__=="__main__":
	main()