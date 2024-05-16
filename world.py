from actor import *
from obstacle import *
from constants import *
import fonts
import camera

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
        self.camera = camera.Camera()
        self.camera.setup(MAXX*2, MAXY)
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
        entity.destination[0] = entity.rectangle.centerx
        entity.destination[1] = entity.rectangle.centery

        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()
        self.actors[self.location][entity.id] = entity
        self.actor_id += 1

    def add_obstacle(self, description):
        entity = Obstacle()
        entity.id = self.obstacle_id
        entity.is_gravity_affected = description['is gravity affected']
        entity.rectangle.topleft = description['xy']
        entity.rectangle.width = description['dimensions'][0]
        entity.rectangle.height = description['dimensions'][1]
        if self.location not in self.obstacles.keys():
            self.obstacles[self.location] = dict()
        self.obstacles[self.location][entity.id] = entity
        self.obstacle_id += 1

    def process(self, time_passed):
        self.time_passed = time_passed
        self.processing_human_input()
        self.processing_actors()
        self.camera.apply_offset((self.actors[self.location][0].rectangle.centerx, self.actors[self.location][0].rectangle.bottom),
                                 self.actors[self.location][0].speed * 0.9, 5)
                                 # self.actors[self.location][0].speed * 0.9, self.actors[self.location][0].fall_speed)
        self.render_all()

    def processing_collisions(self, checking_unit):
        # checking_unit.is_enough_space_left = True
        # checking_unit.is_enough_space_right = True
        checking_unit.is_enough_space_above = True
        checking_unit.is_enough_space_below = True
        checking_unit.is_stand_on_ground = False
        # checking_unit.is_edge_grabbed = False

        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]

            # # Check enough spaces right and left:
            # if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.rectangle.width - checking_unit.speed - 2, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
            #     checking_unit.is_enough_space_left = False
            # if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
            #     checking_unit.is_enough_space_right = False

            if checking_unit.fall_speed < 0:
                # CHECK TOP
                if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.top - abs(checking_unit.fall_speed), checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed)):
                    checking_unit.rectangle.top = obs.rectangle.bottom
                    checking_unit.is_enough_space_above = False
                    checking_unit.fall_speed = 0
                    checking_unit.is_stand_on_ground = False
                    continue
            else:
                # CHECK BOTTOM
                if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.bottom, checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed) + 1):
                    checking_unit.rectangle.bottom = obs.rectangle.top
                    checking_unit.is_stand_on_ground = True
                    checking_unit.fall_speed = 0
                    checking_unit.is_enough_space_below = False
                    checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
                    self.is_spacebar = False
                    continue

            # CHECK LEFT
            if checking_unit.look == -1:
                if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.speed - 10, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
                        # Grab over the top of an obstacle.
                        if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
                        # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
                            checking_unit.is_edge_grabbed = True
                            checking_unit.rectangle.top = obs.rectangle.top
                            checking_unit.fall_speed = 0
                            checking_unit.is_stand_on_ground = True
                            checking_unit.rectangle.left = obs.rectangle.right  # - 2
                            checking_unit.is_enough_space_left = False
                            checking_unit.heading[0] = 0
                            checking_unit.speed = 0
                            checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
                            return

                        # # Bounce from the wall
                        # if self.is_spacebar and self.is_input_left_arrow:
                        # # if self.is_spacebar and checking_unit.speed > 0:
                        #     checking_unit.look = 1
                        #     checking_unit.jump_attempts_counter = 1
                        #     checking_unit.rectangle.left = obs.rectangle.right  # - 2
                        #     checking_unit.is_jump = True
                        #     if checking_unit.speed > 0:
                        #         checking_unit.speed *= .8
                        #     else:
                        #         checking_unit.speed = checking_unit.max_speed * 0.7
                        #
                        #     # checking_unit.speed *= .8
                        #     return

                        checking_unit.rectangle.left = obs.rectangle.right
                        checking_unit.is_enough_space_left = False
                        checking_unit.heading[0] = 0
                        checking_unit.speed = 0
                        continue

            # CHECK RIGHT
            if checking_unit.look == 1:
                if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
                    # Grab over the top of an obstacle.
                    if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
                    # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
                        checking_unit.is_edge_grabbed = True
                        checking_unit.rectangle.top = obs.rectangle.top
                        checking_unit.fall_speed = 0
                        checking_unit.is_stand_on_ground = True
                        checking_unit.rectangle.right = obs.rectangle.left  # - 2
                        checking_unit.is_enough_space_right = False
                        checking_unit.heading[0] = 0
                        checking_unit.speed = 0
                        checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
                        return

                    # # Bounce from the wall
                    # if self.is_spacebar and self.is_input_right_arrow:
                    #     # if self.is_spacebar and checking_unit.speed > 0:
                    #     checking_unit.look = -1
                    #     checking_unit.jump_attempts_counter = 1
                    #     checking_unit.is_jump = True
                    #     if checking_unit.speed > 0:
                    #         checking_unit.speed *= .8
                    #     else:
                    #         checking_unit.speed = checking_unit.max_speed * 0.7
                    #     checking_unit.rectangle.right = obs.rectangle.left  # - 2
                    #     return

                    checking_unit.rectangle.right = obs.rectangle.left
                    checking_unit.is_enough_space_right = False
                    checking_unit.heading[0] = 0
                    checking_unit.speed = 0
                    continue

    def processing_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            actor.percept(self.obstacles[self.location])
            actor.check_space_around()
            # actor.reset_self_flags()

            if key == 0:  # Player's actor routines

                if self.is_input_down_arrow:
                    actor.set_action('down action')
                else:
                    actor.set_action('down action cancel')

                if self.is_input_right_arrow:
                    actor.set_action('right action')
                else:
                    actor.set_action('right action cancel')

                if self.is_input_left_arrow:
                    actor.set_action('left action')
                else:
                    actor.set_action('left action cancel')

                if self.is_spacebar:
                    actor.set_action('jump action')
                else:
                    actor.set_action('jump action cancel')

            actor.process(self.time_passed)
            self.processing_collisions(actor)
            actor.reset_self_flags()

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - self.camera.offset_y,
                                                  actor.rectangle.width, actor.rectangle.height))
            gaze_direction_mod = 0 if actor.look == -1 else actor.rectangle.width - 10
            pygame.draw.rect(self.screen, RED, (actor.rectangle.x + gaze_direction_mod - self.camera.offset_x, actor.rectangle.centery - 10 - self.camera.offset_y,
                                                  10, 20))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            pygame.draw.rect(self.screen, WHITE, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))

    def render_all(self):
        self.render_background()
        self.render_obstacles()
        self.render_actors()
        self.render_debug_info()

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
            ('ACTOR HEADING: ' + str(self.actors[self.location][0].heading), WHITE),
            ('ACTOR RECT: ' + str(self.actors[self.location][0].rectangle), WHITE),
            ('ACTOR IS ON OBS: ' + str(self.actors[self.location][0].is_on_obstacle), WHITE),
            ('ACTOR IS ON GROUND: ' + str(self.actors[self.location][0].is_stand_on_ground), WHITE),
            ('ACTOR FALL: ' + str(self.actors[self.location][0].fall_speed), WHITE),
            ('ACTOR SPEED: ' + str(self.actors[self.location][0].speed), WHITE),
            ('ACTOR LOOK: ' + str(self.actors[self.location][0].look), WHITE),
            ('ACTOR GRAB: ' + str(self.actors[self.location][0].is_edge_grabbed), WHITE),
            ('ACTOR JUMP ATTMPS: ' + str(self.actors[self.location][0].jump_attempts_counter), WHITE),
            ('ACTOR JUST JUMPED: ' + str(self.actors[self.location][0].just_got_jumped), WHITE),
            ('ACTOR __STATE: ' + str(self.actors[self.location][0].get_state()), WHITE),
            ('ACTOR IGNORES INPUT: ' + str(self.actors[self.location][0].ignore_user_input), WHITE),
            ('ACTOR ABOVE SPACE: ' + str(self.actors[self.location][0].is_enough_space_above), WHITE),
            ('ACTOR BELOW SPACE: ' + str(self.actors[self.location][0].is_enough_space_below), WHITE),
            ('ACTOR RIGHT SPACE: ' + str(self.actors[self.location][0].is_enough_space_right), WHITE),
            ('ACTOR LEFT SPACE: ' + str(self.actors[self.location][0].is_enough_space_left), WHITE),


        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], BLACK), (stats_x, stats_y + gap))
            gap += font_size
