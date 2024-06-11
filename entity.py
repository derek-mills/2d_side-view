import pygame
from math import sqrt
from constants import *
from graphics import *

class Entity(object):

    def __init__(self):
        self.id:int = 0
        self.type: str = ''  #
        self.name: str = ''
        self.health: float = 0.
        self.max_health: float = 0.
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
        # self.summon_demolisher_at_frame = 0
        self.summon_demolisher_counter = -1
        self.ttl = 0
        self.dead = False

        # ANIMATION
        self.animations = dict()
        self.animation_descriptor: str = ''
        self.animation_sequence = None
        self.animation_sequence_default = None
        self.animation_sequence_done = False
        self.animation_not_interruptable = False
        self.current_animation: str = ''
        self.frame_number: int = 0
        self.frame_change_counter: int = 0
        self.frames_changing_threshold: float = 0.
        self.frames_changing_threshold_modifier: float = 1.
        self.current_sprite_snap = 0
        self.current_sprite_flip = False
        self.current_frame = 0
        self.current_sprite = None
        self.current_sprite_xy: list = [0, 0]
        self.current_mask_xy = (0, 0)
        self.current_mask_flip = False
        self.active_frames = list()

        # GEOMETRY
        self.origin_xy: tuple = (0, 0)
        self.rectangle = pygame.Rect(0, 0, 50, 50)
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
        self.default_acceleration: float = .8
        self.acceleration: float = self.default_acceleration
        self.default_air_acceleration: float = .1
        self.air_acceleration: float = self.default_air_acceleration
        self.speed: float = 0.
        self.jump_height: int = 0
        self.max_jump_height: int = 22
        self.max_jump_attempts: int = 1  #
        self.jump_attempts_counter: int = 0
        self.just_got_jumped: bool = False
        self.default_max_speed: float = 15.0  # Maximum speed cap for this creature
        self.max_speed: float = self.default_max_speed
        self.max_speed_penalty = 1
        self.heading: list = [0, 0]
        # In some cases entity will move in the opposite direction; default is 1.
        # To invert direction set it to -1.
        self.movement_direction_inverter = 1
        self.travel_distance: float = 0.
        self.potential_moving_distance: float = 0.
        self.potential_falling_distance: float = 0.
        self.fall_speed: float = 0.
        self.is_stand_on_ground: bool = False
        self.is_gravity_affected: bool = False
        # self.destination_list = list()
        # self.destination_point = 0
        self.destination: list = [0, 0]
        self.vec_to_destination: list = [0, 0]

        # Collisions
        self.is_collideable = False
        self.obstacles_around = None
        self.demolishers_around = None
        self.collision_detector_right = pygame.Rect(0,0,0,0)
        self.collision_detector_left = pygame.Rect(0,0,0,0)
        self.collision_detector_top = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_right = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_left = pygame.Rect(0,0,0,0)
        self.is_grabbers_active = True
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

        

    def percept(self, obstacles, demolishers):
        self.obstacles_around = obstacles
        self.demolishers_around = demolishers
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


    def process(self, time_passed):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.die()
        self.process_animation()
        self.process_activity_at_current_animation_frame()
        if self.is_jump:
        # if self.is_jump and self.jump_attempts_counter > 0:
            # Jump
            self.fall_speed = -self.jump_height
            self.is_jump = False
            self.is_stand_on_ground = False

        self.processing_rectangle_size()
        self.check_space_around()  # Detect obstacles on the right and left sides
        self.calculate_fall_speed()  # Discover speed and potential fall distance
        self.calculate_speed()       # Discover fall speed and potential move distance
        self.calculate_colliders()   # Calculate colliders around actor based on his current movement and fall speeds.
        self.detect_collisions()
        self.detect_demolishers_collisions()

        if self.is_gravity_affected:
            # if self.influenced_by_obstacle:
            #     self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            # else:
            # if not self.is_stand_on_ground or not self.is_edge_grabbed:
            if not self.is_stand_on_ground and not self.is_edge_grabbed:
                # self.influenced_by_obstacle = None
                # print('fall!')
                self.fall()
        self.move(time_passed)
        # self.fly(time_passed)
        self.correct_position_if_influenced()
        # if self.influenced_by_obstacle:
        #     print('dd')
        #     self.rectangle.x += self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[0]

    def set_current_animation(self):
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
                if action == 'move':
                    self.speed = self.animations[self.current_animation]['activity at frames'][self.frame_number]['move']
                    # print(f'[process active frames] make step at frame {self.frame_number}')
                elif action == 'demolisher':
                    # print(f'[process active frames] make attack at frame {self.frame_number}')
                    self.summon_demolisher = True
                    self.summon_demolisher_counter += 1
                elif action == 'sound':
                    snd = self.animations[self.current_animation]['activity at frames'][self.frame_number]
                    print(f'[process active frames] make {snd} at frame {self.frame_number}')
            self.active_frames = self.active_frames[1:]


    def process_animation(self):
        # self.set_current_animation()
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

    def set_current_sprite(self):
        self.current_frame = self.animation_descriptor + ' ' + str(self.animation_sequence[self.frame_number])  # For ex., 'Jane 8'
        if self.current_frame in sprites[self.id]['sprites'][self.current_animation].keys():
            self.current_sprite = sprites[self.id]['sprites'][self.current_animation][self.current_frame]
        else:
            self.apply_particular_animation(self.current_animation)
            self.current_sprite = sprites[self.id]['sprites'][self.current_animation][self.current_frame]

    def apply_particular_animation(self, anim):
        self.frame_number = 0
        self.frame_change_counter = 0
        self.animation_sequence_done = False
        self.frames_changing_threshold = self.animations[anim]['speed'] * self.frames_changing_threshold_modifier
        self.animation_sequence = self.animations[anim]['sequence']
        self.set_current_sprite()

    def get_state(self):
        return self.__state

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
            self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - bottom_indent, self.speed + 1, bottom_indent)
            self.collision_detector_bottom_left.update(0, 0, 0, 0)
            self.collision_grabber_right.update(self.rectangle.right-5, self.rectangle.top - 10, 30, 50)
            self.collision_grabber_left.update(0,0,0,0)
            # self.collision_grabber_left.update(self.rectangle.top, self.rectangle.left - 20, 20, 40)

        elif self.look * self.movement_direction_inverter == -1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height)
            self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - bottom_indent)
            self.collision_detector_bottom_right.update(0,0,0,0)
            self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - bottom_indent, self.speed + 1, bottom_indent)
            self.collision_grabber_right.update(0,0,0,0)
            # self.collision_grabber_right.update(self.rectangle.top, self.rectangle.right, 20, 40)
            self.collision_grabber_left.update(self.rectangle.left - 25, self.rectangle.top - 10, 30, 50)

        # Grabbers:
        if self.is_grabbers_active:
            if self.look == 1:
                self.collision_grabber_right.update(self.rectangle.right-5, self.rectangle.top - 10, 30, 50)
                self.collision_grabber_left.update(0,0,0,0)
            elif self.look == -1:
                self.collision_grabber_right.update(0,0,0,0)
                self.collision_grabber_left.update(self.rectangle.left - 25, self.rectangle.top - 10, 30, 50)
        else:
            self.collision_grabber_right.update(0, 0, 0, 0)
            self.collision_grabber_left.update(0, 0, 0, 0)

        # TOP and BOTTOM colliders:
        if self.fall_speed < 0:
            self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4, self.rectangle.width - 4, abs(self.fall_speed))
            self.collision_detector_bottom.update(0,0,0,0)
            # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom, self.rectangle.width - 4, 1)
        elif self.fall_speed >= 0:
            # self.collision_detector_top.update(0,0,0,0)
            self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
            self.collision_detector_bottom.update(self.rectangle.left, self.rectangle.bottom, self.rectangle.width, self.fall_speed + 2)
            # self.collision_detector_bottom.update(self.rectangle.left +2, self.rectangle.bottom, self.rectangle.width-4, self.fall_speed + 2)

    # @staticmethod
    # def get_damage(self, amount):
    #     print('AUCH!')
    #     self.health -= amount
    #     if self.health <= 0:
    #         self.dead = True

    def detect_demolishers_collisions(self):
        for key in self.demolishers_around.keys():
            dem = self.demolishers_around[key]
            if dem.id in self.got_immunity_to_demolishers or dem.parent_id == self.id:
                continue
            if self.rectangle.colliderect(dem.rectangle):
                self.get_damage(dem.damage)
                self.got_immunity_to_demolishers.append(dem.id)
                self.set_state('hop back')

    def get_damage(self, amount):
        print('AUCH!')
        self.health -= amount
        if self.health <= 0:
            self.dead = True

    def detect_collisions(self):
        # self.influenced_by_obstacle = None
        sorted_obs = {
            'above': list(),
            'below': list(),
            'right': list(),
            'left': list(),
        }
        self.collided_top = False
        self.collided_left = False
        self.collided_right = False
        self.collided_bottom =False
        self.is_being_collided_now = False
        # self.ignore_user_input = False
        self.is_stand_on_ground = False
        bottom_already_changed = False

        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            if obs.rectangle.centery < self.rectangle.centery:
                sorted_obs['above'].append(obs.id)
            elif obs.rectangle.centery > self.rectangle.centery:
                sorted_obs['below'].append(obs.id)
            if obs.rectangle.right < self.rectangle.centerx:
                sorted_obs['left'].append(obs.id)
            elif obs.rectangle.left > self.rectangle.centerx:
                sorted_obs['right'].append(obs.id)

        # for key in self.obstacles_around.keys():
        #     obs = self.obstacles_around[key]
        #     if obs.rectangle.centery < self.rectangle.centery:
        #         sorted_obs['above'].append(obs.id)
        #     elif obs.rectangle.centery > self.rectangle.centery:
        #         sorted_obs['below'].append(obs.id)
        #     if obs.rectangle.centerx < self.rectangle.centerx:
        #         sorted_obs['left'].append(obs.id)
        #     elif obs.rectangle.centerx > self.rectangle.centerx:
        #         sorted_obs['right'].append(obs.id)

        #-----------------------------------
        # Check RIGHT
        for key in sorted_obs['right']:
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue

            # GRAB over the top of an obstacle.
            # if not obs.is_gravity_affected:
            if not self.is_stand_on_ground:
                if self.get_state() in ('jump', 'jump cancel', 'run right', 'run left', 'stand still'):
                # if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                    # if self.movement_direction_inverter != 1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                    # if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 10) and self.fall_speed > 0:
                    if self.collision_grabber_right.collidepoint(obs.rectangle.topleft):
                        # self.rectangle.right = obs.rectangle.left - 2
                        self.influenced_by_obstacle = obs.id
                        self.set_state('has just grabbed edge')
                        self.state_machine()
                        continue

            if obs.rectangle.colliderect(self.collision_detector_right):
                obs.is_being_collided_now = True
                self.is_being_collided_now = True

                self.collided_right = True
                # if self.collided_left:
                    # Actor's stuck.
                    # self.ignore_user_input = True

                # Check if obstacle has crawled FROM BEHIND and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left  # Push the actor
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
                        self.set_state('release edge')
                    if key in sorted_obs['above']:
                        sorted_obs['above'].remove(key)
                    continue

                if self.look == 1: # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
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
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                        self.rectangle.right = obs.rectangle.left - 2  # Drop down the actor
                        self.set_state('release edge')
                    else:
                        # print('ksdjhdakjdhsakjdh')
                        bottom_already_changed = True
                        self.rectangle.bottom = obs.rectangle.top
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        # continue
        #-----------------------------------
        # Check LEFT
        for key in sorted_obs['left']:
            obs = self.obstacles_around[key]
            if obs.is_ghost_platform:
                continue

            # GRAB over the top of an obstacle.
            # if not obs.is_gravity_affected:
            if not self.is_stand_on_ground:
                if self.get_state() in ('jump', 'jump cancel','run right', 'run left', 'stand still'):
                # if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                    # if self.movement_direction_inverter != -1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                    # if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 10) and self.fall_speed > 0:
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
                    self.rectangle.left = obs.rectangle.right  # Push the actor
                    self.rectangle.x += obs.vec_to_destination[0]
                    self.rectangle.y += obs.vec_to_destination[1]

                    # self.potential_moving_distance = self.collision_detector_left.right - obs.rectangle.right
                    # self.rectangle.left = obs.rectangle.right
                    self.is_enough_space_left = False
                    self.heading[0] = 0
                    self.speed = 0
                    # self.speed = 0
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        self.set_state('release edge')
                    if key in sorted_obs['above']:
                        sorted_obs['above'].remove(key)

                    continue


                if self.look == -1: # Obstacle is on the left, and actor also looks to the left, and hangs on the edge.
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                        self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
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
                    if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                        self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
                        self.set_state('release edge')
                    else:
                        self.rectangle.bottom = obs.rectangle.top
                        bottom_already_changed = True
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        continue

        # -----------------------------------
        # Check bottom
        for key in sorted_obs['below']:
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            # if obs.is_ghost_platform:
            if obs.rectangle.colliderect(self.collision_detector_bottom):
                if bottom_already_changed and obs.rectangle.top > self.rectangle.bottom:
                    # Current obstacle lower than the actor's rectangle after at least one bottom collision has been registered.
                    # Skip it.
                    continue

                self.collided_bottom = True
                # if self.collided_top:
                #     self.ignore_user_input = True

                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
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

        # -----------------------------------
        # Check top
        for key in sorted_obs['above']:
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.collision_detector_top):
                obs.is_being_collided_now = True
                self.is_being_collided_now = True
                self.collided_top = True
                # if self.collided_bottom:
                #     self.ignore_user_input = True

                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                    self.set_state('release edge')

                if self.fall_speed < 0:
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    # continue

    def check_space_around(self):
        self.is_enough_space_left = True
        self.is_enough_space_right = True
        self.is_enough_space_below = True
        self.is_enough_space_above = True
        self.is_enough_height = True

        # for obs in self.obstacles_around:
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]

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
            if obs.rectangle.colliderect(self.rectangle.left - 2, self.rectangle.bottom - self.target_height,
                                         self.rectangle.width + 4, self.target_height):
            # if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 1,
            #                              self.rectangle.width - 4, abs(self.fall_speed) + 1):
                self.is_enough_height = False
                continue

            # Check if there is enough space ABOVE to perform a jump, for example.
            # if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom - self.target_height - abs(self.fall_speed) - 4,
            #                              self.rectangle.width - 4, abs(self.fall_speed)):
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 1,
                                         self.rectangle.width - 4, abs(self.fall_speed) + 1):
                self.is_enough_space_above = False
                continue
            # Check if there is enough space BELOW
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom,
                                         self.rectangle.width - 4, abs(self.fall_speed) + GRAVITY):
                self.is_enough_space_below = False
                continue

    def fly(self, time_passed):
        self.vec_to_destination = list((self.destination[0] - self.rectangle.x, self.destination[1] - self.rectangle.y))
        # self.vec_to_destination = list((self.destination[0] - self.rectangle.centerx, self.destination[1] - self.rectangle.centery))

        if self.vec_to_destination == (0, 0) or self.destination == self.rectangle.topleft:
        # if self.vec_to_destination == (0, 0) or self.destination == self.rectangle.center:
            self.is_destination_reached = True
            self.speed = 0
            self.heading = [0, 0]
            return
        else:
            self.is_destination_reached = False

        distance_to_destination = sqrt(self.vec_to_destination[0] * self.vec_to_destination[0] + self.vec_to_destination[1] * self.vec_to_destination[1])

        if distance_to_destination > 0:
            # Calculate normalized vector to apply animation set correctly in the future:
            # self.heading = self.vec_to_destination.get_normalized()
            self.heading = [self.vec_to_destination[0] / distance_to_destination, self.vec_to_destination[1] / distance_to_destination]

            self.speed = self.max_speed * self.max_speed_penalty  # * 0.5
            # Define the potential length of current move, depends on basic speed and passed amount of time:
            self.potential_moving_distance = time_passed * self.speed
            # Define current distance to travel:
            self.travel_distance = min(distance_to_destination, self.potential_moving_distance)
            # Set the length of moving vector equal to travel distance, which had already just been calculated:
            l = self.travel_distance / distance_to_destination
            self.vec_to_destination[0] *= l
            self.vec_to_destination[1] *= l

            # print(f'BEFORe: {self.rectangle.center=} {self.vec_to_destination=}')
            self.rectangle.x += round(self.vec_to_destination[0])
            # self.rectangle.centerx += round(self.vec_to_destination[0])
            self.rectangle.y += round(self.vec_to_destination[1])
            # self.rectangle.centery += round(self.vec_to_destination[1])


    # def calculate_colliders_backup(self):
    #     if self.look * self.movement_direction_inverter == 1:
    #         self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
    #         self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, self.speed + 1, 35)
    #
    #         self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height - 35)
    #         self.collision_detector_bottom_left.update(self.rectangle.left - 1, self.rectangle.bottom - 35, 1, 35)
    #     elif self.look * self.movement_direction_inverter == -1:
    #         self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height - 35)
    #         self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, 1, 35)
    #
    #         self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
    #         self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - 35, self.speed + 1, 35)
    #     if self.fall_speed < 0:
    #         self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed), self.rectangle.width - 4, abs(self.fall_speed))
    #         self.collision_detector_bottom.update(0,0,0,0)
    #         # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom, self.rectangle.width - 4, 1)
    #     elif self.fall_speed >= 0:
    #         self.collision_detector_top.update(0,0,0,0)
    #         # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
    #         self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, self.fall_speed + 2)
    #     # else:
    #     #     self.collision_detector_top.update(0,0,0,0)
    #     #     # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
    #     #     self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, 2)

    def calculate_fall_speed(self):
        # if self.influenced_by_obstacle >= 0:
        #     self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        #     self.potential_falling_distance = 1
        #     self.fall_speed = 1
        # else:
        if not self.is_stand_on_ground:
            if self.fall_speed > GRAVITY_G:
                self.fall_speed = GRAVITY_G
            else:
                self.fall_speed += GRAVITY

            if self.is_abort_jump:
                if self.fall_speed >= 0:
                    self.is_abort_jump = False
                else:
                    self.fall_speed = 0
                    self.is_abort_jump = False
            self.potential_falling_distance = self.fall_speed
        else:
            self.potential_falling_distance = 1
            self.fall_speed = 1

    def fall(self):
        # print(f'[FALL]')
        self.rectangle.y += self.potential_falling_distance

    def correct_position_if_influenced(self):
        if self.influenced_by_obstacle >= 0:
            obs = self.obstacles_around[self.influenced_by_obstacle]
            if obs.active:
                self.rectangle.x += round(obs.vec_to_destination[0])
                self.rectangle.y += round(obs.vec_to_destination[1])

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

    def move(self, time_passed):
        # if self.id != 0:
        #     print('Now moves: ', self.type, self.id)
        # if self.heading[0] == 1:
        #     self.destination[0] = self.rectangle.centerx + 500
        # elif self.heading[0] == -1:
        #     self.destination[0] = self.rectangle.centerx - 500
        # else:
        #     self.destination[0] = self.rectangle.x
        # self.fly(time_passed)
        self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter)

    def die(self):
        self.dead = True