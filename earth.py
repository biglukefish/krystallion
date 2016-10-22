import pygame
import constants


class Earth(pygame.sprite.Sprite):


	#methods
	def __init__(self, (width, height)):  #Earth object constructor

		pygame.sprite.Sprite.__init__(self)  #parent constructor


        #   Here's where my 10/19 error was.  I didn't realize "self.image" was 
        #   referring to Sprite.image, which was already a class variable, since
        #   Earth inherited Sprite.  I just named my own variable, called it "chunk,"
        #   and it totally didn't work.
		self.image = pygame.Surface((width, height))   
		self.image.fill(constants.GREEN)

		self.rect = self.image.get_rect()