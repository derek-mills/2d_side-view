import pygame
from math import sqrt
from constants import *

class Entity(object):

    def __init__(self):
        self.id:int = 0
        self.type: str = ''  #
        self.name: str = ''
        self.location: str = ''
        self.__state: str = ''
        self.idle_counter: int = 0

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

        self.look: int = 1  # 1: look right, -1: look left

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
        self.collision_detector_right = pygame.Rect(0,0,0,0)
        self.collision_detector_left = pygame.Rect(0,0,0,0)
        self.collision_detector_top = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_right = pygame.Rect(0,0,0,0)
        self.collision_detector_bottom_left = pygame.Rect(0,0,0,0)
        self.is_destination_reached: bool = False
        self.collided_top: bool = False
        self.collided_left: bool = False
        self.collided_right: bool = False
        self.collided_bottom: bool = False

        # self.aux_counter = 0

        self.influenced_by_obstacle: int = -1
        self.is_edge_grabbed: bool = False
        # self.is_on_obstacle: bool = False
        self.is_on_ghost_platform: bool = False
        self.is_enough_space_above = False
        self.is_enough_space_below = False  # Флаг для определения возможности 'спрыгивания' со специальных платформ.
        self.is_enough_space_for_step = True  # Флаг для определения возможности сделать следующий шаг по горизонтальной платформе;
        #                                         не предусматривает отсутствие препятствия сбоку.
        self.is_enough_space_right = True
        self.is_enough_space_left = True


    def percept(self, obstacles):
        self.obstacles_around = obstacles

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
        if self.is_jump:
        # if self.is_jump and self.jump_attempts_counter > 0:
            # Jump
            self.fall_speed = -self.jump_height
            self.is_jump = False
            self.is_stand_on_ground = False

        self.processing_rectangle_size()
        self.check_space_around()  # Detect obstacles on the right and left sides
        self.fall_speed_calc()  # Discover speed and potential fall distance
        self.speed_calc()       # Discover fall speed and potential move distance
        self.colliders_calc()   # Calculate colliders around actor based on his current movement and fall speeds.
        self.detect_collisions()

        if self.is_gravity_affected:
            # if self.influenced_by_obstacle:
            #     self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            # else:
            # if not self.is_stand_on_ground or not self.is_edge_grabbed:
            if not self.is_stand_on_ground and not self.is_edge_grabbed:
                # self.influenced_by_obstacle = None
                # print('fall!')
                self.fall()
        self.move()
        # if self.influenced_by_obstacle:
        #     print('dd')
        #     self.rectangle.x += self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[0]



    def fall_speed_calc(self):
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
        # if self.influenced_by_obstacle:
        #     self.potential_falling_distance += self.obstacles_around[self.influenced_by_obstacle].fall_speed
        #     # self.potential_falling_distance += self.obstacles_around[self.influenced_by_obstacle].potential_falling_distance



    def speed_calc(self):
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

        # if self.influenced_by_obstacle:
        #     self.potential_moving_distance = self.speed + \
        #                                      self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[0]
        # else:
        self.potential_moving_distance = self.speed
        # self.potential_moving_distance = int(self.speed * self.look)
        # self.rectangle.x += int(self.speed * self.look)

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state

    def state_machine(self):
        ...

    def colliders_calc(self):
        if self.look * self.movement_direction_inverter == 1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
            self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height - 35)
            if self.speed > 0:
                self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, self.speed + 1, 30)
                self.collision_detector_bottom_left.update(self.rectangle.left - 1, self.rectangle.bottom - 35, 1, 30)
            else:
                self.collision_detector_bottom_right.update(0,0,0,0)
                self.collision_detector_bottom_left.update(0,0,0,0)

        elif self.look * self.movement_direction_inverter == -1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height - 35)
            self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
            if self.speed > 0:
                self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, 1, 30)
                self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - 35, self.speed + 1, 30)
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

    def detect_collisions(self):
        self.is_stand_on_ground = False
        # self.influenced_by_obstacle = None
        sorted_obs = {
            'above': list(),
            'below': list(),
            'right': list(),
            'left': list(),
        }
        # for obs in self.obstacles_around:
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            if obs.rectangle.centery < self.rectangle.centery:
                sorted_obs['above'].append(obs.id)
            elif obs.rectangle.centery > self.rectangle.centery:
                sorted_obs['below'].append(obs.id)
            if obs.rectangle.centerx < self.rectangle.centerx:
                sorted_obs['left'].append(obs.id)
            elif obs.rectangle.centerx > self.rectangle.centerx:
                sorted_obs['right'].append(obs.id)

        # # -----------------------------------
        # # Check bottom
        # bottom_already_changed = False
        # for key in sorted_obs['below']:
        #     obs = self.obstacles_around[key]
        #     obs.is_being_collided_now = False
        #     # if obs.is_ghost_platform:
        #     if obs.rectangle.colliderect(self.collision_detector_bottom):
        #         if bottom_already_changed and obs.rectangle.top > self.rectangle.bottom:
        #             # Current obstacle lower than the actor's rectangle after at least one bottom collision has been registered.
        #             # Skip it.
        #             continue
        #         obs.is_being_collided_now = True
        #         # if self.fall_speed >= 0:
        #         self.rectangle.bottom = obs.rectangle.top
        #         self.is_stand_on_ground = True
        #         self.influenced_by_obstacle = obs.id
        #         self.jump_attempts_counter = self.max_jump_attempts
        #         bottom_already_changed = True
        #         # break
        #             # continue
        #
        # # -----------------------------------
        # # Check top
        # for key in sorted_obs['above']:
        #     obs = self.obstacles_around[key]
        #     obs.is_being_collided_now = False
        #     if obs.is_ghost_platform:
        #         continue
        #     if obs.rectangle.colliderect(self.collision_detector_top):
        #         obs.is_being_collided_now = True
        #         if self.fall_speed < 0:
        #             self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
        #             self.is_stand_on_ground = False
        #             self.fall_speed = 0
        #             # continue

        #-----------------------------------
        # Check RIGHT
        for key in sorted_obs['right']:
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue

            if obs.rectangle.colliderect(self.collision_detector_right):
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 2  # Push the actor
                    # self.speed = 0
                    # self.influenced_by_obstacle = None
                    # self.is_edge_grabbed = False
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        self.set_state('release edge')
                    continue
                # Grab over the top of an obstacle.
                # if not obs.is_gravity_affected:
                if not self.is_stand_on_ground:
                    if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                        # if self.movement_direction_inverter != 1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                        if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 10) and self.fall_speed > 0:
                            self.rectangle.right = obs.rectangle.left - 2
                            self.influenced_by_obstacle = obs.id
                            self.set_state('has just grabbed edge')
                            self.state_machine()
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
                        self.rectangle.bottom = obs.rectangle.top
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        continue
        #-----------------------------------
        # Check LEFT
        for key in sorted_obs['left']:
            obs = self.obstacles_around[key]
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.collision_detector_left):
                obs.is_being_collided_now = True
                # self.rectangle.left = obs.rectangle.right + 2

                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 2  # Push the actor
                    # self.speed = 0
                    if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                        self.set_state('release edge')
                    continue

                # Grab over the top of an obstacle.
                # if not obs.is_gravity_affected:
                if not self.is_stand_on_ground:
                    if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                        # if self.movement_direction_inverter != -1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                        if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 10) and self.fall_speed > 0:
                            self.influenced_by_obstacle = obs.id
                            self.set_state('has just grabbed edge')
                            self.state_machine()
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
                # #-----------------------------------
                # # Check top
                # if obs.rectangle.colliderect(self.collision_detector_top):
                #     obs.is_being_collided_now = True
                #     if self.fall_speed < 0 and not obs.is_ghost_platform:
                #         self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                #         self.is_stand_on_ground = False
                #         self.fall_speed = 0
                #         continue
                # -----------------------------------
                # Check bottom
                # if obs.rectangle.colliderect(self.collision_detector_bottom) and not bottom_already_changed:
                #     obs.is_being_collided_now = True
                #     if self.fall_speed >= 0:
                #         self.rectangle.bottom = obs.rectangle.top
                #         self.is_stand_on_ground = True
                #         self.influenced_by_obstacle = obs.id
                #         self.jump_attempts_counter = self.max_jump_attempts
                #         continue

            # obs.is_being_collided_now = False

        # -----------------------------------
        # Check bottom
        bottom_already_changed = False
        for key in sorted_obs['below']:
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            # if obs.is_ghost_platform:
            if obs.rectangle.colliderect(self.collision_detector_bottom):
                if bottom_already_changed and obs.rectangle.top > self.rectangle.bottom:
                    # Current obstacle lower than the actor's rectangle after at least one bottom collision has been registered.
                    # Skip it.
                    continue
                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                    self.set_state('release edge')
                obs.is_being_collided_now = True
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
                if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                    self.set_state('release edge')

                if self.fall_speed < 0:
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    # continue

    def detect_collisions_backup(self):
        self.is_stand_on_ground = False
        # self.influenced_by_obstacle = None
        bottom_already_changed = False
        # for obs in self.obstacles_around:
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            if obs.is_ghost_platform:
                # -----------------------------------
                # Check bottom
                if obs.rectangle.colliderect(self.collision_detector_bottom):
                    obs.is_being_collided_now = True
                    if self.fall_speed >= 0:
                        self.rectangle.bottom = obs.rectangle.top
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        continue
            else:
                #-----------------------------------
                # Check RIGHT
                if obs.rectangle.colliderect(self.collision_detector_right):
                    # if obs.is_ghost_platform:
                    #     continue
                    # Check if obstacle has crawled from behind and pushed actor to his back:
                    if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                        self.rectangle.right = obs.rectangle.left - 2  # Push the actor
                        # self.speed = 0
                        # self.influenced_by_obstacle = None
                        # self.is_edge_grabbed = False
                        if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                            self.set_state('release edge')
                        continue
                    # Grab over the top of an obstacle.
                    # if not obs.is_gravity_affected:
                    if not self.is_stand_on_ground:
                        if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                            # if self.movement_direction_inverter != 1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                            if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 40) and self.fall_speed > 0:
                                self.rectangle.right = obs.rectangle.left - 2
                                self.influenced_by_obstacle = obs.id
                                self.set_state('has just grabbed edge')
                                self.state_machine()
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
                            self.rectangle.bottom = obs.rectangle.top
                            self.is_stand_on_ground = True
                            self.influenced_by_obstacle = obs.id
                            self.jump_attempts_counter = self.max_jump_attempts
                            continue
                #-----------------------------------
                # Check LEFT
                if obs.rectangle.colliderect(self.collision_detector_left):
                    obs.is_being_collided_now = True
                    # self.rectangle.left = obs.rectangle.right + 2

                    # Check if obstacle has crawled from behind and pushed actor to his back:
                    if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                        self.rectangle.left = obs.rectangle.right + 2  # Push the actor
                        # self.speed = 0
                        if self.get_state() in ('hanging on edge', 'hanging on ghost'):
                            self.set_state('release edge')
                        continue

                    # Grab over the top of an obstacle.
                    # if not obs.is_gravity_affected:
                    if not self.is_stand_on_ground:
                        if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                            # if self.movement_direction_inverter != -1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                            if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 40) and self.fall_speed > 0:
                                self.influenced_by_obstacle = obs.id
                                self.set_state('has just grabbed edge')
                                self.state_machine()
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
                #-----------------------------------
                # Check top
                if obs.rectangle.colliderect(self.collision_detector_top):
                    obs.is_being_collided_now = True
                    if self.fall_speed < 0 and not obs.is_ghost_platform:
                        self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                        self.is_stand_on_ground = False
                        self.fall_speed = 0
                        continue
                # -----------------------------------
                # Check bottom
                if obs.rectangle.colliderect(self.collision_detector_bottom) and not bottom_already_changed:
                    obs.is_being_collided_now = True
                    if self.fall_speed >= 0:
                        self.rectangle.bottom = obs.rectangle.top
                        self.is_stand_on_ground = True
                        self.influenced_by_obstacle = obs.id
                        self.jump_attempts_counter = self.max_jump_attempts
                        continue

            obs.is_being_collided_now = False

    def check_space_around(self):
        self.is_enough_space_left = True
        self.is_enough_space_right = True
        self.is_enough_space_below = True
        self.is_enough_space_above = True

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
            # Check if there is enough space ABOVE
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom - self.target_height - abs(self.fall_speed) - 1,
                                         self.rectangle.width - 4, self.target_height - abs(self.fall_speed)):
            # if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4,
            #                              self.rectangle.width - 4, abs(self.fall_speed) + 4):
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
            self.heading = (0, 0)
            return
        else:
            self.is_destination_reached = False

        distance_to_destination = sqrt(self.vec_to_destination[0] * self.vec_to_destination[0] + self.vec_to_destination[1] * self.vec_to_destination[1])

        if distance_to_destination > 0:
            # Calculate normalized vector to apply animation set correctly in the future:
            # self.heading = self.vec_to_destination.get_normalized()
            self.heading = (self.vec_to_destination[0] / distance_to_destination, self.vec_to_destination[1] / distance_to_destination)

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


    # def colliders_calc_backup(self):
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

    def fall(self):
        self.rectangle.y += self.potential_falling_distance

    def move(self):
        if self.influenced_by_obstacle >= 0:
            # print('dd')
            obs = self.obstacles_around[self.influenced_by_obstacle]
            self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter + round(obs.vec_to_destination[0]))
            # self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter + infl.potential_moving_distance*infl.look)
        else:
            # self.rectangle.x += (self.potential_moving_distance * self.heading[0])
            self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter)
        # self.rectangle.x += int(self.speed * self.look)