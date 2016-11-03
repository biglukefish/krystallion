'''class to aim the camera on an object and follow it while
game scrolls.  It is really just an offset to apply before rendering'''

import pygame
from constants import *
import player

class Camera(object):

	def __init__(self, level_width, level_height):
		# target is the center of a rect object representing part of
		# level that should be drawn
		self.shifted_camera = pygame.Rect(0, 0, DISPLAY_WIDTH,
								DISPLAY_HEIGHT)
		self.level_width = level_width
		self.level_height = level_height

	def apply(self, target_character):
		'''receives character rectangle, returns an (x, y) offset tuple'''
		self.shifted_camera = pygame.Rect(target_character.rect.x - (DISPLAY_WIDTH / 2),
								target_character.rect.y - (DISPLAY_HEIGHT / 2),
								DISPLAY_WIDTH,
								DISPLAY_HEIGHT)

		# make sure the camera doesn't scroll off the map
		if self.shifted_camera.left < 0:
			self.shifted_camera.left = 0
		if self.shifted_camera.right > self.level_width:
			self.shifted_camera.right = self.level_width
		if self.shifted_camera.top < 0:
			self.shifted_camera.top = 0
		if self.shifted_camera.bottom > self.level_height:
			self.shifted_camera.bottom = self.level_height

		#return offset tuple
		return (-1 * self.shifted_camera.x, -1 * self.shifted_camera.y)





