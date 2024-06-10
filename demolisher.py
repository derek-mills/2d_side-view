from obstacle import *

class Demolisher(Obstacle):

    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'demolisher'
        self.acceleration = .5
        self.air_acceleration = .4
        self.max_speed = 10
        self.snap_to_actor: int = 0  # Active actor which cause this demolisher to be glued.
        self.snapping_offset = list()
        self.damage: float = 0.
        self.damage_reduce: float = 0.
        self.parent_id: int = -1
        self.static = True

    def update(self, snap_side, snap_rect):
        if snap_side == 1:  # Snapping to the actor's right side
            self.rectangle.left = snap_rect.right + self.snapping_offset[0]
            self.rectangle.top = snap_rect.top + self.snapping_offset[1]
        else:
            self.rectangle.right = snap_rect.left + self.snapping_offset[0]
            self.rectangle.top = snap_rect.top + self.snapping_offset[1]
    # def update(self, snap_rect, snap_direction):
    #     self.rectangle.topleft = (snap_rect.left + self.snapping_offset[0],
    #                               snap_rect.top + self.snapping_offset[1])
        # if snap_direction == 1:
        # self.rectangle.topleft(snap_rect.left + self.snap_points[snap_direction][0],
        #                        snap_rect.top + self.snap_points[snap_direction][1])

    def process_(self, time_passed):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.die()
        if self.damage_reduce > 0:
            self.damage -= self.damage_reduce
        if self.static:
            return
        self.fly(time_passed)