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
        self.rectangle = pygame.Rect(0, 0, 50, 50)

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
        self.max_jump_attempts: int = 3  # n-1 attempts to do a jump in midair.
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
        self.destination_list = list()
        # self.destination_point = 0
        self.destination: list = [0, 0]

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

        self.influenced_by_obstacle = None
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

    def process(self, time_passed):
        # if self.is_move_left:
        #
        #     if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
        #         # Switch off heading to force actor start reducing his speed and slow it down to zero.
        #         # After that self is going to be able to start acceleration to proper direction.
        #         self.heading[0] = 0
        #     else:
        #         self.look = -1
        #         self.heading[0] = -1
        # elif self.is_move_right:
        #     if self.look == -1 and self.speed > 0:  # Actor looks to the other side and runs.
        #         # Switch off heading to force actor start reducing his speed and slow it down to zero.
        #         # After that self is going to be able to start acceleration to proper direction.
        #         self.heading[0] = 0
        #     else:
        #         self.look = 1
        #         self.heading[0] = 1
        # else:
        #     self.heading[0] = 0

        if self.is_jump and self.jump_attempts_counter > 0:
            # Jump
            self.fall_speed = -self.jump_height
            self.is_jump = False
            self.is_stand_on_ground = False

        self.check_space_around()  # Detect obstacles on the right and left sides
        self.fall_speed_calc()  # Discover speed and potential fall distance
        self.speed_calc()       # Discover fall speed and potential move distance
        self.colliders_calc()   # Calculate colliders around actor based on his current movement and fall speeds.
        self.detect_collisions()

        if self.is_gravity_affected:
            # if not self.is_stand_on_ground or not self.is_edge_grabbed:
            if not self.is_stand_on_ground and not self.is_edge_grabbed:
                # self.influenced_by_obstacle = None
                # print('fall!')
                self.fall()
        self.move()


    def fall_speed_calc(self):
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

        self.potential_moving_distance = self.speed
        # self.potential_moving_distance = int(self.speed * self.look)
        # self.rectangle.x += int(self.speed * self.look)

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state

    def state_machine(self):
        ...

    def detect_collisions(self):
        self.is_stand_on_ground = False
        # self.influenced_by_obstacle = None
        bottom_already_changed = False
        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            #-----------------------------------
            # Check RIGHT
            if obs.rectangle.colliderect(self.collision_detector_right) and not obs.is_ghost_platform:
                # if obs.is_ghost_platform:
                #     continue
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 2  # Push the actor
                    # self.speed = 0
                    # self.influenced_by_obstacle = None
                    # self.is_edge_grabbed = False
                    self.set_state('release edge')
                    continue
                # Grab over the top of an obstacle.
                if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                    # if self.movement_direction_inverter != 1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                    if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 30) and self.fall_speed > 0:
                        # self.rectangle.right = obs.rectangle.left - 2
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
            if obs.rectangle.colliderect(self.collision_detector_bottom_right) and not obs.is_ghost_platform:
                obs.is_being_collided_now = True
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 2  # Push the actor
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
            if obs.rectangle.colliderect(self.collision_detector_left) and not obs.is_ghost_platform:
                obs.is_being_collided_now = True
                # self.rectangle.left = obs.rectangle.right + 2

                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 2  # Push the actor
                    # self.speed = 0
                    self.set_state('release edge')
                    continue

                # Grab over the top of an obstacle.
                if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge', 'hopping back process', 'hop back'):
                    # if self.movement_direction_inverter != -1:  # Try to grab the edge only if actor moves exactly at the same direction of his gaze.
                    if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 30) and self.fall_speed > 0:
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
            if obs.rectangle.colliderect(self.collision_detector_bottom_left) and not obs.is_ghost_platform:
                obs.is_being_collided_now = True
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 2  # Push the actor
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
            if obs.rectangle.colliderect(self.collision_detector_bottom) and not bottom_already_changed:
                obs.is_being_collided_now = True
                if self.fall_speed >= 0:
                    self.rectangle.bottom = obs.rectangle.top
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
            obs.is_being_collided_now = False

    def check_space_around(self):
        self.is_enough_space_left = True
        self.is_enough_space_right = True
        self.is_enough_space_below = True
        self.is_enough_space_above = True

        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            # # Check enough spaces right and left:
            if obs.rectangle.colliderect(self.rectangle.left - self.rectangle.width - self.speed - 2, self.rectangle.top,
                                         self.rectangle.width + self.speed + 2, self.rectangle.height - 35):
                self.is_enough_space_left = False
                continue
            if obs.rectangle.colliderect(self.rectangle.right, self.rectangle.top,
                                         self.rectangle.width + self.speed + 2, self.rectangle.height - 35):
                self.is_enough_space_right = False
                continue
            # Check if there is enough space ABOVE
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed) - 4,
                                         self.rectangle.width - 4, abs(self.fall_speed) + 4):
                self.is_enough_space_above = False
                continue
            # Check if there is enough space BELOW
            if obs.rectangle.colliderect(self.rectangle.left + 2, self.rectangle.bottom,
                                         self.rectangle.width - 4, abs(self.fall_speed) + 1):
                self.is_enough_space_below = False
                continue

    def fly(self, time_passed):
        vec_to_destination = list((self.destination[0] - self.rectangle.centerx, self.destination[1] - self.rectangle.centery))
        # vec_to_destination = Vector2(self.destination[0] - self.rectangle.centerx, self.destination[1] - self.rectangle.centery)
        # print(vec_to_destination)
        # print(vec_to_destination[0], vec_to_destination[1])
        # distance_to_destination = vec_to_destination.get_approximate_length()

        if vec_to_destination == (0, 0) or self.destination == self.rectangle.center:
            self.is_destination_reached = True
            self.speed = 0
            self.heading = (0, 0)
            # if self.particle and self.liquid_drop:
            #     self.gravity_affected = False
            #     self.fall_speed = 0
            #     # print(f'[creature move] Particle {self.id}: destination reached!!')
            # # self.state = 'stay still'
            return
        else:
            # self.state = 'move'
            self.is_destination_reached = False

        distance_to_destination = sqrt(vec_to_destination[0] * vec_to_destination[0] + vec_to_destination[1] * vec_to_destination[1])
        # distance_to_destination = vec_to_destination.get_length()

        if distance_to_destination > 0:
            # Calculate normalized vector to apply animation set correctly in the future:
            # self.heading = vec_to_destination.get_normalized()
            self.heading = (vec_to_destination[0] / distance_to_destination, vec_to_destination[1] / distance_to_destination)
            # self.heading = Vector2.from_floats(vec_to_destination[0] / distance_to_destination, vec_to_destination[1] / distance_to_destination)

            self.speed = self.max_speed * self.max_speed_penalty  # * 0.5
            # self.action_points_move_straight = 10 / self.fly_speed
            # self.action_points_move_diagonal = 1.41 * (10 / self.fly_speed)
            # self.fly_speed = self.max_fly_speed - (self.max_fly_speed / 100) * self.max_fly_speed_penalty
            # Define the potential length of current move, depends on basic speed and passed amount of time:
            self.potential_moving_distance = time_passed * self.speed
            # Define current distance to travel:
            self.travel_distance = min(distance_to_destination, self.potential_moving_distance)
            # Set the length of moving vector equal to travel distance, which had already just been calculated:
            l = self.travel_distance / distance_to_destination
            # if self.battle_mode and self.hasten_mode:
            #     self.decrease_stamina(l)
            vec_to_destination[0] *= l
            vec_to_destination[1] *= l
            # vec_to_destination.set_length(self.travel_distance)

            # print(f'BEFORe: {self.rectangle.center=} {vec_to_destination=}')
            self.rectangle.centerx += round(vec_to_destination[0])
            self.rectangle.centery += round(vec_to_destination[1])
            # self.rectangle.center += vec_to_destination
            # print(f'AFTER: {self.rectangle.center=}')
            # print('-'*100)
            # self.rectangle_central_spot = self.rectangle.inflate(-self.rectangle.height // 3, -self.rectangle.width // 2)

    def colliders_calc(self):
        if self.look * self.movement_direction_inverter == 1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
            self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, self.speed + 1, 35)

            self.collision_detector_left.update(self.rectangle.left - 1, self.rectangle.top, 1, self.rectangle.height - 35)
            self.collision_detector_bottom_left.update(self.rectangle.left - 1, self.rectangle.bottom - 35, 1, 35)
        elif self.look * self.movement_direction_inverter == -1:
            self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, 1, self.rectangle.height - 35)
            self.collision_detector_bottom_right.update(self.rectangle.right, self.rectangle.bottom - 35, 1, 35)

            self.collision_detector_left.update(self.rectangle.left - self.speed - 1, self.rectangle.top, self.speed + 1, self.rectangle.height - 35)
            self.collision_detector_bottom_left.update(self.rectangle.left - self.speed - 1, self.rectangle.bottom - 35, self.speed + 1, 35)
        if self.fall_speed < 0:
            self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - abs(self.fall_speed), self.rectangle.width - 4, abs(self.fall_speed))
            self.collision_detector_bottom.update(0,0,0,0)
            # self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom, self.rectangle.width - 4, 1)
        elif self.fall_speed >= 0:
            self.collision_detector_top.update(0,0,0,0)
            # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
            self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, self.fall_speed + 2)
        # else:
        #     self.collision_detector_top.update(0,0,0,0)
        #     # self.collision_detector_top.update(self.rectangle.left + 2, self.rectangle.top - 1, self.rectangle.width - 4, 1)
        #     self.collision_detector_bottom.update(self.rectangle.left + 2, self.rectangle.bottom - 2, self.rectangle.width - 4, 2)

    def fall(self):
        # if self.is_enough_space_below:
        #     if self.fall_speed > GRAVITY_G:
        #         self.fall_speed = GRAVITY_G
        #     else:
        #         self.fall_speed += GRAVITY
        #
        #     if self.is_abort_jump:
        #         if self.fall_speed >= 0:
        #             self.is_abort_jump = False
        #         else:
        #             self.fall_speed = 0
        #             self.is_abort_jump = False
        #     self.rectangle.y += self.fall_speed
        #
        self.rectangle.y += self.potential_falling_distance

    def move(self):
        # if self.heading[0] == 0:
        #     if self.speed > 0:
        #         if self.is_stand_on_ground:
        #             self.speed -= self.acceleration
        #         else:
        #             self.speed -= self.air_acceleration
        #         self.speed = max(self.speed, 0)
        # else:
        #     if self.speed < self.max_speed:
        #         if self.is_stand_on_ground:
        #             self.speed += self.acceleration
        #         else:
        #             self.speed += self.air_acceleration
        # # self.potential_moving_distance = int(self.speed * self.look)
        #
        # self.collision_detector_right.update(self.rectangle.right, self.rectangle.top, self.speed, self.rectangle.height - 35)
        if self.influenced_by_obstacle:
            infl = self.obstacles_around[self.influenced_by_obstacle]
            self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter + infl.potential_moving_distance*infl.look)
        else:
            # self.rectangle.x += (self.potential_moving_distance * self.heading[0])
            self.rectangle.x += (self.potential_moving_distance * self.look * self.movement_direction_inverter)
        # self.rectangle.x += int(self.speed * self.look)