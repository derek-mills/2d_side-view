import pygame

from constants import *


class Camera(object):
    def __init__(self):
        self.max_x: int = 0
        self.max_y: int = 0
        self.max_offset_x: int = 0
        self.max_offset_y: int = 0
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.target_offset_x: int = 0
        self.target_offset_y: int = 0
        self.instant_follow: bool = False
        self.default_offset_scroll_velocity = 1
        self.offset_scroll_velocity_x = 0
        self.offset_scroll_velocity_y = 0
        self.rectangle = pygame.Rect(0, 0, 0, 0)
        self.active_objects_rectangle = pygame.Rect(0, 0, 0, 0)


    def setup(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        if self.max_x < MAXX:
            self.max_offset_x = - (MAXX_DIV_2 - self.max_x // 2)
        else:
            self.max_offset_x = max_x - MAXX
        if self.max_y < MAXY:
            self.max_offset_y = - (MAXY_DIV_2 - self.max_y // 2)
        else:
            self.max_offset_y = max_y - MAXY

        # self.max_offset_y = max_y - MAXY
        print(f'[camera setup] {self.max_x=} {self.max_y=} {self.max_offset_x=} {self.max_offset_y=}')

    def apply_offset(self, xy, velocity_x, velocity_y, instant_follow=False):

        x = xy[0]
        y = xy[1]
        self.offset_scroll_velocity_x = velocity_x
        self.offset_scroll_velocity_y = velocity_y
        self.instant_follow = instant_follow

        if self.max_x < MAXX:
            # self.target_offset_x = -100
            self.target_offset_x = self.max_offset_x
            self.instant_follow = True
        elif x <= MAXX_DIV_2:
            self.target_offset_x = 0
        else:
            self.target_offset_x = x - MAXX_DIV_2
            if self.target_offset_x > self.max_offset_x:
                self.target_offset_x = self.max_offset_x

        if self.max_y < MAXY:
            self.target_offset_y = self.max_offset_y
            self.instant_follow = True
        elif y <= MAXY_DIV_2:
            self.target_offset_y = 0
        else:
            self.target_offset_y = y - MAXY_DIV_2
            if self.target_offset_y > self.max_offset_y:
                self.target_offset_y = self.max_offset_y
    
        if self.instant_follow:
            self.instant_follow = False
            self.offset_x = int(self.target_offset_x)
            self.offset_y = int(self.target_offset_y)
        else:
            if self.offset_x <= self.target_offset_x - self.offset_scroll_velocity_x:
                self.offset_x += int(self.offset_scroll_velocity_x)
            elif self.offset_x > self.target_offset_x + self.offset_scroll_velocity_x:
                self.offset_x -= int(self.offset_scroll_velocity_x)
            else:
                self.offset_x = int(self.target_offset_x)
    
            if self.offset_y <= self.target_offset_y - self.offset_scroll_velocity_y:
                self.offset_y += int(self.offset_scroll_velocity_y)
            elif self.offset_y > self.target_offset_y + self.offset_scroll_velocity_y:
                self.offset_y -= int(self.offset_scroll_velocity_y)
            else:
                self.offset_y = int(self.target_offset_y)

        self.rectangle.update(self.offset_x, self.offset_y, MAXX, MAXY)
        self.active_objects_rectangle.update(self.offset_x - 400, 0, MAXX + 800, self.max_y)
        # self.active_objects_rectangle.update(self.offset_x - 400, self.offset_y - 400, MAXX + 800, MAXY + 800)

    def apply_offset_level_editor(self, xy, velocity_x, velocity_y, instant_follow=False):

        x = xy[0]
        y = xy[1]
        self.offset_scroll_velocity_x = velocity_x
        self.offset_scroll_velocity_y = velocity_y
        self.instant_follow = instant_follow
        self.target_offset_x = x
        self.target_offset_y = y
        # if x <= 0:
        # # if x <= MAXX_DIV_2:
        #     self.target_offset_x = 0
        # else:
        #     self.target_offset_x = x - MAXX_DIV_2
        #     if self.target_offset_x > self.max_offset_x:
        #         self.target_offset_x = self.max_offset_x
        #
        # if y <= MAXY_DIV_2:
        #     self.target_offset_y = 0
        # else:
        #     self.target_offset_y = y - MAXY_DIV_2
        #     if self.target_offset_y > self.max_offset_y:
        #         self.target_offset_y = self.max_offset_y

        if self.instant_follow:
            self.instant_follow = False
            self.offset_x = int(self.target_offset_x)
            self.offset_y = int(self.target_offset_y)
        else:
            if self.offset_x <= self.target_offset_x - self.offset_scroll_velocity_x:
                self.offset_x += int(self.offset_scroll_velocity_x)
            elif self.offset_x > self.target_offset_x + self.offset_scroll_velocity_x:
                self.offset_x -= int(self.offset_scroll_velocity_x)
            else:
                self.offset_x = int(self.target_offset_x)

            if self.offset_y <= self.target_offset_y - self.offset_scroll_velocity_y:
                self.offset_y += int(self.offset_scroll_velocity_y)
            elif self.offset_y > self.target_offset_y + self.offset_scroll_velocity_y:
                self.offset_y -= int(self.offset_scroll_velocity_y)
            else:
                self.offset_y = int(self.target_offset_y)

        self.rectangle.update(self.offset_x, self.offset_y, MAXX, MAXY)
        self.active_objects_rectangle.update(self.offset_x - 400, 0, MAXX + 800, self.max_y)
        # self.active_objects_rectangle.update(self.offset_x - 400, self.offset_y - 400, MAXX + 800, MAXY + 800)
