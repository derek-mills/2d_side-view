from obstacle import *

class Demolisher(Obstacle):

    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'demolisher'
        self.acceleration = .5
        self.air_acceleration = .4
        # self.jump_height: int = 22
        # self.default_max_speed = 10
        # self.max_jump_attempts = 2
        self.max_speed = 10

    def process(self, time_passed):
        ...