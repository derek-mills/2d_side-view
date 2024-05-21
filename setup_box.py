import fonts
from constants import *
import pygame

class SetupBox(object):
    def __init__(self, screen,  xy, items, object_id):
        self.id = 0
        self.object_id = object_id  # Affecting object.
        # self.gift_for_child = []
        # self.gift_for_child_edited = False
        # self.parent = parent
        self.x = xy[0]
        self.y = xy[1]
        self.font_size = 25
        self.font_renderer = fonts.all_fonts[self.font_size]
        # self.path = []  # It will be the list of such content: ['attack', 'left hand', 'torso']
        self.menu_items = items  # incoming dict
        self.menu_items_as_list = []
        self.menu_items_rects = []
        # print(items)
        self.menu_items_spacing = 1
        # self.menu_item_width = max(self.define_width(), rect[2])
        self.current_menu_item = 0
        self.current_menu_level = 0
        self.max_number_of_menu_items = 0
        # self.max_number_of_menu_items = len(self.menu_items)
        self.frame_color = WHITE
        self.background_color = GRAY
        self.text_color = WHITE
        self.text_shadow_color = BLACK
        # self.text_shadow_color = (160, 160, 160)

        # self.menu_height = max((self.menu_item_height + self.menu_items_spacing) * self.max_number_of_menu_items, rect[3])
        self.screen = screen
        # self.align = align
        self.intermediate_value = ''
        self.exist = True
        self.collides_with_mouse_cursor = False
        self.ready_to_return_value = False
        self.execute_command = ''
        self.ready_to_close_self = False
        self.menu_item_selected = False
        self.menu_item_height = self.font_size + self.font_size // 2
        # self.menu_item_width = 0
        self.menu_item_width = self.define_width()
        self.menu_height = 0
        # self.menu_height = self.define_height()
        self.rect = pygame.Rect(self.x, self.y, self.menu_item_width, self.menu_height)
