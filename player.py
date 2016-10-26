"""this module contains the player class, for generating our hero"""
import pdb
import pygame
import earth
import level
import constants

class Player(pygame.sprite.Sprite):

#attributes
	change_x = 0.0
	change_y = 0.0
	can_jump = True
	facing = 'right'
	running = False
	collision_side = ''
	RUNNING_SPEED = 4
	JUMP_VELOCITY = 15
	test_rect = pygame.Rect(0, 0, 0, 0)


#methods
	def __init__(self):  #call to constructor

		super(Player, self).__init__()  #call to parent constructor

		# self.image = pygame.image.load('tiny_krystal.png')
		self.image = pygame.image.load('tiny_krystal.png')
		self.image.set_colorkey(constants.BLACK)
		self.rect = self.image.get_rect()
		self.hitbox = pygame.Rect(0, 0, 40, 60)

	
	def move_left(self):

		self.change_x -= self.RUNNING_SPEED
			

	def move_right(self):

		self.change_x += self.RUNNING_SPEED


	def stop(self):
		self.change_x = 0


	def jump(self, platform_sprite_list):

		self.change_y -= self.JUMP_VELOCITY
		print 'change_y after jump= ' + str(self.change_y)
		

	def apply_gravity(self):
		#simulate gravity by making player fall

		if self.change_y < 100:
			self.change_y += constants.GRAVITY_CONSTANT
		


	def update(self, platform_sprite_list, last_move):

		
		#add in the effects of gravity
		self.apply_gravity()
		print 'after first applying gravity, change y= ' + str(self.change_y)

		
		print "change y before update= " + str(self.change_y)
		print "bottom of rect before update= " + str(self.rect.bottom)


		collision_side = self.test_collision_side(platform_sprite_list)
		print collision_side

		if collision_side == 'none':
			self.rect.x += self.change_x
			self.rect.y += self.change_y
		else:
			self.apply_collision(platform_sprite_list, collision_side)



		# make sure player doesn't fall out of screen
		if self.rect.bottom >= constants.DISPLAY_HEIGHT:
			self.rect.bottom = constants.DISPLAY_HEIGHT
			self.change_y = 0



	def test_collision_side(self, platform_sprite_list):
	

		self.test_rect = self.rect.copy()
		self.test_rect.x += self.change_x
		self.test_rect.y += self.change_y
		# creates a list of each sprite's rect
		sprite_rect_list = []
		for sprite in platform_sprite_list:
			sprite_rect_list.append(sprite.rect)
		self.hit = self.test_rect.collidelist(sprite_rect_list)
		collided_platform = sprite_rect_list[self.hit]

		

		if self.hit == -1:
				return 'none'


		if self.hit != -1:
			print 'self.hit != -1'


			# Check for vertical collision
			
			if (self.rect.bottom + self.change_y > collided_platform.top 
				and self.change_y > 0):
				return 'bottom collision'

			elif (self.rect.top + self.change_y < collided_platform.bottom 
				and self.change_y < 0):
				return 'top collision'


			# Check for horizontal collision
			elif (self.rect.left + self.change_x < collided_platform.right 
				and self.rect.right + self.change_x > collided_platform.left
				and self.change_x < 0):
				return 'left collision'

				
			elif (self.rect.right + self.change_x > collided_platform.left 
				and self.rect.left + self.change_x < collided_platform.right 
				and self.change_x > 0):
				return 'right collision'

				print('right collided with platform')

				self.rect.right = collided_platform.left

			else:
				return 'something is fucked up'


	def apply_collision(self, platform_sprite_list, collision_side):

		self.test_rect = self.rect.copy()
		self.test_rect.x += self.change_x
		self.test_rect.y += self.change_y
		# creates a list of each sprite's rect
		sprite_rect_list = []
		for sprite in platform_sprite_list:
			sprite_rect_list.append(sprite.rect)
		self.hit = self.test_rect.collidelist(sprite_rect_list)
		collided_platform = sprite_rect_list[self.hit]

		

		if self.hit == -1:
				return 'none'


		if self.hit != -1:
			print 'self.hit != -1'

		
		if collision_side == 'top':
			self.rect.bottom = collided_platform.top
		elif collision_side == 'bottom':
			self.rect.top = collided_platform.bottom
		elif collision_side == 'left':
			self.rect.left = collided_platform.right
		elif collision_side == 'right':
			self.rect.right = collided_platform.left



			





		

