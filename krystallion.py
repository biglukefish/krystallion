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
screen = pygame.display.set_mode(constants.DISPLAY_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Krystallion")

# game object will initialize first level and create Krystal
current_game = game.Game()
krystal = current_game.krystal

gunshot = pygame.image.load('assets/bullet (3).png').convert()
gunshot.set_colorkey(constants.WHITE)


clock = pygame.time.Clock()


def main():

	# krystal = characters.Krystal(current_game)

	#build camera
	camera_shifter = camera.Camera(current_game.current_level.level_rect)

	bullet_list = pygame.sprite.Group()
	# load general sounds used throughout the game
	shooting_sound = pygame.mixer.Sound('assets/gunshot.wav')
	shooting_sound.set_volume(0.5)
	bee_sound = pygame.mixer.Sound('assets/Bee.wav')

	# prepare main game loop
	done = False
	#---------main program loop
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			#process user input for playing the game	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_LEFT:
					krystal.facing = 'left'
					krystal.moving_horizontally = True
				if event.key == pygame.K_RIGHT:
					krystal.facing = 'right'
					krystal.moving_horizontally = True
				if event.key == pygame.K_UP:
					krystal.jump()
				if event.key == pygame.K_SPACE:
					shot = Bullet(krystal.rect.x, krystal.rect.y,
									krystal.facing, krystal.rect.x)
					krystal.shooting = True
					shooting_sound.play()
					bullet_list.add(shot)

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
		current_game.current_level.bee_sprites.update()
		current_game.current_level.shroom_sprites.update()
		current_game.current_level.vulture_sprites.update()
		current_game.current_level.dead_sprites.update()


		# Handle bullet hits
		for bullet in bullet_list:
			bee_hit_list = pygame.sprite.spritecollide(
				bullet, current_game.current_level.bee_sprites, True)
			for bee in bee_hit_list:
				bee.alive = False
				current_game.current_level.dead_sprites.add(bee)
			if len(bee_hit_list) > 0:
				bullet_list.remove(bullet)
		for bullet in bullet_list:
			vulture_hit_list = pygame.sprite.spritecollide(
				bullet, current_game.current_level.vulture_sprites, True)
			for vulture in vulture_hit_list:
				vulture.alive = False
				current_game.current_level.dead_sprites.add(vulture)
			if len(vulture_hit_list) > 0:
				bullet_list.remove(bullet)
		for bullet in bullet_list:
			if bullet.state == 'expired':
				bullet_list.remove(bullet)
		for bee in current_game.current_level.bee_sprites.sprites():
			bee.buzz(krystal, bee_sound)

		#handle enemy hits
		bee_stings = pygame.sprite.spritecollide(krystal, current_game.current_level.bee_sprites, False)
		if bee_stings:
			if not krystal.invincible:
				krystal.hit_sequence()
		vulture_pecks = pygame.sprite.spritecollide(krystal, current_game.current_level.vulture_sprites, False)
		if vulture_pecks:
			if not krystal.invincible:
				krystal.hit_sequence()

		camera_offset = camera_shifter.apply(krystal)

		#-----------drawing functions
		#clear screen
		screen.fill(constants.WHITE)
		screen.blit(current_game.current_level.image, camera_offset)

		#draw krystal

		# adjustment needed to compensate for wide sprite due to gun
		if krystal.shooting == True and krystal.facing == 'left':
			screen.blit(krystal.image, (krystal.rect.x + camera_offset[0] -
										krystal.shot_frames_offset[krystal.blit_frame] -
										constants.KRYSTAL_INFLATE_X / 2,
										krystal.rect.y + camera_offset[1] - constants.KRYSTAL_INFLATE_Y))
			if krystal.shot_frame > 2:
				krystal.shooting = False
				krystal.shot_frame = 0
		else:
			screen.blit(krystal.image, (krystal.rect.x + camera_offset[0] - (constants.KRYSTAL_INFLATE_X / 2),
									krystal.rect.y + camera_offset[1] - constants.KRYSTAL_INFLATE_Y + 2))
			if krystal.shot_frame > 2:
				krystal.shooting = False
				krystal.shot_frame = 0

		# UNCOMMENT FOR SEEING ACTUAL CHARACTER/ENEMY RECTANGLE LOCATIONS
		# pygame.draw.rect(screen, constants.BLACK, (krystal.rect.x + camera_offset[0],
		# 								krystal.rect.y + camera_offset[1], krystal.rect.width, krystal.rect.height))

		# for sprite in current_game.current_level.dead_sprites:
		# 	pygame.draw.rect(screen, constants.BLACK, (sprite.rect.x + camera_offset[0],
		# 											   sprite.rect.y + camera_offset[1], sprite.rect.width,
		# 											   sprite.rect.height))

		# for sprite in current_game.current_level.vulture_sprites:
		# 	pygame.draw.rect(screen, constants.BLACK, (sprite.rect.x + camera_offset[0],
		# 											   sprite.rect.y + camera_offset[1], sprite.rect.width,
		# 											   sprite.rect.height))



		#draw enemies
		for bees in current_game.current_level.bee_sprites:
			screen.blit(bees.image, (bees.rect.x + camera_offset[0] - (constants.BEE_INFLATE_X / 3),
									 bees.rect.y + camera_offset[1] - (constants.BEE_INFLATE_Y / 2 + 5)))
		for shrooms in current_game.current_level.shroom_sprites:
			screen.blit(shrooms.image, (shrooms.rect.x + camera_offset[0],
										shrooms.rect.y + camera_offset[1]))
		for vultures in current_game.current_level.vulture_sprites:
			screen.blit(vultures.image, (vultures.rect.x + camera_offset[0],
										vultures.rect.y + camera_offset[1]))
		for enemy in current_game.current_level.dead_sprites:
			screen.blit(enemy.image, (enemy.rect.x + camera_offset[0],
										enemy.rect.y + camera_offset[1]))

		#draw bullets
		for bullet in bullet_list:
			screen.blit(gunshot, (bullet.rect.x + camera_offset[0],
								 bullet.rect.y + camera_offset[1]))

		#draw variables on screen for debugging
		texts("fps= " + str(round(clock.get_fps())), (0, 0))
		texts("life= " + str(krystal.life), (0, 20))

		#exit if krystal dies
		if krystal.life <= 0:
			done = True

		#update the display
		pygame.display.flip()

		#set refresh rate
		clock.tick(40)

	pygame.quit()  

def texts(text, location):
	'''draws game variables on the screen'''
	font=pygame.font.Font(None, 20)
	scoretext=font.render(text, 1,(0, 0, 0))
	screen.blit(scoretext, location)

if __name__=="__main__":
	main()