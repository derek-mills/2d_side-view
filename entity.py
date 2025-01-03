import copy

# import pygame
from math import sqrt, sin

import fonts
# from constants import *
from graphics import *
from misc_tools import check_lines_intersection

class Entity(object):

    def __init__(self):
        self.id:int = 0
        self.type: str = ''  #
        self.name: str = ''
        # self.health: float = 0.
        # self.max_health: float = 0.
        self.combo_counter: int = 0
        self.combo_set_number: int = 0
        # self.got_immunity_to_demolishers = set()
        self.got_immunity_to_demolishers = list()
        self.demolisher_immunity_remove_counter_default = 50
        self.demolisher_immunity_remove_counter = 0
        self.location: str = ''
        self.__state: str = ''
        self.__previous_state: str = ''
        self.scheduled_state: str = ''
        self.idle_counter: int = 0
        self.hit_detected = False
        self.decay_counter_default: int = 500  # After death counter to make dead body slowly disappear.
        self.decay_counter: int = 0  # After death counter to make dead body slowly disappear.
        self.ignore_user_input: bool = False
        self.look: int = 1  # 1: look right, -1: look left
        self.ai_controlled: bool = False
        self.performing_an_interruptable_deed: bool = False
        self.think_type: str = ''
        self.summon_demolisher = False
        self.summon_kicker_demolisher = False
        self.summoned_demolishers_description = list()
        self.is_summoned_demolishers_keep_alive: bool = False
        # self.make_all_following_demolishers_floppy: bool = False
        # self.summoned_demolishers_keep_alive = list()

        self.summon_protector = False
        self.summoned_protectors_description = list()
        self.summoned_protectors_keep_alive = list()
        self.pushed_by_protector: bool = False
        self.pushing_protector_id = 0

        self.summoned_sounds = list()
        self.sounds = dict()
        # self.summoned_demolisher_description = dict()
        self.summon_particle = False
        self.summoned_particle_descriptions = list()
        # self.summon_demolisher_at_frame = 0
        self.summon_demolisher_counter = -1
        self.ttl = 0
        self.is_stunned = False
        self.stun_counter = 0
        self.dead = False
        self.dying = False
        self.disappear_after_death = False
        self.has_got_a_critical_hit = False
        self.is_destructible: bool = False
        self.current_weapon = dict()
        self.time_passed: int = 0
        self.cycles_passed: int = 0
        self.invincibility_timer: int = 0
        self.default_invincibility_timer: int = 10
        self.current_invincibility_timer: int = self.default_invincibility_timer
        self.blood_color = RED
        self.has_just_stopped_demolishers = list()
        self.resistances = {
            'slash': 1,
            'blunt': 1,
            'fire': 1,
            'pierce': 1,
            'whip': 2
        }
        # self.resistances = dict()
        self.total_damage_has_got = 0  # Variable storing a momentary amount of damage got from a single demolisher.

        # STATS
        # self.default_invincibility_time = 10
        self.force_mana_reduce = False
        self.force_mana_reduce_amount: int = 0
        self.force_stamina_reduce = False
        self.force_stamina_reduce_amount: int = 0

        self.normal_stamina_lost_per_second_jump = 10.
        self.normal_stamina_lost_per_hop_back = 15
        self.normal_stamina_lost_per_slide = 15.
        self.normal_stamina_lost_per_attack = 10.
        self.normal_stamina_lost_per_defend = 10.
        self.current_stamina_lost_per_attack = 0.  # Depends on current weapon penalty.
        self.default_normal_stamina_replenish = .1
        self.normal_stamina_replenish = self.default_normal_stamina_replenish
        self.stamina_replenish_modifier = 1

        self.default_normal_mana_replenish = .001
        self.normal_mana_replenish = .001
        self.mana_replenish_modifier = 1
        self.normal_mana_lost_per_attack = 5.
        self.normal_mana_lost_per_defend = 2.
        self.current_mana_lost_per_attack = 0.
        self.body_weight = 0
        self.body_weight_netto = 0
        self.strength = 0
        self.athletics_index = 0  # Will be calculated as strength divided by weight.
        self.stats = {
            'level': 0,
            'exp': 0,
            'health': 100.,
            'max health': 100.,
            'target health': 100.,
            'stamina': 100.,
            'max stamina': 100.,
            'target stamina': 100.,
            'mana': 100.,
            'max mana': 100.,
            'target mana': 100.,
        }
        # ANIMATION
        self.animations = dict()
        self.animation_descriptor: str = ''
        self.animation_sequence = list()
        self.animation_sequence_default = list()
        self.animation_sequence_done = False
        self.animation_not_interruptable = False
        self.current_animation: str = ''
        self.animation_change_denied: bool = False
        self.frame_number: int = 0
        self.frame_change_counter: int = 0
        self.frames_changing_threshold: float = 0.
        self.frames_changing_threshold_modifier: float = 1.
        self.frames_changing_threshold_penalty: float = 1.  # Use above 1 if got need to slow down current animation speed
        self.current_sprite_snap = 0
        self.current_sprite_flip = False
        self.current_frame = 0
        self.current_sprite = None
        self.current_sprite_xy: list = [0, 0]
        self.current_mask_xy = (0, 0)
        self.current_mask_flip = False
        self.active_frames = list()
        self.invisible: bool = False
        self.sprite_x = 0
        self.sprite_y = 0

        # GEOMETRY
        self.origin_xy: tuple = (0, 0)
        self.rectangle = pygame.Rect(0, 0, 50, 50)
        self.sprite_rectangle = pygame.Rect(0, 0, 50, 50)
        self.target_height: int = 0
        self.target_width: int = 0
        self.rectangle_height_default = 0
        self.rectangle_width_default = 0
        self.rectangle_height_sit = 0
        self.rectangle_width_sit = 0
        self.rectangle_height_slide = 0
        self.rectangle_width_slide = 0
        self.rectangle_height_counter: int = 0
        self.rectangle_height_counter_change_speed: int = 1
        self.rectangle_width_counter: int = 0
        self.rectangle_width_counter_change_speed: int = 1

        # MOVEMENT
        self.is_move_right: bool = False
        self.is_move_left: bool = False
        self.is_move_up: bool = False
        self.is_move_down: bool = False
        self.is_jump: bool = False
        self.is_crouch: bool = False
        self.is_abort_jump: bool = False
        self.is_jump_performed: bool = False
        self.default_acceleration: float = .8
        self.acceleration: float = self.default_acceleration
        self.default_friction: float = .8
        self.friction: float = self.default_friction
        self.default_air_acceleration: float = .1
        self.air_acceleration: float = self.default_air_acceleration
        self.base_max_jump_height = 22.
        self.max_jump_height = 22.
        self.jump_height = 0.
        self.default_hop_back_jump_height_modifier = self.max_jump_height // 5 # Rarely used, mostly while hopping back.
        self.hop_back_jump_height_modifier = self.default_hop_back_jump_height_modifier  # Rarely used, mostly while hopping back.
        self.default_max_jump_attempts: int = 1  #
        self.max_jump_attempts: int = 1  #
        self.jump_attempts_counter: int = 0
        self.just_got_jumped: bool = False
        self.base_max_speed: float = 15.0  # Maximum speed cap for this creature
        self.max_speed: float = self.base_max_speed
        self.speed: float = 0.
        self.max_speed_penalty = 1
        self.heading: list = [0, 0]
        # In some cases entity will move in the opposite direction; default is 1.
        # To invert direction set it to -1.
        self.movement_direction_inverter = 1
        self.travel_distance: float = 0.
        self.potential_moving_distance: float = 0.
        self.potential_falling_distance: float = 0.
        self.fall_speed: float = 0.
        self.fall_speed_correction: float = 1.0
        self.is_stand_on_ground: bool = False
        self.is_gravity_affected: bool = False
        self.destination: list = [0, 0]
        self.destination_point: list = [0, 0]
        # self.destination_area = None
        self.destination_area = pygame.Rect(0,0,0,0)
        self.vec_to_destination: list = [0, 0]
        self.exotic_movement = ''
        self.previous_location = [0, 0]
        self.shake_earth = False

        # Collisions
        self.is_collideable = False
        self.obstacles_around = None
        self.activated_triggers_list = list()
        self.sorted_obs = dict()
            # 'above': list(),
            # 'below': list(),
            # 'right': list(),
            # 'left': list(),
        self.demolishers_around = None
        self.protectors_around = None
        self.collision_detector_right = pygame.Rect(0,0,0,0)
        self.collision_detector_left = pygame.Rect(0,0,0,0)
        self.collision_detector_top = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_right = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_left = pygame.Rect(0,0,0,0)
        self.is_grabbers_active = False
        self.collision_grabber_right = pygame.Rect(0,0,0,0)
        self.collision_grabber_left = pygame.Rect(0,0,0,0)
        self.is_destination_reached: bool = False
        self.collided_top: bool = False
        self.collided_left: bool = False
        self.collided_right: bool = False
        self.collided_bottom: bool = False
        self.influenced_by_obstacle: int = -1
        self.is_edge_grabbed: bool = False
        self.is_on_ghost_platform: bool = False
        self.is_enough_space_above = False
        self.is_enough_space_below = False  # Флаг для определения возможности 'спрыгивания' со специальных платформ.
        self.is_enough_space_for_step = True  # Флаг для определения возможности сделать следующий шаг по горизонтальной платформе;
        #                                         не предусматривает отсутствие препятствия сбоку.
        self.is_enough_height = False  # Флаг для установления достаточного пространства над объектом, чтобы выпрямиться на нужную высоту.
        self.is_enough_space_right = True
        self.is_enough_space_left = True
        self.is_being_collided_now = False

        self.living_entities = None

    def percept_living_entities(self, entities):
        self.living_entities = entities

    def percept(self, obstacles, demolishers, protectors):
        self.obstacles_around = obstacles
        self.sorted_obs = {
            'above': list(),
            'below': list(),
            'right': list(),
            'left': list(),
        }
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            if obs.rectangle.centery < self.rectangle.centery:
                self.sorted_obs['above'].append(obs.id)
            elif obs.rectangle.centery > self.rectangle.centery:
                self.sorted_obs['below'].append(obs.id)
            if obs.rectangle.right < self.rectangle.centerx:
                self.sorted_obs['left'].append(obs.id)
            elif obs.rectangle.left > self.rectangle.centerx:
                self.sorted_obs['right'].append(obs.id)

        self.demolishers_around = demolishers
        self.protectors_around = protectors
        # print(self.obstacles_around)
        # if not self.protectors_around:
        #     print(f'[percept] {self.name} {self.id} doesn\'t see any protectors..')
        # exit()

    def set_rect_height(self, height):
        floor = self.rectangle.bottom
        self.rectangle.height = height
        self.rectangle.bottom = floor

    def set_rect_width(self, width):
        floor = self.rectangle.bottom
        center = self.rectangle.centerx
        right = self.rectangle.right
        left = self.rectangle.left
        self.rectangle.width = width
        if self.speed > 0:
            if self.look == 1:
                self.rectangle.left = left
            else:
                self.rectangle.right = right
        else:
            self.rectangle.centerx = center
        self.rectangle.bottom = floor

    def processing_rectangle_size_in_place(self):
        """
            This procedure changes actor's rectangle in place.
        """
        self.set_rect_width(self.target_width)
        # self.set_rect_width(self.sprite_rectangle.w)
        self.set_rect_height(self.target_height)
        # self.set_rect_height(self.sprite_rectangle.h)

    def set_new_desired_height(self, h, speed=0):
        self.target_height = h
        self.rectangle_height_counter = self.rectangle.height
        self.rectangle_height_counter_change_speed = speed

    def set_new_desired_width(self, w, speed=0):
        self.target_width = w
        self.rectangle_width_counter = self.rectangle.width
        self.rectangle_width_counter_change_speed = speed

    def processing_rectangle_size(self):
        """
            This procedure changes actor's rectangle smoothly.
            Use of this one has the point only if pure rectangles using instead of sprites.
            The procedure works with set_new_desired_height() and set_new_desired_width()
        """
        if self.target_height != self.rectangle.height:
            if self.rectangle_height_counter_change_speed == 0:
                # If height changing speed set to 0, change it instantly:
                self.set_rect_height(self.target_height)
            else:
                if self.rectangle.height > self.target_height:
                    self.rectangle_height_counter -= self.rectangle_height_counter_change_speed
                    if self.rectangle_height_counter < self.target_height:
                        self.rectangle_height_counter = self.target_height
                else:
                    self.rectangle_height_counter += self.rectangle_height_counter_change_speed
                    if self.rectangle_height_counter > self.target_height:
                        self.rectangle_height_counter = self.target_height
                self.set_rect_height(self.rectangle_height_counter)

        if self.target_width != self.rectangle.width:
            if self.rectangle_width_counter_change_speed == 0:
                # If width changing speed set to 0, change it instantly:
                self.set_rect_width(self.target_width)
            else:
                if self.rectangle.width > self.target_width:
                    self.rectangle_width_counter -= self.rectangle_width_counter_change_speed
                    if self.rectangle_width_counter < self.target_width:
                        self.rectangle_width_counter = self.target_width
                else:
                    self.rectangle_width_counter += self.rectangle_width_counter_change_speed
                    if self.rectangle_width_counter > self.target_width:
                        self.rectangle_width_counter = self.target_width
                self.set_rect_width(self.rectangle_width_counter)

    def apply_new_measurements(self):
        # self.rectangle.width = w
        # self.rectangle.height = h
        # self.rectangle_height_default = self.rectangle.height
        # self.rectangle_width_default = self.rectangle.width
        self.rectangle_height_sit = self.rectangle.height // 3 * 2
        self.rectangle_width_sit = self.rectangle.width
        self.rectangle_height_slide = self.rectangle.height // 3
        self.rectangle_width_slide = self.rectangle.height // 4 * 3

    def apply_rectangle_according_to_sprite(self):
        if self.current_sprite:
            floor = self.rectangle.bottom
            center = self.rectangle.centerx
            self.sprite_rectangle.width = self.current_sprite['sprite'].get_width()
            self.sprite_rectangle.height = self.current_sprite['sprite'].get_height()
            self.sprite_rectangle.bottom = floor
            self.sprite_rectangle.centerx = center
            # self.sprite_rectangle.bottom = self.rectangle.bottom
            # self.sprite_rectangle.centerx = self.rectangle.centerx

            self.rectangle.height = self.sprite_rectangle.h
            self.rectangle.width = self.sprite_rectangle.w // 1.5
            self.rectangle.bottom = floor
            self.rectangle.centerx = center

    def process(self):
        if self.stats['stamina'] < self.current_stamina_lost_per_attack:
            # print(f'[state machine] NOT ENOUGH STAMINA.')
            # self.frames_changing_threshold = self.animations[anim]['speed'] * self.frames_changing_threshold_modifier
            # self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
            #                                           self.frames_changing_threshold_penalty

            self.frames_changing_threshold_penalty = 2.  # x2 times slower animation
        else:
            # self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier']
            self.frames_changing_threshold_penalty = 1.

        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.die()

        if self.demolisher_immunity_remove_counter > 0:
            self.demolisher_immunity_remove_counter -= 1
        else:
            self.demolisher_immunity_remove_counter = self.demolisher_immunity_remove_counter_default
            if self.got_immunity_to_demolishers:
                self.got_immunity_to_demolishers.remove(self.got_immunity_to_demolishers[0])

        # self.process_animation()
        # self.detect_collisions_with_protectors()
        # self.process_activity_at_current_animation_frame()

        if self.is_jump:
            # Jump
            self.fall_speed = -self.jump_height
            self.is_jump = False
            self.is_stand_on_ground = False
            self.influenced_by_obstacle = -1

        # self.processing_rectangle_size()
        # self.check_space_around()  # Detect obstacles on the right and left sides
        # self.calculate_fall_speed()  # Discover speed and potential fall distance
        self.calculate_speed()       # Discover speed and potential move distance

        if abs(self.speed) > 20:
            if not self.summon_kicker_demolisher:
                demolisher = {
                    'parent': self,
                    # 'rect': pygame.Rect(0, 0, 5, self.sprite_rectangle.h),
                    'rect': pygame.Rect(0, 0, self.rectangle.w, self.rectangle.h // 2),
                    'flyer': False,
                    'snapping offset': (0,0),#self.rectangle.h),
                    # 'snapping offset': (-self.sprite_rectangle.w if self.movement_direction_inverter*self.look == -1 else self.sprite_rectangle.w, 5000),#self.rectangle.h),
                    # 'snapping offset': (-self.sprite_rectangle.w // 2 if self.movement_direction_inverter*self.look == -1 else self.sprite_rectangle.w // 2, 0),
                    'visible': False,
                    'demolisher sprite': None,
                    'type': 'blunt',
                    'pierce': False, 'demolisher TTL': 3, 'speed': 0,
                    'static': True, 'damage reduce': 0,
                    'collides': False,
                    # 'collides': True,
                    'gravity affected': False,
                    'bounce': False, 'bounce factor': 0.,
                    'push': True,
                    'impact recoil': True,
                    'sounds': {
                        'obstacle hit': 'sound_bullet_wall_hit_1',
                        'body hit': 'sound_meat_blow_1',
                        'protector hit': 'sound_bucket_hit_1',
                    },
                    'damage': {
                        'blunt': self.body_weight * self.speed * 0.01,
                    },
                    'aftermath': 'disappear'
                }
                self.summon_demolisher = True
                self.current_stamina_lost_per_attack = 0
                self.current_mana_lost_per_attack = 0
                # self.invincibility_timer = 10
                self.summoned_demolishers_description = list()
                self.summoned_demolishers_description.append(demolisher)
                self.summon_kicker_demolisher = True
                self.is_summoned_demolishers_keep_alive = True
                # self.summoned_demolishers_keep_alive.append(demolisher)
        else:
            if self.summon_kicker_demolisher:
                self.summon_kicker_demolisher = False
                self.is_summoned_demolishers_keep_alive = False
            # self.summoned_demolishers_keep_alive.clear()

        if self.is_collideable:
            if self.ai_controlled:
                self.is_grabbers_active = False  # "Werewolves can't climb oak trees."
            self.calculate_colliders()  # Calculate colliders around actor based on his current movement and fall speeds.
            self.detect_collisions()

        if self.is_destructible:  # and not self.dead:
            self.detect_demolishers_collisions()
            self.check_condition()

        if self.is_gravity_affected:
            # self.calculate_fall_speed()  # Discover speed and potential fall distance
            # self.fall()
            # print(f'FALL: ')
            if not self.is_stand_on_ground and not self.is_edge_grabbed:
                self.calculate_fall_speed()  # Discover speed and potential fall distance
                # print(f'fall! {self.fall_speed=} {self.potential_falling_distance=}')
                self.fall()
            else:
                self.potential_falling_distance = 1
                self.fall_speed = 1
        self.move()
        # self.move(time_passed)
        # self.fly(time_passed)
        self.correct_position_if_influenced()

        self.process_animation()
        self.apply_rectangle_according_to_sprite()
        self.detect_collisions_with_protectors()
        self.process_activity_at_current_animation_frame()

        # if self.animation_sequence_done:
        #     self.make_all_following_demolishers_floppy = False
        # self.total_damage_has_got = 0

    # def process_backup(self, time_passed):
    #     if self.ttl > 0:
    #         self.ttl -= 1
    #         if self.ttl == 0:
    #             self.die()
    #     self.process_animation()
    #     self.process_activity_at_current_animation_frame()
    #     if self.is_jump:
    #         # Jump
    #         self.fall_speed = -self.jump_height
    #         self.is_jump = False
    #         self.is_stand_on_ground = False
    #
    #     self.processing_rectangle_size()
    #     self.check_space_around()  # Detect obstacles on the right and left sides
    #     self.calculate_fall_speed()  # Discover speed and potential fall distance
    #     self.calculate_speed()       # Discover fall speed and potential move distance
    #     self.calculate_colliders()   # Calculate colliders around actor based on his current movement and fall speeds.
    #     self.detect_collisions()
    #     self.detect_demolishers_collisions()
    #
    #     if self.is_gravity_affected:
    #         if not self.is_stand_on_ground and not self.is_edge_grabbed:
    #             # print('fall!')
    #             self.fall()
    #     self.move(time_passed)
    #     # self.fly(time_passed)
    #     self.correct_position_if_influenced()

    def set_current_animation(self, particular_animation=''):
        if self.animation_change_denied:
            return

        state = self.get_state()
        if particular_animation:
            # print(f'[set current animation ({self.name} {self.id})] New animation: {particular_animation}')
            current_animation = particular_animation
            if self.current_weapon:
                if state == self.current_weapon['attack animation']:
                    if self.current_weapon['combo']:
                        current_animation += ' combo ' + str(self.combo_set_number)

            if 'right' not in particular_animation and 'left' not in particular_animation:
                if self.look == 1:
                    current_animation += ' right'
                else:
                    current_animation += ' left'

        else:
            current_animation = state

            if self.current_weapon:
                if state == self.current_weapon['attack animation']:
                    if self.current_weapon['combo']:
                        current_animation += ' combo ' + str(self.combo_set_number)

            if 'right' not in state and 'left' not in state:
                if self.look == 1:
                    current_animation += ' right'
                else:
                    current_animation += ' left'

        if current_animation == self.current_animation:
            # print(f'[set current animation] New animation equal to current_animation. Exit.')
            return
        # If animation for current state does not exist, set default:
        if current_animation not in self.animations.keys():
        # if current_animation not in self.animations.keys() or current_animation == self.current_animation:
            print(f'[set current animation ({self.name} {self.id})] {current_animation} not exist. Exiting with animation: {self.current_animation} ')
            return
            # self.current_animation = 'stand still right'
        else:
            self.current_animation = current_animation
            self.apply_particular_animation(self.current_animation)
        self.active_frames = list(self.animations[self.current_animation]['activity at frames'].keys())
        # print(f'[set current animation] exiting with animation: {self.current_animation} ')

    # def set_current_animation_back(self):
    #     state = self.get_state()
    #     # print(state)
    #     self.current_animation = state + str(self.look)
    #     if 'right' not in state and 'left' not in state:
    #         if self.look == 1:
    #             self.current_animation = state + ' right'
    #         else:
    #             self.current_animation = state + ' left'
    #     else:
    #         self.current_animation = state
    #
    #     # If animation for current state does not exist, set default:
    #     if self.current_animation not in self.animations.keys():
    #         self.current_animation = 'stand still right'
    #     self.apply_particular_animation(self.current_animation)
    #     self.active_frames = list(self.animations[self.current_animation]['activity at frames'].keys())

    def process_activity_at_current_animation_frame(self):
        # print(self.active_frames)
        if self.frame_number in self.active_frames:
            # print(self.frame_number, self.active_frames)
            for action in self.animations[self.current_animation]['activity at frames'][self.frame_number]:
                # print(self.frame_number, action)
                if self.animations[self.current_animation]['activity at frames'][self.frame_number][action]:
                    # IF ACTION IS TRUE:
                    if action == 'protector' and not self.summon_protector:
                        # print(f'[process active frames] defend at frame {self.frame_number}')
                        if 'protectors' in self.current_weapon:
                            # print(f'[process active frames] defend at frame {self.frame_number}')
                            self.summon_protector = True
                            self.summoned_protectors_description = list()
                            protector_set_num = self.animations[self.current_animation]['activity at frames'][self.frame_number]['protectors set number']
                            for p_origin in self.current_weapon['protectors'][protector_set_num]:
                                p = copy.deepcopy(p_origin)
                                p['parent'] = self
                                p['protector sprite'] = p_origin['protector sprite']
                                p['snapping offset'] = sprites[self.name + ' ' + str(self.animation_sequence[self.frame_number])]['demolisher snap point']
                                self.summoned_protectors_description.append(p)
                    elif action == 'demolisher':
                        # print(f'[process active frames] make attack at frame {self.frame_number}')
                        # if self.pushed_by_protector:
                        #     continue
                        # self.summoned_demolishers_description = list()
                        dem_set_num = self.animations[self.current_animation]['activity at frames'][self.frame_number]['demolishers set number']
                        # if self.current_weapon['attack animation'] != self.current_animation:
                        #     return
                        if dem_set_num > len(self.current_weapon['demolishers']) - 1:
                            return
                        try:
                            for d_origin in self.current_weapon['demolishers'][dem_set_num]:
                                d = copy.deepcopy(d_origin)
                                d['parent'] = self
                                d['demolisher sprite'] = d_origin['demolisher sprite']
                                d['snapping offset'] = sprites[self.name + ' ' + str(self.animation_sequence[self.frame_number])]['demolisher snap point']
                                self.summoned_demolishers_description.append(d)
                        except IndexError:
                            print(f'[process activity at frames ({self.name} {self.id})] ERROR! anmtn: {self.current_animation}, {self.current_weapon["label"]}')
                            print(f'[process activity at frames ({self.name} {self.id})] ERROR! {self.get_state()}')
                            exit()
                        self.summon_demolisher = True
                    elif action == 'jump':
                        # self.set_action('jump')
                        if self.is_stand_on_ground:
                            self.fall_speed = -self.animations[self.current_animation]['activity at frames'][self.frame_number]['jump']
                    elif action == 'move':
                        self.speed = self.animations[self.current_animation]['activity at frames'][self.frame_number]['move']
                        self.heading[0] = self.look
                        # print(f'[process active frames] make step at frame {self.frame_number}')
                    elif action == 'shake earth':
                        self.shake_earth = True
                    elif action == 'sound':
                        snd = self.animations[self.current_animation]['activity at frames'][self.frame_number]['sound']
                        self.summoned_sounds.append(snd)
                        # print(f'[entity.process_activity_at_current_animation_frame] make {snd} at frame {self.frame_number}')
                    elif action == 'invincibility':
                        self.invincibility_timer = self.animations[self.current_animation]['activity at frames'][self.frame_number]['invincibility']
            self.active_frames = self.active_frames[1:]


    def process_animation(self):
        # self.set_current_animation()
        threshold = self.frames_changing_threshold * self.frames_changing_threshold_penalty * self.frames_changing_threshold_modifier
        if self.animation_sequence:
            # if not self.is_stunned:
            self.frame_change_counter += 1
            if self.frame_change_counter > threshold:
            # if self.frame_change_counter > self.frames_changing_threshold:
                # It is time to change a frame in sequence:
                self.frame_change_counter = 0
                self.frame_number += 1
                if self.frame_number > (len(self.animation_sequence) - 1):
                    # Sequence has come to an end.
                    self.frame_number = self.animations[self.current_animation]['repeat from frame']
                    # SOUND !!
                    # if self.animations[self.current_animation][self.gaze_direction]['sound']:
                    #     if self.frame_number in self.animations[self.current_animation][self.gaze_direction]['sound at frames']:
                    #         self.consider_which_sound_to_make()
                    self.animation_sequence_done = True
                    self.animation_not_interruptable = False
                    self.performing_an_interruptable_deed = False
                    # self.active_frames = list()
                    self.summon_demolisher_counter = -1
                    # self.force_visible = False
                    # print(f'[actor_process_animation_counter] {self.name} Animation sequence done, release lock from world activity.')
                    if not self.animations[self.current_animation]['repeat']:
                        # self.apply_default_animation()
                        self.active_frames = list()
                        return
                    self.active_frames = list(self.animations[self.current_animation]['activity at frames'].keys())
                else:
                    self.animation_sequence_done = False
                self.set_current_sprite()

            size = self.current_sprite['sprite'].get_size()
            if self.current_sprite_flip:
                if self.current_sprite['sprite asymmetric']:
                    self.sprite_x = self.rectangle.centerx - size[0] + self.current_sprite['sprite center']
                else:
                    self.sprite_x = self.rectangle.centerx - self.current_sprite['sprite center']
            else:
                self.sprite_x = self.rectangle.centerx - self.current_sprite['sprite center']

            self.sprite_y = self.rectangle.bottom - size[1]

    def set_current_sprite(self):
        try:
            self.current_frame = self.animation_descriptor + ' ' + str(self.animation_sequence[self.frame_number])  # For ex., 'Jane 8'
        except IndexError:
            print(f'[set current sprite ({self.name} {self.id})] ERROR: {self.frame_number=} {self.animation_descriptor=} {self.animation_sequence=}')
            exit()
        if self.current_frame in sprites[self.id]['sprites'][self.current_animation].keys():
            self.current_sprite = sprites[self.id]['sprites'][self.current_animation][self.current_frame]
        else:
            self.apply_particular_animation(self.current_animation)
            self.current_sprite = sprites[self.id]['sprites'][self.current_animation][self.current_frame]
        # self.apply_rectangle_according_to_sprite()

    def apply_particular_animation(self, anim):
        self.frame_number = 0
        self.frame_change_counter = 0
        self.animation_sequence_done = False
        # self.frames_changing_threshold = self.animations[anim]['speed'] * self.current_weapon['animation speed modifier']
        self.frames_changing_threshold = self.animations[anim]['speed']
        # self.frames_changing_threshold = self.animations[anim]['speed'] * self.frames_changing_threshold_modifier
        self.animation_sequence = self.animations[anim]['sequence']
        self.set_current_sprite()

    def get_state(self):
        return self.__state

    def get_previous_state(self):
        return self.__previous_state

    def set_action(self, new_action):
        ...

    def set_state(self, new_state):
        # if new_state != self.__state and self.__state not in ('slide', 'sliding'):
        self.__previous_state = self.__state[:]
        self.__state = new_state

    def state_machine(self):
        ...

    # def calculate_colliders_backup(self):
    #     bottom_indent = 35 if self.is_stand_on_ground else 0
    #     if self.look * self.movement_direction_inverter == 1:
    #         self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - bottom_indent)
    #         self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height - bottom_indent)
    #         if self.speed > 0 and bottom_indent > 0:
    #             self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, self.speed + 1, 30)
    #             self.collision_detector_bottom_left.update(self.rectangle.left - 1, self.rectangle.bottom - bottom_indent, 1, 30)
    #         else:
    #             self.collision_detector_bottom_right.update(0,0,0,0)
    #             self.collision_detector_bottom_left.update(0,0,0,0)
    #
    #     elif self.look * self.movement_direction_inverter == -1:
    #         self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height - bottom_indent)
    #         self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
    #         if self.speed > 0 and bottom_indent > 0:
    #             self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, 1, 30)
    #             self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - bottom_indent, self.speed + 1, 30)
    #         else:
    #             self.collision_detector_bottom_right.update(0,0,0,0)
    #             self.collision_detector_bottom_left.update(0,0,0,0)
    #     # TOP and BOTTOM colliders:
    #     if self.fall_speed < 0:
    #         self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4, self.rectangle.width - 4, abs(self.fall_speed))
    #         self.collision_detector_bottom.update(0,0,0,0)
    #     elif self.fall_speed >= 0:
    #         self.collision_detector_top.update(0,0,0,0)
    #         # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
    #         self.collision_detector_bottom.update(self.rectangle.left +2, self.rectangle.bottom, self.rectangle.width-4, self.fall_speed + 2)
    #         # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, self.fall_speed + 2)

    def calculate_colliders(self):
        bottom_indent = 25 #if self.is_stand_on_ground else 0
        if self.look * self.movement_direction_inverter == 1:
            # if self.speed > 0:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - bottom_indent)
            self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height)

            self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, self.speed, bottom_indent)
            # self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, self.speed + 1, bottom_indent)
            self.collision_detector_bottom_left.update(0, 0, 0, 0)
            # self.collision_grabber_right.update(self.rectangle.right-5, self.rectangle.top - 10, 30, 50)
            # self.collision_grabber_left.update(0,0,0,0)

        elif self.look * self.movement_direction_inverter == -1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height)
            self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - bottom_indent)

            self.collision_detector_bottom_right.update(0,0,0,0)
            self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - bottom_indent, self.speed , bottom_indent)
            # self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - bottom_indent, self.speed + 1, bottom_indent)
            # self.collision_grabber_right.update(0,0,0,0)
            # self.collision_grabber_left.update(self.rectangle.left - 25, self.rectangle.top - 10, 30, 50)

        # Grabbers:
        if self.is_grabbers_active:
            if self.look == 1:
                self.collision_grabber_right.update(self.rectangle.right-5, self.rectangle.top, 30, 40)
                # self.collision_grabber_right.update(self.rectangle.right-5, self.rectangle.top - 10, 30, 50)
                self.collision_grabber_left.update(0,0,0,0)
            elif self.look == -1:
                self.collision_grabber_right.update(0,0,0,0)
                self.collision_grabber_left.update(self.rectangle.left - 25, self.rectangle.top, 30, 40)
                # self.collision_grabber_left.update(self.rectangle.left - 25, self.rectangle.top - 10, 30, 50)
        else:
            self.collision_grabber_right.update(0, 0, 0, 0)
            self.collision_grabber_left.update(0, 0, 0, 0)

        # TOP and BOTTOM colliders:
        if self.fall_speed < 0:
            self.collision_detector_top.update(self.rectangle.left + 1, self.rectangle.top - abs(self.fall_speed) - 4, self.rectangle.width - 2, abs(self.fall_speed))
            # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4, self.rectangle.width - 4, abs(self.fall_speed))
            self.collision_detector_bottom.update(0,0,0,0)
            # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom, self.rectangle.width - 4, 1)
        elif self.fall_speed >= 0:
            # self.collision_detector_top.update(0,0,0,0)
            self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
            # self.collision_detector_bottom.update(self.rectangle.left, self.rectangle.bottom, self.rectangle.width, self.fall_speed + 2)
            self.collision_detector_bottom.update(self.rectangle.left +3, self.rectangle.bottom, self.rectangle.width-6, self.fall_speed + 2)


    def get_time(self, time_passed, cycles_passed):
        self.time_passed = time_passed
        self.cycles_passed = cycles_passed

    def get_target(self, target):
        ...

    def detect_collisions_with_protectors(self):
        self.pushed_by_protector = False
        if self.protectors_around:
            # print(f'[detect collision with protectors] {self.id} collision check starting...')
            for k in self.protectors_around.keys():
                p = self.protectors_around[k]
                if p.parent.id == self.id:  # or self.look != p.look:
                    continue
                actor_sprite_rect = pygame.Rect(self.sprite_x, self.sprite_y,
                                                self.sprite_rectangle.width, self.sprite_rectangle.height)
                if actor_sprite_rect.colliderect(p.rectangle):
                # if self.sprite_rectangle.colliderect(p.rectangle) and self.look != p.look:
                #     print(f'[detect collision with protectors {self.name} {self.id}] collided with protecor.')
                    # self.summoned_sounds.append(p.sounds[self.type])
                    # if 'attack' in self.get_state():
                    #     self.set_state('dizzy prepare')
                    self.pushed_by_protector = True
                    self.pushing_protector_id = k
                    return

    def detect_demolishers_collisions(self):
        # print(self.demolishers_around)
        if self.invincibility_timer > 0:
            return
        for key in self.demolishers_around.keys():
            dem = self.demolishers_around[key]
            if dem.floppy:
                continue
            if dem.parent:
                if dem.id in self.got_immunity_to_demolishers or \
                   dem.parent_id == self.id or dem.parent.name == self.name:
                    # dem.parent_id == self.id:
                    continue
            else:
                if dem.id in self.got_immunity_to_demolishers:
                    continue

            hit_detected = False

            if dem.invisible:
                if dem.flyer:
                    demolisher_trace_has_been_passed = (dem.previous_location,
                                                        dem.rectangle.topleft)
                    for line in ((self.rectangle.topleft, self.rectangle.bottomleft),
                                 (self.rectangle.bottomleft, self.rectangle.bottomright),
                                 (self.rectangle.bottomright, self.rectangle.topright),
                                 (self.rectangle.topright, self.rectangle.topleft)):
                        if check_lines_intersection(demolisher_trace_has_been_passed, line):
                            hit_detected = True
                            # print('HIT')
                            # print(f'[detect collision with protectors {self.id}] trace={self_trace_has_been_passed} protector={protector_diagonals}')
                            break
                else:
                    # Just a rectangle-based collision detector:
                    if self.rectangle.colliderect(dem.rectangle):
                    # if self.sprite_rectangle.colliderect(dem.rectangle):
                        hit_detected = True
            else:

                current_mask = self.current_sprite['mask']
                # current_mask = self.current_sprite['mask'] if self.look == 1 else self.current_sprite['mask flipped']
                # # print(self.current_sprite)
                current_mask_rect = self.current_sprite['mask rect']
                current_mask_rect.topleft = (self.sprite_x, self.sprite_y)
                # current_mask_rect.topleft = self.rectangle.topleft
                # current_mask_rect.topleft = self.sprite_rectangle.topleft
                # current_mask_rect.center = self.sprite_rectangle.center
                # self.current_sprite['current mask rect'] = current_mask_rect

                # print(self.rectangle, current_mask_rect)
                # exit()
                # current_mask_rect = current_mask.get_rect(center=self.rectangle.center)
                # print(dem.current_sprite)
                current_demolisher_mask = dem.current_sprite['mask'] if dem.look == 1 else dem.current_sprite['mask flipped']
                current_demolisher_mask_rect = dem.current_sprite['mask rect']
                current_demolisher_mask_rect.topleft = dem.rectangle.topleft
                # current_demolisher_mask_rect.center = dem.rectangle.center
                # current_demolisher_mask_rect = dem.current_sprite['mask rect'].move(dem.rectangle.topleft)
                # current_demolisher_mask_rect = current_demolisher_mask.get_rect(center=dem.rectangle.center)
                # if self.current_sprite['current mask rect'].colliderect(current_demolisher_mask_rect):
                if current_mask_rect.colliderect(current_demolisher_mask_rect):
                    x = current_demolisher_mask_rect.x - current_mask_rect.x  # x coordinate relative to inner mask space
                    y = current_demolisher_mask_rect.y - current_mask_rect.y  # y coordinate relative to inner mask space
                    # x = dem.rectangle.x - current_mask_rect.x  # x coordinate relative to inner mask space
                    # y = dem.rectangle.y - current_mask_rect.y  # y coordinate relative to inner mask space
                else:
                    continue

                # print( current_mask_rect, current_demolisher_mask_rect)
                # if current_mask_rect.colliderect(dem.rectangle):
                #     x = int(dem.rectangle.centerx - current_mask_rect.centerx)  # x coordinate relative to inner mask space
                #     y = int(dem.rectangle.centery - current_mask_rect.centery)  # y coordinate relative to inner mask space
                # else:
                #     continue

                # if current_mask.get_at((x, y)):
                if current_mask.overlap(current_demolisher_mask, (x,y)):
                    # tmp_mask_sprite = current_mask.to_surface()

                    hit_detected = True

            if hit_detected:
                # print(f'[detect demolishers collision] Dem #{dem.id} hit {self.name}')
                # print(f'[detect demolishers collision] Dem rect {dem.rectangle} self rect {self.rectangle}')
                self.hit_detected = True
                self.combo_counter = 0
                self.combo_set_number = 0
                if not dem.pierce and not self.dead:
                    self.has_just_stopped_demolishers.append(dem.id)

                if dem.parent:
                    self.get_target(dem.parent)
                    dem.become_mr_floppy()

                self.summon_particle = True
                # if dem.sounds['body hit'] not in self.summoned_sounds:
                # self.got_immunity_to_demolishers.add(dem.id)
                if dem.id not in self.got_immunity_to_demolishers:
                    self.got_immunity_to_demolishers.append(dem.id)
                if not self.dead:
                    self.summoned_sounds.append(dem.sounds['body hit'])
                    # If actor hit from behind, the damage increased by 50%:
                    total_damage_multiplier = 1.5 if dem.look == self.look else 1
                    # total_damage_multiplier = 1.5 if dem.look == self.look and dem.snap_to_actor >= 0 else 1
                    self.get_damage(dem.damage, total_damage_multiplier)
                    if int(self.total_damage_has_got) > 0:
                        state = self.get_state()
                        if state in ('hanging on edge', 'has just grabbed edge', 'climb on', 'climb on rise'):
                            self.set_state('release edge')
                            self.state_machine()
                        elif 'stash' in state:
                            self.set_state('drop stash')
                            self.state_machine()

                        # Damage amount show:
                        txt_color = RED if self.id == 0 else WHITE
                        self.summon_info_blob(str(int(self.total_damage_has_got)), txt_color, dem.parent.look if dem.parent else 1)
                        # sprite = fonts.all_fonts[30].render(str(int(self.total_damage_has_got)), True, txt_color)
                        # # if self.total_damage_has_got > 0:
                        # #     self.invincibility_timer = 30
                        # self.summoned_particle_descriptions.append({
                        #     'sprite': sprite,
                        #     'fall speed correction': 0.6,
                        #     'particle TTL': 100,
                        #     'width': sprite.get_width(),
                        #     'height': sprite.get_height(),
                        #     'xy': self.rectangle.center,
                        #     'bounce': False,
                        #     'bounce factor': 0.,
                        #     'subtype': 'text',
                        #     'color': txt_color,
                        #     'look': dem.parent.look if dem.parent else 1,
                        #     # 'look': self.look * -1,  # Splatter always fly in the opposite direction
                        #     'speed': 1 + randint(6, 8),
                        #     'jump height': 15,
                        #     # 'jump height': randint(15, 20),
                        #     'collides': True,
                        #     'gravity affected': True
                        # })

                        # Blood splatters:
                        if 'slash' in dem.damage.keys():
                            # if 'slash' in dem.attack_type:
                            # self.summon_particle = True
                            critical_hit_modifier = 3 if self.has_got_a_critical_hit else 1
                            for particle_quantity in range(randint(12 * critical_hit_modifier, 12 * critical_hit_modifier + dem.damage['slash'] // 10)):
                                # for particle_quantity in range(randint(10, 20)):
                                size = randint(1, max(2, int(dem.damage['slash']) >> 4)) * critical_hit_modifier
                                self.summoned_particle_descriptions.append({
                                    'sprite': None,
                                    'particle TTL': 100,
                                    'width': size,
                                    'height': size,
                                    'xy': self.rectangle.center,
                                    'bounce': False,
                                    'bounce factor': 0.,
                                    'subtype': 'splatter',
                                    'color': self.blood_color,
                                    'look': dem.parent.look if dem.parent else dem.look,
                                    # 'look': self.look * -1,  # Splatter always fly in the opposite direction
                                    'speed': 1 + randint(1, 8),
                                    'jump height': randint(0, 20),
                                    'collides': True,
                                    'gravity affected': True
                                })
                        self.set_state('prepare to get hurt')

                if dem.push:
                # if 'push' in dem.damage.keys():
                #     print(f'[demolishers detector] {self.name} has been smashed and thrown away.')
                    if self.get_state() not in ('hold stash', 'carry stash right', 'carry stash left'):
                        if dem.parent:
                            strength_difference = (dem.parent_strength + dem.parent_weight) / (self.strength + self.body_weight)
                            self.hop_back_jump_height_modifier = min(4, strength_difference) if strength_difference > 0.2 else 0
                            # self.hop_back_jump_height_modifier = (dem.damage['smash'] * 0.05) ** ((dem.parent_strength + dem.parent_weight) / (self.strength + self.body_weight))
                            self.movement_direction_inverter = -1 if dem.parent.look != self.look else 1
                        else:
                            strength_difference = 0
                            self.hop_back_jump_height_modifier = self.total_damage_has_got * 0.01
                            # self.hop_back_jump_height_modifier = min(3, dem.damage['smash'] * 0.1)
                            self.movement_direction_inverter = -1 if dem.look != self.look else 1

                        # print(f'[demolishers detector] {self.name} has been thrown away {strength_difference=} hop: {self.hop_back_jump_height_modifier}.')
                        if (self.movement_direction_inverter == -1 and self.is_enough_space_left or
                            self.movement_direction_inverter == 1 and self.is_enough_space_right) and self.hop_back_jump_height_modifier > 0:
                            # print(f'[demolishers collision] {self.hop_back_jump_height_modifier} {dem.damage["smash"]=}')
                            # self.scheduled_state = 'hopping prepare'
                            # self.scheduled_state ='prepare to get hurt'
                            self.set_state('prepare to get hurt and hopping')
                            self.state_machine()
                #         else:
                #             self.set_state('prepare to get hurt')
                # else:
                #     self.set_state('prepare to get hurt')

                # # Blood splatters:
                # if 'slash' in dem.damage.keys():
                # # if 'slash' in dem.attack_type:
                #     # self.summon_particle = True
                #     critical_hit_modifier = 3 if self.has_got_a_critical_hit else 1
                #     for particle_quantity in range(randint(12 * critical_hit_modifier, 12 * critical_hit_modifier + dem.damage['slash'] // 10)):
                #     # for particle_quantity in range(randint(10, 20)):
                #         size = randint(1, max(2, int(dem.damage['slash']) >> 4)) * critical_hit_modifier
                #         self.summoned_particle_descriptions.append({
                #             'sprite': None,
                #             'particle TTL': 100,
                #             'width': size,
                #             'height': size,
                #             'xy': self.rectangle.center,
                #             'bounce': False,
                #             'bounce factor': 0.,
                #             'subtype': 'splatter',
                #             'color': self.blood_color,
                #             'look': dem.parent.look if dem.parent else dem.look,
                #             # 'look': self.look * -1,  # Splatter always fly in the opposite direction
                #             'speed': 1 + randint(1, 8),
                #             'jump height': randint(0, 20),
                #             'collides': True,
                #             'gravity affected': True
                #         })



                # print('[detect_demolishers_collisions] actor get damage in state:', self.__state)

    def summon_info_blob(self, txt, color, look=1):
        sprite = fonts.all_fonts[30].render(txt, True, color)
        self.summoned_particle_descriptions.append({
            'sprite': sprite,
            'fall speed correction': 0.6,
            'particle TTL': 100,
            'width': sprite.get_width(),
            'height': sprite.get_height(),
            'xy': self.rectangle.center,
            'bounce': False,
            'bounce factor': 0.,
            'subtype': 'text',
            'color': color,
            'look': look,
            # 'look': self.look * -1,  # Splatter always fly in the opposite direction
            'speed': 1 + randint(6, 8),
            'jump height': 15,
            # 'jump height': randint(15, 20),
            'collides': True,
            'gravity affected': True
        })

    def check_condition(self):
        if self.dead or self.dying:
            # if self.get_state() != 'lie dead':
            #     self.set_state('lie dead')
            return
        # Stamina routines:
        if int(self.stats['stamina']) < self.stats['target stamina']:
            self.stats['target stamina'] -= 1
        elif int(self.stats['stamina']) > self.stats['target stamina']:
            self.stats['target stamina'] += 1
        # if self.stats['stamina'] < self.current_stamina_lost_per_attack \
        #         or self.stats['stamina'] < 0:
        #     self.frames_changing_threshold_penalty = 2
        #     self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
        #                                               self.frames_changing_threshold_penalty
        # else:
        #     self.frames_changing_threshold_penalty = 1
        #     self.frames_changing_threshold_modifier = 1
        #     self.frames_changing_threshold = self.animations[self.current_animation]['speed']

        # self.frames_changing_threshold_penalty = 2 if self.stats['stamina'] <= self.current_stamina_lost_per_attack \
        #                                            else 1


        # Mana routines:
        if int(self.stats['mana']) < self.stats['target mana']:
            self.stats['target mana'] -= 1
        elif int(self.stats['mana']) > self.stats['target mana']:
            self.stats['target mana'] += 1

        if int(self.stats['health']) < self.stats['target health']:
            self.stats['target health'] -= 1
        elif int(self.stats['health']) > self.stats['target health']:
            self.stats['target health'] += 1

        if self.stats['health'] < 0:
            self.stats['health'] = 0
            self.stats['target health'] = 0
            # # self.has_got_a_critical_hit = True
            # if self.total_damage_has_got > self.stats['health'] * 2:
            #     self.has_got_a_critical_hit = True
            self.set_state('dying')
            # print(f'[check condition] {self.name} (#{self.id}): change state to *DYING* | HP: {self.stats["health"]}')
            # self.dying = True
            # self.dead = True

    def get_damage(self, damage, damage_multiplier):
        if self.invincibility_timer > 0:
            self.total_damage_has_got = 0
            return
        # if self.dead:
        #     return
        # print(f'[entity.get_damage] incoming damage dealt to {self.name} | {self.stats["health"]=}')
        # self.total_damage_has_got = 0
        remain_health = self.stats['health']
        for damage_type in damage:
            d = damage[damage_type] * self.resistances[damage_type] * damage_multiplier
            self.stats['health'] -= d
            # self.stats['health'] -= d
            self.total_damage_has_got += d

        self.stun_counter = min(200, self.total_damage_has_got * 200 // (remain_health + 1))
        # print(f'[get damage] {self.name} has been stunned for {self.stun_counter} frames.')

        if self.total_damage_has_got >= remain_health * 2:
            self.has_got_a_critical_hit = True
        else:
            self.has_got_a_critical_hit = False

        # self.invincibility_timer = self.default_invincibility_timer

    def health_replenish(self):
        if self.stats['health'] < self.stats['max health']:
            self.stats['health'] += 1

    def mana_reduce(self, amount):
        if self.stats['mana'] < 0:
            return
        self.stats['mana'] -= amount
        if self.stats['mana'] < 0 and self.force_mana_reduce:
            self.get_damage({'blunt': -self.stats['mana']}, 1)
             # self.stats['health'] += self.stats['mana']
             # self.total_damage_has_got -= self.stats['mana']

    # def mana_reduce(self, amount):
    #     if self.stats['mana'] == 0:
    #         return
    #     self.stats['mana'] -= amount
    #     if self.stats['mana'] < 0:
    #          self.stats['mana'] = 0

    def mana_replenish(self):
        if self.stats['mana'] > self.stats['max mana']:
            self.stats['mana'] = self.stats['max mana']
            return
        elif self.stats['mana'] == self.stats['max mana']:
            return
        else:
            self.stats['mana'] += (self.normal_mana_replenish * self.mana_replenish_modifier)
            # If modifier was changed before, we have to return it to normal state.
            self.mana_replenish_modifier = 1

    def stamina_reduce(self, amount):
        # if self.id == 0:
        #     print(f'[entity stamina reduce] player stamina reduced by amount: {amount}')
        # print(f'[entity stamina reduce] {self.name}\'s stamina reduced by amount: {amount}')
        if self.stats['stamina'] < 0:
            return
        self.stats['stamina'] -= amount
        if self.stats['stamina'] < 0 and self.force_stamina_reduce:
            self.get_damage({'blunt': -self.stats['stamina']}, 1)

             # self.stats['health'] += self.stats['stamina']
             # self.total_damage_has_got -= self.stats['stamina']

    # def stamina_reduce(self, amount):
    #     # if self.id == 0:
    #     #     print(f'[entity stamina reduce] player stamina reduced by amount: {amount}')
    #     # print(f'[entity stamina reduce] {self.name}\'s stamina reduced by amount: {amount}')
    #     if self.stats['stamina'] > 0:
    #         self.stats['stamina'] -= amount
    #     # if self.stats['stamina'] < 0:
    #     #      self.stats['stamina'] = 0

    def stamina_replenish(self):
        # if self.stats['target stamina'] > self.stats['max stamina']:
        #     self.stats['target stamina'] = self.stats['max stamina']
        #     return
        # elif self.stats['target stamina'] == self.stats['max stamina']:
        #     return
        # else:
        #     self.stats['target stamina'] += (self.normal_stamina_replenish * self.stamina_replenish_modifier)
        if self.stats['stamina'] > self.stats['max stamina']:
            self.stats['stamina'] = self.stats['max stamina']
            return
        elif self.stats['stamina'] == self.stats['max stamina']:
            return
        else:
            if self.stats['stamina'] < 0:
                self.stats['stamina'] += (self.normal_stamina_replenish * self.stamina_replenish_modifier) / 2
            else:
                self.stats['stamina'] += (self.normal_stamina_replenish * self.stamina_replenish_modifier)
            self.stamina_replenish_modifier = 1


    def detect_collisions(self):
        # self.influenced_by_obstacle = None
        # sorted_obs = {
        #     'above': list(),
        #     'below': list(),
        #     'right': list(),
        #     'left': list(),
        # }
        self.collided_top = False
        self.collided_left = False
        self.collided_right = False
        self.collided_bottom =False
        self.is_being_collided_now = False
        self.is_stand_on_ground = False
        bottom_already_changed = False
        self.activated_triggers_list = list()
        # for k in self.obstacles_around.keys():
        #     self.obstacles_around[k].trigger_activated = False
        # -----------------------------------
        # Check bottom
        for key in self.sorted_obs['below']:
            obs = self.obstacles_around[key]
            if obs.invincibility_timer > 0:
                continue

            obs.is_being_collided_now = False

            # Check if obstacle is just a passable trigger for some event:
            if obs.let_actors_pass_through:
                if obs.trigger or obs.teleport:
                    # obs.trigger_activated = False
                    if obs.rectangle.colliderect(self.rectangle):
                        if self.id == 0:
                            # # obs.trigger_activated = True
                            self.activated_triggers_list.append(key)
                            continue
                continue

            # if obs.is_ghost_platform:
            if obs.rectangle.colliderect(self.collision_detector_bottom):
                if bottom_already_changed and obs.rectangle.top > self.rectangle.bottom:
                    # Current obstacle lower than the actor's rectangle after at least one bottom collision has been registered.
                    # Skip it.
                    continue

                if self.id == 0:
                    # obs.trigger_activated = True
                    self.activated_triggers_list.append(key)

                if not self.collided_bottom:
                    if self.fall_speed > 15 and self.body_weight > 100:
                        self.shake_earth = 10
                        # self.shake_earth = min(10, int(self.fall_speed * self.body_weight))
                        # print(self.shake_earth, self.fall_speed, self.body_weight)

                self.collided_bottom = True
                # if self.collided_top:
                #     self.ignore_user_input = True

                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                    self.set_state('release edge')

                # if not obs.is_being_collided_now:
                #     if self.fall_speed > 15 and self.body_weight > 100:
                #         self.shake_earth = min(10, self.fall_speed * self.body_weight)
                #         print(self.shake_earth, self.fall_speed, self.body_weight)
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                # if self.fall_speed >= 0:
                self.rectangle.bottom = obs.rectangle.top
                self.is_stand_on_ground = True
                self.influenced_by_obstacle = obs.id
                self.jump_attempts_counter = self.max_jump_attempts
                bottom_already_changed = True
                # break
                    # continue
            # else:
            #     obs.is_being_collided_now = False

        #-----------------------------------
        # Check RIGHT
        for key in self.sorted_obs['right']:
            obs = self.obstacles_around[key]
            if obs.invincibility_timer > 0:
                continue

            obs.is_being_collided_now = False
            # obs.trigger_activated = False
            if obs.is_ghost_platform:
                continue

            # Check if obstacle is just a passable trigger for some event:
            if obs.let_actors_pass_through:
                if obs.trigger or obs.teleport:
                    if self.id == 0:
                        if obs.rectangle.colliderect(self.rectangle):
                            obs.is_being_collided_now = True
                            # obs.trigger_activated = True
                            self.activated_triggers_list.append(key)
                            continue
                continue

            # GRAB over the top of an obstacle.
            if obs.let_actors_grab:
                if not self.is_stand_on_ground:
                    if self.get_state() in ('jump', 'jump cancel', 'fly right', 'fly left','stand still'):
                    # if self.get_state() in ('jump', 'jump cancel', 'run right', 'run left', 'stand still'):

                        if self.collision_grabber_right.collidepoint(obs.rectangle.topleft):
                            self.influenced_by_obstacle = obs.id
                            # # obs.trigger_activated = True
                            self.activated_triggers_list.append(key)
                            self.set_state('has just grabbed edge')
                            self.state_machine()
                            continue

            if obs.rectangle.colliderect(self.collision_detector_right):
                # if self.id == 0:
                #     # obs.trigger_activated = True
                self.activated_triggers_list.append(key)
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                self.collided_right = True

                # Check if obstacle has crawled FROM BEHIND and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 1  # Push the actor
                    self.rectangle.x += obs.vec_to_destination[0]
                    self.rectangle.y += obs.vec_to_destination[1]
                    # self.speed = 0
                    # self.influenced_by_obstacle = -1
                    # self.is_edge_grabbed = False
                    # self.potential_moving_distance = obs.rectangle.left - self.collision_detector_right.left
                    # self.rectangle.right = obs.rectangle.left
                    self.is_enough_space_right = False
                    self.heading[0] = 0
                    self.speed = 0
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        # print(f'[detect collisions] forced to release edge')
                        self.set_state('release edge')
                    if key in self.sorted_obs['above']:
                        self.sorted_obs['above'].remove(key)
                    continue

                if self.look == 1: # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                        self.rectangle.right = obs.rectangle.left - 2  # Drop down the actor
                        self.set_state('release edge')
                    else:
                        if self.movement_direction_inverter == -1:
                            continue

                        self.potential_moving_distance = obs.rectangle.left - self.collision_detector_right.left
                        # self.rectangle.right = obs.rectangle.left
                        self.is_enough_space_right = False
                        self.heading[0] = 0
                        self.speed = 0
                        continue
            #-----------------------------------
            # Check bottom-right
            if obs.rectangle.colliderect(self.collision_detector_bottom_right):
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                self.collided_right = True
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 2  # Push the actor
                    # print('gg')
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        self.set_state('release edge')
                    continue
                if self.look == 1:  # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                        self.rectangle.right = obs.rectangle.left - 2  # Drop down the actor
                        # print(f'[detect collisions] forced to release edge')
                        self.set_state('release edge')
                    else:
                        # print('ksdjhdakjdhsakjdh')
                        bottom_already_changed = True
                        self.rectangle.bottom = obs.rectangle.top
                        self.rectangle.y += self.look * 2 * self.movement_direction_inverter
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        # continue
        #-----------------------------------
        # Check LEFT
        for key in self.sorted_obs['left']:
            obs = self.obstacles_around[key]
            if obs.invincibility_timer > 0:
                continue

            obs.is_being_collided_now = False
            # obs.trigger_activated = False
            if obs.is_ghost_platform:
                continue

            # Check if obstacle is just a passable trigger for some event:
            if obs.let_actors_pass_through:
                if obs.trigger or obs.teleport:
                    if obs.rectangle.colliderect(self.rectangle):
                        if self.id == 0:
                            # obs.trigger_activated = True
                            self.activated_triggers_list.append(key)
                            continue
                continue

            # GRAB over the top of an obstacle.
            if obs.let_actors_grab:
                if not self.is_stand_on_ground:
                    if self.get_state() in ('jump', 'jump cancel', 'fly right', 'fly left','stand still'):
                    # if self.get_state() in ('jump', 'jump cancel','run right', 'run left', 'stand still'):
                        if self.collision_grabber_left.collidepoint(obs.rectangle.topright):
                            self.influenced_by_obstacle = obs.id
                            self.set_state('has just grabbed edge')
                            self.state_machine()
                            continue

            if obs.rectangle.colliderect(self.collision_detector_left):
                self.collided_left = True
                obs.is_being_collided_now = True
                self.is_being_collided_now = True

                # Check if obstacle has crawled FROM BEHIND and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 1  # Push the actor
                    self.rectangle.x += obs.vec_to_destination[0]
                    self.rectangle.y += obs.vec_to_destination[1]

                    # self.potential_moving_distance = self.collision_detector_left.right - obs.rectangle.right
                    # self.rectangle.left = obs.rectangle.right
                    self.is_enough_space_left = False
                    self.heading[0] = 0
                    self.speed = 0
                    # self.speed = 0
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        # print(f'[detect collisions] forced to release edge')
                        self.set_state('release edge')
                    if key in self.sorted_obs['above']:
                        self.sorted_obs['above'].remove(key)

                    continue


                if self.look == -1: # Obstacle is on the left, and actor also looks to the left, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                        self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
                        # print(f'[detect collisions] forced to release edge')
                        self.set_state('release edge')
                    else:

                        if self.movement_direction_inverter == -1:
                            continue

                        self.potential_moving_distance = self.collision_detector_left.right - obs.rectangle.right
                        # self.rectangle.left = obs.rectangle.right
                        self.is_enough_space_left = False
                        self.heading[0] = 0
                        self.speed = 0
                        continue
            #-----------------------------------
            # Check bottom-left
            if obs.rectangle.colliderect(self.collision_detector_bottom_left):
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 2  # Push the actor
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        self.set_state('release edge')
                    continue
                if self.look == -1:  # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                        self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
                        self.set_state('release edge')
                    else:
                        self.rectangle.bottom = obs.rectangle.top
                        self.rectangle.y += self.look * 2 * self.movement_direction_inverter
                        bottom_already_changed = True
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        continue

        # -----------------------------------
        # Check top
        for key in self.sorted_obs['above']:
            obs = self.obstacles_around[key]
            if obs.invincibility_timer > 0:
                continue

            obs.is_being_collided_now = False
            # obs.trigger_activated = False
            if obs.is_ghost_platform:
                continue

            # Check if obstacle is just a passable trigger for some event:
            if obs.let_actors_pass_through:
                if obs.trigger or obs.teleport:
                    if obs.rectangle.colliderect(self.rectangle):
                        if self.id == 0:
                            # obs.trigger_activated = True
                            self.activated_triggers_list.append(key)
                            continue
                continue

            if obs.rectangle.colliderect(self.collision_detector_top):
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                self.collided_top = True
                # if self.collided_bottom:
                #     self.ignore_user_input = True

                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                    self.set_state('release edge')

                if self.fall_speed < 0:
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    # continue

    # def check_space_above(self, desired_height):
    #     pass

    def check_space_around(self):
        self.is_enough_space_left = True
        self.is_enough_space_right = True
        self.is_enough_space_below = True
        self.is_enough_space_above = True
        self.is_enough_height = True

        # for obs in self.obstacles_around:
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            # if obs.type == 'protector':
            #     continue
            if obs.is_ghost_platform or obs.let_actors_pass_through:
                continue

            # # Check enough spaces right and left:
            if obs.rectangle.colliderect(self.rectangle.left - self.speed - 2, self.rectangle.top + 5,
                                         # self.speed + 2, self.rectangle.height):
                                         self.rectangle.width + self.speed + 2, self.rectangle.height - 10):
                                         # self.rectangle.width + self.speed + 2, self.rectangle.height - 35):
                self.is_enough_space_left = False
                continue
            if obs.rectangle.colliderect(self.rectangle.right, self.rectangle.top + 5,
                                         # self.speed + 2, self.rectangle.height):
                                         self.rectangle.width + self.speed + 2, self.rectangle.height - 10):
                                         # self.rectangle.width + self.speed + 2, self.rectangle.height - 35):
                self.is_enough_space_right = False
                continue
            # Check if there is enough space to raise:
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom - self.target_height,
                                         self.rectangle.width - 4, self.target_height):
            # if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 1,
            #                              self.rectangle.width - 4, abs(self.fall_speed) + 1):
                self.is_enough_height = False
                continue

            # Check if there is enough space ABOVE to perform a jump, for example.
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 1,
                                         self.rectangle.width - 4, abs(self.fall_speed) + 1):
                self.is_enough_space_above = False
                continue
            # Check if there is enough space BELOW
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom,
                                         self.rectangle.width - 4, abs(self.fall_speed) + GRAVITY):
                self.is_enough_space_below = False
                continue

    def fly(self):
        # print('fly', self.id)
        destination_reached_flag = False
        if self.destination_area:
            self.destination = self.destination_area.center
            if self.destination_area.collidepoint(self.rectangle.topleft):
                destination_reached_flag = True
        else:
            self.destination = self.destination_point
            if self.destination == self.rectangle.topleft:
                destination_reached_flag = True

        self.vec_to_destination = list((self.destination[0] - self.rectangle.x, self.destination[1] - self.rectangle.y))
        # print('fly', self.id, self.vec_to_destination)
        if self.vec_to_destination == (0, 0):
        # if self.vec_to_destination == (0, 0) or self.destination == self.rectangle.topleft:
            destination_reached_flag = True

        if destination_reached_flag:
            self.is_destination_reached = True
            self.speed = 0
            self.heading = [0, 0]
            return
        else:
            self.is_destination_reached = False

        distance_to_destination = sqrt(self.vec_to_destination[0] * self.vec_to_destination[0] + self.vec_to_destination[1] * self.vec_to_destination[1])
        # print(f'[fly] {self.id=} {self.vec_to_destination=} {distance_to_destination=}')
        if distance_to_destination > 0:
            # Calculate normalized vector to apply animation set correctly in the future:
            # self.heading = self.vec_to_destination.get_normalized()
            self.heading = [self.vec_to_destination[0] / distance_to_destination, self.vec_to_destination[1] / distance_to_destination]
            # print(f'[fly] {self.id=} {self.vec_to_destination} {distance_to_destination} {self.heading}')
            self.speed = self.max_speed * self.max_speed_penalty  # * 0.5
            # print(f'[fly] {self.id=} {self.vec_to_destination} {distance_to_destination} {self.heading} {self.speed=}')
            # Define the potential length of current move, depends on basic speed and passed amount of time:
            self.potential_moving_distance = self.time_passed * self.speed
            # Define current distance to travel:
            self.travel_distance = min(distance_to_destination, self.potential_moving_distance)
            # Set the length of moving vector equal to travel distance, which had already just been calculated:
            l = self.travel_distance / distance_to_destination
            self.vec_to_destination[0] *= l
            self.vec_to_destination[1] *= l

            # print(f'BEFORe: {self.rectangle.center=} {self.vec_to_destination=}')
            # self.rectangle.x += round(self.vec_to_destination[0])
            self.previous_location[0] = self.rectangle.x
            self.previous_location[1] = self.rectangle.y
            self.rectangle.x += self.vec_to_destination[0]
            # self.rectangle.y += round(self.vec_to_destination[1])
            if self.exotic_movement == 'sin':
                self.rectangle.y = self.origin_xy[1] + 200 * sin(self.rectangle.x * 0.01)
            else:
                self.rectangle.y += self.vec_to_destination[1]

            # self.rectangle.y += self.vec_to_destination[1]

        # elif self.MovementType == 'sin':
        #     # y = a + b * sin (cx + d)
        #     # a: смещает график по оси Y;
        #     # b: растяжение по оси Y (амплитуда);
        #     # c: растяжение по оси Х (с увеличением с растёт частота колебаний);
        #     # d: сдвиг графика по оси Х.
        #     self.Location[0] -= self.Speed * 10
        #     self.Location[1] = 200 + 200*sin(self.Location[0] * 0.02 )


    def calculate_fall_speed(self):
        # if not self.is_stand_on_ground:
        if self.fall_speed > GRAVITY_CAP:
            self.fall_speed = GRAVITY_CAP
        else:
            self.fall_speed += GRAVITY * self.fall_speed_correction

        if self.is_abort_jump:
            if self.fall_speed >= 0:
                self.is_abort_jump = False
            else:
                self.fall_speed = 0
                self.is_abort_jump = False
        self.potential_falling_distance = self.fall_speed
        # else:
        #     self.potential_falling_distance = 1
        #     self.fall_speed = 1

    def fall(self):
        # print(f'[FALL]')
        self.rectangle.y += self.potential_falling_distance

    def correct_position_if_influenced(self):
        if self.influenced_by_obstacle >= 0:
            if self.influenced_by_obstacle in self.obstacles_around.keys():
                obs = self.obstacles_around[self.influenced_by_obstacle]
                if obs.active:
                    self.rectangle.x += obs.vec_to_destination[0]
                    self.rectangle.y += obs.vec_to_destination[1]
                    # self.rectangle.x += round(obs.vec_to_destination[0])
                    # self.rectangle.y += round(obs.vec_to_destination[1])

    def calculate_speed(self):
        if self.heading[0] == 0:
            if self.speed > 0:
                if self.is_stand_on_ground:
                    self.speed -= self.friction
                    # self.speed -= self.acceleration
                else:
                    self.speed -= self.air_acceleration
                self.speed = max(self.speed, 0)
        else:
            if self.speed < self.max_speed:
                if self.is_stand_on_ground:
                    self.speed += self.acceleration
                else:
                    self.speed += self.air_acceleration
            else:
                self.speed = self.max_speed

        # self.speed *= self.max_speed_penalty

        if self.speed == 0:
        # if self.speed <= 0:
            self.movement_direction_inverter = 1

        self.potential_moving_distance = self.speed

    def move(self):
        self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter)

    def die(self):
        self.dead = True

    def calculate_athletics_index(self):
        # The lesser this index -- the greater the max speed and jump height.
        self.athletics_index = self.body_weight / self.strength
        print(f'[calc athletics] {self.name} has athletic index: {self.athletics_index}')

    def calculate_max_jump_height_and_speed(self):
        # print(f'[calculate_max_jump_height_and_speed] enter...')
        self.max_jump_height = self.base_max_jump_height - self.athletics_index * 0.5
        # self.max_jump_height = self.base_max_jump_height - self.base_max_jump_height * self.athletics_index
        self.max_speed = self.base_max_speed - self.athletics_index * 0.1
        print(f'[calc max speed and jump] {self.name}: {self.max_jump_height=} {self.max_speed=} {self.base_max_speed=}')
        # self.max_speed = self.base_max_speed - self.base_max_speed * self.athletics_index
