import pygame
import pytmx
import characters

"""
holds game object and level objects
"""


class Game(object):
	'''class for new instances of game'''
	level = 1
	def __init__(self):
		# Create level objects
		self.level_1 = Level_1()

class Level(object):
	'''superclass for level'''
	def __init__(self):
		pass

	def create_tmx_rects(self, layer_name, level_map):
		'''create list of rectangles for use in collision.
		:param layer_name: string
		:return: list of rect objects
		'''
		rectangles = []
		tiled_map = pytmx.TiledMap(level_map)
		group = tiled_map.get_layer_by_name(layer_name)
		for obj in group:
			objrect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
			rectangles.append(objrect)
		return rectangles


class Level_1(Level):
	'''level one, the adventure begins'''

	image = 'Level_01_Tile_Map_Shorter.bmp'
	level_1_tmx_file = 'Level_01_Tile_Map_Shorter.tmx'
	all_collision_rects = []
	bee_coords = [(2000, 0), (2500, 300), (3000, 150), (5000, 100)]



	def __init__(self):
		super(Level_1, self).__init__()

		# create collision rects for level
		self.terrain_rects = self.create_tmx_rects('Terrain', self.level_1_tmx_file)
		self.trampoline_rects = self.create_tmx_rects('Trampolines', self.level_1_tmx_file)

		# add to list
		for terrain in self.terrain_rects:
			self.all_collision_rects.append(terrain)
		for trampolines in self.trampoline_rects:
			self.all_collision_rects.append(trampolines)

		# initialize enemies
		self.enemy_sprites = pygame.sprite.Group()
		for element in self.bee_coords:
			self.enemy_sprites.add(characters.Bee(element))


class Level_2(Level):
	'''level two'''
