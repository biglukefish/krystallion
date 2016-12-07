import pygame
import constants



class SpriteSheet(object):
	'''Class to get images out of a spritesheet.  Returns image object'''

	def __init__(self, file_name):

		#load up the sprite sheet
		self.sprite_sheet = pygame.image.load(file_name)

	def get_image(self, (x, y, width, height)):
		#pull single image out of spritesheet

		#create a blank image the same size as the image needed
		image = pygame.Surface([width, height], pygame.SRCALPHA)

		#copy the image from the spritesheet onto the new image
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

		image.set_colorkey(constants.BLACK)

		return image
