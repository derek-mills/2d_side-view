from actor import *
from obstacle import *
from demolisher import *
# from constants import *
import fonts
import camera
from locations import *
from load_content import load_animations
from misc_tools import *  #black_out, black_in
# import pickle
from random import choice

class World(object):
    def __init__(self):
        # Entities
        self.obstacles = dict()
        self.obstacle_id: int = 0
        self.active_obstacles = list()
        self.demolishers = dict()
        self.demolisher_id: int = 0
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
        self.is_attack = False
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
        self.spacebar_multiple_press_prevent = False
        self.is_l_shift = False
        self.is_l_ctrl = False
        self.is_l_alt = False
        self.l_alt_multiple_press_prevent = False
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

    def set_screen(self, surface):
        self.screen = surface

    def add_actor(self, description):
        entity = Actor()
        entity.id = self.actor_id
        entity.name = description['name']
        entity.max_health = description['health']
        entity.health = description['health']
        entity.is_gravity_affected = description['gravity affected']
        entity.rectangle.height = description['height']
        entity.rectangle.width = description['width']
        entity.rectangle.center = description['start_xy']
        entity.apply_measurements()
        entity.destination[0] = entity.rectangle.centerx
        entity.destination[1] = entity.rectangle.centery
        entity.max_speed = description['max speed']
        entity.default_max_speed = description['max speed']

        entity.animations = description['animations']
        entity.animation_descriptor = entity.name  # for ex.: 'player1'
        load_animations(entity)
        entity.set_state('stand still')
        entity.set_current_animation()
        # print(entity.get_state(), entity.current_animation)
        # exit()
        entity.frames_changing_threshold = entity.animations[entity.current_animation]['speed']
        # entity.frames_changing_threshold = entity.animations[entity.current_animation][entity.look]['speed']
        entity.animation_sequence = entity.animations[entity.current_animation]['sequence']
        # entity.animation_sequence = entity.animations[entity.current_animation][entity.look]['sequence']
        entity.set_current_sprite()

        entity.ai_controlled = description['AI controlled']
        entity.think_type = description['think type']
        entity.add_items_to_inventory(description['items'])
        entity.activate_weapon(0)

        # entity.change_animation()
        # entity.process_animation_counter()

        entity.set_state('stand still')
        # entity.max_jump_attempts = 3

        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()
        self.actors[self.location][entity.id] = entity
        self.actor_id += 1

    def add_obstacle(self, description):
        entity = Obstacle()
        entity.id = self.obstacle_id
        entity.is_gravity_affected = True if 'gravity affected' in description else False
        entity.rectangle.topleft = description[0]
        entity.origin_xy = description[0]
        entity.rectangle.width = description[1][0]
        entity.rectangle.height = description[1][1]
        # entity.max_speed = 0.6
        # entity
        # entity.is_move_right = True if 'move right' in description else False
        # entity.is_move_up = True if 'move up' in description else False
        # entity.is_move_down = True if 'move down' in description else False
        # entity.is_move_left = True if 'move left' in description else False
        entity.is_ghost_platform = True if 'ghost' in description else False
        entity.is_collideable = True if 'collideable' in description else False
        if entity.id in self.locations[self.location]['obstacles']['actions'].keys():
            entity.active = True
            entity.actions = self.locations[self.location]['obstacles']['actions'][entity.id]
            entity.max_speed = self.locations[self.location]['obstacles']['settings'][entity.id]['speed']
            print(f'[add_obstacle] Added active obstacle: {entity.actions=}')
        # Add an obstacle to the world storage:
        # if self.location not in self.obstacles.keys():
        #     self.obstacles[self.location] = dict()
        self.obstacles[self.location][entity.id] = entity
        self.obstacle_id += 1

    def add_demolisher(self, description):
        demol = Demolisher()
        demol.id = self.demolisher_id
        self.demolisher_id += 1
        demol.name = 'demolisher ' + str(demol.id)
        demol.snap_to_actor = description['snap to actor']
        actor = self.actors[self.location][description['snap to actor']]
        demol.parent_id = actor.id
        demol.ttl = description['demolisher TTL']
        demol.rectangle.width = description['rect'].width
        demol.rectangle.height = description['rect'].height
        # demol.rectangle.topleft = (100, 750)
        # demol.origin_xy = description['rect'].topleft

        demol.snapping_offset = actor.animations[actor.current_animation]['demolisher offset'][actor.look]
        # demol.snapping_offset = actor.current_weapon['demolisher offset'][actor.look]
        demol.update(actor.look, actor.rectangle)
        demol.bounce = description['bounce']
        demol.flyer = description['flyer']
        if demol.flyer:
            # if not demol.static:
            demol.destination = (self.camera.max_offset_x + MAXX, demol.rectangle.y) if actor.look == 1 else (-100, demol.rectangle.y)
        demol.aftermath = description['aftermath']
        demol.damage = description['damage']
        demol.static = description['static']
        demol.damage_reduce = description['damage reduce']
        demol.max_speed = description['speed']
        demol.speed = description['speed']
        demol.is_collideable = description['collides']
        demol.is_gravity_affected = description['gravity affected']
        # demol.rectangle.y += randint(-150, 150)
        demol.look = actor.look
        # self.demolishers[self.location][self.demolisher_id] = ent
        self.demolishers[self.location][demol.id] = demol
        # print(f'[add_demolisher] Added: {demol.id=} {demol.name} {demol.rectangle} {demol.max_speed=} {demol.destination=}')

    def process(self, time_passed):
        self.time_passed = time_passed

        self.processing_obstacles()
        self.processing_human_input()
        self.processing_actors()
        if self.actors[self.location][0].dead:
            self.game_over()
        self.processing_demolishers()

        # Applying camera offset:
        if self.actors[self.location][0].speed > 0:
            y_offset_speed = self.actors[self.location][0].speed
        elif self.actors[self.location][0].influenced_by_obstacle >= 0:
            y_offset_speed = self.obstacles[self.location][self.actors[self.location][0].influenced_by_obstacle].speed
        else:
            y_offset_speed = 1

        self.camera.apply_offset((self.actors[self.location][0].rectangle.centerx, self.actors[self.location][0].rectangle.bottom),
                                 y_offset_speed, 5)
                                 # self.actors[self.location][0].speed * 0.9, self.actors[self.location][0].fall_speed)
        # self.detect_active_actors()
        self.detect_active_obstacles()

        self.render_all()

    def detect_active_obstacles(self):
        self.active_obstacles = list()
        for k in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][k]
            if obs.rectangle.colliderect(self.camera.active_objects_rectangle):
            # if obs.rectangle.colliderect(self.camera.rectangle):
                self.active_obstacles.append(k)

    # def detect_active_actors(self):
    #     self.active_actors = list()
    #     for k in self.obstacles[self.location].keys():
    #         obs = self.obstacles[self.location][k]
    #         if obs.rectangle.colliderect(self.camera.rectangle):
    #             self.active_obstacles.append(k

    def processing_obstacles(self):
        for key in self.obstacles[self.location].keys():
        # for key in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][key]
            obs.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers)
            # obs.percept(self.obstacles[self.location])
            obs.process_(self.time_passed)

    def processing_demolishers(self):
        dead = list()
        for key in self.demolishers[self.location].keys():
            dem = self.demolishers[self.location][key]
            if dem.dead:
                if dem.aftermath == 'explode':
                    print(f'[process demolishers] KA-BOOM!')
                dead.append(dem.id)
                continue
            if dem.is_collideable:
                dem.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None)
            if dem.static:
                actor = self.actors[self.location][dem.snap_to_actor]
                dem.update(actor.look, actor.rectangle)
            dem.process_demolisher(self.time_passed)

        for dead_id in dead:
            del self.demolishers[self.location][dead_id]

    def processing_actors(self):
        dead = list()
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            if actor.dead:
                dead.append(actor.id)
                continue
            if not actor.rectangle.colliderect(self.camera.active_objects_rectangle):
                continue
            actor.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location])
            # actor.percept(self.obstacles[self.location])
            if actor.ai_controlled:
                actor.get_target(self.actors[self.location][0])
                if not actor.ignore_user_input:
                    actor.think()
            else:
                if not actor.ignore_user_input:  # routines for Player actor
                # if key == 0 and not actor.ignore_user_input:  # routines for Player actor
                    if self.is_input_up_arrow:
                        actor.set_action('up action')
                    else:
                        # if actor.get_state() == 'up action':
                        actor.set_action('up action cancel')

                    if self.is_input_down_arrow:
                        actor.set_action('down action')
                    else:
                        # if actor.get_state() == 'down action':
                        actor.set_action('down action cancel')

                    if self.is_input_right_arrow:
                        actor.set_action('right action')
                    else:
                        # if actor.get_state() == 'right action':
                        actor.set_action('right action cancel')

                    if self.is_input_left_arrow:
                        actor.set_action('left action')
                    else:
                        # if actor.get_state() == 'left action':
                        actor.set_action('left action cancel')

                    if self.is_spacebar:
                        actor.set_action('jump action')
                    else:
                        actor.set_action('jump action cancel')

                    if self.is_l_alt and not self.l_alt_multiple_press_prevent:
                        self.l_alt_multiple_press_prevent = True
                        actor.set_action('hop back')
                    else:
                        if actor.get_state() == 'hop back progress':
                            actor.set_action('hop back action cancel')

                    if self.is_attack:
                        self.is_attack = False
                        actor.set_action('attack')

            actor.process(self.time_passed)
            if actor.summon_demolisher:
                actor.summon_demolisher = False
                # actor.current_weapon_demolishers_reveal_frames = actor.current_weapon_demolishers_reveal_frames[1:]
                # print('ATTACK!', actor.frame_number, actor.current_weapon_demolishers_reveal_frames)
                # frame =
                # frame = actor.active_frames[0]
                # actor.active_frames = actor.active_frames[1:]
                # frame = actor.current_weapon_demolishers_reveal_frames[0]
                # actor.current_weapon_demolishers_reveal_frames = actor.current_weapon_demolishers_reveal_frames[1:]
                # print(actor.summon_demolisher_counter)
                demolisher = actor.current_weapon['demolishers'][actor.summon_demolisher_counter]
                # demolisher = actor.current_weapon['demolishers'][actor.summon_demolisher_at_frame]
                # demolisher = actor.current_weapon['demolisher reveals at frame'][actor.frame_number]
                demolisher['snap to actor'] = actor.id
                # demolisher['snap points']['right'] = (0, 8)
                # demolisher['snap points']['left'] = (0, 8)
                # for k in demolisher:
                #     print(k, demolisher[k])
                # print('*' * 100)
                # self.press_any_key()
                self.add_demolisher(demolisher)
                # If, for example, actor.current_weapon_demolishers_reveal_frames at the very beginning was: [13, 17, 23, 28], so:
                # ATTACK! 13 [17, 23, 28]
                # ATTACK! 17 [23, 28]
                # ATTACK! 23 [28]
                # ATTACK! 28 []
            # actor.reset_self_flags()
        for dead_id in dead:
            del self.actors[self.location][dead_id]

    def render_background(self):
        pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

    def render_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            size = actor.current_sprite['sprite'].get_size()
            # Offset sprite to the left from the center of rectangle using anchor point.
            if actor.current_sprite_flip:
                if actor.current_sprite['sprite asymmetric']:
                    x = actor.rectangle.centerx - self.camera.offset_x \
                        - size[0] + actor.current_sprite['sprite center']
                else:
                    x = actor.rectangle.centerx - self.camera.offset_x \
                        - actor.current_sprite['sprite center']
            else:
                x = actor.rectangle.centerx - self.camera.offset_x - actor.current_sprite['sprite center']

            y = actor.rectangle.bottom - self.camera.offset_y - size[1]

            self.screen.blit(actor.current_sprite['sprite'], (x, y))

            pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - self.camera.offset_y,
                                                  actor.rectangle.width, actor.rectangle.height), 5)
            # Colliders rects:
            # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_right.x - self.camera.offset_x, actor.collision_detector_right.y - self.camera.offset_y,
            #                                       actor.collision_detector_right.width, actor.collision_detector_right.height))
            # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_left.x - self.camera.offset_x, actor.collision_detector_left.y - self.camera.offset_y,
            #                                       actor.collision_detector_left.width, actor.collision_detector_left.height))
            # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_top.x - self.camera.offset_x, actor.collision_detector_top.y - self.camera.offset_y,
            #                                       actor.collision_detector_top.width, actor.collision_detector_top.height))
            # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_bottom.x - self.camera.offset_x, actor.collision_detector_bottom.y - self.camera.offset_y,
            #                                       actor.collision_detector_bottom.width, actor.collision_detector_bottom.height))
            # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_right.x - self.camera.offset_x, actor.collision_detector_bottom_right.y - self.camera.offset_y,
            #                                       actor.collision_detector_bottom_right.width, actor.collision_detector_bottom_right.height))
            # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_left.x - self.camera.offset_x, actor.collision_detector_bottom_left.y - self.camera.offset_y,
            #                                       actor.collision_detector_bottom_left.width, actor.collision_detector_bottom_left.height))
            # pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_right.x - self.camera.offset_x, actor.collision_grabber_right.y - self.camera.offset_y,
            #                                       actor.collision_grabber_right.width, actor.collision_grabber_right.height))
            # pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_left.x - self.camera.offset_x, actor.collision_grabber_left.y - self.camera.offset_y,
            #                                       actor.collision_grabber_left.width, actor.collision_grabber_left.height))

            # The eye
            gaze_direction_mod = 0 if actor.look == -1 else actor.rectangle.width - 10
            pygame.draw.rect(self.screen, CYAN, (actor.rectangle.x + gaze_direction_mod - self.camera.offset_x, actor.rectangle.centery - 10 - self.camera.offset_y,
                                                  10, 20))
            # Enemies Health bar.
            if actor.id != 0:
                pygame.draw.rect(self.screen, WHITE, (actor.rectangle.x - self.camera.offset_x - 2, actor.rectangle.y - 12 - self.camera.offset_y,
                                                     actor.rectangle.width + 4, 7), 1)
                pygame.draw.rect(self.screen, RED, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - 10 - self.camera.offset_y,
                                                     actor.health * actor.rectangle.width // actor.max_health, 3))


    def render_demolishers(self):
        for key in self.demolishers[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            dem = self.demolishers[self.location][key]
            pygame.draw.rect(self.screen, PINK, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
                                                  dem.rectangle.width, dem.rectangle.height))
            # self.screen.blit(fonts.all_fonts[20].render(str(dem.id) + ' ' + str(dem.speed) + ' ' + str(dem.rectangle.y), True, CYAN),
            #                  (dem.rectangle.x - self.camera.offset_x, dem.rectangle.bottom - self.camera.offset_y + dem.id * 20))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            if key not in self.active_obstacles:
                continue
            obs = self.obstacles[self.location][key]
            if obs.is_being_collided_now:
                color = RED
            else:
                color = WHITE if obs.is_ghost_platform else CYAN
            pygame.draw.rect(self.screen, color, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))
            if obs.active:
                dx = 10
                stats_y = 1
                gap = 1
                font_size = 10
                params = (
                    #
                    #(' IS ON OBS: ' + str(self.actors[self.location][0].is_on_obstacle), WHITE),
                    ('      ACTIVE    : ' + str(obs.active), BLACK),
                    ('WAIT COUNTER    : ' + str(obs.wait_counter), BLACK),
                    ('DEST REACHED    : ' + str(obs.is_destination_reached), BLACK),
                    ('RECTANGLE       : ' + str(obs.rectangle), BLACK),
                    ('ACTION          : ' + str(obs.actions[obs.actions_set_number][obs.current_action]), BLACK),
                    ('NEED NEXT ACTION: ' + str(obs.need_next_action), BLACK),
                    ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), BLACK),
                    'CR',
                    # ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), BLACK),


                )
                for p in params:
                    if p == 'CR':
                        dx += 300
                        gap = 1
                        continue
                    self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1]),
                                     (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
                    gap += font_size
            else:
                dx = 10
                stats_y = 1
                gap = 1
                font_size = 10
                params = (
                    #
                    #(' IS ON OBS: ' + str(self.actors[self.location][0].is_on_obstacle), WHITE),
                    ('RECTANGLE       : ' + str(obs.rectangle), BLACK),
                    ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), BLACK),
                    # ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), BLACK),


                )
                for p in params:
                    if p == 'CR':
                        dx += 300
                        gap = 1
                        continue
                    self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1]),
                                     (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
                    gap += font_size


    def render_all(self):
        self.render_background()
        self.render_obstacles()
        self.render_demolishers()
        self.render_actors()
        self.render_debug_info()
        self.render_info_panel_overlay()

    def render_info_panel_overlay(self):
        # Player stats:
        start_x = 50
        start_y = MAXY - 100
        max_stripes_width = 500
        gap_between_stripes = 10
        font_size = 12
        params = (
            ('HEALTH:' + str(int(self.actors[self.location][0].max_health)) + '/' + str(int(self.actors[self.location][0].health)),int(self.actors[self.location][0].health * max_stripes_width // self.actors[self.location][0].max_health), RED),
            # ('BLOOD VOLUME(' + str(int(actor.body_state['blood volume'])) + '):', int(actor.body_state['blood volume']*stripes_width//actor.body_state['max blood volume']), RED),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[2]), (start_x, start_y + gap_between_stripes))
            pygame.draw.rect(self.screen, p[2], (start_x + 200 ,start_y+gap_between_stripes, p[1],10))
            gap_between_stripes += font_size

    def load(self):
        # try:
        #     with open('locations_'+self.location+'.dat', 'rb') as f:
        #         loaded_data = pickle.load(f)
        # except FileNotFoundError:
        #     self.obstacles[self.location] = dict()
        #     return

        # for d in loaded_data:
        # print(f'{d}: {loaded_data[d]}')  #
        # print('*' * 100)
        # self.obstacles[self.location] = loaded_data
        if self.location not in self.locations.keys():
            self.locations[self.location] = dict()
            self.obstacles[self.location] = dict()
            self.demolishers[self.location] = dict()
        self.locations[self.location] = locations[self.location]
        for obs in self.locations[self.location]['obstacles']['obs rectangles']:
            self.add_obstacle(obs)
        for dem in self.locations[self.location]['demolishers']['dem rectangles']:
            self.add_demolisher(dem)

        self.camera.setup(self.locations[self.location]['size'][0], self.locations[self.location]['size'][1])

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
                self.l_alt_multiple_press_prevent = False
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
                    self.spacebar_multiple_press_prevent = False
                # if event.key == K_RIGHT:
                #     self.is_attack = False
            if event.type == KEYDOWN:
                self.is_key_pressed = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    raise SystemExit()
                if event.key == K_RIGHT:
                    self.is_attack = True

                if event.key == K_d:
                    self.is_input_right_arrow = True
                if event.key == K_a:
                    self.is_input_left_arrow = True
                if event.key == K_w:
                    self.is_input_up_arrow = True
                if event.key == K_s:
                    self.is_input_down_arrow = True
                if event.key == K_SPACE:
                    if not self.spacebar_multiple_press_prevent:
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
            #
            #(' IS ON OBS: ' + str(self.actors[self.location][0].is_on_obstacle), WHITE),
            ('SCREEN OFFSETS: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), GREEN),
            ('', WHITE),
            (' RECT: ' + str(self.actors[self.location][0].rectangle), WHITE),
            ('╔ TARGET HEIGHT ╗: ' + str(self.actors[self.location][0].target_height), YELLOW),
            ('╚ TARGET WIDTH  ╝: ' + str(self.actors[self.location][0].target_width), YELLOW),
            (' FALL SPEED: ' + str(self.actors[self.location][0].fall_speed), WHITE),
            (' SPEED: ' + str(self.actors[self.location][0].speed), WHITE),
            (' LOOK: ' + str(self.actors[self.location][0].look), WHITE),
            (' HEADING: ' + str(self.actors[self.location][0].heading), WHITE),
            (' IDLE COUNT: ' + str(self.actors[self.location][0].idle_counter), (200, 100, 50)),
            (' ACTIVE FRAMES: ' + str(self.actors[self.location][0].active_frames), (200, 100, 50)),

            (' JUMP ATTEMPTS: ' + str(self.actors[self.location][0].jump_attempts_counter), YELLOW),
            (' JUST JUMPED: ' + str(self.actors[self.location][0].just_got_jumped), YELLOW),
            (' IGNORES INPUT: ' + str(self.actors[self.location][0].ignore_user_input), WHITE),
            (' __STATE: ' + str(self.actors[self.location][0].get_state()), CYAN),

            (' STAND ON GROUND: ' + str(self.actors[self.location][0].is_stand_on_ground), WHITE),
            ('HEIGHT SPACE: ' + str(self.actors[self.location][0].is_enough_height), GREEN),
            (' ABOVE SPACE: ' + str(self.actors[self.location][0].is_enough_space_above), GREEN),
            (' BELOW SPACE: ' + str(self.actors[self.location][0].is_enough_space_below), GREEN),
            (' RIGHT SPACE: ' + str(self.actors[self.location][0].is_enough_space_right), GREEN),
            (' LEFT SPACE: ' + str(self.actors[self.location][0].is_enough_space_left), GREEN),
            (' IS GRABBING: ' + str(self.actors[self.location][0].is_edge_grabbed), WHITE),
            (' INFLUENCED BY PLATFORM #: ' + str(self.actors[self.location][0].influenced_by_obstacle), WHITE),
            ('', WHITE),
            (str([str(self.demolishers[self.location][k].id) + str(self.demolishers[self.location][k].rectangle.topleft) for k in self.demolishers[self.location].keys()]),GRAY),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], BLACK), (stats_x, stats_y + gap))
            gap += font_size

    # def processing_collisions(self, checking_unit):
    #     # checking_unit.is_enough_space_left = True
    #     # checking_unit.is_enough_space_right = True
    #     checking_unit.is_enough_space_above = True
    #     checking_unit.is_enough_space_below = True
    #     checking_unit.is_stand_on_ground = False
    #     # checking_unit.is_edge_grabbed = False
    #
    #     for key in self.obstacles[self.location].keys():
    #         obs = self.obstacles[self.location][key]
    #
    #         # # Check enough spaces right and left:
    #         # if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.rectangle.width - checking_unit.speed - 2, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
    #         #     checking_unit.is_enough_space_left = False
    #         # if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
    #         #     checking_unit.is_enough_space_right = False
    #
    #         if checking_unit.fall_speed < 0:
    #             # CHECK TOP
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.top - abs(checking_unit.fall_speed),
    #                                          checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed)):
    #                 checking_unit.rectangle.top = obs.rectangle.bottom
    #                 checking_unit.is_enough_space_above = False
    #                 checking_unit.fall_speed = 0
    #                 checking_unit.is_stand_on_ground = False
    #                 continue
    #         else:
    #             # CHECK BOTTOM
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.bottom,
    #                                          checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed) + 1):
    #                 checking_unit.rectangle.bottom = obs.rectangle.top
    #                 checking_unit.is_stand_on_ground = True
    #                 checking_unit.fall_speed = 0
    #                 checking_unit.is_enough_space_below = False
    #                 checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                 self.is_spacebar = False
    #                 continue
    #
    #         # CHECK LEFT
    #         if checking_unit.look == -1:
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.speed - 10, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
    #                     # Grab over the top of an obstacle.
    #                     if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
    #                     # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
    #                         checking_unit.is_edge_grabbed = True
    #                         checking_unit.rectangle.top = obs.rectangle.top
    #                         checking_unit.fall_speed = 0
    #                         checking_unit.is_stand_on_ground = True
    #                         checking_unit.rectangle.left = obs.rectangle.right  # - 2
    #                         checking_unit.is_enough_space_left = False
    #                         checking_unit.heading[0] = 0
    #                         checking_unit.speed = 0
    #                         checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                         return
    #
    #                     # # Bounce from the wall
    #                     # if self.is_spacebar and self.is_input_left_arrow:
    #                     # # if self.is_spacebar and checking_unit.speed > 0:
    #                     #     checking_unit.look = 1
    #                     #     checking_unit.jump_attempts_counter = 1
    #                     #     checking_unit.rectangle.left = obs.rectangle.right  # - 2
    #                     #     checking_unit.is_jump = True
    #                     #     if checking_unit.speed > 0:
    #                     #         checking_unit.speed *= .8
    #                     #     else:
    #                     #         checking_unit.speed = checking_unit.max_speed * 0.7
    #                     #
    #                     #     # checking_unit.speed *= .8
    #                     #     return
    #
    #                     checking_unit.rectangle.left = obs.rectangle.right
    #                     checking_unit.is_enough_space_left = False
    #                     checking_unit.heading[0] = 0
    #                     checking_unit.speed = 0
    #                     continue
    #
    #         # CHECK RIGHT
    #         if checking_unit.look == 1:
    #             if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
    #                 # Grab over the top of an obstacle.
    #                 if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
    #                 # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
    #                     checking_unit.is_edge_grabbed = True
    #                     checking_unit.rectangle.top = obs.rectangle.top
    #                     checking_unit.fall_speed = 0
    #                     checking_unit.is_stand_on_ground = True
    #                     checking_unit.rectangle.right = obs.rectangle.left  # - 2
    #                     checking_unit.is_enough_space_right = False
    #                     checking_unit.heading[0] = 0
    #                     checking_unit.speed = 0
    #                     checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                     return
    #
    #                 # # Bounce from the wall
    #                 # if self.is_spacebar and self.is_input_right_arrow:
    #                 #     # if self.is_spacebar and checking_unit.speed > 0:
    #                 #     checking_unit.look = -1
    #                 #     checking_unit.jump_attempts_counter = 1
    #                 #     checking_unit.is_jump = True
    #                 #     if checking_unit.speed > 0:
    #                 #         checking_unit.speed *= .8
    #                 #     else:
    #                 #         checking_unit.speed = checking_unit.max_speed * 0.7
    #                 #     checking_unit.rectangle.right = obs.rectangle.left  # - 2
    #                 #     return
    #
    #                 checking_unit.rectangle.right = obs.rectangle.left
    #                 checking_unit.is_enough_space_right = False
    #                 checking_unit.heading[0] = 0
    #                 checking_unit.speed = 0
    #                 continue

    @staticmethod
    def press_any_key():
        command = None
        while command is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit()
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    command = 'key pressed'

    @staticmethod
    def press_any_key_passed():
        # command = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                # command = 'key pressed'
                # print('ok')
                return True
            # else:
            #     return False

    def game_over(self):
        print("--== G A M E   O V E R ==--")
        # self.info_windows[0].get_new_message('All survivors have died.')
        # self.info_windows[0].get_new_message("--== G A M E   O V E R ==--")
        # from misc_tools import render_text
        black_out(self.screen, self.screen, 10)
        render_text('GAME OVER', self.screen, 150, RED, 'AlbionicRegular.ttf', ('center_x', 'center_y'))
        pygame.display.flip()
        self.press_any_key()
        pygame.quit()
        exit()