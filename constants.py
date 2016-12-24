import imaging

#color constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (67, 111, 168)
PINK = (255, 0, 128)

#display and level size constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 640
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

#level constants -->  width, height, x location, y location
LEVEL_01 = [[0, 0, 0, 0]]

#character constants
HERO_SIZE = (50, 60)
STARTING_POSITION_X, STARTING_POSITION_Y = DISPLAY_WIDTH / 6, DISPLAY_HEIGHT * 3 / 4
HERO_RUNNING_SPEED = 7
HERO_JUMP_VELOCITY = 16

#other constants
GRAVITY_CONSTANT = 1
BULLET_SPEED = 20

#dictionaries of image locations
KRYSTAL_IMAGES = imaging.get_image_locations('assets/krystal_images/image_locations.json')
KRYSTAL_OFFSETS = imaging.get_krystal_offsets()
L_1_ENEMIES_1 = imaging.get_image_locations('assets/level_1_assets/level_1_enemies_1.json')
KRYSTAL_INFLATE_X = 20
KRYSTAL_INFLATE_Y = 20
BEE_INFLATE_X = 30
BEE_INFLATE_Y = 10
VULTURE_INFLATE_X = 0
VULTURE_INFLATE_Y = 0
