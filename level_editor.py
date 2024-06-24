# import pygame
import uuid

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

class World(object):
    def __init__(self):
        self.allow_import_locations = False
        # CONTROLS
        self.is_key_pressed = False
        self.is_input_up_arrow = False
        self.is_input_down_arrow = False
        self.is_input_right_arrow = False
        self.is_input_left_arrow = False
        self.is_input_confirm = False
        self.is_input_cancel = False
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
        self.demolishers = dict()
        self.demolishers_id: int = 0
        # self.location = '01'
        self.location = ''
        self.screen = None
        self.camera = camera.Camera()
        # self.camera.setup(MAXX*2, MAXY)
        self.global_offset_xy = [MAXX_DIV_2, MAXY_DIV_2]

        self.menu_items = dict()
        self.menu_item_id = 1

        self.new_obs_rect = pygame.Rect(0,0,0,0)
        self.new_obs_rect_started = False
        self.new_obs_rect_start_xy = [0, 0]

        self.snap_mesh = dict()
        self.snap_mesh_size = 50
        self.snap_mesh_size_change_step = 25
        self.zoom_factor = 1.

        # self.setup_box = list()

    def set_screen(self, surface):
        self.screen = surface

    def processing_menu_items(self):
        while self.menu_items:
            self.processing_human_input()
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
                    self.menu_items = dict()
                    self.menu_item_id = 1
                    return command
            self.render_menu_items()
            pygame.display.flip()
            # return selected_item

    def processing_menu_items_back(self):
        selected_item = 0
        for k in self.menu_items.keys():
            menu_item = self.menu_items[k]
            menu_item['hovered'] = False
            if not menu_item['active']:
                continue
            if menu_item['rectangle'].collidepoint(self.mouse_xy):
                menu_item['hovered'] = True
                selected_item = k
        return selected_item


    def setup(self):
        self.add_menu_item(pygame.Rect(MAXX_DIV_2 // 2, 200, MAXX_DIV_2, 200), 'EDIT EXISTING OR CREATE NEW?', '', False)
        self.add_menu_item(pygame.Rect(MAXX_DIV_2 // 2, 400, MAXX_DIV_2 // 2, 200), 'EXISTING', 'EXISTING', True)
        self.add_menu_item(pygame.Rect(MAXX_DIV_2, 400, MAXX_DIV_2 // 2, 200), 'NEW', 'NEW', True)

        command = self.processing_menu_items()

        # exec(command)
        # print(human_choice)
        if command == 'NEW':
            # print('make new')
            # # Setting up the new map:
            width = MAXX
            height = MAXY
            new_location_description = list()
            with open('locations.py', 'r') as f:
                existing_locations_description = f.readlines()

            map_name = 'New map ' + str(uuid.uuid1())

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
            # print('edit existing')
            # User wants to edit an existing map.
            import locations
            self.reset_human_input()
            self.render_background()
            self.add_menu_item(pygame.Rect(MAXX_DIV_2 // 2, 20, MAXX_DIV_2, 100), 'CHOOSE AN EXISTING MAP', '', False)
            map_names = list(locations.locations.keys())
            menu_item_height = 50
            for name in map_names:
                self.add_menu_item(pygame.Rect(MAXX_DIV_2 // 2, 100+map_names.index(name)*menu_item_height, MAXX_DIV_2, menu_item_height), name, map_names.index(name), True)
                # print(f'{name} [{map_names.index(name)}]')
            # print(self.menu_items)
            command = self.processing_menu_items()
            self.location = map_names[command]

        # print(f'{width}, {height}')
        # for l in existing_locations_description:
        #     print(l)
        #
        # exit()

    def setup_back(self):
        i= ''
        while i not in ('e', 'E', 'n', 'N'):
            i = input('Edit [E]xisting level or create [N]ew? :>')
        if i in ('n', 'N'):
            # Setting up the new map:
            width = 0
            height = 0
            while int(width) < MAXX or int(width) > MAXX * 4:
                width = input(f'Input map width in range [{MAXX}..{MAXX*4}], default {MAXX} :>')
                if not width:
                    width = MAXX
            while int(height) < MAXY or int(height) > MAXY * 4:
                height = input(f'Input map height in range [{MAXY}..{MAXY*4}], default {MAXY} :>')
                if not height:
                    height = MAXY
            map_name = str(input(f'Input map name :>'))

            new_location_description = list()
            with open('locations.py', 'r') as f:
                existing_locations_description = f.readlines()

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
            # User wants to edit an existing map.
            import locations
            map_names = list(locations.locations.keys())
            for name in map_names:
                print(f'{name} [{map_names.index(name)}]')
            i = input('Please, select map number :> ')
            self.location = map_names[int(i)]
        # print(f'{width}, {height}')
        # for l in existing_locations_description:
        #     print(l)
        #
        # exit()

    def reset_human_input(self):
        self.is_mouse_button_down = False
        self.is_left_mouse_button_down = False
        self.is_right_mouse_button_down = False

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
                    pygame.quit()
                    raise SystemExit()
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
                if event.key == K_F8:
                    self.load()
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

    def add_menu_item(self, rectangle, text, command, active=True, frame_color=BLUE, bg_color=DARKGRAY, txt_color=WHITE):
        self.menu_items[self.menu_item_id] = dict()
        self.menu_items[self.menu_item_id]['text'] = text
        self.menu_items[self.menu_item_id]['text color'] = txt_color
        self.menu_items[self.menu_item_id]['frame color'] = frame_color
        self.menu_items[self.menu_item_id]['back color'] = bg_color
        self.menu_items[self.menu_item_id]['command'] = command
        self.menu_items[self.menu_item_id]['active'] = active
        self.menu_items[self.menu_item_id]['rectangle'] = rectangle
        self.menu_items[self.menu_item_id]['hovered'] = False
        self.menu_item_id += 1

    def load(self):
        # Loading with pickle:
        # try:
        #     with open('locations_'+self.location+'.dat', 'rb') as f:
        #         loaded_data = pickle.load(f)
        # except FileNotFoundError:
        #     self.obstacles[self.location] = dict()
        #     return

        #Loading with JSON:
        # try:
        #     with open('locations.py', 'r') as f:
        #     # with open('locations_'+self.location+'.dat', 'r') as f:
        #         loaded_data = f.read()
        #         print(loaded_data)
        #         print(json.loads(loaded_data))
        #         exit()
        #         # loaded_data = json.load(f)
        # except FileNotFoundError:
        #     self.obstacles[self.location] = dict()
        #     return

        # self.obstacles[self.location] = dict()
        # self.obstacle_id = 0
        # loc_found = False
        # platf_found = False
        # with open('locations.py', 'r') as f:
        #     # self.obstacles[self.location][self.obstacle_id] =
        #     for line in f:
        #         if platf_found:
        #             if ')  # END' in line:
        #                 break
        #             obs_data = line.strip().split(',  #')[0]
        #             print(list(obs_data))
        #         if loc_found:
        #             if '\'platforms\':' in line:
        #                 platf_found = True
        #                 # for k in self.obstacles[self.location].keys():
        #                 #     obs = self.obstacles[self.location][k]
        #                 loc_found = False
        #         if '\''+self.location+'\':' in line and not loc_found:
        #             # print('Location found!')
        #             loc_found = True

        try:
            max_obs_id = 0
            for obs in locations[self.location]['obstacles']['obs rectangles']:
                self.add_obstacle(obs)
                if max_obs_id < obs[-1]:
                    max_obs_id = obs[-1]
            self.obstacle_id = max_obs_id + 1
            # for dem in locations[self.location]['demolishers']['dem rectangles']:
            #     self.add_demolisher(dem)
            self.camera.setup(locations[self.location]['size'][0], locations[self.location]['size'][1])
        except NameError:
            self.obstacles[self.location] = dict()
            self.demolishers[self.location] = dict()
            self.camera.setup(MAXX, MAXY)
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

    def save_old(self):
        # Saving with pickle:
        # with open('locations_'+self.location+'.dat', 'wb') as f:
        #     pickle.dump(self.obstacles[self.location], f)

        # Saving using JSON:
        # obs_geometry = list()

        obs_rects = list()
        for k in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][k]
            # ghost = ', \'ghost\' ' if obs.is_ghost_platform else ''
            # move_right = ', \'move right\' ' if obs.is_move_right else ''
            # move_left = ', \'move left\' ' if obs.is_move_left else ''
            # collideable = ', \'collideable\' ' if obs.is_collideable else ''
            # actions = ', \'active\' ' if obs.actions else ''
            # gravity_affected = ', \'gravity affected\' ' if obs.is_gravity_affected else ''
            # str(obs.rectangle.size) + ghost + move_right + move_left + \

            total_strg = '                ' + \
                         '(' + \
                         str(obs.rectangle.topleft) + ', ' + \
                         str(obs.rectangle.size) + \
                         ', ' + str(k) + '),  #' + str(k) + '\n'
            obs_rects.append(total_strg)
            # str(obs.rectangle.size) + ghost + move_right + move_left + collideable + gravity_affected + '),  #' + str(obs.id) + '\n'


        dem_rects = list()
        if self.location in self.demolishers:
            for k in self.demolishers[self.location].keys():
                dem = self.demolishers[self.location][k]
                # ghost = ', \'ghost\' ' if dem.is_ghost_platform else ''
                # move_right = ', \'move right\' ' if dem.is_move_right else ''
                # move_left = ', \'move left\' ' if dem.is_move_left else ''
                # collideable = ', \'collideable\' ' if dem.is_collideable else ''
                # actions = ', \'active\' ' if dem.actions else ''
                # gravity_affected = ', \'gravity affected\' ' if dem.is_gravity_affected else ''

                # str(dem.rectangle.size) + ghost + move_right + move_left + \
                total_strg = '                ' + \
                       '(' + \
                       str(dem.rectangle.topleft) + ', ' + \
                       str(dem.rectangle.size) + ', ' + str(k) + \
                       '),  #' + str(k) + '\n'
                dem_rects.append(total_strg)
                       # str(dem.rectangle.size) + ghost + move_right + move_left + collideable + gravity_affected + '),  #' + str(dem.id) + '\n'

        # print(obs_rects)
        # print(dem_rects)
        # exit()
        # ['                ((100, 950), (1550, 50), 0),  #0\n',
        #  '                ((1300, 500), (300, 250), 1),  #1\n',
        #  '                ((950, 350), (100, 150), 2),  #2\n',
        #  '                ((650, 300), (200, 200), 3),  #3\n']

        # ['                ((550, 750), (200, 200), 0),  #0\n']


        loc_found = False
        f_dest = open('locations.py', 'w')
        with open('locations_template.py', 'r') as f_source:
            for line in f_source:
                f_dest.write(line)
                if loc_found:
                    if '\'obs rectangles\':' in line:
                        for obs_rect_line in obs_rects:
                            f_dest.write(obs_rect_line)
                    if '\'dem rectangles\':' in line:
                        for dem_rect_line in dem_rects:
                            f_dest.write(dem_rect_line)
                if '\''+self.location+'\':' in line and not loc_found:
                    # print('Location found!')
                    loc_found = True
        f_dest.close()

        self.allow_import_locations = True

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            pygame.draw.rect(self.screen, WHITE, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x),
                                                  self.zoom_factor * (obs.rectangle.y - self.camera.offset_y),
                                                  self.zoom_factor * obs.rectangle.width,
                                                  self.zoom_factor * obs.rectangle.height))
            s = fonts.font15.render(str(obs.id), True, GREEN)
            self.screen.blit(s, (self.zoom_factor * (obs.rectangle.x - self.camera.offset_x + 2),
                                 self.zoom_factor * (obs.rectangle.y - self.camera.offset_y + 2)))

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
        for k in self.menu_items.keys():
            menu_item = self.menu_items[k]
            # print(menu_item['rectangle'].x,menu_item['rectangle'].y,menu_item['rectangle'].w,menu_item['rectangle'].h)
            pygame.draw.rect(self.screen, menu_item['back color'], (menu_item['rectangle'].x, menu_item['rectangle'].y,
                                                                     menu_item['rectangle'].w,menu_item['rectangle'].h), 0)
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
            ('SAVE: F2 | LOAD: F8 | W/A/S/D: MOVE CAMERA | [SHIFT+] +/- : CHANGE SNAP MESH SCALE | [/] : change inserting object type | MOUSE WHEEL : ZOOM| ESC: QUIT', BLUE),

            ('OBJECT TYPE        : ' + str(self.object_types[self.current_object_type]), BLACK),
            ('WORLD SIZE         : ' + str(self.camera.max_x) + ':' + str(self.camera.max_y), BLACK),
            ('MAX OFFSET         : ' + str(self.camera.max_offset_x) + ':' + str(self.camera.max_offset_y), BLACK),
            ('SNAP MESH SCALE    : ' + str(self.snap_mesh_size), BLACK),
            ('OFFSET GLOBAL      : ' + str(self.global_offset_xy), BLACK),
            ('CAMERA INNER OFFSET: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), BLACK),
            ('MOUSE XY           : ' + str(self.mouse_xy_snapped_to_mesh), WHITE),
            ('ZOOM               : ' + str(self.zoom_factor), WHITE),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], GRAY), (stats_x, stats_y + gap))
            gap += font_size

    def render_snap_mesh(self):
        pygame.draw.circle(self.screen, RED, (self.zoom_factor * (self.mouse_xy_snapped_to_mesh[0] - self.camera.offset_x),
                                              self.zoom_factor * (self.mouse_xy_snapped_to_mesh[1] - self.camera.offset_y)), 5)
        for k in self.snap_mesh.keys():
            pygame.draw.circle(self.screen, YELLOW, (self.zoom_factor *(k[0] - self.camera.offset_x),
                                                     self.zoom_factor *(k[1] - self.camera.offset_y)), 1)

    def render_snap_mesh_back(self):
        pygame.draw.circle(self.screen, RED, (self.mouse_xy_snapped_to_mesh[0] - self.camera.offset_x,
                                              self.mouse_xy_snapped_to_mesh[1] - self.camera.offset_y), 5)
        for k in self.snap_mesh.keys():
            pygame.draw.circle(self.screen, YELLOW, (k[0] - self.camera.offset_x, k[1] - self.camera.offset_y), 1)


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

    def process(self):
        self.processing_human_input()

        if self.menu_items:
            command = self.processing_menu_items()
            exec(command)
        else:
            if self.is_mouse_wheel_up:
                self.is_mouse_wheel_up = False
                self.zoom_factor += .1
            elif self.is_mouse_wheel_down:
                self.is_mouse_wheel_down = False
                self.zoom_factor -= .1

            if self.is_spacebar:
                obs_id = self.check_mouse_xy_collides_obs()
                if obs_id > -1:
                    # Try to delete existing obs:
                    del self.obstacles[self.location][obs_id]

            if self.is_right_mouse_button_down:
                ...

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
world.setup()
from locations import *

# try:
#     from locations import *
# except ModuleNotFoundError:
#     pass
# world.set_screen(screen)
world.obstacles[world.location] = dict()
world.load()
world.create_snap_mesh()

allow_import_location = False
def main():
    global allow_import_location
    while True:
        if world.allow_import_locations:
            allow_import_location = True
            world.allow_import_locations = False
        world.process()
        pygame.display.flip()


if __name__ == "__main__":
    if allow_import_location:
        from locations import *
        allow_import_location = False
    main()