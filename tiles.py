"testing out pytmx for importing tileset"

import pygame
import pytmx

tiled_map = pytmx.TiledMap('Level_01_Tile_Map.tmx')
group = tiled_map.get_layer_by_name("CollisionBackgrounds")

rectangles = []

for obj in group:
	x, y, width, height = obj.x, obj.y, obj.width, obj.height
	objrect = pygame.Rect(x, y, width, height)
	rectangles.append(objrect)

print rectangles
