'''bullets to fire at enemies'''

import pygame
from constants import *

class Bullet(pygame.sprite.Sprite):


	def __init__(self, x, y, facing, initial_x):

		super(Bullet, self).__init__()  # call to parent constructor

		'''fire bullet from location of player, in the correct direction'''
		self.image = pygame.Surface([8, 8])
		self.rect = self.image.get_rect()
		if facing == 'right':
			self.rect.x = x + 15
		else:
			self.rect.x = x - 5
		self.rect.y = y + 40
		self.initial_x = initial_x
		self.direction = facing
		self.state = 'blazing across the screen'


	def update(self):
		if self.direction == 'right':
			self.rect.x += BULLET_SPEED
			if self.rect.x - self.initial_x > (DISPLAY_WIDTH * 3):
				self.state = 'expired'
		else:
			self.rect.x -= BULLET_SPEED
			if self.initial_x - self.rect.x > (DISPLAY_WIDTH * 3):
				self.state = 'expired'

