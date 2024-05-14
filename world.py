from actor import *
from obstacle import *
from constants import *
import fonts

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
        self.render_all()

    # def processing_free_space_checking(self, checking_unit):
    #     above_checked = False
    #     below_checked = False
    #     next_step_checked = False
    #
    #     for obs in self.obstacles[self.location].values():
    #         if checking_unit.look == 'right':
    #             if obs.rectangle.colliderect((checking_unit.rectangle.right + 5, checking_unit.rectangle.bottom + 10), (1, 1)):# or \
    #                 next_step_checked = True
    #                 checking_unit.is_enough_space_for_step = True
    #         elif checking_unit.look == 'left':
    #             if obs.rectangle.colliderect((checking_unit.rectangle.left - 5, checking_unit.rectangle.bottom + 10), (1, 1)):# or \
    #                 next_step_checked = True
    #                 checking_unit.is_enough_space_for_step = True
    #
    #         if obs.rectangle.colliderect((checking_unit.rectangle.left + 10, checking_unit.rectangle.top - 25), (checking_unit.rectangle.width - 20, 1)):
    #
    #             checking_unit.is_enough_space_above = False
    #             above_checked = True
    #             continue
    #         if obs.rectangle.colliderect((checking_unit.rectangle.left , checking_unit.rectangle.bottom + 20), (checking_unit.rectangle.width, 2)):
    #             checking_unit.is_enough_space_below = False
    #             #checking_unit.is_stand_on_ground = True
    #             if obs.is_ghost_platform:
    #                 checking_unit.is_on_ghost_platform = True
    #             else:
    #                 checking_unit.is_on_ghost_platform = False
    #             # if obs.Obstacle:
    #             #     checking_unit.IsOnObstacle = True
    #             # else:
    #             checking_unit.is_on_obstacle = True
    #             below_checked = True
    #             continue
    #         if above_checked and below_checked and next_step_checked:
    #             return
    #     if not above_checked:
    #         checking_unit.is_enough_space_above = True
    #     if not below_checked:
    #         checking_unit.is_enough_space_below = True
    #     if not next_step_checked:
    #         checking_unit.is_enough_space_for_step = False

    def processing_collisions(self, checking_unit):
        checking_unit.is_enough_space_left = True
        checking_unit.is_enough_space_right = True
        checking_unit.is_enough_space_above = True
        checking_unit.is_stand_on_ground = False
        # checking_unit.is_edge_grabbed = False

        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            # if obs.rectangle.colliderect(checking_unit.rectangle):
                # print('collide')

            # CHECK LEFT
            if checking_unit.look < 0:
            # if checking_unit.heading[0] < 0:
                if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.speed - 5, checking_unit.rectangle.top + 5, checking_unit.speed + 5, checking_unit.rectangle.height - 35):
                    if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
                    # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.is_need_to_grab_edge:
                        print('GRAB LEFT')
                        checking_unit.is_edge_grabbed = True
                        checking_unit.rectangle.top = obs.rectangle.top
                        checking_unit.fall_speed = 0
                        checking_unit.is_stand_on_ground = True
                        checking_unit.rectangle.left = obs.rectangle.right  # - 2
                        checking_unit.is_enough_space_left = False
                        checking_unit.heading[0] = 0
                        checking_unit.speed = 0
                        return
                    checking_unit.rectangle.left = obs.rectangle.right
                    checking_unit.is_enough_space_left = False
                    #checking_unit.is_need_to_jump = False
                    checking_unit.heading[0] = 0
                    # checking_unit.fall_speed = 0
                    checking_unit.speed = 0
                    continue

            # CHECK RIGHT
            if checking_unit.look > 0:
            # if checking_unit.heading[0] > 0:
                if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top + 5, checking_unit.speed + 5, checking_unit.rectangle.height - 35):
                    if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
                    # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.is_need_to_grab_edge:
                        print('GRAB RIGHT')
                        checking_unit.is_edge_grabbed = True
                        checking_unit.rectangle.top = obs.rectangle.top
                        checking_unit.fall_speed = 0
                        checking_unit.is_stand_on_ground = True
                        checking_unit.rectangle.right = obs.rectangle.left  # - 2
                        checking_unit.is_enough_space_right = False
                        checking_unit.heading[0] = 0
                        checking_unit.speed = 0
                        # checking_unit.is_need_to_jump = False
                        return

                    checking_unit.rectangle.right = obs.rectangle.left  # - 2
                    checking_unit.is_enough_space_right = False
                    checking_unit.heading[0] = 0
                    checking_unit.speed = 0
                    continue
                    # checking_unit.destination[0] = checking_unit.rectangle.centerx



            # CHECK TOP
            if checking_unit.fall_speed < 0:
                if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.top - 2, checking_unit.rectangle.width - 4, 2):
                    checking_unit.rectangle.top = obs.rectangle.bottom + 2
                    # checking_unit.destination[1] = checking_unit.rectangle.centery
                    checking_unit.is_enough_space_above = False
                    checking_unit.fall_speed = 0
                    # checking_unit.is_need_to_jump = False
                    continue

            # CHECK BOTTOM
            if checking_unit.fall_speed > 0:
                # if checking_unit.heading[1] > 0:
                if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.bottom, checking_unit.rectangle.width - 4, 2):
                    checking_unit.rectangle.bottom = obs.rectangle.top
                    # checking_unit.destination[1] = checking_unit.rectangle.centery
                    checking_unit.is_stand_on_ground = True
                    checking_unit.fall_speed = 0
                    checking_unit.is_enough_space_below = False
                    # checking_unit.is_need_to_jump = False
                    continue

                # if checking_unit.heading[0] > 0:
                #     if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top + 5, 2, checking_unit.rectangle.height - 35):
                #         checking_unit.rectangle.right = obs.rectangle.left - 2
                #         continue
                #         # checking_unit.destination[0] = checking_unit.rectangle.centerx
                # elif checking_unit.heading[0] < 0:
                #     if obs.rectangle.colliderect(checking_unit.rectangle.left -2, checking_unit.rectangle.top + 5, 2, checking_unit.rectangle.height - 35):
                #         checking_unit.rectangle.left = obs.rectangle.right + 2
                #         continue
                #
                # if checking_unit.heading[1] > 0:
                #     if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.bottom, checking_unit.rectangle.width - 4, 2):
                #         checking_unit.rectangle.bottom = obs.rectangle.top
                #         checking_unit.destination[1] = checking_unit.rectangle.centery
                #         checking_unit.is_stand_on_ground = True
                #         checking_unit.fall_speed = 0
                #         # checking_unit.is_need_to_jump = False
                #         continue

    def processing_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            #actor.is_stand_on_ground = False
            #actor.is_enough_space_above = True
            #self.processing_collisions(actor)

            # self.processing_free_space_checking(actor)
            
            if key == 0:  # Player's actor routines
                actor.is_need_to_move_left = False
                actor.is_need_to_move_right = False
                # actor.is_need_to_grab_edge = False
                actor.is_need_to_jump = False

                if self.is_input_left_arrow:
                    actor.is_need_to_move_left = True

                elif self.is_input_right_arrow:
                    actor.is_need_to_move_right = True
                    # actor.is_need_to_move_left = False

                    # actor.heading[0] = 1
                    # if actor.look == -1 and actor.speed > 0:  # Actor looks to the other side and runs.
                    #     # Switch off heading to force actor start reducing his speed and slow it down to zero.
                    #     # After that actor is going to be able to start acceleration to proper direction.
                    #     actor.heading[0] = 0
                    # else:
                    #     actor.look = 1

                    # actor.heading[0] = 0

                if self.is_spacebar:
                    if actor.is_stand_on_ground or actor.is_edge_grabbed:
                    # if actor.is_enough_space_above and actor.is_stand_on_ground:
                        self.is_spacebar = False
                        actor.is_need_to_jump = True
                        # actor.is_need_to_grab_edge = True
                    # else:
                    #     actor.is_need_to_grab_edge = True



            actor.process(self.time_passed)
            # self.processing_free_space_checking(actor)
            self.processing_collisions(actor)
            #actor.is_stand_on_ground = False

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x, actor.rectangle.y, actor.rectangle.width, actor.rectangle.height))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            pygame.draw.rect(self.screen, WHITE, (obs.rectangle.x, obs.rectangle.y, obs.rectangle.width, obs.rectangle.height))

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


        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], BLACK), (stats_x, stats_y + gap))
            gap += font_size
