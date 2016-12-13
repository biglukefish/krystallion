"""this module contains the character class, for generating
characters in the game"""

import pygame
import constants
import spritesheet
import assets



class Krystal(pygame.sprite.Sprite):
	dx = 0
	dy = 0
	moving_horizontally = False
	shooting = False
	action = 'idle'  # options are: run, jump, slide, shoot, stab, or idle
	facing = 'right'
	collision_side = ''
	JUMP_VELOCITY = constants.HERO_JUMP_VELOCITY
	on_ground = True
	collision_status = 'none'
	dead_frame = 0
	shot_frame = 0
	idle_frame = 0
	jump_frame = 0
	run_frame = 0
	pacer = 0

	# frames for animation
	dead_frames = constants.KRYSTAL_IMAGES[0:9]
	idle_frames = constants.KRYSTAL_IMAGES[9:16]
	jump_frames = constants.KRYSTAL_IMAGES[16:26]
	melee_frames = constants.KRYSTAL_IMAGES[26:33]
	run_frames = constants.KRYSTAL_IMAGES[33:41]
	shot_frames = constants.KRYSTAL_IMAGES[41:44]
	slide_frames = constants.KRYSTAL_IMAGES[44:49]
	shot_frames_offset = constants.KRYSTAL_OFFSETS[41:44]



	def __init__(self, game):
		super(Krystal, self).__init__()

		self.game = game
		self.hitlist_indices = []
		self.is_hit = False


		self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[0])
		self.rect = self.image.get_rect()
		self.char_rect = pygame.Rect(0, 0, self.rect.width * 2 / 3, self.rect.height * 3 / 4)
		self.char_rect.x, self.char_rect.y = constants.STARTING_POSITION_X, constants.STARTING_POSITION_Y

	def move_horizontal(self):
		if self.moving_horizontally == True:
			if self.facing == 'right':
				self.dx += constants.HERO_RUNNING_SPEED
			elif self.facing == 'left':
				self.dx -= constants.HERO_RUNNING_SPEED


	def jump(self):
		'''applies jump if char is standing on ground'''
		if self.on_ground == True:
			self.dy -= constants.HERO_JUMP_VELOCITY
			self.on_ground = False
			self.action = 'jump'

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
		self.update_image()
		self.pacer += 1

		self.dx = 0
		#temp code to catch character if she falls off screen
		if self.char_rect.bottom > constants.DISPLAY_HEIGHT:
			self.char_rect.bottom = constants.DISPLAY_HEIGHT - 5



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

	def update_image(self):
		'''determines the value of self.action'''
		if self.shooting == True:
			self.animate_shot()
		else:
			self.shot_frame = 0
			if self.on_ground == False:
				self.action = 'jump'
				self.animate_jump()
			elif self.on_ground == True and self.moving_horizontally == True:
				self.action = 'run'
				self.animate_run()
			elif self.on_ground == True and self.moving_horizontally == False:
				self.action = 'idle'
				self.animate_idle()


	def animate_shot(self):
			if self.action != 'shoot':
				self.shot_frame = 0
				self.action = 'shoot'
				if self.facing == 'right':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
				elif self.facing == 'left':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
					self.image = pygame.transform.flip(self.image, True, False)
					self.shot_frame += 1
			elif self.action == 'shoot' and self.shot_frame < 2:
				if self.facing == 'right':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
				elif self.facing == 'left':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
					self.image = pygame.transform.flip(self.image, True, False)
				self.shot_frame += 1
			elif self.action == 'shoot' and self.shot_frame == 2:
				if self.facing == 'right':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
				elif self.facing == 'left':
					self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
					self.image = pygame.transform.flip(self.image, True, False)



	def animate_jump(self):
		if self.action == 'jump' and self.jump_frame < 9:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 3 == 0:
				self.jump_frame += 1

		elif self.action == 'jump' and self.jump_frame == 9:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			self.jump_frame = 0

		elif self.action != 'jump':
			self.jump_frame = 0
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.jump_frames[self.jump_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 3 == 0:
				self.jump_frame += 1

	def animate_idle(self):
		if self.action == 'idle' and self.idle_frame < 6:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 4 == 0:
				self.idle_frame += 1

		elif self.action == 'idle' and self.idle_frame == 6:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			self.idle_frame = 0

		elif self.action != 'idle':
			self.idle_frame = 0
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[self.idle_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 4 == 0:
				self.idle_frame += 1

	def animate_run(self):
		if self.action == 'run' and self.run_frame < 7:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 4 == 0:
				self.run_frame += 1

		elif self.action == 'run' and self.run_frame == 7:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			self.run_frame = 0

		elif self.action != 'run':
			self.run_frame = 0
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.run_frames[self.run_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 4 == 0:
				self.run_frame += 1



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
