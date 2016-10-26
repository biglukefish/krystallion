"""Krystallion, by SwimmingFish Games"""
import pdb
import pygame
import constants
import level
from player import Player
from earth import Earth

screen = pygame.display.set_mode(constants.DISPLAY_SIZE)

clock = pygame.time.Clock()

pygame.init()

#program starts here
def main():
	
	#create our heroine
	krystal = Player()
	krystal.rect.x = 50
	krystal.rect.y = constants.DISPLAY_HEIGHT - constants.HERO_SIZE[1]
	


	#  create new instance of level called "level_01".  Pass in list of where platforms 
	#  should go.  new level object has an attribute that is a 
	#  sprite list of the platforms that you can retrieve with get_platforms()
	level_01 = level.Level(constants.LEVEL_01)
	platform_sprite_list = level_01.get_platforms()

	#add krystal to a list containing all sprites
	all_sprite_list = pygame.sprite.Group()
	all_sprite_list.add(krystal)
	all_sprite_list.add(platform_sprite_list)

	last_move = ''

	#prepare main game loop
	done = False

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
					krystal.jump(platform_sprite_list)
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

		krystal.update(platform_sprite_list, last_move)

		# if krystal.rect.x > 150 and krystal.running == True:
		# 	level_01.scroll_right()

		#-----------draw functions
		#clear the screen
		screen.fill(constants.YELLOW)
		all_sprite_list.draw(screen)

		#draw reference grid
		# for i in range(0, 500, 50):
		# 	pygame.draw.line(screen, constants.WHITE, (i, 0), (i, 500))
		# 	pygame.draw.line(screen, constants.WHITE, (0, i), (500, i))

		#update the display
		pygame.display.flip()

		#set refresh
		clock.tick(40)

	pygame.quit()  

if __name__=="__main__":
	main()