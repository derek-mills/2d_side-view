import copy

import pygame
from math import sqrt, sin

import fonts
from constants import *
from graphics import *

class Entity(object):

    def __init__(self):
        self.id:int = 0
        self.type: str = ''  #
        self.name: str = ''
        # self.health: float = 0.
        # self.max_health: float = 0.
        self.got_immunity_to_demolishers = list()
        self.location: str = ''
        self.__state: str = ''
        self.idle_counter: int = 0
        self.ignore_user_input: bool = False
        self.look: int = 1  # 1: look right, -1: look left
        self.ai_controlled: bool = False
        self.performing_an_interruptable_deed: bool = False
        self.think_type: str = ''
        self.summon_demolisher = False
        self.summoned_demolishers_description = list()
        self.summon_protector = False
        self.summoned_protectors_description = list()
        self.summoned_protectors_keep_alive = list()
        # self.summoned_demolisher_description = dict()
        self.summon_particle = False
        self.summoned_particle_descriptions = list()
        # self.summon_demolisher_at_frame = 0
        self.summon_demolisher_counter = -1
        self.ttl = 0
        self.dead = False
        self.dying = False
        self.disappear_after_death = False
        self.is_destructible: bool = False
        self.current_weapon = dict()
        self.time_passed: int = 0
        self.cycles_passed: int = 0
        self.invincibility_timer: int = 0
        self.blood_color = RED
        self.has_just_stopped_demolishers = list()
        self.resistances = dict()
        self.total_damage_has_got = 0  # Variable storing a momentary amount of damage got from a single demolisher.

        # STATS
        self.normal_stamina_lost_per_second_jump = 10.
        self.normal_stamina_lost_per_hop_back = 5.5
        self.normal_stamina_lost_per_slide = 15.
        self.normal_stamina_lost_per_attack = 10.
        self.current_stamina_lost_per_attack = 0.  # Depends on current weapon penalty.
        self.normal_stamina_replenish = .1
        self.stamina_replenish_modifier = 1

        self.normal_mana_replenish = .001
        self.mana_replenish_modifier = 1
        self.normal_mana_lost_per_attack = 5.
        self.current_mana_lost_per_attack = 0.
        self.body_weight = 0
        self.strength = 0
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
        self.default_air_acceleration: float = .1
        self.air_acceleration: float = self.default_air_acceleration
        self.jump_height = 0.
        self.max_jump_height = 22.
        self.default_hop_back_jump_height_modifier: float = 2.6  # Rarely used, mostly while hopping back.
        self.hop_back_jump_height_modifier = 2.6  # Rarely used, mostly while hopping back.
        self.default_max_jump_attempts: int = 1  #
        self.max_jump_attempts: int = 1  #
        self.jump_attempts_counter: int = 0
        self.just_got_jumped: bool = False
        self.default_max_speed: float = 15.0  # Maximum speed cap for this creature
        self.max_speed: float = self.default_max_speed
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
        # print(self.demolishers_around)
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

    def set_new_desired_height(self, h, speed=0):
        self.target_height = h
        self.rectangle_height_counter = self.rectangle.height
        self.rectangle_height_counter_change_speed = speed

    def set_new_desired_width(self, w, speed=0):
        self.target_width = w
        self.rectangle_width_counter = self.rectangle.width
        self.rectangle_width_counter_change_speed = speed

    def processing_rectangle_size(self):

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
        # floor = self.rectangle.bottom
        # center = self.rectangle.centerx
        self.sprite_rectangle.width = self.current_sprite['sprite'].get_width()
        self.sprite_rectangle.height = self.current_sprite['sprite'].get_height()
        self.sprite_rectangle.bottom = self.rectangle.bottom
        self.sprite_rectangle.centerx = self.rectangle.centerx

    def process(self):
    # def process(self, time_passed):
    #     if self.id == 25:
    #         print('super process of #25')
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.die()

        self.process_animation()
        self.process_activity_at_current_animation_frame()

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

    def set_current_animation(self):
        state = self.get_state()
        # print(state)
        current_animation = state + str(self.look)
        if 'right' not in state and 'left' not in state:
            if self.look == 1:
                current_animation = state + ' right'
            else:
                current_animation = state + ' left'
        else:
            current_animation = state

        # If animation for current state does not exist, set default:
        if current_animation not in self.animations.keys():
            return
            # self.current_animation = 'stand still right'
        else:
            self.current_animation = current_animation
            self.apply_particular_animation(self.current_animation)
        self.active_frames = list(self.animations[self.current_animation]['activity at frames'].keys())

    def set_current_animation_back(self):
        state = self.get_state()
        # print(state)
        self.current_animation = state + str(self.look)
        if 'right' not in state and 'left' not in state:
            if self.look == 1:
                self.current_animation = state + ' right'
            else:
                self.current_animation = state + ' left'
        else:
            self.current_animation = state

        # If animation for current state does not exist, set default:
        if self.current_animation not in self.animations.keys():
            self.current_animation = 'stand still right'
        self.apply_particular_animation(self.current_animation)
        self.active_frames = list(self.animations[self.current_animation]['activity at frames'].keys())

    def process_activity_at_current_animation_frame(self):
        if self.frame_number in self.active_frames:
            for action in self.animations[self.current_animation]['activity at frames'][self.frame_number]:
                # print(self.frame_number, action)
                if self.animations[self.current_animation]['activity at frames'][self.frame_number][action]:
                    # IF ACTION IS TRUE:
                    if action == 'protector':
                        # print(f'[process active frames] defend at frame {self.frame_number}')
                        if 'protectors' in self.current_weapon:
                            self.summon_protector = True
                            self.summoned_protectors_description = list()
                            dem_set_num = self.animations[self.current_animation]['activity at frames'][self.frame_number]['protectors set number']
                            for d_origin in self.current_weapon['protectors'][dem_set_num]:
                                d = copy.deepcopy(d_origin)
                                d['parent'] = self
                                d['protector sprite'] = d_origin['protector sprite']
                                d['snapping offset'] = sprites[self.name + ' ' + str(self.animation_sequence[self.frame_number])]['demolisher snap point']
                                self.summoned_protectors_description.append(d)
                    elif action == 'demolisher':
                        # print(f'[process active frames] make attack at frame {self.frame_number}')
                        self.summon_demolisher = True
                        self.summoned_demolishers_description = list()
                        dem_set_num = self.animations[self.current_animation]['activity at frames'][self.frame_number]['demolishers set number']
                        for d_origin in self.current_weapon['demolishers'][dem_set_num]:
                            d = copy.deepcopy(d_origin)
                            d['parent'] = self
                            d['demolisher sprite'] = d_origin['demolisher sprite']
                            d['snapping offset'] = sprites[self.name + ' ' + str(self.animation_sequence[self.frame_number])]['demolisher snap point']
                            self.summoned_demolishers_description.append(d)
                else:
                    # Other actions
                    if action == 'move':
                        self.speed = self.animations[self.current_animation]['activity at frames'][self.frame_number]['move']
                        # print(f'[process active frames] make step at frame {self.frame_number}')
                    elif action == 'sound':
                        snd = self.animations[self.current_animation]['activity at frames'][self.frame_number]
                        # print(f'[entity.process_activity_at_current_animation_frame] make {snd} at frame {self.frame_number}')
            self.active_frames = self.active_frames[1:]


    def process_animation(self):
        # self.set_current_animation()
        if self.animation_sequence:
            self.frame_change_counter += 1
            if self.frame_change_counter > self.frames_changing_threshold:
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
                    # SOUND !!
                    # if self.animations[self.current_animation][self.look]['sound']:
                    #     if self.frame_number in self.animations[self.current_animation][self.look]['sound at frames']:
                    #         self.consider_which_sound_to_make()
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
        self.current_frame = self.animation_descriptor + ' ' + str(self.animation_sequence[self.frame_number])  # For ex., 'Jane 8'
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
        self.frames_changing_threshold = self.animations[anim]['speed'] * self.frames_changing_threshold_modifier
        self.animation_sequence = self.animations[anim]['sequence']
        self.set_current_sprite()

    def get_state(self):
        return self.__state

    def set_action(self, new_action):
        ...

    def set_state(self, new_state):
        self.__state = new_state

    def state_machine(self):
        ...

    def calculate_colliders_backup(self):
        bottom_indent = 35 if self.is_stand_on_ground else 0
        if self.look * self.movement_direction_inverter == 1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - bottom_indent)
            self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height - bottom_indent)
            if self.speed > 0 and bottom_indent > 0:
                self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, self.speed + 1, 30)
                self.collision_detector_bottom_left.update(self.rectangle.left - 1, self.rectangle.bottom - bottom_indent, 1, 30)
            else:
                self.collision_detector_bottom_right.update(0,0,0,0)
                self.collision_detector_bottom_left.update(0,0,0,0)

        elif self.look * self.movement_direction_inverter == -1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height - bottom_indent)
            self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
            if self.speed > 0 and bottom_indent > 0:
                self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, 1, 30)
                self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - bottom_indent, self.speed + 1, 30)
            else:
                self.collision_detector_bottom_right.update(0,0,0,0)
                self.collision_detector_bottom_left.update(0,0,0,0)
        # TOP and BOTTOM colliders:
        if self.fall_speed < 0:
            self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4, self.rectangle.width - 4, abs(self.fall_speed))
            self.collision_detector_bottom.update(0,0,0,0)
        elif self.fall_speed >= 0:
            self.collision_detector_top.update(0,0,0,0)
            # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
            self.collision_detector_bottom.update(self.rectangle.left +2, self.rectangle.bottom, self.rectangle.width-4, self.fall_speed + 2)
            # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, self.fall_speed + 2)

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

    # @staticmethod
    # def get_damage(self, amount):
    #     print('AUCH!')
    #     self.health -= amount
    #     if self.health <= 0:
    #         self.dead = True

    def get_time(self, time_passed, cycles_passed):
        self.time_passed = time_passed
        self.cycles_passed = cycles_passed

    def detect_demolishers_collisions(self):
        # print(self.demolishers_around)
        if self.invincibility_timer > 0:
            return
        for key in self.demolishers_around.keys():
            dem = self.demolishers_around[key]
            if dem.parent:
                if dem.id in self.got_immunity_to_demolishers or \
                    dem.parent_id == self.id or dem.parent.name == self.name:  # or \
                     # dem.floppy:
                    continue
            hit_detected = False
            if dem.invisible:
                # Just a rectangle-based collision detector:
                if self.rectangle.colliderect(dem.rectangle):
                    hit_detected = True
            else:

                current_mask = self.current_sprite['mask']
                # current_mask = self.current_sprite['mask'] if self.look == 1 else self.current_sprite['mask flipped']
                # # print(self.current_sprite)
                current_mask_rect = self.current_sprite['mask rect']
                current_mask_rect.center = self.sprite_rectangle.center
                # self.current_sprite['current mask rect'] = current_mask_rect

                # print(self.rectangle, current_mask_rect)
                # exit()
                # current_mask_rect = current_mask.get_rect(center=self.rectangle.center)
                # print(dem.current_sprite)
                current_demolisher_mask = dem.current_sprite['mask'] if dem.look == 1 else dem.current_sprite['mask flipped']
                current_demolisher_mask_rect = dem.current_sprite['mask rect']
                current_demolisher_mask_rect.center = dem.rectangle.center
                # current_demolisher_mask_rect = dem.current_sprite['mask rect'].move(dem.rectangle.topleft)
                # current_demolisher_mask_rect = current_demolisher_mask.get_rect(center=dem.rectangle.center)
                # if self.current_sprite['current mask rect'].colliderect(current_demolisher_mask_rect):
                if current_mask_rect.colliderect(current_demolisher_mask_rect):
                #     x = dem.rectangle.x - self.current_sprite['current mask rect'].x  # x coordinate relative to inner mask space
                    x = dem.rectangle.x - current_mask_rect.x  # x coordinate relative to inner mask space
                    # y = dem.rectangle.y - self.current_sprite['current mask rect'].y  # y coordinate relative to inner mask space
                    y = dem.rectangle.y - current_mask_rect.y  # y coordinate relative to inner mask space
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
                if dem.floppy:
                    # Most probably a demolishers has a collision with protector (player shield).
                    if dem.parent:
                        # self.hop_back_jump_height_modifier = ((dem.parent_strength / self.strength) + (dem.parent_weight / self.body_weight)) / dem.parent_penalty
                        self.movement_direction_inverter = -1 if dem.parent.look != self.look else 1
                        forces_balance = ((dem.parent_strength + dem.parent_weight) / dem.parent_penalty) / (self.strength + self.body_weight)
                        # forces_balance = ((dem.parent_strength / self.strength) + (dem.parent_weight / self.body_weight)) / dem.parent_penalty
                        self.speed = 5 + forces_balance
                        print(f'{dem.total_damage_amount=} {forces_balance=} {dem.parent_penalty=}')
                    else:
                        self.movement_direction_inverter = -1 if dem.look != self.look else 1
                        forces_balance = 0.1
                        self.speed = 3
                        print(f'{dem.total_damage_amount=} {forces_balance=} {dem.parent_penalty=}')
                    if 'smash' in dem.damage.keys():
                        self.speed *= 1.5
                    if self.stats['stamina'] > 0:
                        self.stamina_reduce(dem.total_damage_amount * forces_balance * 0.08)
                        self.invincibility_timer = 20
                        # self.stamina_reduce(dem.total_damage_amount * forces_balance * 0.08)
                        continue

                if not dem.pierce and not self.dead:
                    self.has_just_stopped_demolishers.append(dem.id)

                self.summon_particle = True
                self.invincibility_timer = 30
                if not self.dead:  # or not self.dying:
                    # If actor hit from behind, the damage increased by 50%:
                    total_damage_multiplier = 1.5 if dem.look == self.look and dem.snap_to_actor >= 0 else 1
                    self.get_damage(dem.damage, total_damage_multiplier)
                    # self.invincibility_timer = 100 if self.id == 0 else 30

                    # Damage amount show:
                    txt_color = RED if self.id == 0 else WHITE
                    sprite = fonts.all_fonts[40].render(str(int(self.total_damage_has_got)), True, txt_color)
                    # if self.total_damage_has_got > 0:
                    #     self.invincibility_timer = 30
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
                        'color': txt_color,
                        'look': dem.parent.look if dem.parent else 1,
                        # 'look': self.look * -1,  # Splatter always fly in the opposite direction
                        'speed': 1 + randint(6, 8),
                        'jump height': 15,
                        # 'jump height': randint(15, 20),
                        'collides': True,
                        'gravity affected': True
                    })

                if 'smash' in dem.damage.keys():
                    if self.get_state() not in ('hold stash', 'carry stash right', 'carry stash left'):
                        if dem.parent:
                            # print('sdsdsadasdsadasd')
                            self.hop_back_jump_height_modifier = ((dem.parent_strength + dem.parent_weight) / (self.strength + self.body_weight))  # / dem.parent_penalty
                            # self.hop_back_jump_height_modifier = ((dem.parent_strength / self.strength) + (dem.parent_weight / self.body_weight)) / dem.parent_penalty
                            self.movement_direction_inverter = -1 if dem.parent.look != self.look else 1
                            # if dem.parent.look != self.look:
                            #     self.set_state('hop back')
                            # else:
                            #     self.set_state('hop forward')
                            # self.movement_direction_inverter = -1 if dem.parent.look != self.look else 1
                        else:
                            self.movement_direction_inverter = -1 if dem.look != self.look else 1
                            # if dem.look != self.look:
                            #     self.set_state('hop back')
                            # else:
                            #     self.set_state('hop forward')
                            # self.movement_direction_inverter = -1 if dem.look != self.look else 1
                        # if self.get_state() != 'lie dead':
                        self.set_state('hopping prepare')
                        # self.set_state('hop back')

                # Blood splatters:
                if 'slash' in dem.damage.keys():
                # if 'slash' in dem.attack_type:
                    # self.summon_particle = True
                    for particle_quantity in range(randint(12, 12 + dem.damage['slash'] // 10)):
                    # for particle_quantity in range(randint(10, 20)):
                        size = randint(1, max(2, int(dem.damage['slash']) >> 4))
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

                # print('[detect_demolishers_collisions] actor get damage in state:', self.__state)


    def check_condition(self):
        if self.dead or self.dying:
            # if self.get_state() != 'lie dead':
            #     self.set_state('lie dead')
            return
        if int(self.stats['stamina']) < self.stats['target stamina']:
            self.stats['target stamina'] -= 1
        elif int(self.stats['stamina']) > self.stats['target stamina']:
            self.stats['target stamina'] += 1

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
            self.set_state('dying')
            # print(f'[check condition] {self.name} (#{self.id}): change state to *DYING* | HP: {self.stats["health"]}')
            # self.dying = True
            # self.dead = True

    def get_damage(self, damage, damage_multiplier):
        # if self.dead:
        #     return
        # print(f'[entity.get_damage] incoming damage dealt to {self.name} | {self.stats["health"]=}')
        self.total_damage_has_got = 0
        for damage_type in damage:
            d = damage[damage_type] * self.resistances[damage_type] * damage_multiplier
            self.stats['health'] -= d
            # self.stats['health'] -= d
            self.total_damage_has_got += d

        # if self.stats['health'] <= 0:
        #     self.set_state('dying')
        #     print(f'[entity.get_damage] {self.name} {self.id} ***DYING*** | {self.stats["health"]=}')
        #     # self.dying = True
        #     # self.dead = True
        #     # self.set_state('lie dead')

    def mana_reduce(self, amount):
        if self.stats['mana'] == 0:
            return
        self.stats['mana'] -= amount
        if self.stats['mana'] < 0:
             self.stats['mana'] = 0

    def mana_replenish(self):
        if self.stats['mana'] > self.stats['max mana']:
            self.stats['mana'] = self.stats['max mana']
            return
        elif self.stats['mana'] == self.stats['max mana']:
            return
        else:
            self.stats['mana'] += (self.normal_mana_replenish * self.mana_replenish_modifier)

    def stamina_reduce(self, amount):
        # if self.id == 0:
        #     print(f'[entity stamina reduce] player stamina reduced by amount: {amount}')
        if self.stats['stamina'] > 0:
            # return
            self.stats['stamina'] -= amount
        # if self.stats['stamina'] < 0:
        #      self.stats['stamina'] = 0

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
            self.stats['stamina'] += (self.normal_stamina_replenish * self.stamina_replenish_modifier)

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
            # obs.trigger_activated = False
            obs.is_being_collided_now = False
            # obs.trigger_activated = False
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
                self.collided_bottom = True
                # if self.collided_top:
                #     self.ignore_user_input = True

                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id and obs.active:
                    self.set_state('release edge')
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

        #-----------------------------------
        # Check RIGHT
        for key in self.sorted_obs['right']:
            obs = self.obstacles_around[key]
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
                    self.speed -= self.acceleration
                else:
                    self.speed -= self.air_acceleration
                self.speed = max(self.speed, 0)
        else:
            if self.speed < self.max_speed:
                if self.is_stand_on_ground:
                    self.speed += self.acceleration
                else:
                    self.speed += self.air_acceleration

        if self.speed <= 0:
            self.movement_direction_inverter = 1

        self.potential_moving_distance = self.speed

    def move(self):
        self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter)

    def die(self):
        self.dead = True