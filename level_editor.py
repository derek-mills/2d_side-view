import pygame

from constants import *
# from world import *
try:
    from locations import *
except ModuleNotFoundError:
    pass
from obstacle import *
import camera
# from sound import *
import fonts
import json
# import pickle
# import setup_box
# import menu

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
        self.is_spacebar = False
        self.is_F2 = False
        self.is_F8 = False
        self.is_l_shift = False
        self.is_l_ctrl = False
        self.is_l_alt = False
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

        self.obstacles = dict()
        self.obstacle_id: int = 0
        self.location = '01'
        self.screen = None
        self.camera = camera.Camera()
        self.camera.setup(MAXX*2, MAXY)
        self.global_offset_xy = [MAXX_DIV_2, MAXY_DIV_2]

        self.new_obs_rect = pygame.Rect(0,0,0,0)
        self.new_obs_rect_started = False
        self.new_obs_rect_start_xy = [0, 0]

        self.snap_mesh = dict()
        self.snap_mesh_size = 50
        # self.setup_box = list()

    def set_screen(self, surface):
        self.screen = surface

    def processing_human_input(self):
        self.mouse_xy = pygame.mouse.get_pos()
        self.mouse_xy_global = (self.mouse_xy[0] + self.camera.offset_x, self.mouse_xy[1] + self.camera.offset_y)
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
                    self.snap_mesh_size += 1
                    self.create_snap_mesh()
                if event.key == K_KP_MINUS:
                    self.snap_mesh_size -= 1
                    self.create_snap_mesh()
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
            # elif event.type == MOUSEWHEEL:
            #     # print(event)
            #     # print(event.x, event.y)
            #     # print(event.flipped)
            #     # print(event.which)
            #     self.is_mouse_wheel_rolls = True
            #     if event.y == 1:
            #         # Mouse wheel up:
            #         self.is_mouse_wheel_up = True
            #         # self.wandering_screen_target_scale += self.wandering_scale_amount
            #     elif event.y == -1:
            #         # Mouse wheel down:
            #         self.is_mouse_wheel_down = True
            if event.type == MOUSEBUTTONUP:
                self.is_mouse_button_down = False
                if self.is_right_mouse_button_down:
                    self.is_right_mouse_button_down = False
                if self.is_left_mouse_button_down:
                    self.is_left_mouse_button_down = False

    def add_obstacle(self, description):
        entity = Obstacle()
        entity.id = self.obstacle_id
        entity.is_gravity_affected = True if 'is gravity affected' in description else False
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
        self.obstacle_id += 1

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
            for obs in locations['01']['obstacles']['platforms']:
                self.add_obstacle(obs)
        except NameError:
            self.obstacles[self.location] = dict()

        # self.obstacle_id = len(self.obstacles[self.location].keys()) + 1

    def save(self):
        # Saving with pickle:
        # with open('locations_'+self.location+'.dat', 'wb') as f:
        #     pickle.dump(self.obstacles[self.location], f)

        # Saving using JSON:
        # obs_geometry = list()
        loc_found = False
        f_dest = open('locations.py', 'w')
        with open('locations_template.py', 'r') as f_source:
            for line in f_source:
                f_dest.write(line)
                if loc_found:
                    if '\'platforms\':' in line:
                        for k in self.obstacles[self.location].keys():
                            obs = self.obstacles[self.location][k]
                            ghost = ', \'ghost\', ' if obs.is_ghost_platform else ''
                            move_right = ', \'move right\', ' if obs.is_move_right else ''
                            move_left = ', \'move left\', ' if obs.is_move_left else ''
                            collideable = ', \'collideable\', ' if obs.is_collideable else ''
                            total_strg = '                ('+str(obs.rectangle.topleft) + ', ' + \
                                   str(obs.rectangle.size) + ghost + move_right + move_left + collideable + '),  #' + str(obs.id) + '\n'
                            f_dest.write(total_strg)
                        loc_found = False
                if '\''+self.location+'\':' in line and not loc_found:
                    # print('Location found!')
                    loc_found = True

        f_dest.close()
        self.allow_import_locations = True
        # exit()
        # with open('locations_' + self.location + '.dat', 'w') as f:
        #     for k in self.obstacles[self.location].keys():
        #         obs = self.obstacles[self.location][k]
        #         obs_geometry = (obs.id, obs.rectangle.topleft, obs.rectangle.size)
        #         # obs_geometry.append((obs.id, obs.rectangle.topleft, obs.rectangle.size))
        #         # f.write(str(obs.id) + ' ' + str(obs_geometry) + '\n')
        #         f.write(obs_geometry)
        #         # f.write(json.dumps(obs_geometry))

            # json.dump(obs_geometry, f)

            # settings = {
            #     ''
            # }
            # pickle.dump(settings, f)

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            pygame.draw.rect(self.screen, WHITE, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))
            s = fonts.font15.render(str(obs.id), True, GREEN)
            self.screen.blit(s, (obs.rectangle.x - self.camera.offset_x + 2, obs.rectangle.y - self.camera.offset_y + 2))

    def render_menu(self):
        ...
        # if self.menu:
        #     self.menu.draw()

    def render_new_obs(self):

        pygame.draw.rect(self.screen, CYAN, (self.new_obs_rect.x - self.camera.offset_x, self.new_obs_rect.y - self.camera.offset_y,
                                              self.new_obs_rect.width, self.new_obs_rect.height))

    def render_debug_info(self):
        stats_x = 1
        stats_y = 1
        # stripes_width = 500
        gap = 1
        font_size = 12
        # m_hover_item = 'None' if not self.mouse_hovers_item else self.items[self.mouse_hovers_item].name
        # m_hover_actor = 'None' if not self.mouse_hovers_actor else self.wandering_actors[self.mouse_hovers_actor].name + ' ' + str(self.wandering_actors[self.mouse_hovers_actor].id)
        # m_hover_cell = 'None' if self.point_mouse_cursor_shows is None else str(self.locations[self.location]['points'][self.point_mouse_cursor_shows]['rect'].center)
        params = (
            ('SAVE: F2 | LOAD: F8 | WASD: MOVE CAMERA | + - : CHANGE SNAP MESH SCALE | ESC: QUIT', BLUE),
            ('SNAP MESH SCALE: ' + str(self.snap_mesh_size), BLACK),
            ('OFFSET GLOBAL: ' + str(self.global_offset_xy), BLACK),
            ('CAMERA INNER OFFSET: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), BLACK),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], GRAY), (stats_x, stats_y + gap))
            gap += font_size

    def render_snap_mesh(self):
        pygame.draw.circle(self.screen, RED, (self.mouse_xy_snapped_to_mesh[0] - self.camera.offset_x,
                                              self.mouse_xy_snapped_to_mesh[1] - self.camera.offset_y), 5)
        for k in self.snap_mesh.keys():
            # dot = self.snap_mesh[k]
            pygame.draw.circle(self.screen, YELLOW, (k[0] - self.camera.offset_x, k[1] - self.camera.offset_y), 1)

    def create_snap_mesh(self):
        self.snap_mesh = dict()
        for x in range(0, self.camera.max_offset_x + MAXX, self.snap_mesh_size):
            for y in range(0, self.camera.max_offset_y + MAXY, self.snap_mesh_size):
                self.snap_mesh[(x, y)] = (x, y)

    def check_mouse_xy_collides_obs(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            if obs.rectangle.collidepoint(self.mouse_xy_global):
                return obs.id
        return -1

    # def menu_bar(self, menu_items, xy):
    #     items = list()
    #     dx = xy[0]
    #     dy = xy[1]
    #     for i in menu_items.keys():
    #         items.append((i, dx, dy, menu_items[i][0], menu_items[i][1]))
    #         dy += 20
    #
    #     pygame.draw.rect(self.screen, pygame.Color(100, 100, 100, 10), (dx - 2, dy - 2, self.menu_item_width + 4, self.menu_height + self.menu_items_spacing + 2), 0)
    #     print(items)
    #     exit()

    def process(self):
        self.processing_human_input()

        if self.is_spacebar:
            obs_id = self.check_mouse_xy_collides_obs()
            if obs_id > -1:
                # Try to delete existing obs:
                del self.obstacles[self.location][obs_id]

        if self.is_right_mouse_button_down:
            ...
            # obs_id = self.check_mouse_xy_collides_obs()
            # if obs_id > -1:
            #     menu_items = {
            #         'IS GHOST?:': ('checkbox', 'is_ghost_platform'),
            #         'MOVE RIGHT:': ('checkbox', 'is_move_right'),
            #         'MOVE LEFT:': ('checkbox', 'is_move_left'),
            #         'MOVE UP:': ('checkbox', 'is_move_up'),
            #         'MOVE DOWN:': ('checkbox', 'is_move_down'),
            #         'GRAVITY AFFECTED:': ('checkbox', 'is_gravity_affected'),
            #         'COLLIDEABLE:': ('checkbox', 'is_collideable'),
            #     }
            #     # self.menu_bar(menu_items, self.mouse_xy)
            #     self.obstacles[self.location][obs_id].is_ghost_platform = input('Is ghost? (True/False):')


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
                    description = (self.new_obs_rect.topleft, self.new_obs_rect.size)
                    self.add_obstacle(description)
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
                                 self.camera_scroll_speed, self.camera_scroll_speed, True)

        # if self.menu:
        #     self.menu.process()
        #     # self.menu.process(self.mouse_xy, self.is_left_mouse_button_down)
        #
        # Rendering:
        self.render_background()
        self.render_obstacles()
        self.render_new_obs()
        self.render_debug_info()
        # self.render_menu()
        self.render_snap_mesh()

world = World()
world.set_screen(screen)
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