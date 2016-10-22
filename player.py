"""this module contains the player class, for generating our hero"""

import pygame
import earth
import level
import constants

class Player(pygame.sprite.Sprite):

#attributes
	change_x = 0
	change_y = 0
	can_jump = 0  # <--- limit of 2 jumps
	facing = 'right'
	running = False
	RUNNING_SPEED = 4
	GRAVITY_CONSTANT = 0.15
	JUMP_VELOCITY = 4


#methods
	def __init__(self):  #call to constructor

		super(Player, self).__init__()  #call to parent constructor

		self.image = pygame.image.load('tiny_krystal.png')
		self.rect = self.image.get_rect()

	
	def move_left(self, platform_sprite_list):
		
		self.change_x -= self.RUNNING_SPEED		
			


	def move_right(self, platform_sprite_list):

		self.change_x += self.RUNNING_SPEED

		


	def stop(self):
		self.change_x = 0


	def jump(self):
		if self.can_jump < 2:
			self.change_y -= self.JUMP_VELOCITY
			self.can_jump += 1


	def calc_gravity(self):
		#simulate gravity by making player fall
		self.change_y += self.GRAVITY_CONSTANT


	def update(self, platform_sprite_list):

		#add in the effects of gravity
		self.calc_gravity()
		
		
		if self.change_x < 0:
			#collision detection to the left
			self.rect.x -= 2
			if len(pygame.sprite.spritecollide(self, platform_sprite_list, False)) > 0:
				self.change_x = 0
			self.rect.x += 2

			if self.rect.x < 5:
				self.change_x = 0

			
		if self.change_x > 0:
			#collision detection to the right
			self.rect.x += 2
			if len(pygame.sprite.spritecollide(self, platform_sprite_list, False)) > 0:
				self.change_x = 0
			self.rect.x -= 2

			# limit player from walking off the screen
			if self.rect.x > 150:
				self.change_x = 0



		#update the position
		self.rect.x += self.change_x
		self.rect.y += self.change_y



		#	drop the player down 2 pixels and if he hits something, stop from
		#	falling (i.e. stop the effect of gravity)
		self.rect.y += 2
		if len(pygame.sprite.spritecollide(self, platform_sprite_list, False)) > 0:

			#  In this case, player has collided with something so we need to reset her location.
			#  We take the first sprite collided with, and reset position in relation to that sprite.
			collided_object = pygame.sprite.spritecollide(self, platform_sprite_list, False)
			self.rect.y = collided_object[0].rect.y - constants.HERO_SIZE[1]
			self.change_y = 0
			if self.can_jump == 1:
				self.can_jump = 2
			elif self.can_jump == 2:
				self.can_jump = 0
		else:		
			self.rect.y -= 2

		#   do the same for ceiling
		self.rect.y -= 2
		if len(pygame.sprite.spritecollide(self, platform_sprite_list, False)) > 0:

			#  In this case, player has collided with something so we need to reset her location.
			#  We take the first sprite collided with, and reset position in relation to that sprite.
			collided_object = pygame.sprite.spritecollide(self, platform_sprite_list, False)
			self.rect.y = collided_object[0].rect.y + collided_object[0].rect.height
			self.change_y = 0
		self.rect.y += 2

		

		

