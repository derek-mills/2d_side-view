# import pygame
import uuid

import pygame

from constants import *
# from locations import *
# from world import *
# try:
#     from locations import *
# except ModuleNotFoundError:
#     pass
from obstacle import *
from demolisher import *
import camera
import fonts
# from sound import *
# import json
# import pickle
# import setup_box
# import menu
from uuid import *
import importlib


class World(object):
    def __init__(self):

        self.need_to_load = False
        self.allow_import_locations = False
        self.clipboard = dict()
        self.default_font_size = 15
        # CONTROLS
        self.is_key_pressed = False
        self.is_input_up_arrow = False
        self.is_input_down_arrow = False
        self.is_input_right_arrow = False
        self.is_input_left_arrow = False
        self.is_input_confirm = False
        self.input_cancel = False
        self.is_z = False
        self.is_p = False
        self.is_i = False
        self.is_x = False
        self.is_n = False
        self.is_b = False
        # self.is_b = False
        self.is_y = False
        self.is_spacebar = False
        self.is_F2 = False
        self.is_F8 = False
        self.is_l_shift = False
        self.is_l_ctrl = False
        self.is_l_alt = False
        self.is_left_bracket = False
        self.is_right_bracket = False
        self.is_mouse_button_down = False
        self.is_left_mouse_button_down = False
        self.is_right_mouse_button_down = False
        self.is_mouse_wheel_rolls = False
        self.is_mouse_wheel_up = False
        self.is_mouse_wheel_down = False
        self.mouse_xy = list()  #
        self.mouse_xy_global = list()  #
        self.mouse_xy_snapped_to_mesh = list()  #
        self.is_mouse_hovers_item: bool = False
        self.mouse_hovers_item: int = 0
        self.is_mouse_hovers_actor: bool = False
        self.mouse_hovers_actor: int = 0
        self.camera_follows_mouse = True
        self.camera_scroll_speed = 4

        self.object_types = ('obstacle', 'demolisher')
        self.current_object_type = 0

        self.obstacles = dict()
        self.obstacle_id: int = 0
        self.obs_settings = dict()
        self.demolishers = dict()
        self.demolishers_id: int = 0
        # self.location = '01'
        self.location = ''
        self.screen = None
        self.camera = camera.Camera()
        # self.camera.setup(MAXX*2, MAXY)
        self.global_offset_xy = [MAXX_DIV_2, MAXY_DIV_2]

        self.new_obs_rect = pygame.Rect(0,0,0,0)
        self.new_obs_rect_started = False
        self.new_obs_rect_start_xy = [0, 0]

        self.snap_mesh = dict()
        self.snap_mesh_size = 50
        self.snap_mesh_size_change_step = 25
        self.zoom_factor = 1.

        self.menu_items = dict()
        self.menu_item_id = 0
        self.menu_pile_id = 0  # ID of a bunch of tied together menu items
        self.active_menu_pile = 0
        self.menu_buttons_height = 100
        self.menu_buttons_width = 300
        self.menu_small_buttons_height = 50
        self.menu_small_buttons_width = 100
        self.menu_buttons_spacing = 10
        self.menu_headers_height = 100
        self.menu_headers_width = MAXX_DIV_2
        self.menu_screen_edge_margin = 50
        self.menu_elements_bindings = {
            'top header': (MAXX_DIV_2 - self.menu_headers_width // 2, self.menu_screen_edge_margin,
                           self.menu_headers_width, self.menu_headers_height),
            'central header': (MAXX_DIV_2 - self.menu_headers_width // 2, MAXY_DIV_2 - self.menu_headers_height // 2,
                               self.menu_headers_width, self.menu_headers_height),
            'central right button': (MAXX_DIV_2 + self.menu_screen_edge_margin, MAXY_DIV_2 + self.menu_headers_height // 2 + self.menu_screen_edge_margin,
                               self.menu_buttons_width, self.menu_buttons_height),
            'central left button': (MAXX_DIV_2 - self.menu_screen_edge_margin - self.menu_buttons_width, MAXY_DIV_2 + self.menu_headers_height // 2 + self.menu_screen_edge_margin,
                               self.menu_buttons_width, self.menu_buttons_height),
            'bottom right button': (MAXX - (self.menu_buttons_width + self.menu_screen_edge_margin),
                                    MAXY - (self.menu_buttons_height + self.menu_screen_edge_margin),
                                    self.menu_buttons_width, self.menu_buttons_height),
            'bottom left button': (self.menu_screen_edge_margin, MAXY - (self.menu_buttons_height + self.menu_screen_edge_margin),
                                   self.menu_buttons_width, self.menu_buttons_height),
        }
        self.menu_actions_done = False
        self.menu_actions_pending = list()
        # import locations
        self.location_names = dict()
        self.location_names['names list'] = list()
        self.menu_structure = {
            'list maps': {
                  'generate list from': "self.location_names['list ref'] = self.location_names['names list']",
                  # 'generate list from': "self.location_names['list ref'] = self.location_names['names list']",
            },
            'teleport/trigger': {
                'header': {
                    'rectangle': None,
                    'label': 'CHOOSE TYPE:',
                    'on hover action': None,
                    'LMB action': None,
                    'active': False,
                    'after action': None
                },
                'trigger': {
                    'rectangle': None,
                    'label': '[ACTION TRIGGER]',
                    'on hover action': ('submenu', 'list maps'),
                    'LMB action': None,
                    'active': True,
                    'after action': None
                },
                'teleport': {
                    'rectangle': None,
                    'label': '[TELEPORT]',
                    'on hover action': ('submenu', 'list maps'),
                    'LMB action': None,
                    'active': True,
                    'after action': None
                },
            },
            'obstacle edit': {
                'header': {
                    'rectangle': None,
                    'label': 'INTRODUCE OBSTACLE AS:',
                    'on hover action': None,
                    'LMB action': None,
                    'active': False,
                    'after action': None
                },
                'trigger': {
                    'rectangle': None,
                    'label': '[MAKE EVENT INITIATOR >]',
                    'on hover action': ('submenu', 'teleport/trigger'),
                    'LMB action': None,
                    'active': True,
                    'after action': None
                },
                'moving platform': {
                    'rectangle': None,
                    'label': '[MAKE MOVING PLATFORM]',
                    'on hover action': None,
                    'LMB action': ('return string', 'moving'),
                    'active': True,
                    'after action': None
                },
                'custom': {
                    'rectangle': None,
                    'label': '[CUSTOM EDIT PROPERTIES]',
                    'on hover action': None,
                    'LMB action': ('submenu', 'custom obs properties'),
                    # 'LMB action': ('return string', 'custom'),
                    'active': True,
                    'after action': None
                },
            },
            'custom obs properties': {
                'header': {
                    'rectangle': self.menu_elements_bindings['central header'],
                    'label': 'EDIT OBSTACLE PROPERTIES:',
                    'on hover action': None,
                    'LMB action': None,
                    'active': False,
                    'after action': None
                },
                'ghost': {
                    'rectangle': pygame.Rect(0,0,0,0),
                    'label': 'ghost',
                    'on hover action': None,
                    'LMB action': ['switch state', {'ghost': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'speed': {
                    'rectangle': pygame.Rect(0,0,0,0),
                    'label': 'speed',
                    'on hover action': None,
                    'LMB action': ('input number', {'speed': 0}),
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'active': {
                    'rectangle': pygame.Rect(0,0,0,0),
                    'label': 'active',
                    'on hover action': None,
                    'LMB action': ['switch state', {'active': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'collideable': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'collideable',
                    'on hover action': None,
                    'LMB action': ['switch state', {'collideable': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'gravity affected': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'gravity affected',
                    'on hover action': None,
                    'LMB action': ['switch state', {'gravity affected': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'invisible': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'invisible',
                    'on hover action': None,
                    'LMB action': ['switch state', {'invisible': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                },
                'trigger': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'trigger',
                    'on hover action': None,
                    'LMB action': ['switch state', {'trigger': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                    # self.obs_settings[]
                },
                'actors pass through': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'actors pass through',
                    'on hover action': None,
                    'LMB action': ['switch state', {'actors pass through': False}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                    # self.obs_settings[]
                },
                'trigger description': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'trigger description',
                    'on hover action': None,
                    'LMB action': ['input string', {'trigger description': {}}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                    # self.obs_settings[]
                },
                'actions': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': 'actions',
                    'on hover action': None,
                    'LMB action': ['input string', {'actions': {}}],
                    'active': True,
                    'also affects on': None,
                    'after action': 'keep going'
                    # self.obs_settings[]
                },
                'ok': {
                    'rectangle': pygame.Rect(0, 0, 0, 0),
                    'label': '[CONFIRM]',
                    'on hover action': None,
                    'LMB action': ('return string', 'custom obs edit done'),
                    'active': True,
                    'also affects on': None,
                    'after action': None
                },

                # 'generate list from': (
                #     'ghost', 'speed', 'active', 
                # ),
            },
            'initial setup': {
                'header': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central header']),
                    'label': 'EDIT EXISTING OR CREATE NEW?',
                    'on hover action': None,
                    'LMB action': None,
                    'active': False,
                    'after action': None
                },
                'existing': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central right button']),
                    'label': '[LOAD]',
                    'on hover action': None,
                    'LMB action': ('return string', 'load'),  # Return string type of 'load'
                    'active': True,
                    'after action': None
                },
                'new': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central left button']),
                    'label': '[CREATE NEW MAP]',
                    'on hover action': None,
                    'LMB action': ('return string', 'new'),  # Return string type of 'new'
                    'active': True,
                    'after action': None
                },
                'quit': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['bottom right button']),
                    'label': 'QUIT',
                    'on hover action': None,
                    'LMB action': ('exec', 'pygame.quit()\nraise SystemExit()'),
                    'active': True,
                    'after action': None
                },
            },
            'main menu': {
                'header': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central header']),
                    'label': 'Now edit map: ' + self.location + ' (ESC to quit)',
                    'on hover action': None,
                    'LMB action': None,
                    'active': False,
                    'after action': None
                },
                'save': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central left button']),
                    'label': '[SAVE CURRENT MAP]',
                    'on hover action': None,
                    'LMB action': ('return string', 'save'),
                    # 'LMB action': ('exec', 'self.save()'),
                    'active': True,
                    'after action': None
                },
                'load': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['central right button']),
                    'label': '[LOAD...]',
                    'on hover action': None,
                    'LMB action': ('return string', "load"),
                    # 'LMB action': ('exec', "self.reset_menu()\nself.need_to_load = True\nreturn"),
                    'active': True,
                    'after action': None
                },
                'resize': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['bottom right button']),
                    'label': '[RESIZE MAP...]',
                    'on hover action': None,
                    'LMB action': ('return string', "resize"),
                    # 'LMB action': ('exec', "x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')\ny = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')\nself.camera.setup(int(x), int(y))\nself.create_snap_mesh()"),
                    'active': True,
                    'after action': None
                },
                'quit': {
                    'rectangle': pygame.Rect(self.menu_elements_bindings['bottom left button']),
                    'label': '[QUIT TO DOS...]',
                    'on hover action': None,
                    'LMB action': ('return string', "quit"),
                    # 'LMB action': ('exec', "self.reset_menu()"),
                    'active': True,
                    'after action': None
                },
            },
        }
        # self.setup_box = list()

    def set_screen(self, surface):
        self.screen = surface

    def reset_menu_actions_pending(self):
        self.menu_actions_pending = list()

    def reset_menu(self):
        self.reset_human_input()
        self.menu_items = dict()
        self.menu_item_id = 0
        self.menu_actions_done = False
        self.active_menu_pile = 0
        # self.menu_actions_pending = list()

    # def reset_particular_menu(self, menu_id):
    #     self.reset_human_input()
    #     self.menu_items[menu_id] = dict()
    #     self.menu_item_id = 0
    #     self.active_menu_pile = menu_id - 1

    # def close_all_menus(self):
    #     self.active_menu_pile = 1
    #     self.menu_items = dict()

    def processing_menu_items_old(self, close_after_use=False):
        while self.menu_items:
            self.processing_human_input()
            if self.input_cancel:
                self.input_cancel = False
                self.reset_human_input()
                self.menu_items = dict()
                self.menu_item_id = 1
                return 'CANCEL MENU'
            selected_item = 0
            for k in self.menu_items.keys():
                menu_item = self.menu_items[k]
                menu_item['hovered'] = False
                if not menu_item['active']:
                    continue
                if menu_item['rectangle'].collidepoint(self.mouse_xy):
                    menu_item['hovered'] = True
                    selected_item = k
            if self.is_left_mouse_button_down:
                if selected_item != 0:
                    command = self.menu_items[selected_item]['command']
                    self.menu_items[selected_item]['checked'] = False if self.menu_items[selected_item]['checked'] else True
                    if close_after_use:
                        self.menu_items = dict()
                        self.menu_item_id = 1
                    self.reset_human_input()
                    return command
            self.render_menu_items()
            pygame.display.flip()
            # return selected_item

    def processing_menu_items(self):
        # self.processing_human_input()
        if self.input_cancel:
            self.input_cancel = False
            # Delete LIFO menu pile:
            keys = list(self.menu_items.keys())
            del self.menu_items[keys.pop()]
            if keys:
                self.active_menu_pile = keys[-1]
            else:
                self.active_menu_pile = 0
                self.menu_actions_pending.append('CANCEL MENU')
                self.menu_actions_done = True
                # self.menu_action_pending = 'CANCEL MENU'

        menu_item_has_been_already_checked = False

        for pile_id in reversed(self.menu_items.keys()):
            for k in self.menu_items[pile_id].keys():
                menu_item = self.menu_items[pile_id][k]
                if menu_item_has_been_already_checked:
                    menu_item['hovered'] = False
                    menu_item['has been already activated'] = False
                    continue
                # if not menu_item['active']:
                #     continue

                if menu_item['rectangle'].collidepoint(self.mouse_xy):
                    menu_item_has_been_already_checked = True
                    if not menu_item['active']:
                        # If mouse cursor has collided with any single menu item, all further checks are futile:
                        continue
                    menu_item['hovered'] = True
                    if menu_item['on hover action']:
                        if not menu_item['has been already activated']:
                            menu_item['has been already activated'] = True
                            # self.reset_human_input()
                            if menu_item['on hover action'][0] == 'submenu':
                                self.delete_all_child_menu_piles(pile_id)
                                self.active_menu_pile += 1
                                menu_name = menu_item['on hover action'][1]
                                if 'generate list from' in self.menu_structure[menu_name].keys():
                                    # Let's generate a new menu items from the given list:
                                    exec(self.menu_structure[menu_name]['generate list from'])
                                    # print(self.location_names['list ref'])
                                    # exit()
                                    for l in self.location_names['list ref']:
                                        # print(f'[processing menu items] Adding new menu item {l} to {menu_name}:')
                                        self.menu_structure[menu_name][l] = dict()
                                        self.menu_structure[menu_name][l]['rectangle'] = pygame.Rect(0,0,0,0)
                                        self.menu_structure[menu_name][l]['label'] = l
                                        self.menu_structure[menu_name][l]['on hover action'] = None
                                        self.menu_structure[menu_name][l]['LMB action'] = ('return string', l)
                                        self.menu_structure[menu_name][l]['active'] = True
                                        self.menu_structure[menu_name][l]['after action'] = None
                                self.add_menu((menu_item['rectangle'].x + menu_item['rectangle'].width // 2, menu_item['rectangle'].centery),
                                              menu_item['rectangle'].width, 20, [self.menu_structure[menu_name][i] for i in self.menu_structure[menu_name].keys() if i != 'generate list from'])
                                return
                    else:
                        if self.active_menu_pile > pile_id:
                            self.delete_all_child_menu_piles(pile_id)
                            return
                    if self.is_left_mouse_button_down:
                        self.is_left_mouse_button_down = False
                        if menu_item['LMB action']:
                            if menu_item['LMB action'][0] == 'exec':
                                # RAW CODE EXECUTION
                                exec(menu_item['LMB action'][1])
                            elif menu_item['LMB action'][0] == 'submenu':
                                # REVEAL SUBMENU
                                menu_name = menu_item['LMB action'][1]
                                self.add_menu((menu_item['rectangle'].x + menu_item['rectangle'].width // 2, menu_item['rectangle'].centery),
                                              menu_item['rectangle'].width, 20, [self.menu_structure[menu_name][i] for i in self.menu_structure[menu_name].keys() if i != 'generate list from'])
                                return
                            elif menu_item['LMB action'][0] == 'switch state':
                                menu_item['text'] = ''
                                # menu_item['text'] = menu_item['text'].split(' ')[0]
                                for k_tmp in menu_item['LMB action'][1].keys():
                                    menu_item['LMB action'][1][k_tmp] = True if not menu_item['LMB action'][1][k_tmp] else False
                                    menu_item['text'] += str(k_tmp) + ':' + str(menu_item['LMB action'][1][k_tmp]) + ' '
                            elif menu_item['LMB action'][0] == 'return string':
                                # SIMPLY RETURN STRING SODE
                                self.menu_actions_pending.append(menu_item['LMB action'][1])
                                # self.menu_action_pending = menu_item['LMB action'][1]

                            # Aftermath:
                            if menu_item['after action']:
                                if menu_item['after action'] == 'keep going':
                                    continue
                            else:
                                self.menu_actions_done = True
                                # self.reset_menu()
                                return

                else:
                    menu_item['hovered'] = False
                    # menu_item['has been already activated'] = False
                    # Delete all already revealed submenus:
                    # self.delete_all_child_menu_piles(pile_id)


                    if menu_item['on hover action'] and menu_item['has been already activated']:
                        menu_item['has been already activated'] = False
                        # Delete all already revealed submenus:
                        self.delete_all_child_menu_piles(pile_id)
                        return

            #                 delete_child_menus = True
            #                 break
            # if delete_child_menus:
            #     break

    def delete_all_child_menu_piles(self, parent_pile_number):
        piles_to_delete = list()
        # print(f'[delete child menus] {parent_pile_number=} {list(self.menu_items.keys())}')
        for pile in self.menu_items.keys():
            if pile > parent_pile_number:
                # if pile > self.active_menu_pile:
                piles_to_delete.append(pile)
        # print(f'[delete child menus] {piles_to_delete=}')
        for p in piles_to_delete:
            del self.menu_items[p]
        self.active_menu_pile = parent_pile_number

    def create_menu_items_from_list(self, a_list, button_text, menu_items_size='medium'):
        if menu_items_size == 'small':
            w = self.menu_small_buttons_width
            h = self.menu_small_buttons_height
        elif menu_items_size == 'medium':
            w = self.menu_buttons_width
            h = self.menu_buttons_height
        start_y = self.menu_screen_edge_margin + self.menu_headers_height + self.menu_buttons_spacing
        max_height_of_free_space = MAXY - self.menu_screen_edge_margin - start_y
        max_menu_elements_fits = max_height_of_free_space // (h + self.menu_buttons_spacing)
        columns_needed = len(a_list) // max_menu_elements_fits + 1
        # print(f'{max_height_of_free_space=} {max_menu_elements_fits=} {len(obs_id_list)=} {columns_needed=}')
        # Define start x coordinate:
        if columns_needed / 2 == columns_needed // 2:
            # Quantity of columns is even.
            start_x = MAXX_DIV_2 - w * columns_needed // 2  # - self.menu_buttons_spacing // 2
        else:
            # Quantity of columns is odd.
            start_x = MAXX_DIV_2 - w // 2 - w // 2 * columns_needed // 2

        c = 0
        for element in a_list:
            item = {
                'label': button_text + str(element),
                'LMB action': ('return string', element),
                'active': True,
                'rectangle': pygame.Rect(start_x, start_y + c * (h + self.menu_buttons_spacing),
                                           w, h),
                'on hover action': None,
                'after action': None
            }

            self.add_menu_item(item)
            c += 1
            if c == max_menu_elements_fits:
                c = 0
                start_x += (w + self.menu_buttons_spacing)
                start_y = self.menu_screen_edge_margin + self.menu_headers_height + self.menu_buttons_spacing

    def setup(self):
        # self.add_menu_item( pygame.Rect(self.menu_elements_bindings['central header']), 'EDIT EXISTING OR CREATE NEW?', '', False)
        # self.add_menu_item( pygame.Rect(self.menu_elements_bindings['central left button']), 'EXISTING', 'EXISTING', True)
        # self.add_menu_item( pygame.Rect(self.menu_elements_bindings['central right button']), 'NEW', 'NEW', True)
        # self.add_menu_item( pygame.Rect(self.menu_elements_bindings['bottom right button']), 'QUIT', 'quit', True)

        # command = self.processing_menu_items(True)
        # self.reset_human_input()

        for i in self.menu_structure['initial setup'].keys():
            item = self.menu_structure['initial setup'][i]
            self.add_menu_item(item)

        while not self.menu_actions_done:
        # while self.menu_action_pending == '':
            self.processing_human_input()
            self.processing_menu_items()
            self.render_background()
            self.render_menu_items()
            pygame.display.flip()
        self.reset_human_input()
        self.reset_menu()

        if self.menu_actions_pending[-1] == 'CANCEL MENU':
            pygame.quit()
            raise SystemExit()
        else:
            if self.menu_actions_pending[-1] == 'new':
                self.reset_menu_actions_pending()
                # self.menu_action_pending = ''
                # print('make new')
                # # Setting up the new map:
                width = MAXX
                height = MAXY
                new_location_description = list()
                with open('locations.py', 'r') as f:
                    existing_locations_description = f.readlines()

                map_name = str(uuid.uuid1())

                # Using the template to build a structure of new map's description:
                with open('locations_template.py', 'r') as template_source:
                    for line in template_source:
                        if 'new_map_name' in line:
                            new_line = '    \'' + map_name + '\':\n'
                            new_location_description.append(new_line)
                        elif 'new_map_size' in line:
                            new_line = '            \'size\': (' + str(width) + ', ' + str(height) + '), \n'
                            new_location_description.append(new_line)
                        else:
                            new_location_description.append(line)

                # Insert the new map description into the existing locations.py file:
                for line in existing_locations_description:
                    if 'locations = {' in line:
                        line_index = existing_locations_description.index(line) + 1
                        for new_line in new_location_description:
                            existing_locations_description.insert(line_index, new_line)
                            line_index += 1
                        break

                with open('locations.py', 'w') as f_dest:
                    f_dest.writelines(existing_locations_description)

                self.location = map_name

            else:
                self.reset_menu_actions_pending()
                # self.menu_action_pending = ''
                # print('edit existing')
                # User wants to edit an existing map.
                import locations
                self.reset_human_input()
                self.render_background()
                map_names = list(locations.locations.keys())
                # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'CHOOSE AN EXISTING MAP', '', False)
                self.create_menu_items_from_list(map_names, '', 'medium')
                # command = self.processing_menu_items(True)
                # self.location = command
                while not self.menu_actions_done:
                # while self.menu_action_pending == '':
                    self.processing_human_input()
                    self.processing_menu_items()
                    self.render_background()
                    self.render_menu_items()
                    pygame.display.flip()
                self.reset_menu()
                self.reset_human_input()
                self.location = self.menu_actions_pending[-1]
                self.reset_menu_actions_pending()

    def reset_human_input(self):
        self.is_mouse_button_down = False
        self.is_left_mouse_button_down = False
        self.is_right_mouse_button_down = False

    def main_menu(self):
        # if self.menu_items:
        #     self.menu_items = dict()
        #     self.menu_item_id = 0
        # else:
            # if event.key == K_F3:
            #     self.need_to_load = True
            # if event.key == K_F2:
            #     self.save()
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central header']), 'Editing map (ESC quit program): ' + self.location, '', False)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), 'SAVE CURRENT', 'save', True)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), 'LOAD...', 'load', True)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom right button']), '[RESIZE MAP]', 'resize', True)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom left button']), '[BACK TO EDITOR...]', 'return', True)
        for i in self.menu_structure['main menu'].keys():
            item = self.menu_structure['main menu'][i]
            self.add_menu_item(item)
            # self.add_menu_item(item['rectangle'], item['label'], item['LMB action'], item['active'], item['on hover action'])

        while not self.menu_actions_done:
        # while self.menu_action_pending == '':
            self.processing_human_input()
            self.processing_menu_items()
            self.render_background()
            self.render_menu_items()
            pygame.display.flip()
        self.reset_human_input()
        self.reset_menu()

        if self.menu_actions_pending[-1] == 'CANCEL MENU':
            self.reset_menu_actions_pending()
            return
        else:
            if self.menu_actions_pending[-1] == 'save':
                self.reset_menu_actions_pending()
                self.save()
            elif self.menu_actions_pending[-1] == 'load':
                self.reset_menu_actions_pending()
                self.need_to_load = True
                return
            elif self.menu_actions_pending[-1] == 'quit':
                pygame.quit()
                raise SystemExit()
            elif self.menu_actions_pending[-1] == 'resize':
                self.reset_menu_actions_pending()
                # self.menu_action_pending = ''
                x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')
                y = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')
                self.camera.setup(int(x), int(y))
                self.create_snap_mesh()
            else:
                self.reset_menu_actions_pending()
                return

            #     if command == 'CANCEL MENU':
            #         # if command in ('quit', 'CANCEL MENU'):
            #         pygame.quit()
            #         raise SystemExit()
            #     elif command == 'load':
            #         self.reset_menu()
            #         self.need_to_load = True
            #         return
            #     elif command == 'resize':
            #     elif command == 'save':
            #         self.save()

    def main_menu_old(self):
        if self.menu_items:
            self.menu_items = dict()
            self.menu_item_id = 1
        else:
            # if event.key == K_F3:
            #     self.need_to_load = True
            # if event.key == K_F2:
            #     self.save()
            self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central header']), 'Editing map (ESC quit program): ' + self.location, '', False)
            self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), 'SAVE CURRENT', 'save', True)
            self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), 'LOAD...', 'load', True)
            self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom right button']), '[RESIZE MAP]', 'resize', True)
            self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom left button']), '[BACK TO EDITOR...]', 'return', True)
            self.render_background()
            command = ''
            while command != 'return':
                command = self.processing_menu_items()  # Do not Close menu after use
                self.reset_human_input()
                if command == 'CANCEL MENU':
                    # if command in ('quit', 'CANCEL MENU'):
                    pygame.quit()
                    raise SystemExit()
                elif command == 'load':
                    self.reset_menu()
                    self.need_to_load = True
                    return
                elif command == 'resize':
                    x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')
                    y = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')
                    self.camera.setup(int(x), int(y))
                    self.create_snap_mesh()
                elif command == 'save':
                    self.save()

    def processing_human_input(self):
        self.mouse_xy = pygame.mouse.get_pos()
        self.mouse_xy_global = (self.mouse_xy[0] // self.zoom_factor + self.camera.offset_x,
                                self.mouse_xy[1] // self.zoom_factor + self.camera.offset_y)
        # self.mouse_xy_global = ((self.mouse_xy[0] + self.camera.offset_x) // self.zoom_factor,
        #                         (self.mouse_xy[1] + self.camera.offset_y) // self.zoom_factor)
        # self.mouse_xy_global = (self.zoom_factor * (self.mouse_xy[0] + self.camera.offset_x),
        #                         self.zoom_factor * (self.mouse_xy[1] + self.camera.offset_y))
        # self.mouse_xy_global = (self.mouse_xy[0] + self.camera.offset_x, self.mouse_xy[1] + self.camera.offset_y)
        # self.mouse_xy_snapped_to_mesh = (self.zoom_factor * self.mouse_xy_global[0] // self.snap_mesh_size * self.snap_mesh_size,
        #                                  self.zoom_factor * self.mouse_xy_global[1] // self.snap_mesh_size * self.snap_mesh_size)
        self.mouse_xy_snapped_to_mesh = (self.mouse_xy_global[0] // self.snap_mesh_size * self.snap_mesh_size,
                                         self.mouse_xy_global[1] // self.snap_mesh_size * self.snap_mesh_size)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit()
            mods = pygame.key.get_mods()
            if mods & KMOD_LSHIFT:  # use whatever KMOD_ constant you want;)
                self.is_l_shift = True
            elif mods & KMOD_LCTRL:
                self.is_l_ctrl = True
            elif mods & KMOD_LALT:
                self.is_l_alt = True
            else:
                self.is_l_ctrl = False
                self.is_l_shift = False
                self.is_l_alt = False
            # # print(self.l_shift)
            if event.type == KEYUP:
                self.is_key_pressed = False

                if event.key == K_SPACE:
                    self.is_spacebar = False
                # elif event.key == K_F8:
                #     self.load()
                # elif event.key == K_F2:
                #     self.save()
                # if event.key == K_KP_PLUS:
                #     self.snap_mesh_size += 1
                #     self.create_snap_mesh()
                # if event.key == K_KP_MINUS:
                #     self.snap_mesh_size -= 1
                #     self.create_snap_mesh()
                if event.key == K_RIGHTBRACKET:
                    self.is_right_bracket = False
                if event.key == K_LEFTBRACKET:
                    self.is_left_bracket = False
                if event.key == K_y:
                    self.is_y = False
                if event.key == K_x:
                    self.is_x = False
                if event.key == K_d:
                    self.is_input_right_arrow = False
                if event.key == K_a:
                    self.is_input_left_arrow = False
                if event.key == K_w:
                    self.is_input_up_arrow = False
                if event.key == K_s:
                    self.is_input_down_arrow = False
            if event.type == KEYDOWN:
                self.is_key_pressed = True
                if event.key == K_ESCAPE:
                    # self.main_menu()
                    if self.menu_items:
                        # self.menu_items = dict()
                        # self.menu_item_id = 1
                        self.input_cancel = True
                    else:
                        self.main_menu()
                    #     pygame.quit()
                    #     raise SystemExit()
                if event.key == K_KP_PLUS:
                    if self.is_x:
                        self.camera.setup(self.camera.max_offset_x + 100, self.camera.max_offset_y)
                        return
                    elif self.is_y:
                        self.camera.setup(self.camera.max_offset_x, self.camera.max_offset_y + 100)
                        return

                    if self.is_l_shift:
                        self.snap_mesh_size += self.snap_mesh_size_change_step
                    else:
                        self.snap_mesh_size += 1
                    self.create_snap_mesh()
                if event.key == K_KP_MINUS:
                    if self.is_x:
                        self.camera.setup(self.camera.max_offset_x - 100, self.camera.max_offset_y)
                        return
                    elif self.is_y:
                        self.camera.setup(self.camera.max_offset_x, self.camera.max_offset_y - 100)
                        return


                    if self.is_l_shift:
                        self.snap_mesh_size -= self.snap_mesh_size_change_step
                    else:
                        self.snap_mesh_size -= 1
                    self.create_snap_mesh()
                if event.key == K_RIGHTBRACKET:
                    self.is_right_bracket = True
                if event.key == K_LEFTBRACKET:
                    self.is_left_bracket = True
                if event.key == K_SPACE:
                    self.is_spacebar = True
                if event.key == K_F3:
                    self.need_to_load = True
                if event.key == K_F2:
                    self.save()
                if event.key == K_d:
                    self.is_input_right_arrow = True
                if event.key == K_a:
                    self.is_input_left_arrow = True
                if event.key == K_w:
                    self.is_input_up_arrow = True
                if event.key == K_s:
                    self.is_input_down_arrow = True
                if event.key == K_y:
                    self.is_y = True
                if event.key == K_x:
                    self.is_x = True

            #         self.is_input_right_arrow = True
            #     if event.key == K_a:
            #         self.is_input_left_arrow = True
            #     if event.key == K_w:
            #         self.is_input_up_arrow = True
            #     if event.key == K_s:
            #         self.is_input_down_arrow = True
            #     if event.key == K_SPACE:
            #         self.is_spacebar = True
            #     # if event.key == K_F5:
            #     #     self.need_quick_save = True
            #     # elif event.key == K_F8:
            #     #     self.need_quick_load = True
            #     #     # quick_save(self, self.locations)
            #     # elif event.key == K_F3:
            #     #     self.music_on = False if self.music_on else True
            #     #     if not self.music_on:
            #     #         pygame.mixer.music.fadeout(2000)
            #     elif event.key == K_z:
            #         # Cool stuff with if-then-else expression compress:
            #         self.is_z = False if self.is_z else True
            #     elif event.key == K_x:
            #         # self.change_mode()
            #         self.is_x = False if self.is_x else True
            #         # self.screen_follows_actor = False if self.screen_follows_actor else True
            #     # elif event.key == K_b:
            #     #     # self.change_mode()
            #     #     self.b = False if self.b else True
            #     # elif event.key == K_f:
            #     #     self.follow_mode = False if self.follow_mode else True
            #     # elif event.key == K_l:
            #     #     # self.change_mode()
            #     #     self.locations[self.location]['lights on'] = False if self.locations[self.location]['lights on'] else True
            #     # elif event.key == K_l:
            #     #     # self.change_mode()
            #     #     self.lights_on = False if self.lights_on else True
            #     # elif event.key == K_m:
            #     #     self.need_to_show_minimap = False if self.need_to_show_minimap else True
            #     elif event.key == K_n:
            #         # self.change_mode()
            #         self.is_n = False if self.is_n else True
            #         # msg = 'NEW EMPTY MESSAGE FOR TEST PURPOSES.'
            #         # self.info_windows[0].get_bunch_of_new_messages((msg, msg))
            #         # self.add_info_window(self.calculate_info_string_xy(), [msg, ], 300, False)
            #
            #     elif event.key == K_p:
            #         # Cool stuff with if-then-else expression compress:
            #         self.is_p = False if self.is_p else True
            #     elif event.key == K_i:
            #         # Cool stuff with if-then-else expression compress:
            #         self.is_i = False if self.is_i else True
            #     # elif event.key == K_SPACE:
            #     #     self.change_player_actors()
            #     # elif event.key == K_e:
            #     # # elif event.key == K_KP_ENTER:
            #     #     # elif event.key == K_SPACE:
            #     #     # self.input_confirm = True
            #     #     self.wandering_actor.end_turn()
            #     #     self.player_turn = False
            #     # elif event.key == K_c:
            #     #     self.skip_actor()
            #     # elif event.key == K_TAB:
            #     #     self.need_to_show_party_inventory = True if not self.need_to_show_party_inventory else False
            if event.type == MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    self.is_mouse_button_down = True
                    self.is_left_mouse_button_down = True
                if buttons[2]:
                    self.is_mouse_button_down = True
                    self.is_right_mouse_button_down = True
            elif event.type == MOUSEWHEEL:
                # print(event)
                # print(event.x, event.y)
                # print(event.flipped)
                # print(event.which)
                self.is_mouse_wheel_rolls = True
                if event.y == 1:
                    # Mouse wheel up:
                    self.is_mouse_wheel_up = True
                    # self.wandering_screen_target_scale += self.wandering_scale_amount
                elif event.y == -1:
                    # Mouse wheel down:
                    self.is_mouse_wheel_down = True
            if event.type == MOUSEBUTTONUP:
                self.is_mouse_button_down = False
                if self.is_right_mouse_button_down:
                    self.is_right_mouse_button_down = False
                if self.is_left_mouse_button_down:
                    self.is_left_mouse_button_down = False

    def add_obstacle(self, description):
        entity = Obstacle()
        entity.id = description[-1]
        # entity.id = self.obstacle_id
        entity.is_gravity_affected = True if 'gravity affected' in description else False
        entity.is_collideable = True if 'collideable' in description else False
        entity.rectangle.topleft = description[0]
        entity.rectangle.width = description[1][0]
        entity.rectangle.height = description[1][1]
        # entity.max_speed = 0.6
        entity.is_move_right = True if 'move right' in description else False
        entity.is_move_up = True if 'move up' in description else False
        entity.is_move_down = True if 'move down' in description else False
        entity.is_move_left = True if 'move left' in description else False
        entity.is_ghost_platform = True if 'ghost' in description else False

        # Add an obstacle to the world storage:
        if self.location not in self.obstacles.keys():
            self.obstacles[self.location] = dict()
        self.obstacles[self.location][entity.id] = entity
        # self.obstacle_id = entity.id + 1
        # self.obstacle_id += 1

    def add_demolisher(self, description):
        entity = Demolisher()
        entity.id = description[-1]
        # entity.id = self.demolishers_id
        entity.is_gravity_affected = True if 'gravity affected' in description else False
        entity.is_collideable = True if 'collideable' in description else False
        entity.rectangle.topleft = description[0]
        entity.rectangle.width = description[1][0]
        entity.rectangle.height = description[1][1]
        # entity.max_speed = 0.6
        # entity.is_move_right = True if 'move right' in description else False
        # entity.is_move_up = True if 'move up' in description else False
        # entity.is_move_down = True if 'move down' in description else False
        # entity.is_move_left = True if 'move left' in description else False
        # entity.is_ghost_platform = True if 'ghost' in description else False

        # Add an obstacle to the world storage:
        if self.location not in self.demolishers.keys():
            self.demolishers[self.location] = dict()
        self.demolishers[self.location][entity.id] = entity
        self.demolishers_id = entity.id + 1
        # self.demolishers_id += 1

    def add_menu_item(self, menu_item, frame_color=GREEN, bg_color=DARKGRAY, txt_color=WHITE):
        # self.active_menu_pile = parent_self.active_menu_pile + 1
        if self.active_menu_pile not in self.menu_items.keys():
            self.menu_items[self.active_menu_pile] = dict()
        self.menu_items[self.active_menu_pile][self.menu_item_id] = dict()
        self.menu_items[self.active_menu_pile][self.menu_item_id]['hovered'] = False  # Flag to recognize if mouse cursor hovers over this menu item.
        self.menu_items[self.active_menu_pile][self.menu_item_id]['checked'] = False  # This menu item has been checked by the user.
        self.menu_items[self.active_menu_pile][self.menu_item_id]['has been already activated'] = False  # Menu item has been already activated, to avoid multiple triggers while cursor  hovers over.
        self.menu_items[self.active_menu_pile][self.menu_item_id]['text color'] = txt_color
        self.menu_items[self.active_menu_pile][self.menu_item_id]['frame color'] = frame_color
        self.menu_items[self.active_menu_pile][self.menu_item_id]['back color'] = bg_color

        # Properties depends on menu_item dict:
        self.menu_items[self.active_menu_pile][self.menu_item_id]['text'] = menu_item['label']
        self.menu_items[self.active_menu_pile][self.menu_item_id]['LMB action'] = menu_item['LMB action']
        self.menu_items[self.active_menu_pile][self.menu_item_id]['active'] = menu_item['active']  # Menu item responses on human input.
        self.menu_items[self.active_menu_pile][self.menu_item_id]['rectangle'] = menu_item['rectangle']
        self.menu_items[self.active_menu_pile][self.menu_item_id]['on hover action'] = menu_item['on hover action']  # Activate a command of this menu item just only if mouse cursor hovers over it.
        self.menu_items[self.active_menu_pile][self.menu_item_id]['after action'] = menu_item['after action']  #

        self.menu_item_id += 1


    def add_menu(self, top_left_corner, width, font_size, items):
    # def add_menu(self, top_left_corner, width, font_size, items):
    #     self.menu_action_pending = ''
        self.menu_item_id = 0
        dy = 0
        height = font_size + 16
        total_menu_height = height * len(items)
        if MAXY - top_left_corner[1] < total_menu_height:
            start_y = MAXY - height
        else:
            start_y = top_left_corner[1] + total_menu_height - height
        for i in reversed(items):
            # print(i)
            i['rectangle'] = pygame.Rect(top_left_corner[0], start_y - dy, width, height)
            self.add_menu_item(i)

            dy += height
        # for i in items:
        #     # print(i)
        #     i['rectangle'] = pygame.Rect(top_left_corner[0], top_left_corner[1] + dy, width, height)
        #     self.add_menu_item(i)
        #
        #     dy += height

    def create_text_input(self, xy, prompt, input_type='str'):
        txt_surf = fonts.all_fonts[self.default_font_size].render(prompt, True, WHITE, DARKGRAY)
        back_color = GRAY

        window_height = txt_surf.get_height() + 20
        window_width = txt_surf.get_width() + 20
        # window_width_inflate = 20
        # text_to_return_list = list()
        text_to_return_str = str()
        text_to_return_surf = fonts.all_fonts[self.default_font_size].render(text_to_return_str, True, WHITE, DARKGRAY)
        window_width_inflate = text_to_return_surf.get_width()

        while True:
            cursor_x_start = xy[0] + window_width
            cursor_x = 0
            pygame.draw.rect(self.screen, back_color, (xy[0], xy[1], window_width + window_width_inflate, window_height), 0)
            pygame.draw.rect(self.screen, BLUE, (xy[0], xy[1], window_width + window_width_inflate, window_height), 3)
            self.screen.blit(txt_surf, (xy[0] + 10, xy[1] + 10))
            # pygame.draw.line(self.screen, BLACK, (cursor_x_start + cursor_x, xy[1] + 5), (cursor_x_start + cursor_x, xy[1] + window_height - 10), 3)
            # self.processing_human_input()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    k = pygame.key.name(event.key)
                    print(k)
                    if event.key == K_ESCAPE:
                        return 'CANCEL MENU'
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        return text_to_return_str
                    if event.key == K_BACKSPACE:
                        if len(text_to_return_str) > 0:
                            text_to_return_str = text_to_return_str[0:-1]
                            break
                    if input_type == 'digit':

                        if k in DIGITS:
                            if k[0] == '[':
                                text_to_return_str += k[1]
                            else:
                                text_to_return_str += k
                                # text_to_return_str += pygame.key.name(event.key)
                    elif input_type == 'str':
                        if k in ALPHA or pygame.key.name(event.key) in DIGITS:
                        # if pygame.key.name(event.key) in ALPHA or pygame.key.name(event.key) in DIGITS:
                            if k[0] == '[':
                                text_to_return_str += k[1]
                            else:
                                text_to_return_str += k
                            # text_to_return_str += pygame.key.name(event.key)
                        elif k == 'space':
                        # elif pygame.key.name(event.key) == 'space':
                            text_to_return_str += ' '
                            # text_to_return_surf = fonts.all_fonts[self.default_font_size].render(text_to_return_str, True, WHITE, DARKGRAY)
                            # window_width_inflate = text_to_return_surf.get_width()
                    elif input_type == 'any':
                        text_to_return_str += k
                        # text_to_return_str += pygame.key.name(event.key)

            text_to_return_surf = fonts.all_fonts[self.default_font_size].render(text_to_return_str, True, WHITE, DARKGRAY)
            window_width_inflate = text_to_return_surf.get_width()

            self.screen.blit(text_to_return_surf, (cursor_x_start + cursor_x, xy[1] + 10))
            # if self.input_cancel:
            #     self.input_cancel = False
            #     self.reset_human_input()
            #     return 'CANCEL MENU'

            pygame.display.flip()

        # self.add_menu_item(pygame.Rect(xy[0], xy[1], txt_surf.get_width() + 20, txt_surf.get_height() + 20), prompt + ': ', '', False)

    def load(self):
        self.obstacles[self.location] = dict()
        try:
            max_obs_id = 0
            for obs in locations.locations[self.location]['obstacles']['obs rectangles']:
                self.add_obstacle(obs)
                if max_obs_id < obs[-1]:
                    max_obs_id = obs[-1]
            self.obstacle_id = max_obs_id + 1

            self.obs_settings = locations.locations[self.location]['obstacles']['settings']
            for active_obs_id in self.obs_settings.keys():
                if active_obs_id in self.obstacles[self.location].keys():
                    self.obstacles[self.location][active_obs_id].active_flag = True
            # for dem in locations[self.location]['demolishers']['dem rectangles']:
            #     self.add_demolisher(dem)
            self.camera.setup(locations.locations[self.location]['size'][0], locations.locations[self.location]['size'][1])
            self.create_snap_mesh()
        except NameError:
            self.obstacles[self.location] = dict()
            self.demolishers[self.location] = dict()
            self.camera.setup(MAXX, MAXY)
            self.create_snap_mesh()
        # self.obstacle_id = len(self.obstacles[self.location].keys()) + 1

    def save(self):
        # Saving with pickle:
        # with open('locations_'+self.location+'.dat', 'wb') as f:
        #     pickle.dump(self.obstacles[self.location], f)

        # Saving using JSON:
        # obs_geometry = list()

        obs_rects = list()
        for k in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][k]
            total_strg = '\n                ' + \
                         '(' + \
                         str(obs.rectangle.topleft) + ', ' + \
                         str(obs.rectangle.size) + \
                         ', ' + str(k) + '),  #' + str(k)
            obs_rects.append(total_strg)

        dem_rects = list()
        if self.location in self.demolishers:
            for k in self.demolishers[self.location].keys():
                dem = self.demolishers[self.location][k]
                total_strg = '\n                ' + \
                       '(' + \
                       str(dem.rectangle.topleft) + ', ' + \
                       str(dem.rectangle.size) + ', ' + str(k) + \
                       '),  #' + str(k)
                dem_rects.append(total_strg)

        from locations import locations as loc
        from templates import obstacle_settings_list
        # settings_list = list()
        # print(obs_rects)
        # print(dem_rects)
        # exit()
        # ['                ((100, 950), (1550, 50), 0),  #0\n',
        #  '                ((1300, 500), (300, 250), 1),  #1\n',
        #  '                ((950, 350), (100, 150), 2),  #2\n',
        #  '                ((650, 300), (200, 200), 3),  #3\n']

        # ['                ((550, 750), (200, 200), 0),  #0\n']
        # new_location_description = list()
        # import locations as loc

        print(loc[self.location]['obstacles']['settings'])
        # exit()
        with open('locations.py', 'w') as f:
        # with open('tmp_test.py', 'w') as f:
            f.write('from constants import *')
            f.write('\nlocations = {\n    ')
            for k in loc.keys():
                f.write('\n    \'' + k + '\':\n        {')  # Map name
                f.write('\n            \'music\': \'' + loc[k]['music'] + '\',')
                f.write('\n            \'description\': \'' + loc[k]['description'] + '\',')
                if k == self.location:
                    f.write('\n            \'size\': (' + str(self.camera.max_x) + ', ' + str(self.camera.max_y) + '),')
                else:
                    f.write('\n            \'size\': (' + str(loc[k]['size'][0]) + ', ' + str(loc[k]['size'][1]) + '),')
                f.write('\n            \'hostiles\': {')
                f.write('\n              },')
                f.write('\n            \'demolishers\': {')

                # Demolishers settings:
                f.write('\n                \'dem rectangles\': (')
                if k == self.location:
                    # Save demolishers rectangles which were edited right now.
                    for dem in dem_rects:
                        f.write(dem)
                else:
                    # Save demolishers remain unchanged.
                    for dem in loc[k]['demolishers']['dem rectangles']:
                        f.write('\n                ' + str(dem) + ',' )
                f.write('\n                  ), # DEMOLISHERS RECTANGLE SECTION END' )
                f.write('\n            },')

                # OBSTACLES:
                f.write('\n            \'obstacles\': {' )
                f.write('\n                \'obs rectangles\': (' )
                if k == self.location:
                    # Save obstacles rectangles which were edited right now.
                    for rect in obs_rects:
                        f.write(rect)
                else:
                    # Save obstacles remain unchanged.
                    for obs in loc[k]['obstacles']['obs rectangles']:
                        f.write('\n                ' + str(obs) + ',' )
                f.write('\n                  ), # OBSTACLE RECTANGLES SECTION END' )

                # SAVE ACTIVE OBSTACLES SETTINGS:
                f.write('\n                \'settings\': {')
                if k == self.location:
                    # Save all settings we've just edited:
                    for s_key in self.obs_settings.keys():
                        f.write('\n                    ' + str(s_key) + ': {')  # Dict key which is pointer to active obstacle ID.
                        for ss_key in self.obs_settings[s_key].keys():
                            f.write('\n                        \'' + ss_key + '\': ' + str(self.obs_settings[s_key][ss_key]) + ',')
                        f.write('\n                  },')
                else:
                    # Save settings of other levels remain unchanged:
                    for active_obs_key in loc[k]['obstacles']['settings'].keys():
                        l = loc[k]['obstacles']['settings'][active_obs_key]
                        f.write('\n                    ' + str(active_obs_key) + ': {')
                        for i in obstacle_settings_list:
                            # Save 'settings' section line by line:
                            f.write('\n                        \'' + i + '\': ' + str(l[i]) + ',')
                        f.write('\n                  },')

                # Closing tails:
                f.write('\n                  } # OBSTACLE SETTINGS SECTION END')
                f.write('\n              },')
                f.write('\n            \'items\': {' +  '},')
                f.write('\n    },')
            f.write('\n}')

    def save_back(self):
        # Saving with pickle:
        # with open('locations_'+self.location+'.dat', 'wb') as f:
        #     pickle.dump(self.obstacles[self.location], f)

        # Saving using JSON:
        # obs_geometry = list()

        obs_rects = list()
        for k in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][k]
            total_strg = '                ' + \
                         '(' + \
                         str(obs.rectangle.topleft) + ', ' + \
                         str(obs.rectangle.size) + \
                         ', ' + str(k) + '),  #' + str(k) + '\n'
            obs_rects.append(total_strg)

        dem_rects = list()
        if self.location in self.demolishers:
            for k in self.demolishers[self.location].keys():
                dem = self.demolishers[self.location][k]
                total_strg = '                ' + \
                       '(' + \
                       str(dem.rectangle.topleft) + ', ' + \
                       str(dem.rectangle.size) + ', ' + str(k) + \
                       '),  #' + str(k) + '\n'
                dem_rects.append(total_strg)

        settings_list = list()

        # print(obs_rects)
        # print(dem_rects)
        # exit()
        # ['                ((100, 950), (1550, 50), 0),  #0\n',
        #  '                ((1300, 500), (300, 250), 1),  #1\n',
        #  '                ((950, 350), (100, 150), 2),  #2\n',
        #  '                ((650, 300), (200, 200), 3),  #3\n']

        # ['                ((550, 750), (200, 200), 0),  #0\n']
        # new_location_description = list()
        with open('locations.py', 'r') as f:
            existing_locations_description = f.readlines()

        print(f'Start searching {self.location} to remove obsolete rectangles...')
        loc_found = False
        lines_counter = 0
        for line in existing_locations_description:
            if '\'' + self.location + '\':' in line and not loc_found:
                print(f'Location {self.location} found.')
                loc_found = True

            if loc_found:
                if '\'obs rectangles\':' in line:
                    # Now need to delete all obsolete information about rectangles:
                    start_index_to_delete = lines_counter + 1
                    # start_index_to_delete = existing_locations_description.index(line) + 1
                    print(f'Start index to delete records: {start_index_to_delete}')
                elif 'OBSTACLE RECTANGLES SECTION END' in line:
                    end_index_to_delete = lines_counter
                    # end_index_to_delete = existing_locations_description.index(line)
                    print(f'Ending index to delete records: {end_index_to_delete}. Abort search.')
                    break
            lines_counter += 1

        if loc_found:
            del existing_locations_description[start_index_to_delete:end_index_to_delete]

        loc_found = False
        with open('locations.py', 'w') as f_dest:
            for line in existing_locations_description:
                f_dest.write(line)
                if loc_found:
                    if '\'obs rectangles\':' in line:
                        for obs_rect_line in obs_rects:
                            f_dest.write(obs_rect_line)
                        loc_found = False

                    if '\'dem rectangles\':' in line:
                        for dem_rect_line in dem_rects:
                            f_dest.write(dem_rect_line)
                        # loc_found = False

                if '\''+self.location+'\':' in line and not loc_found:
                    # print('Location found!')
                    loc_found = True
        # f_dest.close()

        self.allow_import_locations = True

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            color = CYAN if obs.active_flag else WHITE
            pygame.draw.rect(self.screen, color, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x),
                                                  self.zoom_factor * (obs.rectangle.y - self.camera.offset_y),
                                                  self.zoom_factor * obs.rectangle.width,
                                                  self.zoom_factor * obs.rectangle.height))
            pygame.draw.rect(self.screen, BLUE, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x),
                                                  self.zoom_factor * (obs.rectangle.y - self.camera.offset_y),
                                                  self.zoom_factor * obs.rectangle.width,
                                                  self.zoom_factor * obs.rectangle.height), 1)
            s = fonts.font20.render(str(obs.id), True, GREEN)
            self.screen.blit(s, (self.zoom_factor * (obs.rectangle.centerx - s.get_width() // 2 - self.camera.offset_x + 2),
                                 self.zoom_factor * (obs.rectangle.centery - s.get_height() // 2 - self.camera.offset_y + 2)))

    def render_obstacles_back(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            pygame.draw.rect(self.screen, WHITE, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))
            s = fonts.font15.render(str(obs.id), True, GREEN)
            self.screen.blit(s, (obs.rectangle.x - self.camera.offset_x + 2, obs.rectangle.y - self.camera.offset_y + 2))

    def render_demolishers(self):
        if self.location not in self.demolishers.keys():
            return
        for key in self.demolishers[self.location].keys():
            dem = self.demolishers[self.location][key]
            pygame.draw.rect(self.screen, RED, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
                                                  dem.rectangle.width, dem.rectangle.height))
            s = fonts.font15.render(str(dem.id), True, WHITE)
            self.screen.blit(s, (dem.rectangle.x - self.camera.offset_x + 2, dem.rectangle.y - self.camera.offset_y + 2))

    def render_menu_items(self):
        # pygame.draw.rect(self.screen, BLACK, (self.menu_items[0]['rectangle'].x + 10, self.menu_items[0]['rectangle'].y)
        for pile_id in self.menu_items.keys():
            for k in reversed(self.menu_items[pile_id].keys()):
                menu_item = self.menu_items[pile_id][k]
                # print(menu_item['rectangle'].x,menu_item['rectangle'].y,menu_item['rectangle'].w,menu_item['rectangle'].h)
                if menu_item['active']:
                    # Active menu items.
                    # SHADOW:
                    pygame.draw.rect(self.screen, BLACK, (menu_item['rectangle'].x + 10, menu_item['rectangle'].y + 10,
                                                                             menu_item['rectangle'].w,menu_item['rectangle'].h), 0)
                    if menu_item['hovered']:
                        back_color = TINY_TMP
                        txt_color = WHITE
                    else:
                        if menu_item['checked']:
                            back_color = WHITE
                            txt_color = BLACK
                        else:
                            back_color = menu_item['back color']
                            txt_color = menu_item['text color']

                    # BACKGROUND:
                    pygame.draw.rect(self.screen, back_color, (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                             menu_item['rectangle'].w,menu_item['rectangle'].h), 0, 5)
                    # # FRAME:
                    # pygame.draw.rect(self.screen, BLACK, (menu_item['rectangle'].x+1, menu_item['rectangle'].y+1,
                    #                                                          menu_item['rectangle'].w,menu_item['rectangle'].h), 1)
                    # pygame.draw.rect(self.screen, menu_item['frame color'], (menu_item['rectangle'].x, menu_item['rectangle'].y,
                    #                                                          menu_item['rectangle'].w,menu_item['rectangle'].h), 1)


                    # pygame.draw.rect(self.screen, RED, (menu_item['rectangle'].x + 1, menu_item['rectangle'].y + 1,
                    #                                                          menu_item['rectangle'].w - 2, menu_item['rectangle'].h - 2), 1)

                    s = fonts.font15.render(str(menu_item['text']) + ' (PILE: ' + str(pile_id) + ' #' + str(k) + ')', True, txt_color)
                    # s = fonts.font15.render(str(menu_item['text'] + str(pile_id)), True, txt_color)
                    self.screen.blit(s, (menu_item['rectangle'].centerx - s.get_size()[0] // 2, menu_item['rectangle'].centery - s.get_size()[1] // 2))
                else:
                    # Inactive menu items (mostly, the headers)
                    # SHADOW:
                    pygame.draw.rect(self.screen, BLACK, (menu_item['rectangle'].x + 10, menu_item['rectangle'].y + 10,
                                                                             menu_item['rectangle'].w,menu_item['rectangle'].h), 0)

                    back_color = GRAY
                    txt_color = YELLOW

                    # BACKGROUND:
                    pygame.draw.rect(self.screen, back_color, (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                             menu_item['rectangle'].w,menu_item['rectangle'].h), 0)
                    # # FRAME:
                    # pygame.draw.rect(self.screen, BLACK, (menu_item['rectangle'].x+1, menu_item['rectangle'].y+1,
                    #                                                          menu_item['rectangle'].w,menu_item['rectangle'].h), 1)
                    pygame.draw.rect(self.screen, menu_item['frame color'], (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                             menu_item['rectangle'].w,menu_item['rectangle'].h), 2)


                    # pygame.draw.rect(self.screen, RED, (menu_item['rectangle'].x + 1, menu_item['rectangle'].y + 1,
                    #                                                          menu_item['rectangle'].w - 2, menu_item['rectangle'].h - 2), 1)

                    s = fonts.font15.render(str(menu_item['text']) + ' (PILE: ' + str(pile_id) + ' #' + str(k) + ')', True, txt_color)
                    # s = fonts.font15.render(str(menu_item['text']), True, txt_color)

                    self.screen.blit(s, (menu_item['rectangle'].centerx - s.get_size()[0] // 2, menu_item['rectangle'].centery - s.get_size()[1] // 2))

    def render_menu_items_old(self):
        # pygame.draw.rect(self.screen, BLACK, (self.menu_items[0]['rectangle'].x + 10, self.menu_items[0]['rectangle'].y)
        for k in self.menu_items.keys():
            menu_item = self.menu_items[k]
            # print(menu_item['rectangle'].x,menu_item['rectangle'].y,menu_item['rectangle'].w,menu_item['rectangle'].h)
            # SHADOW:
            pygame.draw.rect(self.screen, DARKGRAY, (menu_item['rectangle'].x + 10, menu_item['rectangle'].y + 10,
                                                                     menu_item['rectangle'].w,menu_item['rectangle'].h), 0)

            if menu_item['checked']:
                back_color = GRAY
            else:
                back_color = menu_item['back color']

            # BACKGROUND:
            pygame.draw.rect(self.screen, back_color, (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                     menu_item['rectangle'].w,menu_item['rectangle'].h), 0)
            # FRAME:
            pygame.draw.rect(self.screen, BLACK, (menu_item['rectangle'].x+1, menu_item['rectangle'].y+1,
                                                                     menu_item['rectangle'].w,menu_item['rectangle'].h), 1)
            pygame.draw.rect(self.screen, menu_item['frame color'], (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                     menu_item['rectangle'].w,menu_item['rectangle'].h), 1)

            if menu_item['hovered']:
                pygame.draw.rect(self.screen, RED, (menu_item['rectangle'].x + 1, menu_item['rectangle'].y + 1,
                                                                         menu_item['rectangle'].w - 2, menu_item['rectangle'].h - 2), 1)

            s = fonts.font15.render(str(menu_item['text']), True, menu_item['text color'])

            self.screen.blit(s, (menu_item['rectangle'].centerx - s.get_size()[0] // 2, menu_item['rectangle'].centery - s.get_size()[1] // 2))

    def render_new_obs(self):

        pygame.draw.rect(self.screen, CYAN, (self.zoom_factor * (self.new_obs_rect.x - self.camera.offset_x),
                                             self.zoom_factor * (self.new_obs_rect.y - self.camera.offset_y),
                                             self.zoom_factor * self.new_obs_rect.width,
                                             self.zoom_factor * self.new_obs_rect.height))

    def render_new_obs_back(self):

        pygame.draw.rect(self.screen, CYAN, (self.new_obs_rect.x - self.camera.offset_x, self.new_obs_rect.y - self.camera.offset_y,
                                              self.new_obs_rect.width, self.new_obs_rect.height))

    def render_debug_info(self):
        stats_x = 1
        stats_y = 1
        # stripes_width = 500
        gap = 1
        font_size = 18
        # m_hover_item = 'None' if not self.mouse_hovers_item else self.items[self.mouse_hovers_item].name
        # m_hover_actor = 'None' if not self.mouse_hovers_actor else self.wandering_actors[self.mouse_hovers_actor].name + ' ' + str(self.wandering_actors[self.mouse_hovers_actor].id)
        # m_hover_cell = 'None' if self.point_mouse_cursor_shows is None else str(self.locations[self.location]['points'][self.point_mouse_cursor_shows]['rect'].center)
        params = (
            ('SAVE: F2 | LOAD: F3 | W/A/S/D: MOVE CAMERA | [SHIFT] +/- : CHANGE SNAP MESH SCALE | [ ] : change inserting object type | MOUSE WHEEL : ZOOM | ESC: QUIT', BLUE),

            ('OBJECT TYPE        : ' + str(self.object_types[self.current_object_type]), BLACK),
            ('WORLD SIZE         : ' + str(self.camera.max_x) + ':' + str(self.camera.max_y), BLACK),
            ('MAX OFFSET         : ' + str(self.camera.max_offset_x) + ':' + str(self.camera.max_offset_y), BLACK),
            ('SNAP MESH SCALE    : ' + str(self.snap_mesh_size), BLACK),
            ('OFFSET GLOBAL      : ' + str(self.global_offset_xy), BLACK),
            ('CAMERA INNER OFFSET: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), BLACK),
            ('MOUSE XY           : ' + str(self.mouse_xy_snapped_to_mesh), WHITE),
            ('ZOOM               : ' + str(self.zoom_factor), WHITE),
            ('ACTIVE MENU PILE   : ' + str(self.active_menu_pile), YELLOW),
            # ('MENU               : ' + str(self.menu_items[self.active_menu_pile]), YELLOW),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], GRAY), (stats_x, stats_y + gap))
            gap += font_size

    def render_snap_mesh(self):
        for k in self.snap_mesh.keys():
            pygame.draw.circle(self.screen, YELLOW, (self.zoom_factor *(k[0] - self.camera.offset_x),
                                                     self.zoom_factor *(k[1] - self.camera.offset_y)), 1)

        for dot in self.clipboard.keys():
            if self.clipboard[dot]['location'] == self.location:
                xy = self.clipboard[dot]['coordinate']
                self.screen.blit(fonts.all_fonts[10].render(str(xy[0]) + ', ' + str(xy[1]), True, WHITE),
                                                            (self.zoom_factor * (xy[0] - self.camera.offset_x) - 30,
                                                             self.zoom_factor * (xy[1] - self.camera.offset_y) - 30))
                pygame.draw.circle(self.screen, DARK_ORANGE, (self.zoom_factor * (xy[0] - self.camera.offset_x),
                                                              self.zoom_factor * (xy[1] - self.camera.offset_y)), 8)

        pygame.draw.circle(self.screen, RED, (self.zoom_factor * (self.mouse_xy_snapped_to_mesh[0] - self.camera.offset_x),
                                              self.zoom_factor * (self.mouse_xy_snapped_to_mesh[1] - self.camera.offset_y)), 5)


    def create_snap_mesh(self):
        self.snap_mesh = dict()
        for x in range(0, self.camera.max_x + self.snap_mesh_size, self.snap_mesh_size):
            for y in range(0, self.camera.max_y + self.snap_mesh_size, self.snap_mesh_size):
        # for x in range(0, self.camera.max_offset_x + MAXX, self.snap_mesh_size):
        #     for y in range(0, self.camera.max_offset_y + MAXY, self.snap_mesh_size):
                self.snap_mesh[(x, y)] = (x, y)

    def check_mouse_xy_collides_obs(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            if obs.rectangle.collidepoint(self.mouse_xy_global):
                return obs.id
        return -1

    def edit_obs_old(self, obs):
        # print(obs.id)
        # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central header']), 'INTRODUCE OBSTACLE #' + str(obs.id) + ' AS:', '', False)
        # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), '[ACTION INITIATOR]', 'action', True)
        # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), '[MOVING PLATFORM]', 'a', True)
        menu_items = (
            ('INTRODUCE OBSTACLE #' + str(obs.id) + ' AS:', '', False),
            ('[ACTION INITIATOR]', 'action', True),
            ('[MOVING PLATFORM]', 'a', True)
        )
        self.add_menu(self.mouse_xy, 400, 20, menu_items)
        # self.render_background()
        command = self.processing_menu_items(True)  # Close menu after use
        # self.reset_human_input()
        # self.render_obstacles()

        self.obs_settings[obs.id] = dict()
        if command == 'CANCEL MENU':
            return
        elif command == 'action':
            # obs_settings = {}
            self.obs_settings[obs.id] = {
                'ghost': False,
                'speed': 0.,
                'active': False,
                'collideable': False,
                'gravity affected': False,
                'actors pass through': True,
                'invisible': True,
                'trigger': True,
                'trigger description': {
                    # 'make active': (26,28,30),
                    'change location': {
                        'new location': '',
                        'xy': (0, 0),
                    },
                    'disappear': False,
                },
                'actions': {},
            }
            # Start new menu:
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central header']), 'EDIT OBSTACLE #' + str(obs.id) + ' (current map: ' + self.location + ')', '', False)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), '[ACTION TRIGGER]', 'trig', True)
            # self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), '[TELEPORT]', 'tel', True)
            menu_items = (
                ('EDIT OBSTACLE #' + str(obs.id) + ' (current map: ' + self.location + ')', '', False),
                ('[ACTION TRIGGER]', 'trig', True),
                ('[TELEPORT]', 'tel', True)
            )
            self.add_menu(self.mouse_xy, 400, 20, menu_items)

            command = self.processing_menu_items(True)  # Close menu after use
            # self.reset_human_input()
            self.render_background()
            self.render_obstacles()

            if command == 'CANCEL MENU':
                return
            elif command == 'trig':
                self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'CHOOSE AN OBSTACLE(S):', '', False, BLUE, GRAY, YELLOW)
                self.create_menu_items_from_list(list(self.obstacles[self.location].keys()), 'small', 'OBS#: ')
                self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom right button']), '[OK]', 'stop', True)
                self.obs_settings[obs.id]['trigger description']['make active'] = list()

                # Info window at the bottom of the screen:
                self.add_menu_item(pygame.Rect(self.menu_screen_edge_margin,MAXY - self.menu_screen_edge_margin - self.menu_small_buttons_height,
                                               MAXX_DIV_2, self.menu_small_buttons_height),
                                   str(self.clipboard), '', False)

                # Choose a bunch of obstacles being triggered by this obstacle.
                while command != 'stop':
                    command = self.processing_menu_items()
                    # self.reset_human_input()
                    if command != 'stop':
                        if command == 'CANCEL MENU':
                            return
                        else:
                            if command in self.obs_settings[obs.id]['trigger description']['make active']:
                                self.obs_settings[obs.id]['trigger description']['make active'].remove(command)
                            else:
                                self.obs_settings[obs.id]['trigger description']['make active'].append(command)
                            print(self.obs_settings[obs.id]['trigger description']['make active'])

                self.menu_items = dict()
                self.menu_item_id = 1

                self.obs_settings[obs.id]['trigger description']['change location'] = {}
                obs.active_flag = True
                # print(self.obs_settings)
            else:
                # Teleport
                import locations
                self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'CHOOSE AN EXISTING MAP: ', '', False)
                map_names = list(locations.locations.keys())
                self.create_menu_items_from_list(map_names, 'medium', '')
                # menu_item_height = 20
                # for name in map_names:
                #     self.add_menu_item(pygame.Rect(self.mouse_xy[0], self.mouse_xy[1] + map_names.index(name) * menu_item_height, 400, menu_item_height), name, map_names.index(name), True)
                map_name = self.processing_menu_items(True)
                # self.reset_human_input()
                self.render_background()


                if self.clipboard:
                    self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'ENTER A POSITION TO WRAP: ', '', False)
                    self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), '[FROM CLIP BOARD]', 'clip', True)
                    self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), '[MANUAL]', 'manual', True)
                    command = self.processing_menu_items(True)
                    self.render_background()
                    if command == 'CANCEL MENU':
                        return
                else:
                    command = 'manual'

                if command == 'CANCEL MENU':
                    return
                elif command == 'clip':
                    self.reset_menu()
                    dots = list(self.clipboard.keys())
                    self.create_menu_items_from_list(dots, 'medium', '')
                    xy = self.processing_menu_items(True)
                    self.render_background()
                    # self.reset_human_input()

                    self.obs_settings[obs.id]['trigger description']['make active'] = None
                    self.obs_settings[obs.id]['trigger description']['change location'] = {
                        'new location': map_name,
                        'xy': self.clipboard[xy]['coordinate'],
                    }
                elif command == 'manual':

                    x = self.create_text_input((self.menu_elements_bindings['central header'][0], self.menu_elements_bindings['central header'][1] +
                                                self.menu_elements_bindings['central header'][3] + 10),
                                               'Enter X coordinate of position to teleport (just hit [ENTER] to force keeping X after location change): ', 'digit')
                    if len(x) == 0:
                        x = 'keep X'
                    else:
                        x = int(x)
                    y = self.create_text_input((self.menu_elements_bindings['central header'][0], self.menu_elements_bindings['central header'][1] +
                                                self.menu_elements_bindings['central header'][3] + 50),
                                               'Enter Y coordinate of position to teleport (just hit [ENTER] to force keeping Y after location change): ', 'digit')
                    if len(y) == 0:
                        y = 'keep Y'
                    else:
                        y = int(y)

                    self.obs_settings[obs.id]['trigger description']['make active'] = None
                    self.obs_settings[obs.id]['trigger description']['change location'] = {
                        'new location': map_name,
                        'xy': (x, y),
                        # 'xy': (int(x), int(y)),
                    }

                obs.active_flag = True
                return


    def edit_obs(self, obs):
        # self.menu_action_pending = ''
        self.reset_menu_actions_pending()
        # Create menu of 'obstacle edit' type, which was predefined in self.menu_structure:
        self.add_menu(self.mouse_xy, 400, 20, [self.menu_structure['obstacle edit'][i] for i in self.menu_structure['obstacle edit'].keys()])

        while not self.menu_actions_done:
        # while self.menu_action_pending == '':
            self.processing_human_input()
            self.processing_menu_items()
            self.render_background()
            self.render_menu_items()
            pygame.display.flip()
        self.reset_human_input()
        self.reset_menu()

        self.obs_settings[obs.id] = dict()

        print(f'[edit_obs] {self.menu_actions_pending=}')

        if self.menu_actions_pending[-1] == 'moving':
            self.reset_menu_actions_pending()
            # self.menu_actions_pending = ''
            print('make moving platform')
            self.add_menu(self.mouse_xy, 400, 20, [i for i in self.obs_settings[obs.id].keys()])
            while not self.menu_actions_done:
                self.processing_human_input()
                self.processing_menu_items()
                self.render_background()
                self.render_menu_items()
                pygame.display.flip()
            self.reset_human_input()
            self.reset_menu()
        elif self.menu_actions_pending[-1] == 'custom obs edit done':
            summary = list()
            for k in self.menu_structure['custom obs properties'].keys():
                if obs.id not in self.obs_settings.keys():
                    self.obs_settings[obs.id] = dict()
                if self.menu_structure['custom obs properties'][k]['LMB action'] is not None and \
                    self.menu_structure['custom obs properties'][k]['LMB action'][0] in \
                        ('input number', 'switch state', 'input string'):
                    for j in self.menu_structure['custom obs properties'][k]['LMB action'][1].keys():
                        self.obs_settings[obs.id][j] =  self.menu_structure['custom obs properties'][k]['LMB action'][1][j]

            for j in self.obs_settings[obs.id].keys():
                print(j, self.obs_settings[obs.id][j])
            self.reset_menu_actions_pending()
        elif self.menu_actions_pending[-1] == 'teleport':
            self.reset_menu_actions_pending()
            # self.menu_action_pending = ''
            print('make teleport')
        else:
            print('make other deed')

        return
            # self.obs_settings[obs.id] = {
            #     'ghost': False,
            #     'speed': 0.,
            #     'active': False,
            #     'collideable': False,
            #     'gravity affected': False,
            #     'actors pass through': True,
            #     'invisible': True,
            #     'trigger': True,
            #     'trigger description': {
            #         # 'make active': (26,28,30),
            #         'change location': {
            #             'new location': '',
            #             'xy': (0, 0),
            #         },
            #         'disappear': False,
            #     },
            #     'actions': {},
            # }
            # if command == 'trig':
            #
            #     self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'CHOOSE AN OBSTACLE(S):', '', False, BLUE, GRAY, YELLOW)
            #     self.create_menu_items_from_list(list(self.obstacles[self.location].keys()), 'small', 'OBS#: ')
            #     self.add_menu_item(pygame.Rect(self.menu_elements_bindings['bottom right button']), '[OK]', 'stop', True)
            #     self.obs_settings[obs.id]['trigger description']['make active'] = list()
            #
            #     # Info window at the bottom of the screen:
            #     self.add_menu_item(pygame.Rect(self.menu_screen_edge_margin,MAXY - self.menu_screen_edge_margin - self.menu_small_buttons_height,
            #                                    MAXX_DIV_2, self.menu_small_buttons_height),
            #                        str(self.clipboard), '', False)
            #
            #     # Choose a bunch of obstacles being triggered by this obstacle.
            #     while command != 'stop':
            #         command = self.processing_menu_items()
            #         # self.reset_human_input()
            #         if command != 'stop':
            #             if command == 'CANCEL MENU':
            #                 return
            #             else:
            #                 if command in self.obs_settings[obs.id]['trigger description']['make active']:
            #                     self.obs_settings[obs.id]['trigger description']['make active'].remove(command)
            #                 else:
            #                     self.obs_settings[obs.id]['trigger description']['make active'].append(command)
            #                 print(self.obs_settings[obs.id]['trigger description']['make active'])
            #
            #     self.menu_items = dict()
            #     self.menu_item_id = 1
            #
            #     self.obs_settings[obs.id]['trigger description']['change location'] = {}
            #     obs.active_flag = True
            #     # print(self.obs_settings)
            # else:
            #     # Teleport
            #     import locations
            #     self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'CHOOSE AN EXISTING MAP: ', '', False)
            #     map_names = list(locations.locations.keys())
            #     self.create_menu_items_from_list(map_names, 'medium', '')
            #     # menu_item_height = 20
            #     # for name in map_names:
            #     #     self.add_menu_item(pygame.Rect(self.mouse_xy[0], self.mouse_xy[1] + map_names.index(name) * menu_item_height, 400, menu_item_height), name, map_names.index(name), True)
            #     map_name = self.processing_menu_items(True)
            #     # self.reset_human_input()
            #     self.render_background()
            #
            #
            #     if self.clipboard:
            #         self.add_menu_item(pygame.Rect(self.menu_elements_bindings['top header']), 'ENTER A POSITION TO WRAP: ', '', False)
            #         self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central left button']), '[FROM CLIP BOARD]', 'clip', True)
            #         self.add_menu_item(pygame.Rect(self.menu_elements_bindings['central right button']), '[MANUAL]', 'manual', True)
            #         command = self.processing_menu_items(True)
            #         self.render_background()
            #         if command == 'CANCEL MENU':
            #             return
            #     else:
            #         command = 'manual'
            #
            #     if command == 'CANCEL MENU':
            #         return
            #     elif command == 'clip':
            #         self.reset_menu()
            #         dots = list(self.clipboard.keys())
            #         self.create_menu_items_from_list(dots, 'medium', '')
            #         xy = self.processing_menu_items(True)
            #         self.render_background()
            #         # self.reset_human_input()
            #
            #         self.obs_settings[obs.id]['trigger description']['make active'] = None
            #         self.obs_settings[obs.id]['trigger description']['change location'] = {
            #             'new location': map_name,
            #             'xy': self.clipboard[xy]['coordinate'],
            #         }
            #     elif command == 'manual':
            #
            #         x = self.create_text_input((self.menu_elements_bindings['central header'][0], self.menu_elements_bindings['central header'][1] +
            #                                     self.menu_elements_bindings['central header'][3] + 10),
            #                                    'Enter X coordinate of position to teleport (just hit [ENTER] to force keeping X after location change): ', 'digit')
            #         if len(x) == 0:
            #             x = 'keep X'
            #         else:
            #             x = int(x)
            #         y = self.create_text_input((self.menu_elements_bindings['central header'][0], self.menu_elements_bindings['central header'][1] +
            #                                     self.menu_elements_bindings['central header'][3] + 50),
            #                                    'Enter Y coordinate of position to teleport (just hit [ENTER] to force keeping Y after location change): ', 'digit')
            #         if len(y) == 0:
            #             y = 'keep Y'
            #         else:
            #             y = int(y)
            #
            #         self.obs_settings[obs.id]['trigger description']['make active'] = None
            #         self.obs_settings[obs.id]['trigger description']['change location'] = {
            #             'new location': map_name,
            #             'xy': (x, y),
            #             # 'xy': (int(x), int(y)),
            #         }
            #
            #     obs.active_flag = True
            #     return

                # print(self.obs_settings)
            # exit()
    def process(self):
        # self.create_text_input((100, 100), 'INPUT TEXT XXXXXXXXXXXXXXXXXXXXXXXXXXX:', 'str')
        self.processing_human_input()
        # print('ok')
        if self.menu_items:
            # self.processing_menu_items(True)
            self.processing_menu_items()
            # exec(command)
        else:
            if self.is_mouse_wheel_up:
                self.is_mouse_wheel_up = False
                self.zoom_factor += .1
            elif self.is_mouse_wheel_down:
                self.is_mouse_wheel_down = False
                self.zoom_factor -= .1

            obs_id = self.check_mouse_xy_collides_obs()

            if self.is_spacebar:
                # obs_id = self.check_mouse_xy_collides_obs()
                if obs_id > -1:
                    # Try to delete existing obs:
                    del self.obstacles[self.location][obs_id]
                    if obs_id in self.obs_settings.keys():
                        del self.obs_settings[obs_id]

            # RMB
            if self.is_right_mouse_button_down:
                self.is_right_mouse_button_down = False
                if obs_id > -1:
                    self.edit_obs(self.obstacles[self.location][obs_id])
                else:

                    if self.mouse_xy_snapped_to_mesh in self.clipboard.keys():
                        # Delete existing dot from the clipboard.
                        del self.clipboard[self.mouse_xy_snapped_to_mesh]
                    else:
                        # Place current mouse coordinate to clipboard.
                        self.clipboard[self.mouse_xy_snapped_to_mesh] = {
                            'location': self.location,
                            'coordinate': self.mouse_xy_snapped_to_mesh
                        }

            if self.is_right_bracket:
                self.is_right_bracket = False
                self.current_object_type += 1
                if self.current_object_type == len(self.object_types):
                    self.current_object_type = 0
            if self.is_left_bracket:
                self.is_left_bracket = False
                self.current_object_type -= 1
                if self.current_object_type < 0:
                    self.current_object_type = len(self.object_types) - 1

            if self.is_left_mouse_button_down:
                if self.new_obs_rect_started:
                    # Update new obs.
                    # last_point = (self.mouse_xy_global[0] // self.snap_mesh_size * self.snap_mesh_size,
                    #               self.mouse_xy_global[1] // self.snap_mesh_size * self.snap_mesh_size)
                    last_point = self.mouse_xy_snapped_to_mesh
                    if self.new_obs_rect_start_xy[0] < last_point[0]:
                        x = self.new_obs_rect_start_xy[0]
                        w = last_point[0] - self.new_obs_rect_start_xy[0]
                    else:
                        x = last_point[0]
                        w = self.new_obs_rect_start_xy[0] - last_point[0]

                    if self.new_obs_rect_start_xy[1] < last_point[1]:
                        y = self.new_obs_rect_start_xy[1]
                        h = last_point[1] - self.new_obs_rect_start_xy[1]
                    else:
                        y = last_point[1]
                        h = self.new_obs_rect_start_xy[1] - last_point[1]
                    self.new_obs_rect.update(x, y, w, h)
                else:
                    # Start new obs.
                    self.new_obs_rect_started = True
                    self.new_obs_rect_start_xy = self.mouse_xy_snapped_to_mesh
                    # self.new_obs_rect_start_xy = self.mouse_xy_global  # Without snap to mesh.
            else:
                if self.new_obs_rect_started:
                    # Add new obs.

                    if self.new_obs_rect.width != 0 and self.new_obs_rect.height != 0:
                        if self.object_types[self.current_object_type] == 'obstacle':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.obstacle_id)
                            self.obstacle_id += 1
                            self.add_obstacle(description)
                        elif self.object_types[self.current_object_type] == 'demolisher':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.demolishers_id)
                            self.demolishers_id += 1
                            self.add_demolisher(description)
                    self.new_obs_rect_started = False
                    self.new_obs_rect_start_xy = [0, 0]
                    self.new_obs_rect.update(0,0,0,0)

            # Update camera viewport:
            if self.is_input_left_arrow:
                self.global_offset_xy[0] -= self.camera_scroll_speed * 10
                if self.global_offset_xy[0] < MAXX_DIV_2:
                    self.global_offset_xy[0] = MAXX_DIV_2
            if self.is_input_right_arrow:
                self.global_offset_xy[0] += self.camera_scroll_speed * 10
                if self.global_offset_xy[0] > MAXX_DIV_2 + self.camera.max_offset_x:
                    self.global_offset_xy[0] = MAXX_DIV_2 + self.camera.max_offset_x
            if self.is_input_down_arrow:
                self.global_offset_xy[1] += self.camera_scroll_speed * 10
                if self.global_offset_xy[1] > MAXY_DIV_2 + self.camera.max_offset_y:
                    self.global_offset_xy[1] = MAXY_DIV_2 + self.camera.max_offset_y
            if self.is_input_up_arrow:
                self.global_offset_xy[1] -= self.camera_scroll_speed * 10
                if self.global_offset_xy[1] < MAXY_DIV_2:
                    self.global_offset_xy[1] = MAXY_DIV_2
            self.camera.apply_offset(self.global_offset_xy,
                                     self.camera_scroll_speed * 10, self.camera_scroll_speed * 10, False)

            # Rendering:
            self.render_background()
            self.render_obstacles()
            self.render_demolishers()
            self.render_new_obs()
            self.render_debug_info()
            self.render_snap_mesh()
            self.render_menu_items()

    def process_old(self):
        # self.create_text_input((100, 100), 'INPUT TEXT XXXXXXXXXXXXXXXXXXXXXXXXXXX:', 'str')
        self.processing_human_input()

        if self.menu_items:
            # self.processing_menu_items(True)
            command = self.processing_menu_items(True)
            # exec(command)
        else:
            if self.is_mouse_wheel_up:
                self.is_mouse_wheel_up = False
                self.zoom_factor += .1
            elif self.is_mouse_wheel_down:
                self.is_mouse_wheel_down = False
                self.zoom_factor -= .1

            obs_id = self.check_mouse_xy_collides_obs()

            if self.is_spacebar:
                # obs_id = self.check_mouse_xy_collides_obs()
                if obs_id > -1:
                    # Try to delete existing obs:
                    del self.obstacles[self.location][obs_id]
                    if obs_id in self.obs_settings.keys():
                        del self.obs_settings[obs_id]

            # RMB
            if self.is_right_mouse_button_down:
                self.is_right_mouse_button_down = False
                if obs_id > -1:
                    self.edit_obs(self.obstacles[self.location][obs_id])
                else:

                    if self.mouse_xy_snapped_to_mesh in self.clipboard.keys():
                        # Delete existing dot from the clipboard.
                        del self.clipboard[self.mouse_xy_snapped_to_mesh]
                    else:
                        # Place current mouse coordinate to clipboard.
                        self.clipboard[self.mouse_xy_snapped_to_mesh] = {
                            'location': self.location,
                            'coordinate': self.mouse_xy_snapped_to_mesh
                        }

            if self.is_right_bracket:
                self.is_right_bracket = False
                self.current_object_type += 1
                if self.current_object_type == len(self.object_types):
                    self.current_object_type = 0
            if self.is_left_bracket:
                self.is_left_bracket = False
                self.current_object_type -= 1
                if self.current_object_type < 0:
                    self.current_object_type = len(self.object_types) - 1

            if self.is_left_mouse_button_down:
                if self.new_obs_rect_started:
                    # Update new obs.
                    # last_point = (self.mouse_xy_global[0] // self.snap_mesh_size * self.snap_mesh_size,
                    #               self.mouse_xy_global[1] // self.snap_mesh_size * self.snap_mesh_size)
                    last_point = self.mouse_xy_snapped_to_mesh
                    if self.new_obs_rect_start_xy[0] < last_point[0]:
                        x = self.new_obs_rect_start_xy[0]
                        w = last_point[0] - self.new_obs_rect_start_xy[0]
                    else:
                        x = last_point[0]
                        w = self.new_obs_rect_start_xy[0] - last_point[0]

                    if self.new_obs_rect_start_xy[1] < last_point[1]:
                        y = self.new_obs_rect_start_xy[1]
                        h = last_point[1] - self.new_obs_rect_start_xy[1]
                    else:
                        y = last_point[1]
                        h = self.new_obs_rect_start_xy[1] - last_point[1]
                    self.new_obs_rect.update(x, y, w, h)
                else:
                    # Start new obs.
                    self.new_obs_rect_started = True
                    self.new_obs_rect_start_xy = self.mouse_xy_snapped_to_mesh
                    # self.new_obs_rect_start_xy = self.mouse_xy_global  # Without snap to mesh.
            else:
                if self.new_obs_rect_started:
                    # Add new obs.

                    if self.new_obs_rect.width != 0 and self.new_obs_rect.height != 0:
                        if self.object_types[self.current_object_type] == 'obstacle':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.obstacle_id)
                            self.obstacle_id += 1
                            self.add_obstacle(description)
                        elif self.object_types[self.current_object_type] == 'demolisher':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.demolishers_id)
                            self.demolishers_id += 1
                            self.add_demolisher(description)
                    self.new_obs_rect_started = False
                    self.new_obs_rect_start_xy = [0, 0]
                    self.new_obs_rect.update(0,0,0,0)

            # Update camera viewport:
            if self.is_input_left_arrow:
                self.global_offset_xy[0] -= self.camera_scroll_speed * 10
                if self.global_offset_xy[0] < MAXX_DIV_2:
                    self.global_offset_xy[0] = MAXX_DIV_2
            if self.is_input_right_arrow:
                self.global_offset_xy[0] += self.camera_scroll_speed * 10
                if self.global_offset_xy[0] > MAXX_DIV_2 + self.camera.max_offset_x:
                    self.global_offset_xy[0] = MAXX_DIV_2 + self.camera.max_offset_x
            if self.is_input_down_arrow:
                self.global_offset_xy[1] += self.camera_scroll_speed * 10
                if self.global_offset_xy[1] > MAXY_DIV_2 + self.camera.max_offset_y:
                    self.global_offset_xy[1] = MAXY_DIV_2 + self.camera.max_offset_y
            if self.is_input_up_arrow:
                self.global_offset_xy[1] -= self.camera_scroll_speed * 10
                if self.global_offset_xy[1] < MAXY_DIV_2:
                    self.global_offset_xy[1] = MAXY_DIV_2
            self.camera.apply_offset(self.global_offset_xy,
                                     self.camera_scroll_speed * 10, self.camera_scroll_speed * 10, False)

            # Rendering:
            self.render_background()
            self.render_obstacles()
            self.render_demolishers()
            self.render_new_obs()
            self.render_debug_info()
            # self.render_menu()
            self.render_snap_mesh()

world = World()
world.set_screen(screen)
# world.create_text_input((100, 100), 'INPUT TEXT:', 'digit')

world.setup()
import locations
world.location_names['names list'] = list(locations.locations.keys())
world.load()

allow_import_location = False
def main():
    global allow_import_location
    # while True:
    #     if world.allow_import_locations:
    #         allow_import_location = True
    #         world.allow_import_locations = False

        # if world.need_to_load:
        #     world.need_to_load = False
        #     world.setup()
        #     allow_import_location = True
        #     world.obstacles[world.location] = dict()
        #     world.load()
        #     world.create_snap_mesh()
    world.process()
    pygame.display.flip()


if __name__ == "__main__":
    while True:
        if world.need_to_load:
            world.need_to_load = False
            importlib.reload(locations)
            world.setup()
            # importlib.reload(locations)
            world.load()
            # world.create_snap_mesh()
        # if allow_import_location:
        #     from locations import *
        #     allow_import_location = False
        main()