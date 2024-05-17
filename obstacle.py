from entity import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'obstacle'
        self.is_ghost_platform: bool = False
        self.max_speed = 1

    def process(self, time_passed):

        super().process(time_passed)