import pygame

from constants import *
# from world import *
from locations import *
from obstacle import *
import camera
# from sound import *
import fonts
import pickle

class World(object):
    def __init__(self):
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



    def set_screen(self, surface):
        self.screen = surface

    def processing_human_input(self):
        self.mouse_xy = pygame.mouse.get_pos()
        self.mouse_xy_global = (self.mouse_xy[0] + self.camera.offset_x, self.mouse_xy[1] + self.camera.offset_y)
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
            #
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
        try:
            with open('locations_'+self.location+'.dat', 'rb') as f:
                loaded_data = pickle.load(f)
        except FileNotFoundError:
            self.obstacles[self.location] = dict()
            return

        # for d in loaded_data:
        # print(f'{d}: {loaded_data[d]}')  #
        # print('*' * 100)
        self.obstacles[self.location] = loaded_data
        self.obstacle_id = len(self.obstacles[self.location].keys()) + 1
        # with open('locations.dat' , 'r') as f:
        #     for line in f:
        #         print(line.split('|'))
        #         # obs_id,obs_xy,obs_size = line.split('|')
        #         # print(obs_id, obs_xy, obs_size)
        # # for obs in locations[self.location]['obstacles']['platforms']:
        # #     self.add_obstacle(obs)
        # # print(f'[world.load] loaded obstacles: {len(self.obstacles[self.location])}')

    def save(self):
        with open('locations_'+self.location+'.dat', 'wb') as f:
            # for k in self.obstacles[self.location].keys():
            #     obs = self.obstacles[self.location][k]
            #     # self.new_obs_rect.topleft, self.new_obs_rect.size
            #     f.write(str(obs.id) + '|' + str(obs.rectangle.topleft) + '|' + str(obs.rectangle.size) + '\n')
            pickle.dump(self.obstacles[self.location], f)
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
            ('OFFSET GLOBAL: ' + str(self.global_offset_xy), WHITE),
            ('CAMERA INNER OFFSET: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), WHITE),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], BLACK), (stats_x, stats_y + gap))
            gap += font_size


    def check_mouse_xy_collides_obs(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            if obs.rectangle.collidepoint(self.mouse_xy_global):
                return obs.id
        return -1

    def process(self):
        self.processing_human_input()
        if self.is_right_mouse_button_down:
            obs_id = self.check_mouse_xy_collides_obs()
            if obs_id > -1:
                del self.obstacles[self.location][obs_id]
        if self.is_left_mouse_button_down:
            if self.new_obs_rect_started:
                self.new_obs_rect.update(self.new_obs_rect_start_xy[0], self.new_obs_rect_start_xy[1],
                                         self.mouse_xy_global[0] - self.new_obs_rect_start_xy[0], self.mouse_xy_global[1] - self.new_obs_rect_start_xy[1] )
            else:
                self.new_obs_rect_started = True
                self.new_obs_rect_start_xy = self.mouse_xy_global
        else:
            if self.new_obs_rect_started:
                description = (self.new_obs_rect.topleft, self.new_obs_rect.size)
                self.add_obstacle(description)
                self.new_obs_rect_started = False
                self.new_obs_rect_start_xy = [0, 0]
                self.new_obs_rect.update(0,0,0,0)

        # if self.is_l_shift:
        #     self.camera.apply_offset((self.mouse_xy_global[0], self.mouse_xy_global[1]),
        #                              self.camera_scroll_speed, self.camera_scroll_speed)
        #     self.global_offset_xy = [self.camera.offset_x, self.camera.offset_x]
        # if self.is_key_pressed:
        if self.is_input_left_arrow:
            self.global_offset_xy[0] -= self.camera_scroll_speed * 10
            if self.global_offset_xy[0] < MAXX_DIV_2:
                self.global_offset_xy[0] = MAXX_DIV_2
            # self.camera.apply_offset(self.global_offset_xy,
            #                          self.camera_scroll_speed, self.camera_scroll_speed, True)
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

        self.render_background()
        self.render_obstacles()
        self.render_new_obs()
        self.render_debug_info()


world = World()
world.set_screen(screen)
world.obstacles[world.location] = dict()
# world.load()
def main():
    while True:
        world.process()
        pygame.display.flip()


if __name__ == "__main__":
    main()