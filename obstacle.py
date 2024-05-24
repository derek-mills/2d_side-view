from entity import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'obstacle'
        self.is_ghost_platform: bool = False
        self.max_speed = 2
        self.is_being_collided_now: bool = False

    def process_(self, time_passed):
        # ...
        # super().process(time_passed)
        if self.is_move_left:
            if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
            else:
                self.look = -1
                self.heading[0] = -1
        elif self.is_move_right:
            if self.look == -1 and self.speed > 0:  #
                self.heading[0] = 0
            else:
                self.look = 1
                self.heading[0] = 1
        elif self.is_move_up:
            self.fall_speed = -2
        else:
            self.heading[0] = 0

        # self.check_space_around()  # Detect obstacles on the right and left sides
        self.fall_speed_calc()  # Discover speed and potential fall distance
        self.speed_calc()       # Discover fall speed and potential move distance

        if self.is_collideable:
            self.colliders_calc()  # Calculate colliders around actor based on his current movement and fall speeds.
            self.detect_collisions()

        if self.is_gravity_affected:
            if not self.is_stand_on_ground:
                self.fall()
                # !!! RUDE HACK FOR TESTING PURPOSE!!!
                if self.rectangle.y < 0:
                    self.rectangle.y = 1000
        self.move()

    def detect_collisions(self):
        self.is_stand_on_ground = False
        # self.influenced_by_obstacle = None
        for key in self.obstacles_around.keys():
            if key == self.id:
                continue
            obs = self.obstacles_around[key]
            #-----------------------------------
            # Check RIGHT
            if obs.rectangle.colliderect(self.collision_detector_right) and not obs.is_ghost_platform:
                # if obs.is_ghost_platform:
                #     continue
                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == -1:  # Obstacle is on the right, but actor looks to the left.
                    self.rectangle.right = obs.rectangle.left - 2  # Push the actor
                    # self.influenced_by_obstacle = None
                    # self.is_edge_grabbed = False
                    # self.set_state('release edge')
                    continue
                # # Grab over the top of an obstacle.
                # if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge'):
                #     if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 30) and self.fall_speed > 0:
                #         # self.rectangle.right = obs.rectangle.left - 2
                #         self.influenced_by_obstacle = obs.id
                #         self.set_state('has just grabbed edge')
                #         self.state_machine()
                #         continue

                # if self.look == 1: # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                #     if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                #         self.rectangle.right = obs.rectangle.left - 2  # Drop down the actor
                #         self.set_state('release edge')

                self.potential_moving_distance = obs.rectangle.left - self.collision_detector_right.left
                # self.rectangle.right = obs.rectangle.left
                self.is_enough_space_right = False
                self.heading[0] = 0
                # self.speed = 0
                continue
            #-----------------------------------
            # Check LEFT
            if obs.rectangle.colliderect(self.collision_detector_left) and not obs.is_ghost_platform:
                # self.rectangle.left = obs.rectangle.right + 2

                # Check if obstacle has crawled from behind and pushed actor to his back:
                if self.look == 1:  # Obstacle is on the left, but actor looks to the right.
                    self.rectangle.left = obs.rectangle.right + 2  # Push the actor
                    # self.set_state('release edge')
                    continue

                # # Grab over the top of an obstacle.
                # if self.get_state() not in ('release edge', 'hanging on edge', 'has just grabbed edge'):
                #     if obs.rectangle.top >= self.rectangle.top > (obs.rectangle.top - 30) and self.fall_speed > 0:
                #         self.influenced_by_obstacle = obs.id
                #         self.set_state('has just grabbed edge')
                #         self.state_machine()
                #         continue

                # if self.look == -1: # Obstacle is on the left, and actor also looks to the left, and hangs on the edge.
                #     if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                #         self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
                #         self.set_state('release edge')

                self.potential_moving_distance = self.collision_detector_left.right - obs.rectangle.right
                # self.rectangle.left = obs.rectangle.right
                self.is_enough_space_left = False
                self.heading[0] = 0
                # self.speed = 0
                continue
            #-----------------------------------
            # Check top
            if self.fall_speed < 0 and not obs.is_ghost_platform:
                if obs.rectangle.colliderect(self.collision_detector_top):
                    # if obs.is_ghost_platform:
                    #     continue
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    continue
            # if self.fall_speed > 0:
            else:
                # -----------------------------------
                # Check bottom
                if obs.rectangle.colliderect(self.collision_detector_bottom):
                    # print('OOO')
                    # self.potential_falling_distance = obs.rectangle.top - self.collision_detector_bottom.top
                    self.rectangle.bottom = obs.rectangle.top
                    # self.rectangle.bottom = self.collision_detector_bottom.top
                    self.is_stand_on_ground = True
                    self.influenced_by_obstacle = obs.id
                    # self.fall_speed = 0
                    self.jump_attempts_counter = self.max_jump_attempts
                    # self.is_spacebar = False
                    continue
        # self.is_stand_on_ground = False
        # self.influenced_by_obstacle = None
