"""this module contains the player class, for generating our hero"""
#TODO change from checking collisions with only one rectangle, to all

import pygame
from constants import *
import spritesheet
import pytmx

class Player(pygame.sprite.Sprite):

#class attributes
	change_x = 0
	change_y = 0
	can_jump = True
	facing = 'right'
	running = False
	collision_side = ''
	RUNNING_SPEED = 6
	JUMP_VELOCITY = 15
	test_rect = pygame.Rect(0, 0, 0, 0)
	outline = pygame.Rect(0, 0, 0, 0)
	on_ground = True


#methods
	def __init__(self):  #call to constructor

		super(Player, self).__init__()  #call to parent constructor


		self.walking_frames_l = []
		self.walking_frames_r = []
		self.standing_frames_l = []
		self.standing_frames_r = []
		self.flying_frames_l = []
		self.flying_frames_r = []
		self.falling_frames_l = []
		self.falling_frames_r = []
		self.hitlist_indices = []  #list of indices of terrain rect objects that collided
		self.platform_rectangles = []  #list of rectangle objects representing terrain

		# creates a list of collision rects
		self.tiled_map = pytmx.TiledMap('Level_01_Tile_Map.tmx')
		self.group = self.tiled_map.get_layer_by_name("CollisionBackgrounds")



		# Fill out rectangle list with list of collision rectangle
		# coordinates
		for obj in self.group:
			self.x, self.y, self.width, self.height = obj.x, obj.y, obj.width, obj.height
			self.objrect = pygame.Rect(self.x, self.y, self.width, self.height)
			self.platform_rectangles.append(self.objrect)


		#load spritesheets
		sprite_sheet = spritesheet.SpriteSheet('KrystalSpriteSheet_transparent.png')

		#fill out image lists for walking
		image = sprite_sheet.get_image(0, 60, 50, 60)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(50, 60, 50, 60)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(100, 60, 50, 60)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(150, 60, 50, 60)
		self.walking_frames_r.append(image)


		#get reverse images for walking
		image = sprite_sheet.get_image(0, 60, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(50, 60, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(100, 60, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(150, 60, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)



		#get images for standing
		image = sprite_sheet.get_image(0, 0, 50, 60)
		self.standing_frames_r.append(image)
		image = sprite_sheet.get_image(50, 0, 50, 60)
		self.standing_frames_r.append(image)
		image = sprite_sheet.get_image(100, 0, 50, 60)
		self.standing_frames_r.append(image)
		image = sprite_sheet.get_image(150, 0, 50, 60)
		self.standing_frames_r.append(image)
		image = sprite_sheet.get_image(200, 0, 50, 60)
		self.standing_frames_r.append(image)
		image = sprite_sheet.get_image(250, 0, 50, 60)
		self.standing_frames_r.append(image)


		#get reverse images for standing
		image = sprite_sheet.get_image(0, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)
		image = sprite_sheet.get_image(50, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)
		image = sprite_sheet.get_image(100, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)
		image = sprite_sheet.get_image(150, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)
		image = sprite_sheet.get_image(200, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)
		image = sprite_sheet.get_image(250, 0, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.standing_frames_l.append(image)

		# get image for flying
		image = sprite_sheet.get_image(200, 60, 50, 55)
		self.flying_frames_r.append(image)


		# get reverse image for flying
		image = sprite_sheet.get_image(200, 60, 50, 55)
		image = pygame.transform.flip(image, True, False)
		self.flying_frames_l.append(image)

		# get image for falling
		image = sprite_sheet.get_image(250, 195, 50, 60)
		self.falling_frames_r.append(image)

		# get reverse image for flying
		image = sprite_sheet.get_image(250, 195, 50, 60)
		image = pygame.transform.flip(image, True, False)
		self.falling_frames_l.append(image)


		# Set the image the player starts with
		self.image = self.walking_frames_r[0]

		# Set a reference to the image rect.
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = STARTING_POSITION_X, STARTING_POSITION_Y

	def move_left(self):
		self.change_x -= self.RUNNING_SPEED


	def move_right(self):
		self.change_x += self.RUNNING_SPEED


	def stop(self):
		self.change_x = 0


	def jump(self):
		'''applies jump if player is standing on ground'''
		self.change_y -= self.JUMP_VELOCITY
		self.on_ground = False




	def apply_gravity(self):
		'''simulate gravity by making player fall'''

		if (self.check_for_collision(self.rect.x, self.rect.y + 2, self.rect.width, self.rect.height) == False
			and self.change_y < 100):
			self.on_ground = False
			self.change_y += GRAVITY_CONSTANT
			print "gravity applied"
		else:
			self.on_ground = True


	def update(self):

		
		#add in the effects of gravity
		self.apply_gravity()

		#move the player
		self.apply_collision()


		# update what image of the player is used
		pos = self.rect.x
		if self.facing == 'right' and self.change_x != 0:
			frame = (pos // 30) % len(self.walking_frames_r)
			self.image = self.walking_frames_r[frame]
		if self.facing == 'left' and self.change_x != 0:
			frame = (pos // 30) % len(self.walking_frames_l)
			self.image = self.walking_frames_l[frame]

		pos = self.rect.x
		if self.change_x == 0 and self.change_y == 0:
			if self.facing == 'right':
				frame = (pos // 30) % len(self.standing_frames_r)
				self.image = self.standing_frames_r[frame]
			if self.facing == 'left':
				frame = (pos // 30) % len(self.standing_frames_l)
				self.image = self.standing_frames_l[frame]

		pos = self.rect.x
		if self.change_y > 0:
			if self.facing == 'right':
				frame = (pos // 30) % len(self.flying_frames_r)
				self.image = self.flying_frames_r[frame]
			if self.facing == 'left':
				frame = (pos // 30) % len(self.flying_frames_l)
				self.image = self.flying_frames_l[frame]

		print 'change x = ' + str(self.change_x)
		print 'change y = ' + str(self.change_y)
		print 'x, y = ' + str(self.rect.x) + ', ' + str(self.rect.y)



	def apply_collision(self):
		'''Update position of player based on collision 
		detection (or lack thereof)'''

		# Create a copy of the rectangle for collision test
		self.test_rect = self.rect.copy()
		self.test_rect.x += self.change_x
		self.test_rect.y += self.change_y

		self.hitlist = [] # need this for holding collided platforms objects

		# check for collision with platform rectangles, store
		# resulting indices in a list
		self.hitlist_indices = self.test_rect.collidelistall(self.platform_rectangles)
		print "self.hitlist_indices= " + str(self.hitlist_indices)


		# if no collision, apply normal change in position
		if not self.hitlist_indices:
			self.rect.x += self.change_x
			self.rect.y += self.change_y
			print 'no collision'
			return

		# if two rectangles are collided with, then player is in
		# a corner
		if len(self.hitlist_indices) > 1:
			self.change_x += 0
			self.change_y += 0
			print 'in a corner'
			return

		# convert indices into a list containing the actual
		# platform rectangles

		if self.hitlist_indices:
			print 'collision detected'
			print self.hitlist_indices
			for i in range(len(self.hitlist_indices)):
				self.hitlist.append(self.platform_rectangles[self.hitlist_indices[i]])
			# process each of the collided platforms
			for hit in self.hitlist:
				self.process_hit(hit)
			return

		print 'collision detection error'


			

	def process_hit(self, hit_rectangle):
		'''Test to see what side test rect collided with and apply
		appropriate changes in position and velocity.  Will test
		x and y changes separately to determine what side has
		collided.'''


		# Test horizonal ONLY movement first by adjusting
		# test rectangle's change y back to 0
		self.test_rect.y -= self.change_y

		#run the test
		if (self.test_rect.colliderect(hit_rectangle) == True
			and self.change_x > 0):
			# collided with left side of platform, so reset accordingly
			print 'collided with left side of platform'
			self.rect.right = hit_rectangle.left
			self.rect.y += self.change_y

		elif (self.test_rect.colliderect(hit_rectangle) == True
			and self.change_x < 0):
			# collided with right side of platform, so reset accordingly
			print 'collided with right side of platform'
			self.rect.left = hit_rectangle.right
			self.rect.y += self.change_y



		# Adjust test rectangle to check what happens if it had only
		# moved vertically
		self.test_rect.y += self.change_y
		self.test_rect.x -= self.change_x

		#run the test
		if (self.test_rect.colliderect(hit_rectangle) == True
			and self.change_y > 0):
			# collided with top side of platform, so reset accordingly
			print 'collided with top side of platform'
			self.rect.bottom = hit_rectangle.top
			self.rect.x += self.change_x
			self.change_y = 0
		if (self.test_rect.colliderect(hit_rectangle) == True
			and self.change_y < 0):
			# collided with bottom side of platform, so reset accordingly
			print 'collided with bottom of platform'
			self.rect.top = hit_rectangle.bottom
			self.rect.x += self.change_x
			self.change_y = 0


	def check_for_collision(self, x, y, width, height):
		''' takes a rectangle and checks to see if it collides with
		any of the platforms.
		Return boolean'''

		# Create a test rectangle
		self.test_rect = pygame.Rect(x, y, width, height)

		# check for collision with platform rectangles, store
		# resulting indices in a list
		self.hitlist_index = self.test_rect.collidelist(self.platform_rectangles)

		if self.hitlist_index == -1:
			return False
		else:
			return True


		

