import pygame
import pytmx
import characters
import platforms

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

	image = 'assets/level_1_assets/Level_01_Tile_Map_Shorter_Taller.bmp'
	level_1_tmx_file = 'assets/level_1_assets/Level_01_Tile_Map_Shorter_Taller.tmx'
	all_collision_rects = []
	bee_coords = [(1344, 192), (1920, 256), (3136, 448),
				  (3840, 320), (5504, 448), (6016, 512)]
	vulture_coords = [(1344, 192), (1920, 256), (3136, 448),
				  (3840, 320), (5504, 448), (6016, 512)]

	# create mushrooms, each tile in background is 64x64 pixels.
	# params --> x, bottom, left bound, right bound
	shroom_coords = [(21*64, 9*64, 21*64, 26*64), (8*64, 9*64, 1*64, 9*64) ]


	def __init__(self):
		super(Level_1, self).__init__()

		# create collision rects for level
		self.terrain_rects = self.create_tmx_rects('Terrain', self.level_1_tmx_file)

		# add to list
		for terrain in self.terrain_rects:
			self.all_collision_rects.append(terrain)

		# create sprites out of the rects
		self.platform_sprites = pygame.sprite.Group()
		for rect in self.terrain_rects:
			plat = platforms.Platforms(rect.x, rect.y, rect.width, rect.height)
			self.platform_sprites.add(plat)

		# initialize enemies
		self.bee_sprites = pygame.sprite.Group()
		self.shroom_sprites = pygame.sprite.Group()
		self.vulture_sprites = pygame.sprite.Group()
		for element in self.shroom_coords:
			shroom = characters.Shroom(element)
			self.shroom_sprites.add(shroom)
		for element in self.bee_coords:
			bee = characters.Bee(element)
			self.bee_sprites.add(bee)

		self.all_enemy_sprites = pygame.sprite.Group()
		self.all_enemy_sprites.add(
			self.bee_sprites, self.shroom_sprites,
			self.vulture_sprites
			)

		#create sprite group for dying sprites
		self.dead_sprites = pygame.sprite.Group()



class Level_2(Level):
	'''level two'''
