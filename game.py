import pygame
import pytmx
import characters
import platforms
import leveldata

"""
holds game object and level objects
"""


class Game(object):
	'''class for new instances of game'''
	def __init__(self):
		# Create level objects
		self.current_level_number = 0
		self.current_level = Level(leveldata.level_data[0])
		self.krystal = characters.Krystal(self)

	def go_to(self, level):
		self.current_level_number = level
		self.current_level = Level(leveldata.level_data[level])

class Scene(object):
	def __init__(self):
		pass


class Level(Scene):

	def __init__(self, level_data):
		super(Level, self).__init__()


		self.image = pygame.image.load(level_data['bg_image']).convert()
		self.level_rect = self.image.get_rect()
		pygame.mixer.music.load(level_data['bg_tunes'])
		pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
		pygame.mixer.music.play(loops=-1)
		self.tmx_file = level_data['tmx_file']
		self.bee_coords = level_data['bee_coords']
		self.vulture_coords = level_data['vulture_coords']

		# create mushrooms, each tile in background is 64x64 pixels.
		# params --> x, bottom, left bound, right bound
		self.shroom_coords = level_data['shroom_coords']

		# create collision rects for level and change them
		# into sprites
		self.terrain_rects = self.create_tmx_rects('Terrain', self.tmx_file)
		self.all_collision_rects = []
		# TODO can I delete the two lines below?  Answer is NO
		for terrain in self.terrain_rects:
			self.all_collision_rects.append(terrain)
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