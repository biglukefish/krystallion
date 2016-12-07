"""this module contains the character class, for generating
characters in the game"""

import pygame
import constants
import spritesheet
import assets
import game


class Krystal(pygame.sprite.Sprite):
	dx = 0
	dy = 0
	can_jump = True
	facing = 'right'
	running = False
	collision_side = ''
	RUNNING_SPEED = constants.HERO_RUNNING_SPEED
	JUMP_VELOCITY = constants.HERO_JUMP_VELOCITY
	on_ground = True
	collision_status = 'none'


	def __init__(self, game):
		super(Krystal, self).__init__()

		self.game = game

		# frames for loading images of character in diff positions
		self.img_walk_l = []
		self.img_walk_r = []
		self.img_stand_l = []
		self.img_stand_r = []
		self.img_fly_l = []
		self.img_fly_r = []
		self.img_fall_l = []
		self.img_fall_r = []

		self.hitlist_indices = []
		self.is_hit = False

		# set spritesheet image references
		for element in constants.KRYSTAL_WALKING:
			image = assets.krystal_ssheet.get_image(element)
			self.img_walk_r.append(image)
			self.img_walk_l.append(pygame.transform.flip(image, True, False))
		for element in constants.KRYSTAL_STANDING:
			image = assets.krystal_ssheet.get_image(element)
			self.img_stand_r.append(image)
			self.img_stand_l.append(pygame.transform.flip(image, True, False))
		for element in constants.KRYSTAL_FLYING:
			image = assets.krystal_ssheet.get_image(element)
			self.img_fly_r.append(image)
			self.img_fly_l.append(pygame.transform.flip(image, True, False))
		for element in constants.KRYSTAL_FALLING:
			image = assets.krystal_ssheet.get_image(element)
			self.img_fall_r.append(image)
			self.img_fall_l.append(pygame.transform.flip(image, True, False))

		# Set the image the player starts with
		self.image = self.img_walk_r[0]

		# 'Rect' is a ref to the sprite object.  'Char_rect' is an
		# independent, smaller rectangle to use for collision calcs and repositioning
		# Krystal's character.  Immediately before blitting, 'rect' will be moved to where
		# 'char_rect' is, so image can be pasted in the correct place.
		self.rect = self.image.get_rect()
		self.char_rect = pygame.Rect(0, 0, self.rect.width / 3, self.rect.height)
		self.char_rect.x, self.char_rect.y = constants.STARTING_POSITION_X, constants.STARTING_POSITION_Y

	def move_horizontal(self, direction):
		if direction == 'right':
			self.dx += self.RUNNING_SPEED
		elif direction == 'left':
			self.dx -= self.RUNNING_SPEED
		else:
			self.dx = 0


	def jump(self):
		'''applies jump if char is standing on ground'''
		if self.on_ground == True:
			self.dy -= self.JUMP_VELOCITY
			self.on_ground = False

	def apply_gravity(self):
		'''simulate gravity by making char fall'''

		if (self.check_for_collision(self.char_rect.x,
									 self.char_rect.y + 2,
									 self.char_rect.width,
									 self.char_rect.height,
									 self.game.level_1.all_collision_rects) == False
			and self.dy < 50):
			self.on_ground = False
			self.dy += constants.GRAVITY_CONSTANT
		else:
			self.on_ground = True

	def update(self):

		self.apply_gravity()
		self.apply_collision()

		#temp code to catch character if she falls off screen
		if self.char_rect.bottom > constants.DISPLAY_HEIGHT:
			self.char_rect.bottom = constants.DISPLAY_HEIGHT - 5

		# Update what image of Krystal is used, based on the direction
		# she is facing and what she is doing.
		pos = self.char_rect.x
		if self.facing == 'right' and self.dx != 0:
			frame = (pos // 30) % len(self.img_walk_r)
			self.image = self.img_walk_r[frame]
		if self.facing == 'left' and self.dx != 0:
			frame = (pos // 30) % len(self.img_walk_l)
			self.image = self.img_walk_l[frame]

		pos = self.char_rect.x
		if self.dx == 0 and self.dy == 0:
			if self.facing == 'right':
				frame = (pos // 30) % len(self.img_stand_r)
				self.image = self.img_stand_r[frame]
			if self.facing == 'left':
				frame = (pos // 30) % len(self.img_stand_l)
				self.image = self.img_stand_l[frame]

		pos = self.char_rect.x
		if self.dy > 0:
			if self.facing == 'right':
				frame = (pos // 30) % len(self.img_fly_r)
				self.image = self.img_fly_r[frame]
			if self.facing == 'left':
				frame = (pos // 30) % len(self.img_fly_l)
				self.image = self.img_fly_l[frame]

		self.move_horizontal('stopped')

	def apply_collision(self):
		'''Update position of char based on collision
		detection (or lack thereof)'''

		# Create a copy of the rectangle ('test_rect') and apply proposed velocity
		# changes, just to see if these result in a hit with any
		# existing platforms.  'Test_rect' is sort of like a scout, testing
		# the collision waters before the actual 'char_rect' makes any moves.
		self.test_rect = self.char_rect.copy()
		self.test_rect.x += self.dx
		self.test_rect.y += self.dy

		self.hitlist = []  # List for holding collided platform rectangle objects

		# Check for collision with platform rectangles.  'Collidelistall' method returns
		# indices of collided terrain_rects (or -1 if no collision).
		self.hitlist_indices = self.test_rect.collidelistall(self.game.level_1.terrain_rects)

		# if no collision, apply normal change in position
		if not self.hitlist_indices:
			self.char_rect.x += self.dx
			self.char_rect.y += self.dy
			return


		# convert indices into a list containing the actual
		# platform rectangles

		if self.hitlist_indices:
			self.collision_status = 'collision'
			for i in range(len(self.hitlist_indices)):
				self.hitlist.append(self.game.level_1.terrain_rects[self.hitlist_indices[i]])
			# process each of the collided platforms
			for hit in self.hitlist:
				self.process_hit(hit)
			return

		self.collision_status = 'error'

	def process_hit(self, hit_rectangle):
		'''Test to see what side 'char rect' collided with and apply
		appropriate changes in position and velocity.  Will test
		x and y changes separately to determine what side has
		collided.'''

		# Test horizonal collision first
		self.char_rect.x += self.dx

		if self.char_rect.colliderect(hit_rectangle) == True:
			if self.dx > 0:
				# char collided on her right side, reset accordingly
				self.collision_status = 'right'
				self.char_rect.right = hit_rectangle.left
				self.dx = 0
			elif self.dx < 0:
				# char collided on her left side, reset accordingly
				self.collision_status = 'left'
				self.char_rect.left = hit_rectangle.right
				self.dx = 0

		# Test vertical collision
		self.char_rect.y += self.dy

		# run the test
		if self.char_rect.colliderect(hit_rectangle) == True:
			if self.dy > 0:
				# collided with floor, reset accordingly
				self.collision_status = 'floor'
				self.char_rect.bottom = hit_rectangle.top
				self.dy = 0
				self.on_ground = True
			elif self.dy < 0:
				# collided with ceiling, reset accordingly
				self.collision_status = 'ceiling'
				self.char_rect.top = hit_rectangle.bottom
				self.dy = 0
			else:
				self.collision_status = 'boobs'

	def check_for_collision(self, x, y, width, height, rectangles):
		''' takes a rectangle and checks to see if it collides with
		any of the given rectangles.
		Return boolean'''

		# Create a test rectangle
		self.test_rect = pygame.Rect(x, y, width, height)

		# check for collision withrectangles, store
		# resulting indices in a list
		self.hitlist_index = self.test_rect.collidelist(rectangles)

		if self.hitlist_index == -1:
			return False
		else:
			return True




class Enemy(pygame.sprite.Sprite):

	def __init__(self, (x, y)):
		super(Enemy, self).__init__()

		self.alive = True
		self.death_march = 10000

class Bee(Enemy):
	def __init__(self, (x, y)):
		Enemy.__init__(self, (x, y))

		self.img_bee_l = assets.enemy_ssheet.get_image(constants.ENEMY_IMAGES['bee'])
		self.img_bee_r = pygame.transform.flip(self.img_bee_l, True, False)
		self.img_bee_dead_l = assets.enemy_ssheet.get_image(constants.ENEMY_IMAGES['bee_dead'])
		self.img_bee_dead_r = pygame.transform.flip(self.img_bee_dead_l, True, False)

		self.image = self.img_bee_l
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.can_buzz = True

	def buzz(self, krystal, bee_sound):
		'''play a buzzing sound once, when bee gets close to krystal'''
		if (self.rect.x - krystal.rect.x) < 400 and (
					self.rect.x - krystal.rect.x) > 0 and self.can_buzz == True:
			bee_sound.play()
			self.can_buzz = False

	def update(self):
		if self.alive == True:
			self.move()
		else:
			self.die()

	def move(self):
		self.rect.x -= 1

	def die(self):
		self.image = pygame.transform.flip(self.img_bee_l, False, True)
		self.rect.y += 7