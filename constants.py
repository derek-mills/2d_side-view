import pygame
from pygame.constants import *
# from sound import *
# from game_objects import *
# x = 1.1 * (y / z)
# if z rises, x degrades.
# if y rises, x rises too.

# # control keys:
# K_BLOCK = 'a'
# K_ATTACK = 'd'
# K_SKIP = 'space'
pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode(SCREENSIZE)
# attribs =  pygame.display.gl_get_attribute(pygame.OPENGL)
pygame.display.init()
modes = pygame.display.list_modes()
screen = pygame.display.set_mode(modes[0])
# print(pygame.display.get_desktop_sizes())
# print(f'{modes[0]}')
# exit()

FPS = 60
MENU_FONT_SIZE = 20

MAXX = modes[0][0]
# MAXX = 1366
MAXY = modes[0][1]
# MAXY = 768
# MAXY = int(MAXX // 1.4142857)
MAXX_DIV_2 = MAXX // 2
MAXY_DIV_2 = MAXY // 2
GRAVITY = 1
GRAVITY_G = 30

CONTROL_PANEL_WIDTH = MAXX
CONTROL_PANEL_HEIGHT = 100
INFO_WINDOW_HEIGHT = CONTROL_PANEL_HEIGHT
INFO_WINDOW_WIDTH = MAXX // 3
INFO_HOVER_MESSAGE_FONT_SIZE = 15
INFO_HOVER_MESSAGE_SCREEN_EDGE_OFFSET = 50
INFO_HOVER_MESSAGE_SPACING = INFO_HOVER_MESSAGE_FONT_SIZE + INFO_HOVER_MESSAGE_FONT_SIZE // 2
INFO_HOVER_MESSAGE_WIDTH = 100
INFO_HOVER_MESSAGE_HEIGHT = 100
INFO_HOVER_MESSAGE_SCREEN_BOTTOM_OFFSET = MAXY - INFO_HOVER_MESSAGE_HEIGHT
OUTLINE_DOTS_COUNTER = 5
FOREGROUND_PARALLAX_SPEED = 1.5
# FOREGROUND_PARALLAX_SPEED = 0.7

SCREENSIZE = (MAXX, MAXY + CONTROL_PANEL_HEIGHT)
SCREEN_SCALE: float = 1
GOLDEN_RATIO_X_SMALL = int(MAXX / 100 * 38)
GOLDEN_RATIO_X_BIG = int(MAXX / 100 * 62)
GOLDEN_RATIO_Y_SMALL = int(MAXY / 100 * 38)
GOLDEN_RATIO_Y_BIG = int(MAXY / 100 * 62)

SOUND_VOLUME = 0.1
MUSIC_VOLUME = 0.3
music_ambient_1 = 'music/ambient_1.mp3'
music_fight_1 = 'music/fight_1.mp3'

DEFAULT_MOUSE_CURSOR_SIZE = 50
DEFAULT_MOUSE_CURSOR_SIZE_DIV_2 = 25

DEFAULT_DARKNESS_DEEPNESS = 240

# print(GOLDEN_RATIO_X_SMALL, GOLDEN_RATIO_X_BIG)
# print(GOLDEN_RATIO_Y_SMALL, GOLDEN_RATIO_Y_BIG)
BLACK = (0,   0,   0)
GRAY = (100, 100, 100)
DARKGRAY = (20, 20, 20)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 97, 0)
RED = (255,   0,   0)
MAGENTA = (200,   0,   255)
YELLOW = (255,   255,  0)
VIOLET = (150,   150,  200)
PINK = (255,   200,  200)
CYAN = (64,   255,  255)
BROWN = (40,   20,  0)
DARK_ORANGE = (150,45,35)
ALL_COLORS = (DARK_ORANGE, DARKGRAY, GRAY, GREEN, RED, MAGENTA, YELLOW, PINK, VIOLET, BLUE, BLACK, WHITE, CYAN, BROWN)
COMIX_BORDER_WIDTH = 5
COMIX_BORDER_GAP = 20
COMIX_BACKGROUND_COLOR = BLACK
COMIX_BORDER_COLOR = WHITE

# comix = {
#     # 'frames': ((0, 1),
#     #            (5, 4, 6),
#     #            (2, 3)
#     #           ),
#     'sprites':
#         {
#         0:
#             {'dedicated to': 'first avatar',
#              # 'borders': (50, 38),
#              'borders': ((0, 50), (0, 38)),
#              'sprite offset': (0, 0),
#              'sprite flip': True,
#              'sprite additional attribute': '',
#              'sprite name': None,
#              'frame visible': False,
#              'already done': False,
#              'text': {'content': '', 'snap': 'bottom', 'shape': 'rect', 'font size': 30, 'align': 'center', 'already printed': False, 'reveal counter': 0}
#              },
#         1:
#             {'dedicated to': 'second avatar',
#              # 'borders': (50, 38),
#              'borders': ((50, 100), (0, 38)),
#              'sprite offset': (300, 0),
#              'sprite flip': False,
#              'sprite additional attribute': '',
#              'sprite name': None,
#              'frame visible': False,
#              'already done': False,
#              'text': {'content': '', 'snap': 'bottom', 'shape': 'rect', 'font size': 20, 'align': 'center', 'already printed': False, 'reveal counter': 0}
#              },
#         2:
#             {'dedicated to': 'first act window',
#              # 'borders': (50, 41),
#              'borders': ((0, 50), (60, 100)),
#              'sprite offset': (0, 0),
#              'sprite flip': True,
#              'sprite additional attribute': '',
#              'sprite name': None,
#              'frame visible': False,
#              'already done': False,
#              'text': {'content': '', 'snap': 'top', 'shape': 'rect', 'font size': 20, 'align': 'center', 'already printed': False, 'reveal counter': 0}
#              },
#         3:
#             {'dedicated to': 'second act window',
#              # 'borders': (51, 41),
#              'borders': ((50, 100), (60, 100)),
#              'sprite offset': (0, 0),
#              'sprite flip': False,
#              'sprite additional attribute': '',
#              'sprite name': None,
#              'frame visible': False,
#              'already done': False,
#              'text': {'content': '', 'snap': 'top', 'shape': 'rect', 'font size': 20, 'align': 'center', 'already printed': False, 'reveal counter': 0}
#              },
#         4:
#             {'dedicated to': 'power meter window',
#              # 'borders': (60, 21),
#              'borders': ((20, 80), (38, 60)),
#              'sprite offset': (-100, -200),
#              'sprite flip': False,
#              'sprite additional attribute': '',
#              'sprite name': 'room1',
#              'frame visible': False,
#              'already done': False,
#              'text': {}
#              },
#         5:
#             {'dedicated to': 'final act window',
#              # 'borders': (51, 41),
#              'borders': ((0, 100), (38, 100)),
#              'sprite offset': (0, 0),
#              'sprite flip': False,
#              'sprite additional attribute': '',
#              'sprite name': None,
#              'frame visible': False,
#              'already done': False,
#              'text': {'content': '', 'snap': 'top', 'shape': 'rect', 'font size': 20, 'align': 'center', 'already printed': False, 'reveal counter': 0}
#              },
#         },
#     # Balloon-type tip:
#     # 'text': {'content': 'HAHAHA, YOU FOOL!', 'snap': 'relative', 'shape': 'balloon', 'rect': pygame.Rect(0, -10, 300, 100),
#     #          'talk signal': (100, 150), 'font size': 15, 'align': 'center', 'already printed': False}
#
#
#     # 'width': MAXX_DIV_2,  # Comix width
#     'width': MAXX,  # Comix width
#     'height': MAXY,  # Comix height
#     # 'start_x': COMIX_BORDER_GAP // 2 + (MAXX_DIV_2 - MAXX_DIV_2 // 2),  # Left start x coordinate
#     'start_x': COMIX_BORDER_GAP // 2,  # Left start x coordinate
#     'start_y': COMIX_BORDER_GAP // 2  # Upper start coordinate.
# }

