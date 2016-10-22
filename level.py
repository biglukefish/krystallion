"""used to create a level"""

import pygame
import constants
from earth import Earth

class Level():

	platform_list = pygame.sprite.Group()

	
	def __init__(self, platform_locations):
	# platform locations is a list of lists. [width, height, x loc, y loc]

		for i in range(len(platform_locations)):

			#pass in width, height
			platform = Earth((platform_locations[i][0], platform_locations[i][1]))

			#pass in x y location
			platform.rect.x = platform_locations[i][2]
			platform.rect.y = platform_locations[i][3]

		#add to sprite groups
			self.platform_list.add(platform)

	def get_platforms(self):
		return self.platform_list

	def scroll_right(self):
		for platform in self.platform_list:
			platform.rect.x -= 5


	def scroll_left(self):
		for platform in self.platform_list:
			platform.rect.x += 5





