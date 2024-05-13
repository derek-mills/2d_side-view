from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'
        self.is_need_to_jump: bool = False
        self.jump_height: int = 12

    def process(self, time_passed):
        super().process(time_passed)
        if self.is_need_to_jump:
            # Jump
            # if self.is_stand_on_ground:  # and self.IsEnoughSpaceAbove:
                # self.IsCrouch = False
                # self.IsUp = False
            self.fall_speed = -self.jump_height
            self.is_need_to_jump = False
