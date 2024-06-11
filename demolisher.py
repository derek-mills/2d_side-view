# from obstacle import *
from entity import *
from pygame import Rect

class Demolisher(Entity):
# class Demolisher(object):
# class Demolisher(Obstacle):

    def __init__(self):
        super().__init__()
        # self.id: int = 0
        self.type = 'demolisher'
        self.acceleration = 0.1
        # self.air_acceleration = 0
        # self.max_speed = 0
        self.snap_to_actor: int = 0  # Active actor which cause this demolisher to be glued.
        self.snapping_offset = list()
        self.damage: float = 0.
        self.damage_reduce: float = 0.
        self.parent_id: int = -1
        self.static = True
        self.bounce = False
        self.aftermath: str = ''  # Description of the demolisher behavior after TTL timer runs out.
        self.flyer = False
        # self.rectangle = Rect(0, 0, 50, 50)

    def update(self, snap_side, snap_rect):
        if snap_side == 1:  # Snapping to the actor's right side
            self.rectangle.left = snap_rect.right + self.snapping_offset[0]
            self.rectangle.top = snap_rect.top + self.snapping_offset[1]
        else:
            self.rectangle.right = snap_rect.left + self.snapping_offset[0]
            self.rectangle.top = snap_rect.top + self.snapping_offset[1]

    def detect_obstacle_collision(self):
        # return
        self.is_being_collided_now = False

        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.rectangle):
                self.is_being_collided_now = True
                return

    def process_demolisher(self, time_passed):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                # if self.aftermath == 'disappear':
                self.die()
                return
        if self.damage_reduce > 0:
            self.damage -= self.damage_reduce
        if self.is_collideable:
            # print('Demolisher check collisions with ', self.obstacles_around.keys())
            self.calculate_colliders()
            self.detect_collisions()
            # self.detect_obstacle_collision()
            if self.is_being_collided_now:
                if self.bounce:
                    ...
                else:
                    self.die()
                    return
        if not self.static:
            self.calculate_speed()
            if self.flyer:
                self.fly(time_passed)
            else:
                self.move(time_passed)
            if self.is_gravity_affected:
                self.calculate_fall_speed()  # Discover speed and potential fall distance
                self.fall()