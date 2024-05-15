from constants import *


class Camera(object):
    def __init__(self):
        self.max_offset_x: int = 0
        self.max_offset_y: int = 0
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.target_offset_x: int = 0
        self.target_offset_y: int = 0
        self.instant_follow: bool = False
        self.default_offset_scroll_velocity = 25
        self.offset_scroll_velocity = self.default_offset_scroll_velocity


    def setup(self, max_offset_x, max_offset_y):
        self.max_offset_x = max_offset_x
        self.max_offset_y = max_offset_y

    def apply_offset(self, xy):

        x = xy[0]
        y = xy[1]
        # self.scroll_counter_x = 0
        # self.scroll_counter_y = 0
        # self.allow_screen_scrolling_x = True
        # self.allow_screen_scrolling_y = True
        # print('AA')
    
        if x <= MAXX_DIV_2:
            self.target_offset_x = 0
        else:
            self.target_offset_x = x - MAXX_DIV_2
            if self.target_offset_x > self.max_offset_x:
                self.target_offset_x = self.max_offset_x
    
        if y <= MAXY_DIV_2:
            self.target_offset_y = 0
        else:
            self.target_offset_y = y - MAXY_DIV_2
            if self.target_offset_y > self.max_offset_y:
                self.target_offset_y = self.max_offset_y
    
        if self.instant_follow:
            self.instant_follow = False
            self.offset_x = self.target_offset_x
            self.offset_y = self.target_offset_y
        else:
            if self.offset_x <= self.target_offset_x - self.offset_scroll_velocity:
                self.offset_x += self.offset_scroll_velocity
            elif self.offset_x > self.target_offset_x + self.offset_scroll_velocity:
                self.offset_x -= self.offset_scroll_velocity
            else:
                self.offset_x = self.target_offset_x
    
            if self.offset_y <= self.target_offset_y - self.offset_scroll_velocity:
                self.offset_y += self.offset_scroll_velocity
            elif self.offset_y > self.target_offset_y + self.offset_scroll_velocity:
                self.offset_y -= self.offset_scroll_velocity
            else:
                self.offset_y = self.target_offset_y