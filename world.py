from actor import *
from constants import *

class World(object):
    def __init__(self):
        # Entities
        self.obstacles = dict()
        self.obstacle_id: int = 0
        self.actors = dict()
        self.actor_id: int = 0
        self.items = dict()
        self.item_id: int = 0
        self.particles = dict()
        self.particle_id: int = 0

        self.locations = dict()
        self.location: str = ''
        self.is_new_location_loading: bool = True
        self.new_location_description = dict()

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
        self.is_mouse_hovers_item: bool = False
        self.mouse_hovers_item: int = 0
        self.is_mouse_hovers_actor: bool = False
        self.mouse_hovers_actor: int = 0

        self.screen = None
        self.time_passed: int = 0
        self.game_cycles_counter: int = 0
        self.is_quit:bool = False

    def get_screen(self, surface):
        self.screen = surface

    def add_actor(self, description):
        entity = Actor()
        entity.id = self.actor_id
        entity.is_gravity_affected = True
        entity.rectangle.center = description['xy']
        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()
        self.actors[self.location][entity.id] = entity
        self.actor_id += 1
        # elif description['type'] == 'obstacle':
        #     entity = Obstacle()
        #     entity.id = self.obstacle_id
        #     self.obstacle_id += 1

    def process(self, time_passed):
        self.time_passed = time_passed
        self.processing_human_input()
        self.processing_actors()
        self.render_all()

    def processing_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]

            if key == 0:  # Player's actor routines
                if self.is_input_left_arrow:
                    actor.destination[0] = 0
                elif self.is_input_right_arrow:
                    actor.destination[0] = MAXX
                else:
                    actor.destination[0] = actor.rectangle.centerx

                if self.is_spacebar:
                    self.is_spacebar = False
                    actor.is_need_to_jump = True

            actor.process(self.time_passed)


    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x, actor.rectangle.y, actor.rectangle.width, actor.rectangle.height), 2)

    def render_all(self):
        self.render_background()
        self.render_actors()

    def processing_human_input(self):
        # self.mouse_xy = pygame.mouse.get_pos()
        # self.mouse_xy_absolute = pygame.mouse.get_pos()
        # self.mouse_xy_index = self.define_index_for_point(self.mouse_xy)
        # if self.mode == 'wandering':
        #     self.mouse_xy = (self.mouse_xy[0] + self.offset_x) // self.wandering_screen_scale, \
        #                     (self.mouse_xy[1] + self.offset_y) // self.wandering_screen_scale

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
            # print(self.l_shift)
            if event.type == KEYUP:
                self.is_key_pressed = False
                if event.key == K_d:
                    self.is_input_right_arrow = False
                if event.key == K_a:
                    self.is_input_left_arrow = False
                if event.key == K_w:
                    self.is_input_up_arrow = False
                if event.key == K_s:
                    self.is_input_down_arrow = False
                if event.key == K_SPACE:
                    self.is_spacebar = False
                # elif event.key == K_z:
                #     self.z = False
                # elif event.key == K_x:
                #     self.input_cancel = False
                # if event.key == K_KP_PLUS:
                #     self.avatars_row_scale_decrease = False
                # if event.key == K_KP_MINUS:
                #     self.avatars_row_scale_increase = False
            if event.type == KEYDOWN:
                self.is_key_pressed = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    raise SystemExit()

                if event.key == K_d:
                    self.is_input_right_arrow = True
                if event.key == K_a:
                    self.is_input_left_arrow = True
                if event.key == K_w:
                    self.is_input_up_arrow = True
                if event.key == K_s:
                    self.is_input_down_arrow = True
                if event.key == K_SPACE:
                    self.is_spacebar = True
                # if event.key == K_F5:
                #     self.need_quick_save = True
                # elif event.key == K_F8:
                #     self.need_quick_load = True
                #     # quick_save(self, self.locations)
                # elif event.key == K_F3:
                #     self.music_on = False if self.music_on else True
                #     if not self.music_on:
                #         pygame.mixer.music.fadeout(2000)
                elif event.key == K_z:
                    # Cool stuff with if-then-else expression compress:
                    self.is_z = False if self.is_z else True
                elif event.key == K_x:
                    # self.change_mode()
                    self.is_x = False if self.is_x else True
                    # self.screen_follows_actor = False if self.screen_follows_actor else True
                # elif event.key == K_b:
                #     # self.change_mode()
                #     self.b = False if self.b else True
                # elif event.key == K_f:
                #     self.follow_mode = False if self.follow_mode else True
                # elif event.key == K_l:
                #     # self.change_mode()
                #     self.locations[self.location]['lights on'] = False if self.locations[self.location]['lights on'] else True
                # elif event.key == K_l:
                #     # self.change_mode()
                #     self.lights_on = False if self.lights_on else True
                # elif event.key == K_m:
                #     self.need_to_show_minimap = False if self.need_to_show_minimap else True
                elif event.key == K_n:
                    # self.change_mode()
                    self.is_n = False if self.is_n else True
                    # msg = 'NEW EMPTY MESSAGE FOR TEST PURPOSES.'
                    # self.info_windows[0].get_bunch_of_new_messages((msg, msg))
                    # self.add_info_window(self.calculate_info_string_xy(), [msg, ], 300, False)

                elif event.key == K_p:
                    # Cool stuff with if-then-else expression compress:
                    self.is_p = False if self.is_p else True
                elif event.key == K_i:
                    # Cool stuff with if-then-else expression compress:
                    self.is_i = False if self.is_i else True
                # elif event.key == K_SPACE:
                #     self.change_player_actors()
                # elif event.key == K_e:
                # # elif event.key == K_KP_ENTER:
                #     # elif event.key == K_SPACE:
                #     # self.input_confirm = True
                #     self.wandering_actor.end_turn()
                #     self.player_turn = False
                # elif event.key == K_c:
                #     self.skip_actor()
                # elif event.key == K_TAB:
                #     self.need_to_show_party_inventory = True if not self.need_to_show_party_inventory else False
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
