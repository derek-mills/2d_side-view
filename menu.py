import fonts
from constants import *
import pygame
# EXAMPLE:
# menu={
# 'evade': None,
# 'attack': {'right hand': {'head': None, 'torso': None}, 'left hand': {'head': None, 'torso': None}},
# 'defend': {'head': None, 'torso': None},
# 'stay still': None
# }


class Menu(object):
    def __init__(self, items, screen, xy, parent, align='left'):
        # def __init__(self, items, screen, rect, parent, align='left'):
        self.id = 0
        self.gift_for_child = []
        self.gift_for_child_edited = False
        self.parent = parent
        self.x = xy[0]
        self.y = xy[1]
        # self.x = rect[0]
        # self.y = rect[1]
        # self.rect = pygame.Rect(rect)
        self.font_size = 25
        self.font_renderer = fonts.all_fonts[self.font_size]
        self.path = []  # It will be the list of such content: ['attack', 'left hand', 'torso']
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
        self.align = align
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

        # self.make_menu_items_list()

    def make_menu_items_list(self):

        # menu = list()
        # print(f'{self.path=}')
        if not self.path:
            # Root menu level.
            self.menu_items_as_list = [i for i in self.menu_items.keys()]
        else:
            tmp = self.menu_items[self.path[0]]
            if not tmp:
                self.ready_to_return_value = True
                self.exist = False
                return
            for i in self.path[1:]:
                # print(f'{i=} {tmp[i]=}')
                # i='brass garden key' tmp[i]='1820dff4-7ddd-11ee-b3a2-3d51d47c287c'
                if tmp[i]:
                    if type(tmp[i]) == dict:
                        # Menu item has submenu:
                        tmp = tmp[i]
                    elif type(tmp[i]) == str:
                    # elif tmp[i][0] == '@':
                        self.ready_to_return_value = True
                        self.exist = False
                        self.execute_command = tmp[i]
                        # self.execute_command = tmp[i][1:]
                        return
                    else:
                        self.ready_to_return_value = True
                        self.exist = False
                        # self.execute_command = ''
                        return
                else:
                    # print(f'{tmp[i]=}')
                    self.ready_to_return_value = True
                    self.exist = False
                    return
                    # exit()

                # print(f'{i=} {tmp=}')
            self.menu_items_as_list = [i for i in tmp.keys()]

        self.max_number_of_menu_items = len(self.menu_items_as_list)
        self.menu_height = self.define_height()
        # print(f'[menu.make_menu_items_list] {self.x=}, {self.y=}, {self.menu_item_width=}, {self.menu_height=}')
        self.rect = pygame.Rect(self.x, self.y, self.menu_item_width, self.menu_height)

        self.current_menu_item = 0
        self.menu_items_rects = list()
        dy = self.rect[1]
        for i in self.menu_items_as_list:
            self.menu_items_rects.append(pygame.Rect(self.rect.x, dy, self.rect.width, self.menu_item_height))
            dy += self.menu_item_height
        # print(f'[menu.make_menu_items_list] {self.menu_items_rects=} {self.menu_items_as_list=}')
        # print(f'[menu.make_menu_items_list] {self.menu_items_as_list=}')
        # print(f'[menu.make_menu_items_list] exit... _____________________________________________')
        # print(f'{self.menu_items_rects=}')
        # print(f'FINAL MENU: {self.menu_items_as_list=}')
        # print()
        # exit()

    def check_path(self):
        self.path.append(self.menu_items_as_list[self.current_menu_item])
        self.current_menu_level = len(self.path) - 1
        self.make_menu_items_list()

    def change_settings(self, xy, font_size):
        self.x = xy[0]
        self.y = xy[1]
        self.font_size = font_size
        self.font_renderer = fonts.all_fonts[self.font_size]
        self.menu_item_height = self.font_size + self.font_size // 2
        self.menu_item_width = self.define_width()
        self.menu_height = (self.menu_item_height + self.menu_items_spacing) * self.max_number_of_menu_items
        self.align = 'center'

    def check_collision(self, point):
        if self.rect.collidepoint(point):
            return True

    def check_collision_with_items(self, point):
        for item in self.menu_items_as_list:
            if self.menu_items_rects[self.menu_items_as_list.index(item)].collidepoint(point):
                self.current_menu_item = self.menu_items_as_list.index(item)
                return

    def process(self, point, left_button_press):
        self.collides_with_mouse_cursor = False
        if self.check_collision(point):
            self.collides_with_mouse_cursor = True
            self.check_collision_with_items(point)
            if left_button_press:
                self.menu_item_selected = True

    def return_value(self):
        # print(f'RETURN: {self.path=}')
        return self.path, self.execute_command

    def define_height(self):
        return (self.menu_item_height + self.menu_items_spacing) * self.max_number_of_menu_items

    def define_width(self):
        length = 0
        for i in self.menu_items.keys():
            # item = self.menu_items[key]
            if len(str(i)) > length:
                length = len(str(i))
        return length * self.font_size

    def switch_menu_item_down(self):
        if self.current_menu_item < (self.max_number_of_menu_items - 1):
            self.current_menu_item += 1
        else:
            self.current_menu_item = 0

    def switch_menu_item_up(self):
        if self.current_menu_item > 0:
            self.current_menu_item -= 1
        else:
            self.current_menu_item = (self.max_number_of_menu_items - 1)

    def erase_self(self):
        pygame.draw.rect(self.screen, BLACK, (self.x - 2, self.y - 2, self.menu_item_width + 4, self.menu_height + self.menu_items_spacing + 2), 0)
        # pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.menu_item_width, self.menu_height), 0, 9)
        pygame.display.update()

    def draw(self):
        dx = self.x
        dy = self.y
        # arrow_text = self.font_renderer.render('>', True, self.text_color)
        # pygame.draw.rect(self.screen, DARKGRAY, (dx - 2, dy - 2, self.menu_item_width + 4, self.menu_height + self.menu_items_spacing + 2), 0)
        pygame.draw.rect(self.screen, pygame.Color(100, 100, 100, 10), (dx - 2, dy - 2, self.menu_item_width + 4, self.menu_height + self.menu_items_spacing + 2), 0)
        for item in self.menu_items_as_list:
            # print('[menu.draw]: ', item)
            if item[0] == '@':
                # Current menu item contains an execute command, so we must cut this command out and render just
                # a name (without leading '@').
                # Such item example: '@Flashlight@print("flashlight switched")'
                # Name and command slit by '@' symbol from each other.
                item = item.split('@')[1]
                # item = item[1:].split('|')[0]
            txt_foreground = self.font_renderer.render(item, True, self.text_color)
            txt_background = self.font_renderer.render(item, True, self.text_shadow_color)
            txt_sz = txt_foreground.get_size()
            if self.align == 'center':
                txt_margin_left = self.menu_item_width // 2 - txt_sz[0] // 2
                txt_margin_top = self.menu_item_height // 2 - txt_sz[1] // 2
            elif self.align == 'right':
                txt_margin_left = self.menu_item_width - txt_sz[0] - 10
                txt_margin_top = self.menu_item_height // 2 - txt_sz[1] // 2
            elif self.align == 'left':
                txt_margin_left = 10
                txt_margin_top = self.menu_item_height // 2 - txt_sz[1] // 2
            # Draw background rect of menu cell:
            pygame.draw.rect(self.screen, self.background_color, (dx, dy, self.menu_item_width, self.menu_item_height), 0, 9)

            # if type(self.menu_items) is dict:
            # print(self.menu_items[item])
            # if self.menu_items[item] is not None:
            #     Draw a tiny arrow if this menu item is reference to another submenu.
            # self.screen.blit(arrow_text, (dx + self.menu_item_width - self.font_size, dy + txt_margin_top, 10, 10))

            self.screen.blit(txt_background, (dx + txt_margin_left + 2, dy + txt_margin_top + 2))
            self.screen.blit(txt_foreground, (dx + txt_margin_left, dy + txt_margin_top))

            # pygame.draw.rect(self.screen, self.background_color, (self.rect.x, self.rect.y - 50, self.rect.width, 50), 0, 9)
            # self.screen.blit(gift_txt_rendered, (self.rect.x, self.rect.y - 50))
            dy += (self.menu_item_height + self.menu_items_spacing)

        if self.intermediate_value:
            txt = fonts.font20.render(self.intermediate_value , True, WHITE)
            txt_sz = txt.get_size()
            pygame.draw.rect(self.screen, pygame.Color(100, 100, 100, 200), (self.rect.centerx - txt_sz[0] // 2 - 10, self.rect.y - 50, txt_sz[0] + 20, 40))
            self.screen.blit(txt, (self.rect.centerx - txt_sz[0] // 2, self.rect.top - 45))

        # Draw frame:
        pygame.draw.rect(self.screen, self.frame_color, (self.x, self.y + self.current_menu_item * (self.menu_item_height + self.menu_items_spacing), self.menu_item_width, self.menu_item_height), 1, 9)

        # debugging text below menu
        # txt = ''
        # for i in self.gift_for_child:
        #     txt += i
        # misc_text = fonts.font20.render(txt, True, RED)
        # self.screen.blit(misc_text, (self.x, self.y + self.menu_height + 10))

        # pygame.display.update((self.x, self.y, self.menu_item_width, self.menu_height))
        # pygame.display.update()

    def extract_menu_items(self, incoming_stuff):
        def return_menu_items(stuff):
            tmp_menu = dict()
            for k in stuff.keys():
                if k == 'settings':
                    continue
                # print(f'{k=} {stuff[k]}')
                if 'settings' in stuff[k].keys():
                    if stuff[k]['settings']['submenu']:
                        tmp_menu[k] = return_menu_items(stuff[k])
                    else:
                        if k != 'settings:':
                            tmp_menu[k] = None
                else:
                    if k != 'settings:':
                        tmp_menu[k] = None
            return tmp_menu

        # menu = return_menu_items(self.available_actions)
        menu = return_menu_items(incoming_stuff)
        # print(f'{menu=}')
        # exit()
        return menu

