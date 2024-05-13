from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'
        self.is_need_to_jump: bool = False
        self.jump_height: int = 22


    def process(self, time_passed):
        if self.is_need_to_jump:
            # Jump
            # if self.is_stand_on_ground:  # and self.IsEnoughSpaceAbove:
                # self.IsCrouch = False
                # self.IsUp = False
            self.fall_speed = -self.jump_height
            self.is_need_to_jump = False
            self.is_stand_on_ground = False
            # self.destination[1] = 0

        super().process(time_passed)