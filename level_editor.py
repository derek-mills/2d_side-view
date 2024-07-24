# import pygame
import uuid
from os import listdir
from shutil import move

import pygame
from actors_description import all_hostiles
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
from level_editor_menu_structure import *
from copy import copy, deepcopy
# from sound import *
# import json
# import pickle
# import setup_box
# import menu
from uuid import *
import importlib
from misc_tools import copy_surface_as_surface


class World(object):
    def __init__(self):

        self.need_to_load = False
        self.allow_import_locations = False
        self.clipboard = dict()
        self.default_font_size = 15
        self.tiles = dict()
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
        self.show_debug_info = False
        self.mouse_xy = list()  #
        self.mouse_xy_global = list()  #
        self.mouse_xy_snapped_to_mesh = list()  #
        self.is_mouse_hovers_item: bool = False
        self.mouse_hovers_item: int = 0
        self.is_mouse_hovers_actor: bool = False
        self.mouse_hovers_actor: int = 0
        self.camera_follows_mouse = True
        self.camera_scroll_speed = 4

        self.object_types = ('obstacle', 'enemy')
        # self.object_types = ('obstacle', 'demolisher')
        self.current_object_type = 0

        self.enemies = dict()
        # self.enemy_id: int = 1
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
        # Obstacle which could be selected by LMB, because LMB was pressed while cursor is over it.
        self.to_be_selected_obs_id = -1
        # Obstacle which was selected by LMB, because LMB was pressed and then released while cursor is over it.
        self.selected_obs_id = -1

        self.snap_mesh = dict()
        self.default_snap_mesh_size = 50
        self.snap_mesh_size = self.default_snap_mesh_size
        self.snap_mesh_size_change_step = 25
        self.zoom_factor = 1.

        # MENU MANAGEMENT
        self.menu_items = dict()
        self.menu_item_id = 0
        self.menu_pile_id = 0  # ID of a bunch of tied together menu items
        self.active_menu_pile = 0
        self.menu_actions_done = False
        self.menu_return_value = None
        self.menu_walk_tree = list()
        # self.menu_path = list()
        self.menu_elements_bindings = menu_elements_bindings
        # self.menu_structure = dict()
        self.menu_structure = deepcopy(menu_structure)
        self.menu_items_y_scroll_speed: int = 50  #

        self.minimap = None
        self.minimap_zoomed_out = None
        self.show_minimap = False

    def set_screen(self, surface):
        self.screen = surface

    def generate_menu(self, menu_name):
        # menu_name = menu_item['value']
        # import locations
        # Let's generate a list of new menu items from the given text-type description of sequence:
        if type(self.menu_structure[menu_name]['generate list from']) == str:
            if self.menu_structure[menu_name]['generate list from'][0] == '*':
                # Got string, which is a pointer to an iteration sequence.
                # We have to unfurl it using eval():
                menu_items_list = list(eval(self.menu_structure[menu_name]['generate list from'][1:]))
            elif self.menu_structure[menu_name]['generate list from'][0] == '@':
                # Got string, which has a flag of execution.
                # We have to execute it using exec():
                menu_items_list = list(exec(self.menu_structure[menu_name]['generate list from'][1:]))
            else:
                # Got a simple string. Have to split it using ';' as a delimiter:
                menu_items_list = self.menu_structure[menu_name]['generate list from'].split(';')
        else:
            # Got native iteration sequence. Have to simply convert it to a list:
            menu_items_list = list(self.menu_structure[menu_name]['generate list from'])

        if len(menu_items_list) == 0:
            return

        # self.menu_structure[menu_name] = dict()
        for item in menu_items_list:
            print(f'[generate menu] Adding item: {item}')
            self.menu_structure[menu_name][item] = dict()
            self.menu_structure[menu_name][item]['description'] = item
            for reference_key in self.menu_structure['_template_menu_item_'].keys():
                if reference_key in self.menu_structure[menu_name]['predefined keys'].keys():
                    reference_menu_item = self.menu_structure[menu_name]['predefined keys'][reference_key]
                    if reference_menu_item and type(reference_menu_item) == str:
                        if reference_menu_item[0] == '*':
                            # Has got a pointers to particular global variable:
                            # bunch_of_pointers = reference_menu_item.split('*')
                            # for p in bunch_of_pointers:
                            #     reference_menu_item = eval(reference_menu_item[1:])
                            reference_menu_item = eval(reference_menu_item[1:])
                        elif reference_menu_item[0] == '$':
                            # Pointer to the inner dict key:
                            reference_menu_item = self.menu_structure[menu_name][item][reference_menu_item[1:]]
                        elif reference_menu_item[0] == '@':
                            # '@' this is the sign of executability of all code which remains after this sign.
                            # i = reference_menu_item.split('@')
                            # reference_menu_item = i[0] + eval(i[1])
                            # print(reference_menu_item)
                            reference_menu_item = exec(reference_menu_item[1:])
                    self.menu_structure[menu_name][item][reference_key] = reference_menu_item
                else:
                    self.menu_structure[menu_name][item][reference_key] = self.menu_structure['_template_menu_item_'][reference_key]

            # print(f'[generate_menu] Generating menu: {item}')
            # for k in self.menu_structure[menu_name][item].keys():
            #     i = self.menu_structure[menu_name][item][k]
            #     print(f'[generate_menu] {k}')
            # print(f'[generate_menu] ----------')


    def reset_menu_walk_tree(self):
        self.menu_walk_tree = list()

    def reset_menu(self):
        self.reset_human_input()
        self.menu_items = dict()
        self.menu_item_id = 0
        self.menu_actions_done = False
        self.active_menu_pile = 0
        self.menu_return_value = None
        # self.menu_structure = dict()
        # self.menu_walk_tree = list()
        # self.menu_walk_tree = list()

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
                self.menu_walk_tree.append('CANCEL MENU')
                self.menu_actions_done = True
                return

        menu_item_has_been_already_checked = False

        # MOUSE WHEEL:
        if self.is_mouse_wheel_up:
            self.reset_human_input()
            menu_items_keys = list(self.menu_items[self.active_menu_pile].keys())
            if self.menu_items[self.active_menu_pile][menu_items_keys[-1]]['rectangle'].y < 0:
                for k in menu_items_keys:
                    self.menu_items[self.active_menu_pile][k]['rectangle'].y += self.menu_items_y_scroll_speed
                # self.menu_items_y_correction -= 50
        elif self.is_mouse_wheel_down:
            self.reset_human_input()
            menu_items_keys = list(self.menu_items[self.active_menu_pile].keys())
            if self.menu_items[self.active_menu_pile][menu_items_keys[0]]['rectangle'].y > MAXY:
                for k in menu_items_keys:
                    self.menu_items[self.active_menu_pile][k]['rectangle'].y -= self.menu_items_y_scroll_speed
                # self.menu_items_y_correction -= 50


        for pile_id in reversed(self.menu_items.keys()):
            for k in self.menu_items[pile_id].keys():
                menu_item = self.menu_items[pile_id][k]
                # menu_item['rectangle'].y += self.menu_items_y_correction
                # if menu_item['menu actions done']:

                if menu_item_has_been_already_checked:
                    # If mouse cursor has already collided with any other menu item, all further calculations are futile:
                    menu_item['hovered'] = False
                    menu_item['has been already activated'] = False
                    continue

                if menu_item['rectangle'].collidepoint(self.mouse_xy):
                    menu_item_has_been_already_checked = True
                    if not menu_item['active']:
                        continue
                    menu_item['hovered'] = True
                    # ON HOVER ACTIONS:
                    if menu_item['on hover action']:
                        if not menu_item['has been already activated']:
                            menu_item['has been already activated'] = True
                            # ----------SUBMENU-----------------------------------------
                            if menu_item['on hover action'] == 'reveal submenu':
                                self.delete_all_child_menu_piles(pile_id)
                                self.add_menu(menu_item, (self.mouse_xy[0], menu_item['rectangle'].centery),
                                          menu_item['rectangle'].width, 20)
                                return
                    else:
                        if self.active_menu_pile > pile_id:
                            self.delete_all_child_menu_piles(pile_id)
                            return

                    # LMB MENU ACTION:
                    if self.is_left_mouse_button_down:
                        self.is_left_mouse_button_down = False
                        if menu_item['LMB action']:
                            # ----------EXEC--------------------------------------------
                            if menu_item['LMB action'] == 'exec':
                                exec(menu_item['value'])
                            # ----------INPUT INTEGER---------------------
                            elif menu_item['LMB action'] == 'input int':
                                command = menu_item['target'] + " = self.create_text_input((self.mouse_xy[0], self.mouse_xy[1]), menu_item['label'], int(0), 'int')"
                                exec(command)
                            # ----------INPUT FLOAT---------------------
                            elif menu_item['LMB action'] == 'input float':
                                command = menu_item['target'] + " = self.create_text_input((self.mouse_xy[0], self.mouse_xy[1]), menu_item['label'], 0., 'float')"
                                exec(command)
                            # ----------INPUT STRING---------------------
                            elif menu_item['LMB action'] == 'input str':
                                command = menu_item['target'] + " = self.create_text_input((self.mouse_xy[0], self.mouse_xy[1]), menu_item['label'], '', 'str')"
                                exec(command)
                            # ----------INPUT ANY CHAR---------------------
                            elif menu_item['LMB action'] == 'input any':
                                command = menu_item['target'] + " = self.create_text_input((self.mouse_xy[0], self.mouse_xy[1]), menu_item['label'], '', 'any')"
                                exec(command)
                            # ----------REVEAL SUBMENU---------------------------------
                            elif menu_item['LMB action'] == 'reveal submenu':
                                self.delete_all_child_menu_piles(pile_id)
                                # self.active_menu_pile += 1
                                self.add_menu(menu_item, (menu_item['rectangle'].x, menu_item['rectangle'].y),
                                              menu_item['rectangle'].width, 20)
                                return
                            # ----------APPEND------------------------------------------
                            elif menu_item['LMB action'] == 'append value':
                                print('[processing menu] append value')
                                target = eval(menu_item['target'])
                                if type(menu_item['value']) == str:
                                    if menu_item['value'][0] == '*':
                                        # Pointer to a mutable type variable:
                                        value = eval(menu_item['value'][1:])
                                    else:
                                        # print(menu_item.keys())
                                        value = menu_item['value']
                                else:
                                    # print(menu_item.keys())
                                    value = menu_item['value']
                                    # target.append(menu_item['value'])
                                    # eval(menu_item['target']).append(menu_item['value'])
                                print(f'[processing menu] append {value} to {target}')
                                if value in target:
                                    target.remove(value)
                                    menu_item['checked'] = False
                                else:
                                    target.append(value)
                                    menu_item['checked'] = True
                            # ----------SWITCH STATE-----------------------------------
                            elif menu_item['LMB action'] == 'switch state':
                                # menu_item['label'] = menu_item['label'].split(':')[0]
                                for_exec = ''
                                for k_tmp_string in menu_item['target']:
                                    for_exec = k_tmp_string + ' = True if not eval(k_tmp_string) else False'
                                    exec(for_exec)
                                    # menu_item['label'] += ': ' + str(eval(k_tmp_string))
                            # ----------STORE VALUE------------------------------------------
                            elif menu_item['LMB action'] == 'store value':
                                print('[processing menu] store value: ', menu_item['value'])
                                command = menu_item['target'] + ' = copy(menu_item[\'value\'])'
                                exec(command)
                                if type(menu_item['value']) == list:
                                    menu_item['value'] = list()
                                elif type(menu_item['value']) == dict:
                                    menu_item['value'] = dict()
                                elif type(menu_item['value']) == str:
                                    menu_item['value'] = ''

                                # print('[processing menu] store value: ', eval(menu_item['target']))
                                print('[processing menu] target becomes: ', self.menu_structure['custom obs properties']['ok']['value'])

                                # exec(menu_item['target'] + ' = menu_item[\'value\']')
                            # ----------RETURN VALUE------------------------------------------
                            elif menu_item['LMB action'] == 'return value':
                                self.menu_return_value = menu_item['value']
                                self.menu_actions_done = True
                                return

                            # ------------------------------------------
                            # ----------AFTERMATH ACTIONS--------------------------------
                            # if menu_item['after action']:
                            if menu_item['after action'] == 'keep going':
                                print('[processing menu] keep going')
                                continue
                            elif menu_item['after action'] == 'return to parent':
                                print('[processing menu] returning to parent.')
                                print(f'[processing menu] {self.active_menu_pile=} {self.menu_items.keys()=}')
                                print('[processing menu] parent menu for current:', menu_item['parent menu pile'])
                                self.delete_all_child_menu_piles(menu_item['parent menu pile'])

                                # print('[processing menu]', self.menu_items.keys())
                                return
                            else:  # If None or something else
                                self.menu_return_value = copy(eval(menu_item['target']))
                                # self.delete_all_child_menu_piles(menu_item['menu pile'])
                                self.menu_actions_done = True
                                return
                            # else:
                            #     # Submenu ends action.
                            #     if menu_item['parent menu pile'] == 0:
                            #         self.menu_return_value = eval(menu_item['target'])
                            #         # self.delete_all_child_menu_piles(menu_item['menu pile'])
                            #         self.menu_actions_done = True
                            #         return
                            #     if self.menu_items[menu_item['parent menu pile']][menu_item['parent dict key']]['after action']:
                            #         if self.menu_items[menu_item['parent menu pile']][menu_item['parent dict key']]['after action'] == 'keep going':
                            #             self.delete_all_child_menu_piles(menu_item['parent menu pile'])
                            #             # self.delete_all_child_menu_piles(menu_item['menu pile'] - 1)
                            #             print('[processing menu]', self.menu_structure['main menu']['load']['target'])
                            #             print('[processing menu]', self.menu_items.keys())
                            #             return
                            #         else:
                            #             self.menu_return_value = eval(menu_item['target'])
                            #             self.menu_actions_done = True
                            #             return
                            #     else:
                            #         # self.delete_all_child_menu_piles(menu_item['menu pile'])
                            #         # self.reset_menu()
                            #         self.menu_return_value = eval(menu_item['target'])
                            #         self.menu_actions_done = True
                            #         return

                else:
                    menu_item['hovered'] = False
                    if menu_item['on hover action'] and menu_item['has been already activated']:
                        menu_item['has been already activated'] = False
                        # Delete all already revealed submenus:
                        self.delete_all_child_menu_piles(pile_id)
                        return

    def delete_all_child_menu_piles(self, parent_pile_number):
        piles_to_delete = list()
        # print(f'[delete child menus] {parent_pile_number=} {list(self.menu_items.keys())}')
        for pile in self.menu_items.keys():
            if pile > parent_pile_number:
                # if pile > self.active_menu_pile:
                piles_to_delete.append(pile)
        # print(f'[delete child menus] {piles_to_delete=}')
        for p in piles_to_delete:
            self.menu_walk_tree.pop()
            del self.menu_items[p]
        self.active_menu_pile = parent_pile_number
        self.menu_pile_id = parent_pile_number

    # def create_menu_items_from_list(self, a_list, button_text, menu_items_size='medium'):
    #     if menu_items_size == 'small':
    #         w = self.menu_small_buttons_width
    #         h = self.menu_small_buttons_height
    #     elif menu_items_size == 'medium':
    #         w = self.menu_buttons_width
    #         h = self.menu_buttons_height
    #     start_y = self.menu_screen_edge_margin + self.menu_headers_height + self.menu_buttons_spacing
    #     max_height_of_free_space = MAXY - self.menu_screen_edge_margin - start_y
    #     max_menu_elements_fits = max_height_of_free_space // (h + self.menu_buttons_spacing)
    #     columns_needed = len(a_list) // max_menu_elements_fits + 1
    #     # print(f'{max_height_of_free_space=} {max_menu_elements_fits=} {len(obs_id_list)=} {columns_needed=}')
    #     # Define start x coordinate:
    #     if columns_needed / 2 == columns_needed // 2:
    #         # Quantity of columns is even.
    #         start_x = MAXX_DIV_2 - w * columns_needed // 2  # - self.menu_buttons_spacing // 2
    #     else:
    #         # Quantity of columns is odd.
    #         start_x = MAXX_DIV_2 - w // 2 - w // 2 * columns_needed // 2
    #
    #     c = 0
    #     for element in a_list:
    #         item = {
    #             'label': button_text + str(element),
    #             'LMB action': ('return value', element),
    #             'active': True,
    #             'rectangle': pygame.Rect(start_x, start_y + c * (h + self.menu_buttons_spacing),
    #                                        w, h),
    #             'on hover action': None,
    #             'after action': None
    #         }
    #
    #         self.add_menu_item(item)
    #         c += 1
    #         if c == max_menu_elements_fits:
    #             c = 0
    #             start_x += (w + self.menu_buttons_spacing)
    #             start_y = self.menu_screen_edge_margin + self.menu_headers_height + self.menu_buttons_spacing

    # def setup(self):
    #     for i in self.menu_structure['initial setup'].keys():
    #         item = self.menu_structure['initial setup'][i]
    #         self.add_menu_item(item)
    #     self.add_menu('initial setup', (MAXX_DIV_2 -200, 300), 400, 20)
    #     # self.add_menu('initial setup', (MAXX_DIV_2 -200, 300), 400, 20, [self.menu_structure['initial setup'][i] for i in self.menu_structure['initial setup'].keys()])
    #
    #     while not self.menu_actions_done:
    #     # while self.menu_action_pending == '':
    #         self.processing_human_input()
    #         self.processing_menu_items()
    #         self.render_background()
    #         self.render_menu_items()
    #         self.render_debug_info()
    #         pygame.display.flip()
    #     self.reset_human_input()
    #     self.reset_menu()
    #
    #     if self.menu_walk_tree[-1] in ('CANCEL MENU', 'quit'):
    #         pygame.quit()
    #         raise SystemExit()
    #
    #     if 'map single selection' in self.menu_walk_tree:
    #         print(f'[setup] {self.menu_walk_tree=}')
    #         self.location = self.menu_walk_tree[-1]
    #         self.reset_menu_walk_tree()
    #
    #     elif self.menu_walk_tree[-1] == 'new':
    #         self.reset_menu_walk_tree()
    #         # self.menu_action_pending = ''
    #         # print('make new')
    #         # # Setting up the new map:
    #         width = MAXX
    #         height = MAXY
    #         new_location_description = list()
    #         with open('locations.py', 'r') as f:
    #             existing_locations_description = f.readlines()
    #
    #         map_name = str(uuid.uuid1())
    #
    #         # Using the template to build a structure of new map's description:
    #         with open('locations_template.py', 'r') as template_source:
    #             for line in template_source:
    #                 if 'new_map_name' in line:
    #                     new_line = '    \'' + map_name + '\':\n'
    #                     new_location_description.append(new_line)
    #                 elif 'new_map_size' in line:
    #                     new_line = '            \'size\': (' + str(width) + ', ' + str(height) + '), \n'
    #                     new_location_description.append(new_line)
    #                 else:
    #                     new_location_description.append(line)
    #
    #         # Insert the new map description into the existing locations.py file:
    #         for line in existing_locations_description:
    #             if 'locations = {' in line:
    #                 line_index = existing_locations_description.index(line) + 1
    #                 for new_line in new_location_description:
    #                     existing_locations_description.insert(line_index, new_line)
    #                     line_index += 1
    #                 break
    #
    #         with open('locations.py', 'w') as f_dest:
    #             f_dest.writelines(existing_locations_description)
    #
    #         self.location = map_name

    def reset_human_input(self):
        self.is_mouse_button_down = False
        self.is_left_mouse_button_down = False
        self.is_right_mouse_button_down = False
        self.is_mouse_wheel_down = False
        self.is_mouse_wheel_up = False
        self.is_mouse_wheel_rolls = False

    def rename_map(self, new_name):
        # Read source:
        source = list()
        with open('locations.py', 'r') as f:
            for line in f:
                source.append(line)

        # Rename all signs of previous map name:
        for line in source:
            if self.location in line:
                split_line = line.split(self.location)
                new_line  = split_line[0] + new_name + split_line[1]
                source[source.index(line)] = new_line

                # for line in source:
        #     if '    \'' + self.location + '\':' in line:
        #         print(f'[rename map] {line=}')
                # source[source.index(line)] = '    \'' + new_name + '\':\n'

        # Rewrite corrected map description:
        with open('locations.py', 'w') as f:
            for line in source:
                f.write(line)

        # Rename files linked with this map name:
        file_list = listdir('img/backgrounds')
        for l in file_list:
            if self.location in l:
                file_suffix = l.split('_')[-1]
                move('img/backgrounds/' + l, 'img/backgrounds/' + new_name + '_' + file_suffix)

        self.location = new_name
        self.need_to_load = True


    def main_menu(self):

        # for i in self.menu_structure['main menu'].keys():
        #     item = self.menu_structure['main menu'][i]
        #     self.add_menu_item(item)
        # #    self.add_menu_item(item['rectangle'], item['label'], item['LMB action'], item['active'], item['on hover action'])
        self.add_menu({'submenu name': 'main menu', 'value': ''}, (MAXX_DIV_2 - 200, 300), 400, 20)
        # self.add_menu('main menu', (MAXX_DIV_2 - 200, 300), 400, 20)
        background = self.screen.convert_alpha()
        # self.dim()
        while not self.menu_actions_done:
        # while self.menu_action_pending == '':
            self.processing_human_input()
            self.processing_menu_items()
            self.render_background(background)
            self.dim()
            self.render_menu_items()
            self.render_debug_info()
            pygame.display.flip()
        self.reset_human_input()
        # self.reset_menu()
        print(f'[main menu] {self.menu_walk_tree=} {self.menu_return_value=}')

        if self.menu_walk_tree[-1] == 'CANCEL MENU':
            if not self.location:
                pygame.quit()
                raise SystemExit
            self.reset_menu_walk_tree()
            self.reset_menu()
            self.reset_human_input()
            return
        else:
            if 'map single selection' in self.menu_walk_tree:
                self.location = self.menu_return_value
                self.need_to_load = True
                self.reset_menu_walk_tree()
                self.reset_menu()
                return

            # if self.menu_walk_tree[-1] == 'save':
            #     self.reset_menu_walk_tree()
            #     self.save()
            if self.menu_return_value == 'new':
                self.reset_menu_walk_tree()
                self.reset_menu()
                # self.menu_action_pending = ''
                print('make new map')
                # # Setting up the new map:
                # width = self.camera.max_x
                width = MAXX
                # height = self.camera.max_y
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
                self.need_to_load = True
            # elif self.menu_walk_tree[-1] == 'load':
            #     print(f'[main menu] {self.menu_walk_tree=}')
            #     self.location = self.menu_walk_tree[-1]
            #     self.need_to_load = True
            #     self.reset_menu_walk_tree()
            #     return
            # elif self.menu_walk_tree[-1] == 'quit':
            #     pygame.quit()
            #     raise SystemExit()
            # elif self.menu_return_value == 'resize':
            #     self.reset_menu_walk_tree()
            #     # self.menu_action_pending = ''
            #     x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')
            #     y = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')
            #     self.camera.setup(int(x), int(y))
            #     self.create_snap_mesh()
            else:
                self.reset_menu_walk_tree()
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
                if event.key == K_F1:
                    self.show_debug_info = False if self.show_debug_info else True
                if event.key == K_F3:
                    self.need_to_load = True
                if event.key == K_F2:
                    self.save()
                if event.key == K_m:
                    self.show_minimap = False if self.show_minimap else True
                    if self.show_minimap:
                        self.refresh_minimap()
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
        # entity.is_move_right = True if 'move right' in description else False
        # entity.is_move_up = True if 'move up' in description else False
        # entity.is_move_down = True if 'move down' in description else False
        # entity.is_move_left = True if 'move left' in description else False
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
        for key in menu_item.keys():
            # if type(menu_item[key]) == str:
            #     if menu_item[key][0] == '*':
            #         menu_item[key] = eval(menu_item[key][1:])
            #     elif menu_item[key][0] == '@':
            #         # '@' this is the sign of executability of all code which remains after this sign.
            #         menu_item[key] = exec(menu_item[key][1:])
            self.menu_items[self.active_menu_pile][self.menu_item_id][key] = menu_item[key]

        # self.menu_items[self.active_menu_pile][self.menu_item_id]['text'] = menu_item['label']
        # self.menu_items[self.active_menu_pile][self.menu_item_id]['LMB action'] = menu_item['LMB action']
        # self.menu_items[self.active_menu_pile][self.menu_item_id]['active'] = menu_item['active']  # Menu item responses on human input.
        # self.menu_items[self.active_menu_pile][self.menu_item_id]['rectangle'] = menu_item['rectangle']
        # self.menu_items[self.active_menu_pile][self.menu_item_id]['on hover action'] = menu_item['on hover action']  # Activate a command of this menu item just only if mouse cursor hovers over it.
        # self.menu_items[self.active_menu_pile][self.menu_item_id]['after action'] = menu_item['after action']  #

        self.menu_item_id += 1


    def add_menu(self, parent_menu_item, top_left_corner, width, font_size):
        self.menu_item_id = 0
        if 'menu pile' in parent_menu_item.keys():
            self.menu_pile_id = parent_menu_item['menu pile'] + 1
        else:
            self.menu_pile_id += 1
        self.active_menu_pile = self.menu_pile_id

        restricted = ('generate list from', 'predefined keys','target object', 'rect')

        menu_name = parent_menu_item['submenu name']
        # print(f'[add_menu] Start adding new menu: {menu_name=}, pile: {self.menu_pile_id}')
        # print(f'[add_menu] parent items: {parent_menu_item.keys()}')

        # Need to set 'target' value for all elements of the newborn menu from 'value' of the parent.
        # All the actions will aim this object after new menu has done:
        target = parent_menu_item['value']
        # print(f'[add_menu] target: {target}')

        #
        if 'self dict key' in parent_menu_item.keys():
            parent_dict_key = parent_menu_item['self dict key']
        else:
            parent_dict_key = ''

        #
        if 'menu pile' in parent_menu_item.keys():
            parent_menu_pile = parent_menu_item['menu pile']
        else:
            parent_menu_pile = 0

        if 'submenu after action' in parent_menu_item.keys():
            after_action = parent_menu_item['submenu after action']
        else:
            after_action = None

        # Set the deed which will be performed after the newborn menu has done:
        if 'submenu exit action' in parent_menu_item.keys():
            exit_action = parent_menu_item['submenu exit action']
        else:
            # If particular action doesn't described, set it to default value:
            exit_action = 'return value'
        # print(f'[add_menu] {exit_action=}')

        # Add current new menu name to common global store:
        if menu_name not in self.menu_walk_tree:
                self.menu_walk_tree.append(menu_name)

        # Let's generate a list of new menu items from the given text-type description of sequence, if needed:
        if 'generate list from' in self.menu_structure[menu_name].keys():
            self.generate_menu(menu_name)

        # All the items of the newborn menu:
        items = self.menu_structure[menu_name].keys()

        # Calculate geometry routines:
        if top_left_corner[0] + width > MAXX:
            start_x = MAXX - width
        else:
            start_x = top_left_corner[0]

        dy = 0
        height = font_size + 16
        total_menu_height = height * len([i for i in items if i not in restricted])
        if top_left_corner[1] + total_menu_height > MAXY:
            start_y = MAXY - height
        else:
            start_y = top_left_corner[1] + total_menu_height - height


        # Main cycle of menu items add:
        for i in reversed(items):
            if i in restricted:
                continue
            # print(i)
            item =  self.menu_structure[menu_name][i]
            item['menu pile'] = self.menu_pile_id
            item['parent menu pile'] = parent_menu_pile
            item['parent dict key'] = parent_dict_key
            if after_action:
                item['after action'] = after_action
            # item['submenu actions done'] = False
            item['rectangle'] = pygame.Rect(start_x, start_y - dy, width, height)
            # item['rectangle'] = pygame.Rect(top_left_corner[0], start_y - dy, width, height)
            if 'target' not in item.keys() or not item['target']:
                # print(f'[add_menu] try to set {target=} for {menu_name=}')
                item['target'] = target
            if 'LMB action' not in item.keys() or not item['LMB action']:
                item['LMB action'] = exit_action
            if 'colors' in item.keys():
                self.add_menu_item(item, item['colors']['frame color'], item['colors']['bg color'], item['colors']['txt color'])
            self.add_menu_item(item)
            dy += height

        self.menu_items[self.active_menu_pile][0]['menu rect'] = pygame.Rect(start_x, start_y, width, total_menu_height)
        # self.menu_items[self.active_menu_pile][0]['menu rect'] = pygame.Rect(top_left_corner[0], start_y, width, total_menu_height)

        # print(f'[add_menu] Added new menu: {menu_name}')
        # for k in self.menu_structure[menu_name].keys():
        #     # subm_keys = self.menu_structure[menu_name][k].keys()
        #     # v = self.menu_structure[menu_name][k]['value']
        #     # t = self.menu_structure[menu_name][k]['target']
        #     print(f'[add_menu] submenu: {k} ')
        #     # for i in subm_keys:
        #     #     print(f'[add_menu] submenu: {k}, item: {i} ')
        # print(f'[add_menu] ----------')

    def create_text_input(self, xy, prompt, default_value, input_type='str'):
        txt_surf = fonts.all_fonts[self.default_font_size].render(prompt, True, WHITE, DARKGRAY)
        back_color = GRAY

        window_height = txt_surf.get_height() + 20
        window_width = txt_surf.get_width() + 20
        # window_width_inflate = 20
        # text_to_return_list = list()
        text_to_return_str = str()
        text_to_return_surf = fonts.all_fonts[self.default_font_size].render(text_to_return_str, True, WHITE, DARKGRAY)
        window_width_inflate = text_to_return_surf.get_width() + 20

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
                    print(f'[create text input] key pressed: {k}')
                    if event.key == K_ESCAPE:
                        return default_value
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        if input_type == 'int':
                            print(f'[create text input] returning value: {text_to_return_str}')
                            return int(text_to_return_str)
                        elif input_type == 'float':
                            print(f'[create text input] returning value: {text_to_return_str}')
                            return float(text_to_return_str)
                        elif input_type == 'str' or input_type == 'any':
                            print(f'[create text input] returning value: {text_to_return_str}')
                            return text_to_return_str
                    if event.key == K_BACKSPACE:
                        if len(text_to_return_str) > 0:
                            text_to_return_str = text_to_return_str[0:-1]
                            break
                    if input_type == 'int':
                        if k in DIGITS:
                            if k[0] == '[':
                                text_to_return_str += k[1]
                            else:
                                text_to_return_str += k
                                # text_to_return_str += pygame.key.name(event.key)
                    elif input_type == 'float':
                        if k in DIGITS or k in ('.', '[.]'):
                            if k[0] == '[':
                                text_to_return_str += k[1]
                            else:
                                text_to_return_str += k
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
        self.menu_structure = dict()
        self.menu_structure = deepcopy(menu_structure)
        # LOADING GRAPHICAL TILES:
        if not self.tiles:
            start_x = 0
            start_y = 0
            tile_width = 96
            tile_height = 96
            tiles_x_gap = 0
            tiles_y_gap = 0
            # start_x = 0
            # start_y = 48
            # tile_width = 96
            # tile_height = 192
            # tiles_x_gap = 0
            # tiles_y_gap = 48
            tile_set = pygame.image.load('img/backgrounds/tiles/tileset_1.png')
            sz = tile_set.get_size()
            tile_number = 0
            for x in range (start_x, sz[0], tile_width + tiles_x_gap):
                for y in range (start_y, sz[1], tile_height + tiles_y_gap):
                    self.tiles[tile_number] = tile_set.subsurface((x,y,tile_width,tile_height))
                    tile_number += 1

        # LOADING MAP OBJECTS:
        self.obstacles[self.location] = dict()

        # LOADING OBSTACLE RECTANGLES
        max_obs_id = 0
        for obs in locations.locations[self.location]['obstacles']['obs rectangles']:
            self.add_obstacle(obs)
            if max_obs_id < obs[-1]:  #((350, 850), (1600, 150), 2),
                max_obs_id = obs[-1]
        self.obstacle_id = max_obs_id + 1

        # LOADING ACTIVE OBSTACLE SETTINGS
        self.obs_settings = locations.locations[self.location]['obstacles']['settings']
        for active_obs_id in self.obs_settings.keys():
            if active_obs_id in self.obstacles[self.location].keys():
                self.obstacles[self.location][active_obs_id].active_flag = True

        # LOADING ENEMIES
        self.enemies = dict()
        for enemy_xy in locations.locations[self.location]['hostiles']:
            self.enemies[enemy_xy] = dict()
            enemy_description = locations.locations[self.location]['hostiles'][enemy_xy]
            enemy_to_add = copy(all_hostiles[enemy_description['name']])  # Create a copy of enemy
            for k in enemy_description.keys():
                if k == 'name':
                    continue
                if k in enemy_to_add.keys():
                    enemy_to_add[k] = enemy_description[k]

            self.enemies[enemy_xy]['name'] = enemy_to_add['name']
            self.enemies[enemy_xy]['height'] = enemy_to_add['height']
            self.enemies[enemy_xy]['width'] = enemy_to_add['width']
            self.enemies[enemy_xy]['health'] = enemy_to_add['health']
            self.enemies[enemy_xy]['max speed'] = enemy_to_add['max speed']

        # for dem in locations[self.location]['demolishers']['dem rectangles']:
        #     self.add_demolisher(dem)
        self.global_offset_xy = [MAXX_DIV_2, MAXY_DIV_2]
        self.camera.setup(locations.locations[self.location]['size'][0], locations.locations[self.location]['size'][1])
        self.create_snap_mesh()

        # self.refresh_minimap()
        # self.export_screen('_minimap')
        # self.minimap = pygame.image.load('img/' + self.location + '_minimap.png')
        # self.minimap_zoomed_out = pygame.transform.scale(self.minimap, (self.minimap.get_width() // 4,
        #                                                                 self.minimap.get_height() // 4))

    def save(self):
        # Saving with pickle:
        # with open('locations_'+self.location+'.dat', 'wb') as f:
        #     pickle.dump(self.obstacles[self.location], f)
        # for obs_id in self.obs_settings.keys():
        #     g = self.obs_settings[obs_id]['ghost']
        #     print(f'[save()] {obs_id=} \'ghost\': {g}')

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
        obstacle_settings_list = self.menu_structure['_template_obs_settings_']
        # from templates import obstacle_settings_list

        enemies = list()
        for xy in self.enemies.keys():
            e = self.enemies[xy]
            total_strg = '\n            	' + str(xy) + ': {\n'
            # total_strg = '\n            	' + str(xy) + ': {\n' + \
                         # '                    ' + 'name: ' + e['name'] + ',\n'
            for k in e.keys():
            # for k in loc[self.location]['hostiles'][xy].keys():
            #     if loc[self.location]['hostiles'][xy][k] != e[k]:
                var = str(e[k]) if type(e[k]) != str else '\'' + e[k] + '\''
                total_strg += '                    \'' + str(k) + '\': ' + var + ',\n'
            total_strg += '            	' + '},\n'

            enemies.append(total_strg)
        # print(enemies)
        # exit()
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

        # for k in loc[self.location]['obstacles']['settings'].keys():
        #     print('[save()]', k, loc[self.location]['obstacles']['settings'][k])

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
                # HOSTILES:
                if k == self.location:
                    # Save hostiles which were edited right now.
                    for h in enemies:
                        f.write(h)
                else:
                    # Keep hostile unchanged.
                    for e_xy in loc[k]['hostiles'].keys():
                        enemy = loc[k]['hostiles'][e_xy]
                        f.write('\n            	' + str(e_xy) + ': {\n')
                        for enemy_k in enemy.keys():
                            # Add a single quote if type is string.
                            var = str(enemy[enemy_k]) if type(enemy[enemy_k]) != str else '\'' + enemy[enemy_k] + '\''
                            f.write('                    \'' + str(enemy_k) + '\': ' + var + ',\n')
                        f.write('\n              },')
                f.write('\n              },')
                f.write('\n            \'demolishers\': {')

                # DEMOLISHERS:
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
                            if i in l.keys():
                                f.write('\n                        \'' + i + '\': ' + str(l[i]) + ',')
                        f.write('\n                  },')

                # Closing tails:
                f.write('\n                  } # OBSTACLE SETTINGS SECTION END')
                f.write('\n              },')
                f.write('\n            \'items\': {' +  '},')
                f.write('\n    },')
            f.write('\n}')

    # def save_back(self):
    #     # Saving with pickle:
    #     # with open('locations_'+self.location+'.dat', 'wb') as f:
    #     #     pickle.dump(self.obstacles[self.location], f)
    #
    #     # Saving using JSON:
    #     # obs_geometry = list()
    #
    #     obs_rects = list()
    #     for k in self.obstacles[self.location].keys():
    #         obs = self.obstacles[self.location][k]
    #         total_strg = '                ' + \
    #                      '(' + \
    #                      str(obs.rectangle.topleft) + ', ' + \
    #                      str(obs.rectangle.size) + \
    #                      ', ' + str(k) + '),  #' + str(k) + '\n'
    #         obs_rects.append(total_strg)
    #
    #     dem_rects = list()
    #     if self.location in self.demolishers:
    #         for k in self.demolishers[self.location].keys():
    #             dem = self.demolishers[self.location][k]
    #             total_strg = '                ' + \
    #                    '(' + \
    #                    str(dem.rectangle.topleft) + ', ' + \
    #                    str(dem.rectangle.size) + ', ' + str(k) + \
    #                    '),  #' + str(k) + '\n'
    #             dem_rects.append(total_strg)
    #
    #     settings_list = list()
    #
    #     # print(obs_rects)
    #     # print(dem_rects)
    #     # exit()
    #     # ['                ((100, 950), (1550, 50), 0),  #0\n',
    #     #  '                ((1300, 500), (300, 250), 1),  #1\n',
    #     #  '                ((950, 350), (100, 150), 2),  #2\n',
    #     #  '                ((650, 300), (200, 200), 3),  #3\n']
    #
    #     # ['                ((550, 750), (200, 200), 0),  #0\n']
    #     # new_location_description = list()
    #     with open('locations.py', 'r') as f:
    #         existing_locations_description = f.readlines()
    #
    #     print(f'Start searching {self.location} to remove obsolete rectangles...')
    #     loc_found = False
    #     lines_counter = 0
    #     for line in existing_locations_description:
    #         if '\'' + self.location + '\':' in line and not loc_found:
    #             print(f'Location {self.location} found.')
    #             loc_found = True
    #
    #         if loc_found:
    #             if '\'obs rectangles\':' in line:
    #                 # Now need to delete all obsolete information about rectangles:
    #                 start_index_to_delete = lines_counter + 1
    #                 # start_index_to_delete = existing_locations_description.index(line) + 1
    #                 print(f'Start index to delete records: {start_index_to_delete}')
    #             elif 'OBSTACLE RECTANGLES SECTION END' in line:
    #                 end_index_to_delete = lines_counter
    #                 # end_index_to_delete = existing_locations_description.index(line)
    #                 print(f'Ending index to delete records: {end_index_to_delete}. Abort search.')
    #                 break
    #         lines_counter += 1
    #
    #     if loc_found:
    #         del existing_locations_description[start_index_to_delete:end_index_to_delete]
    #
    #     loc_found = False
    #     with open('locations.py', 'w') as f_dest:
    #         for line in existing_locations_description:
    #             f_dest.write(line)
    #             if loc_found:
    #                 if '\'obs rectangles\':' in line:
    #                     for obs_rect_line in obs_rects:
    #                         f_dest.write(obs_rect_line)
    #                     loc_found = False
    #
    #                 if '\'dem rectangles\':' in line:
    #                     for dem_rect_line in dem_rects:
    #                         f_dest.write(dem_rect_line)
    #                     # loc_found = False
    #
    #             if '\''+self.location+'\':' in line and not loc_found:
    #                 # print('Location found!')
    #                 loc_found = True
    #     # f_dest.close()
    #
    #     self.allow_import_locations = True

    def render_background(self, surf=None):
        if surf:
            self.screen.blit(surf, (0, 0))
        else:
            pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_enemies(self):
        for enemy_xy in self.enemies.keys():
            e = self.enemies[enemy_xy]
            # e_reference = copy(all_hostiles[e['name']])
            pygame.draw.rect(self.screen, DARK_ORANGE,
                             (self.zoom_factor * (enemy_xy[0] - self.camera.offset_x),
                              self.zoom_factor * (enemy_xy[1] - self.camera.offset_y),
                              self.zoom_factor * e['width'],
                              self.zoom_factor * e['height']))

    def refresh_minimap(self):
        self.export_screen('_minimap')
        self.minimap = pygame.image.load('img/backgrounds/' + self.location + '_minimap.png')
        self.minimap_zoomed_out = pygame.transform.scale(self.minimap, (self.minimap.get_width() // 5,
                                                                        self.minimap.get_height() // 5))

    def render_minimap(self):
        sz = self.minimap_zoomed_out.get_size()
        self.screen.blit(self.minimap_zoomed_out, (0, MAXY - sz[1]))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            color = GREEN if obs.active_flag else WHITE
            pygame.draw.rect(self.screen, color, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x),
                                                  self.zoom_factor * (obs.rectangle.y - self.camera.offset_y),
                                                  self.zoom_factor * obs.rectangle.width,
                                                  self.zoom_factor * obs.rectangle.height))
            border_color = RED if self.selected_obs_id == obs.id else BLUE
            border_thickness = 5 if self.selected_obs_id == obs.id else 1
            pygame.draw.rect(self.screen, border_color, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x),
                                                  self.zoom_factor * (obs.rectangle.y - self.camera.offset_y),
                                                  self.zoom_factor * obs.rectangle.width,
                                                  self.zoom_factor * obs.rectangle.height), border_thickness)
            # if obs.id in self.obs_settings.keys():
            #     s = fonts.font15.render(str(obs.id)+' Ghst:'+str(self.obs_settings[obs.id]['ghost']), True, GREEN)
            # else:
            #     s = fonts.font20.render(str(obs.id), True, GREEN)
            # font_sz = int(20 * self.zoom_factor)
            # s = fonts.all_fonts[].render(str(obs.id) + ' ' + str(self.zoom_factor), True, RED)
            s = fonts.font25.render(str(obs.id), True, RED)
            self.screen.blit(pygame.transform.scale(s, (s.get_width() * self.zoom_factor, s.get_height() * self.zoom_factor)), (self.zoom_factor * (obs.rectangle.centerx - s.get_width() // 2 - self.camera.offset_x + 2),
                                 self.zoom_factor * (obs.rectangle.centery - s.get_height() // 2 - self.camera.offset_y + 2)))

    def export_screen(self, filename='_ground', just_obs_contour=False):
        filename = 'img/backgrounds/' + self.location + filename + '.png'
        surf = pygame.Surface((self.camera.max_x, self.camera.max_y)).convert_alpha()
        # surf.set_colorkey(MAGENTA)
        surf.fill(MAGENTA)
        # pygame.draw.rect(surf, BLACK, (0,0,self.camera.max_x, self.camera.max_y))
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            elevation = 0
            # color = GREEN if obs.active_flag else WHITE
            if just_obs_contour:
                pygame.draw.rect(surf, WHITE, (obs.rectangle.x, obs.rectangle.y, obs.rectangle.width, obs.rectangle.height))
            else:
                if key in self.obs_settings.keys():
                    if self.obs_settings[key]['invisible']:
                        continue
                    if 'sprite' in self.obs_settings[key].keys():
                        if self.obs_settings[key]['sprite elevated']:
                            # Elevated obstacle sprite should be at 0.5 higher than the obstacle's rectangle top,
                            # and it should be drowned into the lower obstacle at 0.5 of its height.
                            # Finally, the additional 0.5 of sprite height is dedicated to drop shadow.
                            elevation = int(self.default_snap_mesh_size * 1.5)
                        # Create a surface which corresponds the size of current obstacle representation:
                        obs_surf = pygame.Surface((obs.rectangle.width, obs.rectangle.height + elevation)).convert_alpha()

                        # Extract a sprite and scale it to fit default mesh dimension:
                        sz = self.tiles[self.obs_settings[key]['sprite']].get_size()
                        scale_ratio = self.default_snap_mesh_size / sz[0]
                        sprite = pygame.transform.scale(self.tiles[self.obs_settings[key]['sprite']], (sz[0] * scale_ratio, sz[1] * scale_ratio))

                        # Get size of the new scaled sprite:
                        sz = sprite.get_size()

                        # Fill obstacle's sprite up with corresponding tile:
                        for y in range(0, obs.rectangle.h + elevation, sz[1]):
                            for x in range(0, obs.rectangle.w, sz[0]):
                                obs_surf.blit(sprite, (x,y))

                        # Draw shadow in the very bottom, under the elevated sprite:
                        if elevation != 0:
                            color_alpha = 255
                            for dy in range(obs_surf.get_height() - int(elevation * 0.35), obs_surf.get_height(), 1):
                                pygame.draw.rect(obs_surf, (0,0,0,color_alpha), (0,dy, obs.rectangle.w,1))
                                color_alpha -= 10
                                if color_alpha < 0:
                                    break

                        # Final render of obstacle over the main surface:
                        surf.blit(obs_surf, (obs.rectangle.x, obs.rectangle.y - int(elevation * 0.35)))

                    else:
                        pygame.draw.rect(surf, WHITE, (obs.rectangle.x, obs.rectangle.y, obs.rectangle.width, obs.rectangle.height))
                else:
                    pygame.draw.rect(surf, WHITE, (obs.rectangle.x, obs.rectangle.y, obs.rectangle.width, obs.rectangle.height))
                # pygame.draw.rect(surf, WHITE, (obs.rectangle.x, obs.rectangle.y, obs.rectangle.width, obs.rectangle.height), 1)  # Debugging border
        # copy_surf = pygame.Surface((self.camera.max_x, self.camera.max_y)).convert_alpha()
        # copy_surf.set_colorkey(MAGENTA)
        # copy_surf.blit(surf, (0, 0))
        # pygame.image.save(copy_surf, filename)
        pygame.image.save(surf, filename)

    def render_obstacle_properties(self, obs_id):
        if obs_id not in self.obs_settings.keys():
            return
        obs = self.obstacles[self.location][obs_id]
        settings = self.obs_settings[obs_id]
        gap = 1
        font_size = 15
        params = (
            ('ACTIONS: ' + str(settings['actions']), BLACK) if settings['actions'] else None,
            # ('ACTIONS: ' + str([settings['actions'][0][k] for k in settings['actions'][0]]), BLACK),
            ('ACTORS PASS THROUGH: ' + str(settings['actors pass through']), BLACK) if settings['actors pass through'] else None,
            ('SPEED: ' + str(settings['speed']), BLACK),
            ('COLLIDES: ' + str(settings['collideable']), BLACK) if settings['collideable'] else None,
            ('GRAVITY: ' + str(settings['gravity affected']), BLACK) if settings['gravity affected'] else None,
            ('INVISIBLE: ' + str(settings['invisible']), BLACK) if settings['invisible'] else None,
            ('TELEPORT: ' + str(settings['teleport']), BLACK) if settings['teleport'] else None,
            ('TELEPORT TO: ' + str(settings['teleport description']['new location']), BLACK) if settings['teleport'] else None,
            ('TELEPORT POINT: ' + str(settings['teleport description']['xy']), BLACK) if settings['teleport'] else None,
            ('TRIGGER: ' + str(settings['trigger']), BLACK) if settings['trigger'] else None,
            ('IT MAKES ACTIVE: ' + str(settings['trigger description']['make active']), BLACK) if settings['trigger'] else None,
            ('DISAPPEARS: ' + str(settings['trigger description']['disappear']), BLACK) if settings['trigger'] else None,
        )
        rendered_params = list()
        max_width = 0
        for p in params:
            if not p:
                continue
            s = fonts.all_fonts[font_size].render(p[0], True, p[1], GRAY)
            if s.get_width() > max_width:
                max_width = s.get_width()
            rendered_params.append(s)

        max_height = rendered_params[0].get_height() * len(rendered_params) + len(rendered_params)
        stats_x = self.mouse_xy[0] if self.mouse_xy[0] < MAXX - max_width else MAXX - max_width
        stats_y = self.mouse_xy[1] if self.mouse_xy[1] < MAXY - max_height else MAXY - max_height

        pygame.draw.rect(self.screen, BLUE, (stats_x, stats_y, max_width,max_height))

        for p in rendered_params:
            self.screen.blit(p,(stats_x, stats_y + gap))
            gap += font_size

        if 'sprite' in settings:
            self.screen.blit(self.tiles[settings['sprite']], (stats_x + max_width, stats_y))

    def render_obstacle_properties_old(self, obs_id):
        if obs_id not in self.obs_settings.keys():
            return
        obs = self.obstacles[self.location][obs_id]
        settings = self.obs_settings[obs_id]
        gap = 1
        font_size = 15
        params = (
            ('ACTIONS: ' + str(settings['actions']), BLACK) if settings['actions'] else None,
            # ('ACTIONS: ' + str([settings['actions'][0][k] for k in settings['actions'][0]]), BLACK),
            ('ACTORS PASS THROUGH: ' + str(settings['actors pass through']), BLACK) if settings['actors pass through'] else None,
            ('SPEED: ' + str(settings['speed']), BLACK),
            ('COLLIDES: ' + str(settings['collideable']), BLACK) if settings['collideable'] else None,
            ('GRAVITY: ' + str(settings['gravity affected']), BLACK) if settings['gravity affected'] else None,
            ('INVISIBLE: ' + str(settings['invisible']), BLACK) if settings['invisible'] else None,
            ('TELEPORT: ' + str(settings['teleport']), BLACK) if settings['teleport'] else None,
            ('TELEPORT TO: ' + str(settings['teleport description']['new location']), BLACK) if settings['teleport'] else None,
            ('TELEPORT POINT: ' + str(settings['teleport description']['xy']), BLACK) if settings['teleport'] else None,
            ('TRIGGER: ' + str(settings['trigger']), BLACK) if settings['trigger'] else None,
            ('IT MAKES ACTIVE: ' + str(settings['trigger description']['make active']), BLACK) if settings['trigger'] else None,
            ('DISAPPEARS: ' + str(settings['trigger description']['disappear']), BLACK) if settings['trigger'] else None,
        )
        rendered_params = list()
        max_width = 0
        for p in params:
            if not p:
                continue
            s = fonts.all_fonts[font_size].render(p[0], True, p[1], GRAY)
            if s.get_width() > max_width:
                max_width = s.get_width() * self.zoom_factor
            rendered_params.append(s)

        max_height = (rendered_params[0].get_height() * len(rendered_params) + len(rendered_params)) * self.zoom_factor
        stats_x = obs.rectangle.centerx - max_width // 2
        if stats_x < self.camera.rectangle.left:
            stats_x = self.camera.rectangle.left
        else:
            if stats_x + max_width > self.camera.rectangle.right:
                stats_x = self.camera.rectangle.right - max_width

        stats_y = obs.rectangle.centery - max_height // 2
        if stats_y < self.camera.rectangle.top:
            stats_y = self.camera.rectangle.top
        else:
            if stats_y + max_height > self.camera.rectangle.bottom:
                stats_y = self.camera.rectangle.bottom - max_height
        # stats_x = obs.rectangle.centerx - max_width // 2
        # if stats_x < self.camera.rectangle.left:
        #     stats_x = self.camera.rectangle.left
        # else:
        #     if stats_x + max_width > self.camera.rectangle.right:
        #         stats_x = self.camera.rectangle.right - max_width
        #
        # stats_y = obs.rectangle.centery * self.zoom_factor - max_height // 2
        # if stats_y < self.camera.rectangle.top * self.zoom_factor:
        #     stats_y = self.camera.rectangle.top * self.zoom_factor
        # else:
        #     if stats_y + max_height > self.camera.rectangle.bottom * self.zoom_factor:
        #         stats_y = self.camera.rectangle.bottom * self.zoom_factor - max_height

        pygame.draw.rect(self.screen, BLUE, (self.zoom_factor * (stats_x - self.camera.offset_x),
                                             self.zoom_factor * (stats_y - self.camera.offset_y),
                                             max_width,
                                             max_height))

        for p in rendered_params:
            self.screen.blit(pygame.transform.scale(p, (p.get_width() * self.zoom_factor, p.get_height() * self.zoom_factor)),
                             (self.zoom_factor * (stats_x - self.camera.offset_x),
                              self.zoom_factor * (stats_y - self.camera.offset_y + gap)))
            gap += font_size

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

                    # if 'target' in menu_item.keys():
                    #     add_txt = ' TARGET: ' + str(menu_item['target'])
                    # else:
                    #     add_txt = ' (no target)'
                    # s = fonts.font15.render(str(menu_item['label']) + add_txt, True, txt_color)

                    s = fonts.font15.render(str(menu_item['label']), True, txt_color)
                    self.screen.blit(s, (menu_item['rectangle'].centerx - s.get_size()[0] // 2, menu_item['rectangle'].centery - s.get_size()[1] // 2))

                    # Render additional info about the menu item:
                    if 'additional info' in menu_item.keys():
                        if menu_item['additional info'][0] == '^':
                            # Link to a pure graphic object, not text.
                            # print('[render menu]', menu_item['additional info'])
                            s = eval(menu_item['additional info'][1:])
                            add_box_text_color = WHITE
                            add_box_background_color = DARKGRAY
                            sz = s.get_size()
                            start_y = 0
                        elif menu_item['additional info'][0] == '*':
                            # Link to an object, which must be converted to text info:
                            info = eval(menu_item['additional info'][1:])
                            if type(info) == bool and info:
                                add_box_text_color = BLUE
                                add_box_background_color = WHITE
                            else:
                                add_box_text_color = WHITE
                                add_box_background_color = DARKGRAY
                            s = fonts.font12.render(str(info), True, add_box_text_color)
                            sz = s.get_size()
                            start_y = menu_item['rectangle'].h // 2 - sz[1] //2
                        else:
                            # Just a pure text, no need to convert it:
                            info = menu_item['additional info']
                            if 'True' in info:
                                add_box_text_color = BLUE
                                add_box_background_color = WHITE
                            else:
                                add_box_text_color = WHITE
                                add_box_background_color = DARKGRAY
                            s = fonts.font12.render(str(info), True, WHITE)
                            sz = s.get_size()
                            start_y = menu_item['rectangle'].h // 2 - sz[1] //2

                        add_box_width = 100

                        if menu_item['rectangle'].right + add_box_width > MAXX:
                            add_box_x = menu_item['rectangle'].left - add_box_width - 1
                        else:
                            add_box_x = menu_item['rectangle'].right + 1

                        add_screen = pygame.Surface((add_box_width, menu_item['rectangle'].h))
                        add_screen.fill(add_box_background_color)
                        add_screen.blit(s, (add_box_width // 2 - sz[0] // 2, start_y))
                        self.screen.blit(add_screen, (add_box_x, menu_item['rectangle'].top))

                        # pygame.draw.rect(self.screen, GRAY, (add_box_x, menu_item['rectangle'].y,
                        #                                      add_box_width, menu_item['rectangle'].h), 0)
                        # self.screen.blit(s, (add_box_x + add_box_width // 2 - sz[0] // 2,
                        #                      menu_item['rectangle'].centery - sz[1] // 2))

                        if menu_item['hovered']:
                            if self.mouse_xy[0] + sz[0]//2 + 2 > MAXX:
                                hover_box_x = MAXX - sz[0]
                            elif self.mouse_xy[0] - sz[0] //2 - 2 < 0:
                                hover_box_x = 0
                            else:
                                hover_box_x = self.mouse_xy[0] - sz[0] //2 - 8

                            hover_box_y = self.mouse_xy[1] - sz[1] - 1
                            pygame.draw.rect(self.screen, add_box_background_color, (hover_box_x, hover_box_y,
                                                                 sz[0] + 4, sz[1] + 2), 0)
                            self.screen.blit(s, (hover_box_x + 2, hover_box_y + 1))

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

                    s = fonts.font15.render(str(menu_item['label']) + ' (PILE: ' + str(pile_id) + ' #' + str(k) + ')', True, txt_color)
                    # s = fonts.font15.render(str(menu_item['text']), True, txt_color)

                    self.screen.blit(s, (menu_item['rectangle'].centerx - s.get_size()[0] // 2, menu_item['rectangle'].centery - s.get_size()[1] // 2))
            # if self.active_menu_pile != pile_id:
            #     # print(self.menu_items[pile_id].keys())
            #     self.dim()

    def dim(self):
        # back = surf.convert_alpha()
        # back.fill(BLACK)
        # back.set_alpha(180)

        self.screen.blit(dim_screen_cover, (0, 0))


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
        if not self.show_debug_info:
            return
        stats_x = 1
        stats_y = 1
        # stripes_width = 500
        gap = 1
        font_size = 18
        # m_hover_item = 'None' if not self.mouse_hovers_item else self.items[self.mouse_hovers_item].name
        # m_hover_actor = 'None' if not self.mouse_hovers_actor else self.wandering_actors[self.mouse_hovers_actor].name + ' ' + str(self.wandering_actors[self.mouse_hovers_actor].id)
        # m_hover_cell = 'None' if self.point_mouse_cursor_shows is None else str(self.locations[self.location]['points'][self.point_mouse_cursor_shows]['rect'].center)
        params = (
            ('SAVE: F2 | LOAD: F3 | W/A/S/D: MOVE CAMERA | [SHIFT] +/- : CHANGE SNAP MESH SCALE | [ ] : change inserting object type | MOUSE WHEEL : ZOOM | M: show minimap | ESC: QUIT', BLUE),

            ('OBJECT TYPE        : ' + str(self.object_types[self.current_object_type]), BLACK),
            ('WORLD SIZE         : ' + str(self.camera.max_x) + ':' + str(self.camera.max_y), BLACK),
            ('MAX OFFSET         : ' + str(self.camera.max_offset_x) + ':' + str(self.camera.max_offset_y), BLACK),
            ('SNAP MESH SCALE    : ' + str(self.snap_mesh_size), BLACK),
            ('OFFSET GLOBAL      : ' + str(self.global_offset_xy), BLACK),
            ('CAMERA INNER OFFSET: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), BLACK),
            ('MOUSE XY           : ' + str(self.mouse_xy_snapped_to_mesh), WHITE),
            ('ZOOM               : ' + str(self.zoom_factor), WHITE),
            ('ACTIVE MENU PILE   : ' + str(self.active_menu_pile), YELLOW),
            ('MENU ACTIONS       : ' + str(self.menu_walk_tree), YELLOW),
            ('MENU return value  : ' + str(self.menu_return_value), YELLOW),
            # ('MENU path          : ' + str(self.menu_path), YELLOW),
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

    def check_mouse_xy_collides_hostile(self):
        for enemy_xy in self.enemies.keys():
            e = self.enemies[enemy_xy]
            rect = pygame.Rect(enemy_xy[0], enemy_xy[1], e['width'], e['height'])
            if rect.collidepoint(self.mouse_xy_global):
                return enemy_xy
        return -1

    def check_mouse_xy_collides_obs(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            if obs.rectangle.collidepoint(self.mouse_xy_global):
                return obs.id
        return -1

    def edit_obs(self, obs):
        # self.menu_action_pending = ''
        self.reset_menu()
        self.reset_menu_walk_tree()
        # Create menu of 'obstacle edit' type, which was predefined in self.menu_structure:
        if obs.id not in self.obs_settings.keys():
            # Fill menu items with default values:
            self.menu_structure['custom obs properties']['ok']['value'] = copy(self.menu_structure['custom obs properties']['reset']['value'])
        else:
            for k in self.obs_settings[obs.id].keys():
                self.menu_structure['custom obs properties']['ok']['value'][k] = self.obs_settings[obs.id][k]
        self.add_menu({'submenu name': 'custom obs properties', 'value': ''}, self.mouse_xy, 400, 15)
        # self.add_menu('custom obs properties', self.mouse_xy, 400, 20)
        # self.add_menu('obstacle edit', self.mouse_xy, 400, 20)
        # self.add_menu(self.mouse_xy, 400, 20, [self.menu_structure['obstacle edit'][i] for i in self.menu_structure['obstacle edit'].keys()])
        background = self.screen.convert_alpha()
        while not self.menu_actions_done:
            self.processing_human_input()
            self.processing_menu_items()
            self.render_background(background)
            self.dim()
            self.render_menu_items()
            self.render_debug_info()
            pygame.display.flip()
        self.reset_human_input()

        if 'CANCEL MENU' in self.menu_walk_tree:
            self.reset_menu_walk_tree()
            self.reset_menu()
            return

        print(f'[edit obs] {self.menu_walk_tree=} {self.menu_return_value=}')
        # exit()
        self.obs_settings[obs.id] = dict()
        self.obs_settings[obs.id] = copy(self.menu_return_value)


        for k in self.obs_settings[obs.id].keys():
            o = self.obs_settings[obs.id][k]
            print(f'[edit_obs] {k}: {o}')

        self.reset_menu_walk_tree()
        self.reset_menu()

        # if 'custom obs properties' in self.menu_walk_tree:
        #     # Menu has returned a dictionary, so obstacle properties edit is done.
        #     self.obs_settings[obs.id] = self.menu_return_value
        #     self.reset_menu_walk_tree()
        #     self.reset_menu()
        #     return
        # elif self.menu_walk_tree[-1] == 'make moving platform':
        #     self.reset_menu_walk_tree()
        #     print('make moving platform')
        #     # self.add_menu(self.mouse_xy, 400, 20, [i for i in self.obs_settings[obs.id].keys()])
        #     # while not self.menu_actions_done:
        #     #     self.processing_human_input()
        #     #     self.processing_menu_items()
        #     #     self.render_background()
        #     #     self.render_menu_items()
        #     #     pygame.display.flip()
        #     # self.reset_human_input()
        #     # self.reset_menu()
        # elif self.menu_walk_tree[-1] == 'custom obs edit done':
        #     summary = list()
        #     for k in self.menu_structure['custom obs properties'].keys():
        #         if obs.id not in self.obs_settings.keys():
        #             self.obs_settings[obs.id] = dict()
        #         if self.menu_structure['custom obs properties'][k]['LMB action'] is not None and \
        #             self.menu_structure['custom obs properties'][k]['LMB action'][0] in \
        #                 ('input number', 'switch state', 'input string'):
        #             for j in self.menu_structure['custom obs properties'][k]['LMB action'][1].keys():
        #                 self.obs_settings[obs.id][j] =  self.menu_structure['custom obs properties'][k]['LMB action'][1][j]
        #
        #     for j in self.obs_settings[obs.id].keys():
        #         print(j, self.obs_settings[obs.id][j])
        #     self.reset_menu_walk_tree()
        # elif self.menu_walk_tree[-1] == 'teleport':
        #     self.reset_menu_walk_tree()
        #     # self.menu_action_pending = ''
        #     print('make teleport')
        # else:
        #     print('make other deed')

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
        # hovered_obs_id = None
        if self.need_to_load:
            return
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

            # offset_x = self.camera.max_offset_x * self.zoom_factor
            # offset_y = self.camera.max_offset_y * self.zoom_factor

            obs_id = self.check_mouse_xy_collides_obs()
            hostile_xy = self.check_mouse_xy_collides_hostile()

            if self.is_spacebar:
                # obs_id = self.check_mouse_xy_collides_obs()
                if obs_id > -1:
                    # Try to delete existing obs:
                    del self.obstacles[self.location][obs_id]
                    if obs_id in self.obs_settings.keys():
                        del self.obs_settings[obs_id]

                if hostile_xy != -1:
                    del self.enemies[hostile_xy]

                if self.show_minimap:
                    self.refresh_minimap()

            # RMB
            if self.is_right_mouse_button_down:
                self.is_right_mouse_button_down = False
                if obs_id > -1:
                    self.edit_obs(self.obstacles[self.location][obs_id])
                    if self.show_minimap:
                        self.refresh_minimap()
                    # return
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

            # LMB
            # if not self.is_left_mouse_button_down:
            #     if obs_id == self.to_be_selected_obs_id > 0:
            #         # LMB was pressed and released while mouse is over an obstacle.
            #         # This obstacle follow the mouse to change self location.
            #         self.selected_obs_id = self.to_be_selected_obs_id
            #         self.to_be_selected_obs_id = -1
            if self.is_left_mouse_button_down:
                # if self.object_types[self.current_object_type] == 'enemy':
                #     world.add_actor(player_jake, (200, 200))
                if self.object_types[self.current_object_type] == 'enemy':
                    self.enemies[self.mouse_xy_snapped_to_mesh] = dict()
                    enemy_to_add = copy(all_hostiles['demon 1'])  # Create a copy of enemy
                    self.enemies[self.mouse_xy_snapped_to_mesh]['name'] = enemy_to_add['name']
                    self.enemies[self.mouse_xy_snapped_to_mesh]['height'] = enemy_to_add['height']
                    self.enemies[self.mouse_xy_snapped_to_mesh]['width'] = enemy_to_add['width']
                    self.enemies[self.mouse_xy_snapped_to_mesh]['health'] = enemy_to_add['health']
                    self.enemies[self.mouse_xy_snapped_to_mesh]['max speed'] = enemy_to_add['max speed']
                    self.is_left_mouse_button_down = False
                    if self.show_minimap:
                        self.refresh_minimap()
                    return

                if self.selected_obs_id > 0:
                    # We've got an already selected obstacle, which following mouse cursor.
                    # Release it.
                    self.is_left_mouse_button_down = False
                    self.selected_obs_id = -1
                    if self.show_minimap:
                        self.refresh_minimap()
                    return
                if obs_id > -1:
                    # Mouse cursor is over an obstacle. We have to mark it as a potential candidate to follow mouse.
                    self.to_be_selected_obs_id = obs_id
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
                        self.to_be_selected_obs_id = -1
                        if self.object_types[self.current_object_type] == 'obstacle':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.obstacle_id)
                            self.obstacle_id += 1
                            self.add_obstacle(description)
                            if self.show_minimap:
                                self.refresh_minimap()
                        elif self.object_types[self.current_object_type] == 'demolisher':
                            description = (self.new_obs_rect.topleft, self.new_obs_rect.size, self.demolishers_id)
                            self.demolishers_id += 1
                            self.add_demolisher(description)
                            if self.show_minimap:
                                self.refresh_minimap()
                    self.new_obs_rect_started = False
                    self.new_obs_rect_start_xy = [0, 0]
                    self.new_obs_rect.update(0,0,0,0)
                    return
                else:
                    if obs_id == self.to_be_selected_obs_id > 0:
                        # LMB was pressed and released while mouse is over an obstacle.
                        # This obstacle follow the mouse to change self location.
                        self.selected_obs_id = self.to_be_selected_obs_id
                        self.to_be_selected_obs_id = -1

            if self.selected_obs_id > 0:
                self.obstacles[self.location][self.selected_obs_id].rectangle.topleft = self.mouse_xy_snapped_to_mesh

            # Update camera viewport:
            if self.is_input_left_arrow:
                self.global_offset_xy[0] -= self.camera_scroll_speed * 10
                # if self.global_offset_xy[0] < MAXX_DIV_2:
                #     self.global_offset_xy[0] = MAXX_DIV_2
            if self.is_input_right_arrow:
                self.global_offset_xy[0] += self.camera_scroll_speed * 10
                # if self.global_offset_xy[0] > MAXX_DIV_2 + offset_x:
                #     self.global_offset_xy[0] = MAXX_DIV_2 + offset_x
            if self.is_input_down_arrow:
                self.global_offset_xy[1] += self.camera_scroll_speed * 10
                # if self.global_offset_xy[1] > MAXY_DIV_2 + offset_y:
                #     self.global_offset_xy[1] = MAXY_DIV_2 + offset_y
            if self.is_input_up_arrow:
                self.global_offset_xy[1] -= self.camera_scroll_speed * 10
                # if self.global_offset_xy[1] < MAXY_DIV_2:
                #     self.global_offset_xy[1] = MAXY_DIV_2
            # if self.is_input_left_arrow:
            #     self.global_offset_xy[0] -= self.camera_scroll_speed * 10
            #     if self.global_offset_xy[0] < MAXX_DIV_2:
            #         self.global_offset_xy[0] = MAXX_DIV_2
            # if self.is_input_right_arrow:
            #     self.global_offset_xy[0] += self.camera_scroll_speed * 10
            #     if self.global_offset_xy[0] > MAXX_DIV_2 + self.camera.max_offset_x:
            #         self.global_offset_xy[0] = MAXX_DIV_2 + self.camera.max_offset_x
            # if self.is_input_down_arrow:
            #     self.global_offset_xy[1] += self.camera_scroll_speed * 10
            #     if self.global_offset_xy[1] > MAXY_DIV_2 + self.camera.max_offset_y:
            #         self.global_offset_xy[1] = MAXY_DIV_2 + self.camera.max_offset_y
            # if self.is_input_up_arrow:
            #     self.global_offset_xy[1] -= self.camera_scroll_speed * 10
            #     if self.global_offset_xy[1] < MAXY_DIV_2:
            #         self.global_offset_xy[1] = MAXY_DIV_2

            self.camera.apply_offset_level_editor(self.global_offset_xy,
                                     self.camera_scroll_speed * 10, self.camera_scroll_speed * 10, False)

            # Rendering:
            self.render_background()
            self.render_obstacles()
            self.render_demolishers()
            self.render_enemies()
            self.render_new_obs()
            self.render_debug_info()
            self.render_snap_mesh()
            if self.show_minimap:
                self.render_minimap()
            if obs_id > -1:
                self.render_obstacle_properties(obs_id)
            self.render_menu_items()


world = World()
world.set_screen(screen)
# world.create_text_input((100, 100), 'INPUT TEXT:', 'digit')
import locations
world.main_menu()
# world.setup()
importlib.reload(locations)
# world.location_names['names list'] = list(locations.locations.keys())
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
    # if world.need_to_load:
    #     world.need_to_load = False
    #     importlib.reload(locations)
    #     # world.setup()
    #     # importlib.reload(locations)
    #     world.load()

    world.process()
    pygame.display.flip()


if __name__ == "__main__":
    while True:
        if world.need_to_load:
            world.need_to_load = False
            importlib.reload(locations)
            # world.setup()
            # importlib.reload(locations)
            world.load()
            world.create_snap_mesh()
        # if allow_import_location:
        #     from locations import *
        #     allow_import_location = False
        main()