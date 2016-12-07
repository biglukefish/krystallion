'''class to aim the camera on an object and follow it while
game scrolls.  It is really just an offset to apply before rendering'''

import pygame
from constants import *

class Camera(object):

	def __init__(self, level_rect):
		# target is the center of a rect object representing part of
		# level that should be drawn
		self.shifted_camera = pygame.Rect(0, 0, DISPLAY_WIDTH,
								DISPLAY_HEIGHT)
		self.level_rect = level_rect

	def apply(self, target_character):
		'''receives character rectangle, returns an (x, y) offset tuple'''
		self.shifted_camera = pygame.Rect(target_character.rect.x - (DISPLAY_WIDTH / 2),
								target_character.rect.y - (DISPLAY_HEIGHT / 2),
								DISPLAY_WIDTH,
								DISPLAY_HEIGHT)

		# make sure the camera doesn't scroll off the map
		if self.shifted_camera.left < 0:
			self.shifted_camera.left = 0
		if self.shifted_camera.right > self.level_rect.right:
			self.shifted_camera.right = self.level_rect.right
		if self.shifted_camera.top < 0:
			self.shifted_camera.top = 0
		if self.shifted_camera.bottom > self.level_rect.bottom:
			self.shifted_camera.bottom = self.level_rect.bottom

		#return offset tuple
		return (-1 * self.shifted_camera.x, -1 * self.shifted_camera.y)





