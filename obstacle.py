from entity import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'obstacle'
        self.is_ghost_platform: bool = False
        self.max_speed = 2

    def process(self, time_passed):
        # ...
        # super().process(time_passed)
        if self.is_move_left:
            # if self.is_edge_grabbed:
            #     if self.look == -1 and self.is_jump:
            #         self.is_edge_grabbed = False
            #     if self.look == 1:  # Attempting to release the edge
            #         self.is_edge_grabbed = False
            #         self.is_jump = False
            #     # return
            if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
            # elif self.is_crouch:
            #     self.look = -1
            #     self.heading[0] = 0
            else:
                self.look = -1
                self.heading[0] = -1
        elif self.is_move_right:
            # if self.is_edge_grabbed:
            #     if self.look == 1 and self.is_jump:
            #         self.is_edge_grabbed = False
            #     if self.look == -1:  # Attempting to release the edge
            #         self.is_edge_grabbed = False
            #         self.is_jump = False
            #     # return
            if self.look == -1 and self.speed > 0:  #
                self.heading[0] = 0
            else:
                self.look = 1
                self.heading[0] = 1
        else:
            self.heading[0] = 0

        # if self.is_jump and self.jump_attempts_counter > 0:
        #     # Jump
        #     self.fall_speed = -self.jump_height
        #     self.is_jump = False
        #     self.is_stand_on_ground = False

        # self.check_space_around()  # Detect obstacles on the right and left sides
        self.fall_speed_calc()  # Discover speed and potential fall distance
        self.speed_calc()       # Discover fall speed and potential move distance
        self.colliders_calc()   # Calculate colliders around actor based on his current movement and fall speeds.
        # self.detect_collisions()

        if self.is_gravity_affected:
            if not self.is_stand_on_ground:
                self.fall()
        self.move()