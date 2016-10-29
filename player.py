"""this module contains the player class, for generating our hero"""
import pdb
import pygame
import earth
import level
import constants
import spritesheet

class Player(pygame.sprite.Sprite):

#attributes
	change_x = 0
	change_y = 0
	can_jump = True
	facing = 'right'
	running = False
	collision_side = ''
	RUNNING_SPEED = 4
	JUMP_VELOCITY = 15
	test_rect = pygame.Rect(0, 0, 0, 0)
	outline = pygame.Rect(0, 0, 0, 0)


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

	def move_left(self):

		self.change_x -= self.RUNNING_SPEED

	def move_right(self):

		self.change_x += self.RUNNING_SPEED


	def stop(self):
		self.change_x = 0


	def jump(self, platform_sprite_list):

		if self.change_y >= -1:
			self.change_y -= self.JUMP_VELOCITY
		

	def apply_gravity(self):
		#simulate gravity by making player fall

		if self.change_y < 100:
			self.change_y += constants.GRAVITY_CONSTANT

		


	def update(self, platform_sprite_list):

		
		#add in the effects of gravity
		self.apply_gravity()

		#move the player
		self.apply_collision(platform_sprite_list)



		# as a fail-safe, make sure player doesn't fall out of screen
		# on bottom or shoot out on top or bail on left or right
		if self.rect.bottom >= constants.DISPLAY_HEIGHT:
			self.rect.bottom = constants.DISPLAY_HEIGHT
			self.change_y = 0
		if self.rect.top < 0:
			self.rect.top = 0
			self.change_y -= self.change_y
		if self.rect.left < 50:
			self.rect.left = 50
		if self.rect.right > 400:
			self.rect.right = 400

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



	def apply_collision(self, platform_sprite_list):
		'''Update position of player based on collision 
		detection (or lack thereof)'''

		# Create a copy of the rectangle for collision test
		self.test_rect = self.rect.copy()
		self.test_rect.x += self.change_x
		self.test_rect.y += self.change_y

		# creates a list of each sprite's rect
		sprite_rect_list = []
		for sprite in platform_sprite_list:
			sprite_rect_list.append(sprite.rect)
		self.hit = self.test_rect.collidelist(sprite_rect_list)
		collided_platform = sprite_rect_list[self.hit]

		
		# if no collision, apply normal change in position
		if self.hit == -1:
			self.rect.x += self.change_x
			self.rect.y += self.change_y

		# if there is a collision, test to see what side and apply
		# appropriate changes in position and velocity
		elif self.hit != -1:


			# Adjust test rectangle to check what happens if it had only 
			# moved horizontally
			self.test_rect.y -= self.change_y  

			#run the test
			if (self.test_rect.collidelist(sprite_rect_list) != -1
				and self.change_x > 0):
				# collided with left side of platform, so reset accordingly
				print 'collided with left side of platform'
				self.rect.right = collided_platform.left
				self.rect.y += self.change_y
				return
			elif (self.test_rect.collidelist(sprite_rect_list) != -1
				and self.change_x < 0):
				# collided with right side of platform, so reset accordingly
				print 'collided with right side of platform'
				self.rect.left = collided_platform.right
				self.rect.y += self.change_y
				return



			# Adjust test rectangle to check what happens if it had only
			# moved vertically
			self.test_rect.y += self.change_y
			self.test_rect.x -= self.change_x

			#run the test
			if (self.test_rect.collidelist(sprite_rect_list) != -1
				and self.change_y > 0):
				# collided with top side of platform, so reset accordingly
				print 'collided with top side of platform'
				self.rect.bottom = collided_platform.top
				self.rect.x += self.change_x
				self.change_y = 0
				return


			elif (self.test_rect.collidelist(sprite_rect_list) != -1
				and self.change_y < 0):
				# collided with bottom side of platform, so reset accordingly
				print 'collided with bottom of platform'
				self.rect.top = collided_platform.bottom
				self.rect.x += self.change_x
				self.change_y = 0
				return

			print 'made it through all statements'

			





		

