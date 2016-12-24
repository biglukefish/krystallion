"""this module contains the character class, for generating
characters in the game"""

import pygame
import constants
import spritesheet
import assets
import math



class Krystal(pygame.sprite.Sprite):
	life = 3
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
	invincible_counter = 0
	invincible = False

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
		self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[0])
		self.rect = self.image.get_rect()
		self.rect = self.rect.inflate(
			- constants.KRYSTAL_INFLATE_X,
			- constants.KRYSTAL_INFLATE_Y
		)
		self.rect.x, self.rect.y = constants.STARTING_POSITION_X, \
								   constants.STARTING_POSITION_Y

		# trigger locations
		self.bee_triggers = [
			'self.rect.x > 300', 'self.rect.x > 900',
			'self.rect.x > 2000', 'self.rect.x > 2500',
			'self.rect.x > 4000', 'self.rect.x > 5000'
		]
		self.vulture_triggers = [
			'self.rect.x > 300', 'self.rect.x > 900',
			'self.rect.x > 2000', 'self.rect.x > 2500',
			'self.rect.x > 4000', 'self.rect.x > 5000'
		]

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

		if self.check_for_collision(
				self.rect.x, self.rect.y + 2,
				self.rect.width, self.rect.height,
				self.game.level_1.all_collision_rects
				) == False and self.dy < 50:
			self.on_ground = False
			self.dy += constants.GRAVITY_CONSTANT
		else:
			self.on_ground = True

	def update(self):

		self.apply_gravity()
		self.apply_collisions()
		self.update_image()
		self.apply_triggers()
		self.pacer += 1
		self.dx = 0
		if self.invincible:
			self.go_invincible()

		if self.rect.y > constants.DISPLAY_HEIGHT:
			self.life = 0



	def apply_collisions(self):
		'''handles collision, produces side effect of moving dx, dy'''

		platform_hits_x = []
		platform_hits_y = []
		mushroom_hits_x = []
		mushroom_hits_y = []

		self.rect.x += self.dx

		platform_hits_x = pygame.sprite.spritecollide(self, self.game.level_1.platform_sprites, False)
		mushroom_hits_x = pygame.sprite.spritecollide(self, self.game.level_1.shroom_sprites, False)

		for platform in platform_hits_x:
			self.process_platform_collision('x', platform)
		for mushroom in mushroom_hits_x:
			self.process_mushroom_collision('x', mushroom)

		if mushroom_hits_x:
			return

		self.rect.y += self.dy

		platform_hits_y = pygame.sprite.spritecollide(self, self.game.level_1.platform_sprites, False)
		for platform in platform_hits_y:
			self.process_platform_collision('y', platform)
		mushroom_hits_y = pygame.sprite.spritecollide(self, self.game.level_1.shroom_sprites, False)
		for mushroom in mushroom_hits_y:
			self.process_mushroom_collision('y', mushroom)


	def hit_sequence(self):
		self.life -= 1
		self.invincible = True



	def process_platform_collision(self, axis, platform):

		if axis == 'x':
			if self.dx > 0:
				# char collided on her right side, reset accordingly
				self.collision_status = 'right'
				self.rect.right = platform.rect.left
				self.dx = 0
			elif self.dx < 0:
				# char collided on her left side, reset accordingly
				self.collision_status = 'left'
				self.rect.left = platform.rect.right
				self.dx = 0
		if axis == 'y':
			if self.dy > 0:
				# collided with floor, reset accordingly
				self.collision_status = 'floor'
				self.rect.bottom = platform.rect.top
				self.dy = 0
				self.on_ground = True
			elif self.dy < 0:
				# collided with ceiling, reset accordingly
				self.collision_status = 'ceiling'
				self.rect.top = platform.rect.bottom
				self.dy = 0

	def process_mushroom_collision(self, axis, mushroom):

		if axis == 'x':
			if not self.invincible:
				self.hit_sequence()


		if axis == 'y':
			mushroom.alive = False
			mushroom.add(self.game.level_1.dead_sprites)
			mushroom.remove(self.game.level_1.shroom_sprites)

	def check_for_collision(self, x, y, width, height, rectangles):
		''' takes a rectangle and checks to see if it collides with
		any of the given rectangles.  Used exclusively for the gravity function.
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
		if self.life == 0:
			self.animate_dead()
		elif self.shooting == True:
			self.action = 'shooting'
			self.animate_shot()
		else:
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
		if self.facing == 'right':
			self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
		elif self.facing == 'left':
			self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.shot_frames[self.shot_frame])
			self.image = pygame.transform.flip(self.image, True, False)
		self.blit_frame = self.shot_frame  # need to do this to implement correct offset when blitting shot
		if self.pacer % 4 == 0:
			self.shot_frame += 1

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

	def animate_dead(self):
		if self.dead_frame < 9:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.dead_frames[self.dead_frame])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.dead_frames[self.dead_frame])
				self.image = pygame.transform.flip(self.image, True, False)
			if self.pacer % 4 == 0:
				self.dead_frame += 1

		else:
			if self.facing == 'right':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[8])
			elif self.facing == 'left':
				self.image = spritesheet.KRYSTAL_SPRITESHEET.get_image(self.idle_frames[8])
				self.image = pygame.transform.flip(self.image, True, False)

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

	def apply_triggers(self):
		'''creates enemy if Krystal is within range, then
		removes enemy from trigger list
		'''
		try:
			if eval(self.vulture_triggers[0]):
				vulture = Vulture(self.game.level_1.vulture_coords[0])
				self.game.level_1.vulture_sprites.add(vulture)
				self.vulture_triggers.pop(0)
				self.game.level_1.vulture_coords.pop(0)
		except IndexError:
			pass

	def go_invincible(self):
		print "I'm invincible!"
		self.invincible_counter += 1
		if self.invincible_counter > 120:
			self.invincible_counter = 0
			self.invincible = False



class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()

		self.alive = True
		self.death_march = 10000


class Vulture(Enemy):
	def __init__(self, (x, y)):
		Enemy.__init__(self)

		self.image_locations = constants.L_1_ENEMIES_1[34:]
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[34])
		self.current_animation_frame = 34
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect = self.rect.inflate(- constants.VULTURE_INFLATE_X, - constants.VULTURE_INFLATE_Y)
		self.upperbound = y - 40
		self.lowerbound = y + 40
		self.dx = -7
		self.dy = -4
		self.pacer = 1


	def update(self):
		self.pacer += 1
		if self.alive == True:
			self.move()
			self.animate()
		else:
			self.die()

	def move(self):
		self.rect.x += self.dx

	def animate(self):
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.current_animation_frame])
		self.image = pygame.transform.flip(self.image, True, False)
		if self.pacer % 4 == 0:
			self.current_animation_frame += 1
		if self.current_animation_frame == 38:
			self.current_animation_frame = 34

	def die(self):

		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.current_animation_frame])
		self.image = pygame.transform.flip(self.image, True, True)
		self.rect.y += 14


class Shroom(Enemy):
	def __init__(self, (x, bottom, left_bound, right_bound)):
		Enemy.__init__(self)

		self.alive = True
		self.image_loc_alive = constants.L_1_ENEMIES_1[15:23]
		self.image_loc_dead = constants.L_1_ENEMIES_1[11:15]
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[15])
		self.alive_animation_frame = 15
		self.dead_animation_frame = 11
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.bottom = bottom + 5
		# self.rect = self.rect.inflate( - constants.SHROOM_INFLATE_X, - constants.SHROOM_INFLATE_Y)
		self.left_bound = left_bound
		self.right_bound = right_bound
		self.dx = -2
		self.pacer = 0

	def update(self):
		if self.alive == True:
			self.animate_alive()
			self.move()
		elif self.alive == False:
			self.animate_dead()
			self.newrect = self.image.get_rect()
			self.newrect.bottomleft = self.rect.bottomleft
			self.rect = self.newrect

		self.pacer += 1

	def move(self):
		if self.rect.x < self.left_bound or self.rect.x > self.right_bound:
			self.dx = -self.dx
		self.rect.x += self.dx

	def animate_alive(self):
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.alive_animation_frame])
		self.image = pygame.transform.flip(self.image, True, False)
		self.alive_animation_frame += 1
		if self.alive_animation_frame == 23:
			self.alive_animation_frame = 15

	def animate_dead(self):
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.dead_animation_frame])
		self.image = pygame.transform.flip(self.image, True, False)
		if self.pacer % 3 == 0:
			self.dead_animation_frame += 1
		if self.dead_animation_frame == 15:
			self.kill()

class Bee(Enemy):
	'''Bee that goes in a circle.  x,y passed to init represent center of circle'''
	def __init__(self, (x, y)):
		Enemy.__init__(self)

		self.image_locations = constants.L_1_ENEMIES_1[3:11]
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[3])
		self.current_animation_frame = 3
		self.rect = self.image.get_rect()
		self.center_x = x
		self.center_y = y
		self.centerpivot = self.rect.center
		self.rect = self.rect.inflate(- constants.BEE_INFLATE_X, - constants.BEE_INFLATE_Y)
		self.can_buzz = True
		self.degrees = 0

	def buzz(self, krystal, bee_sound):
		'''play a buzzing sound once, when bee gets close to krystal'''
		if (self.rect.x - krystal.rect.x) < 400 and (
					self.rect.x - krystal.rect.x) > 0 and self.can_buzz == True:
			bee_sound.play()
			self.can_buzz = False

	def update(self):
		if self.alive == True:
			self.move()
			self.animate()

		else:
			self.die()

	def move(self):
		self.degrees += 9
		self.rads = math.radians(self.degrees)
		self.rect.y = 60 * math.sin(self.rads) + self.center_y
		self.rect.x = 40 * math.cos(self.rads) + self.center_x


	def animate(self):
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.current_animation_frame])
		self.image = pygame.transform.flip(self.image, True, False)
		self.current_animation_frame += 1
		if self.current_animation_frame == 11:
			self.current_animation_frame = 3

	def die(self):
		self.image = assets.enemy_ssheet_1.get_image(constants.L_1_ENEMIES_1[self.current_animation_frame])
		self.image = pygame.transform.flip(self.image, False, True)
		self.rect.y += 14