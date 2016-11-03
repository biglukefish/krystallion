'''
class for pulling images from the spritesheet 
for use in terrain
'''

import pygame
import constants

class SpriteSheet(object):

	def __init__(self, file_name):

		#load up the spritesheet
		self.sprite_sheet = pygame.image.load(file_name).convert()

	def get_image(self, x, y, width, height):
		# get single image from the sprite sheet

		# Make blank image
		image = pygame.Surface([width, height]).convert()

		#copy sprite from large sheet into smaller image surface
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

		image.set_colorkey(constants.BLACK)

		return image

