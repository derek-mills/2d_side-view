import pygame
from math import sqrt
from constants import *

class Entity(object):

    def __init__(self):
        self.id:int = 0
        self.type: str = ''  #
        self.name: str = ''
        self.location: str = ''

        # GEOMETRY
        self.rectangle = pygame.Rect(0, 0, 50, 50)

        self.look: str = 'right'

        # MOVEMENT
        self.acceleration: float = .3
        self.speed: float = 0.
        # self.speed_direction: int = 0
        self.speed_reduce = 0.0005
        self.default_max_speed: float = 15.0  # Maximum speed cap for this creature
        self.max_speed: float = self.default_max_speed
        self.max_speed_penalty = 1
        self.heading: list = [0, 0]
        self.travel_distance: float = 0.
        self.potential_moving_distance: float = 0.
        self.fall_speed: float = 0.
        self.is_stand_on_ground: bool = False
        self.is_gravity_affected: bool = False
        self.destination_list = list()
        # self.destination_point = 0
        self.destination: list = [0, 0]
        self.is_destination_reached: bool = False
        self.collided_top: bool = False
        self.collided_left: bool = False
        self.collided_right: bool = False
        self.collided_bottom: bool = False

        self.is_on_obstacle: bool = False
        self.is_on_ghost_platform: bool = False
        self.is_enough_space_above = False
        self.is_enough_space_below = False  # Флаг для определения возможности 'спрыгивания' со специальных платформ.
        self.is_enough_space_for_step = True  # Флаг для определения возможности сделать следующий шаг по горизонтальной платформе;
        #                                         не предусматривает отсутствие препятствия сбоку.
        self.is_enough_space_right = True
        self.is_enough_space_left = True

    def process(self, time_passed):
        if self.is_gravity_affected:
            if not self.is_stand_on_ground:
                # self.destination[1] = MAXY
                self.fall()
        if self.rectangle.center != self.destination:
            self.move()

            # if self.heading[0] > 1:
            #     self.look = 'right'
            # elif self.heading[0] < 1:
            #     self.look = 'left'

    def fall(self):
        # self.StandingOnSuchPlatformID = -1
        # if self.fall_speed == 0:
        #     print('pppp')
        #     self.destination[1] = self.rectangle.centery
        if self.fall_speed > GRAVITY_G:
            self.fall_speed = GRAVITY_G
        else:
            self.fall_speed += GRAVITY
        # self.destination[1] = MAXY
        # else:
        #     self.fall_speed = 0
        # elif self.fall_speed < 0:
        #     self.destination[1] = 0
        #     self.rectangle.y += self.fall_speed

        # self.destination[1] = MAXY
        self.rectangle.y += self.fall_speed

    def move(self):
        if self.heading[0] != 0:
            if self.speed < self.max_speed and self.is_stand_on_ground:
                self.speed += self.acceleration
            self.rectangle.x += (self.speed * self.heading[0])


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
            # self.action_points_need_to_move_straight = 10 / self.fly_speed
            # self.action_points_need_to_move_diagonal = 1.41 * (10 / self.fly_speed)
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
