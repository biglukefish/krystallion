import pygame
import constants
import spritesheets


class Earth(pygame.sprite.Sprite):


	#methods
	def __init__(self): 
	#Earth object constructor

		pygame.sprite.Sprite.__init__(self)  #parent constructor


		sheet = spritesheets.SpriteSheet('spritesheet_ground.png')
		self.image = sheet.get_image(0, 1024, 128, 64)
		self.rect = self.image.get_rect()