import imaging
import spritesheet

#color constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (67, 111, 168)
PINK = (255, 0, 128)

#display and level size constants
DISPLAY_WIDTH = 675
DISPLAY_HEIGHT = 400
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

#level constants -->  width, height, x location, y location
LEVEL_01 = [[0, 0, 0, 0]]

#character constants
HERO_SIZE = (50, 60)
STARTING_POSITION_X, STARTING_POSITION_Y = DISPLAY_WIDTH / 3, DISPLAY_HEIGHT * 3 / 4
HERO_RUNNING_SPEED = 5
HERO_JUMP_VELOCITY = 16

#other constants
GRAVITY_CONSTANT = 1
BULLET_SPEED = 11

#dictionaries of image locations
ENEMY_IMAGES = imaging.Xmlenemies().get_small_dict()

#lists of krystal image locations
KRYSTAL_STANDING = [
	(0, 0, 50, 60), (50, 0, 50, 60), (100, 0, 50, 60),
	(150, 0, 50, 60), (200, 0, 50, 60), (250, 0, 50, 60)]
KRYSTAL_WALKING = [
	(0, 60, 50, 60), (50, 60, 50, 60),
	(100, 60, 50, 60), (150, 60, 50, 60)]
KRYSTAL_JUMPING = [
	(200, 60, 50, 55), (250,60, 50, 55)]
KRYSTAL_FLYING = [
	(200, 60, 50, 55)]
KRYSTAL_FALLING = [
	(250, 195, 50, 60)]


