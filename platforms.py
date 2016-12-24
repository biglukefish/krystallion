import pygame

class Platforms(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height):
		super(Platforms, self).__init__()
		self.image = pygame.Surface([width, height])
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
