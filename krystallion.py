"""
interpreter:
/usr/local/cellar/python/2.7.12/frameworks/python.framework/versions/2.7/bin/python2.7

Krystallion, a game featuring my wife running around and
shooting stuff.
"""

import pygame
import camera
import characters
import constants
from bullet import Bullet
import game

# initialize pygame and build screen
pygame.init()
pygame.mixer.init()
current_game = game.Game()
screen = pygame.display.set_mode(constants.DISPLAY_SIZE)
pygame.display.set_caption("Krystallion")
background_image = pygame.image.load(current_game.level_1.image).convert()
level_rect = background_image.get_rect()
laser = pygame.image.load('lasershot copy.png').convert()
laser.set_colorkey(constants.WHITE)



clock = pygame.time.Clock()



def main():
	
	#create heroine and plop her in the left of the screen
	krystal = characters.Krystal(current_game)
	krystal.char_rect.x = constants.STARTING_POSITION_X
	krystal.char_rect.y = constants.STARTING_POSITION_Y
	direction = '' # Can be 'left', 'right', or 'stopped'

	#build camera

	camera_shifter = camera.Camera(level_rect)

	bullet_list = pygame.sprite.Group()

	#prepare main game loop
	done = False

	#load jams for pumping and other sounds
	pygame.mixer.music.load('Retro Reggae.ogg')
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.mixer.music.play(loops = -1)
	shooting_sound = pygame.mixer.Sound('laser5.ogg')
	bee_sound = pygame.mixer.Sound('Bee.wav')


	#---------main program loop
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			#process user input for playing the game	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					krystal.facing = 'left'
					krystal.moving_horizontally = True
				if event.key == pygame.K_RIGHT:
					krystal.facing = 'right'
					krystal.moving_horizontally = True
				if event.key == pygame.K_UP:
					krystal.jump()
				if event.key == pygame.K_SPACE:
					shot = Bullet(krystal.char_rect.x, krystal.char_rect.y,
									krystal.facing, krystal.char_rect.x)
					shooting_sound.play()
					bullet_list.add(shot)
				if event.key == pygame.K_w:
					pygame.display.set_mode(constants.DISPLAY_SIZE)
				if event.key == pygame.K_f:
					pygame.display.set_mode(constants.DISPLAY_SIZE, pygame.FULLSCREEN)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					krystal.facing = 'left'
					krystal.moving_horizontally = False
				if event.key == pygame.K_RIGHT:
					krystal.facing = 'right'
					krystal.moving_horizontally = False

		#-----------game logic updates
		krystal.move_horizontal()
		krystal.update()
		bullet_list.update()
		current_game.level_1.enemy_sprites.update()

		for bullet in bullet_list:
			bee_hit_list = pygame.sprite.spritecollide(
				bullet, current_game.level_1.enemy_sprites, False)
			for bee in bee_hit_list:
				bee.alive = False
			if len(bee_hit_list) > 0:
				bullet_list.remove(bullet)
		if pygame.sprite.spritecollideany(krystal, current_game.level_1.enemy_sprites) is not None:
			krystal.is_hit = True
		for bullet in bullet_list:
			if bullet.state == 'expired':
				bullet_list.remove(bullet)
		for bee in current_game.level_1.enemy_sprites.sprites():
			bee.buzz(krystal, bee_sound)



		offset_tuple = camera_shifter.apply(krystal)

		#-----------drawing functions
		#clear screen
		screen.fill(constants.WHITE)
		screen.blit(background_image, offset_tuple)

		#draw krystal
		krystal.rect.center = krystal.char_rect.center
		krystal.rect.x = krystal.char_rect.x - 18
		screen.blit(krystal.image, (krystal.rect.x + offset_tuple[0],
									krystal.rect.y + offset_tuple[1]))
		current_game.level_1.enemy_sprites.update()

		#draw enemy
		for bees in current_game.level_1.enemy_sprites:
			screen.blit(bees.image, (bees.rect.x + offset_tuple[0],
									 bees.rect.y + offset_tuple[1]))

		#draw bullets
		for bullet in bullet_list:
			screen.blit(laser, (bullet.rect.x + offset_tuple[0],
								 bullet.rect.y + offset_tuple[1]))



		#draw variables on screen for debugging
		if krystal.is_hit == True:
			texts('you fucking got hit', (constants.DISPLAY_WIDTH / 2, constants.DISPLAY_HEIGHT / 2))
		# texts('y=', krystal.rect.y, (0, 20))
		# texts("fps= ", str(round(clock.get_fps())), (0, 40))
		# texts('dx=', krystal.dx, (constants.DISPLAY_WIDTH - 80, 0))
		# texts('dy=', krystal.dy, (constants.DISPLAY_WIDTH - 80, 20))
		# texts('collide=', krystal.collision_status, (constants.DISPLAY_WIDTH - 200, 40))


		#update the display
		pygame.display.flip()

		#set refresh rate
		clock.tick(40)

	pygame.quit()  

def texts(text, location):
	'''draws game variables on the screen'''
	font=pygame.font.Font(None,30)
	scoretext=font.render(text, 1,(255, 0, 0))
	screen.blit(scoretext, location)

if __name__=="__main__":
	main()