from entity import Entity
from constants import *

class Particle(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'particle'
        self.subtype = 'splatter'
        self.color = RED
        self.is_collideable = True
        self.is_gravity_affected = True
        self.is_force_render: bool = True  # Always render this obstacle in realtime.
        self.max_speed = .2
        self.max_jump_height = 5
        self.let_actors_pass_through: bool = True
        self.bounce = False
        self.bounce_factor: float = 0.  # Vertical and horizontal speed reducing after every bounce.


    def process_particle(self):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                self.die()
                return
        if self.is_collideable:
            # print('Demolisher check collisions with ', self.obstacles_around.keys())
            self.calculate_colliders()
            self.detect_collisions_with_obstacles()
            if self.is_being_collided_now:
                if self.bounce:
                    self.speed *= self.bounce_factor
                    if self.collided_left:
                        self.look = 1
                    elif self.collided_right:
                        self.look = -1
                    elif self.collided_bottom:
                        self.fall_speed *= -self.bounce_factor  # Bounce up from the floor.
                        self.is_stand_on_ground = False
                else:
                    self.die()
                    return
        self.calculate_speed()
        if self.subtype == 'sparkle':
            self.fly()
        else:
            self.move()
        if self.is_gravity_affected:
            self.calculate_fall_speed()  # Discover speed and potential fall distance
            self.fall()

    def detect_collisions_with_obstacles(self):
        # self.influenced_by_obstacle = None
        sorted_obs = {
            'above': list(),
            'below': list(),
            'right': list(),
            'left': list(),
        }
        self.collided_top = False
        self.collided_left = False
        self.collided_right = False
        self.collided_bottom =False
        self.is_being_collided_now = False
        # self.ignore_user_input = False
        self.is_stand_on_ground = False
        bottom_already_changed = False

        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            if obs.let_actors_pass_through:
                continue
            if obs.rectangle.centery < self.rectangle.centery:
                sorted_obs['above'].append(obs.id)
            elif obs.rectangle.centery > self.rectangle.centery:
                sorted_obs['below'].append(obs.id)
            if obs.rectangle.right < self.rectangle.centerx:
                sorted_obs['left'].append(obs.id)
            elif obs.rectangle.left > self.rectangle.centerx:
                sorted_obs['right'].append(obs.id)

        #-----------------------------------
        # Check RIGHT
        for key in sorted_obs['right']:
            obs = self.obstacles_around[key]
            # obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue

            if obs.rectangle.colliderect(self.collision_detector_right):
                # obs.is_being_collided_now = True
                self.is_being_collided_now = True
                self.collided_right = True
                # if self.look == 1: # Obstacle is on the right, and actor also looks to the right, and hangs on the edge.
                #     if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                #         self.rectangle.right = obs.rectangle.left - 2  # Drop down the actor
                #         self.set_state('release edge')
                #     else:
                #         if self.movement_direction_inverter == -1:
                #             continue
                #
                #         self.potential_moving_distance = obs.rectangle.left - self.collision_detector_right.left
                #         # self.rectangle.right = obs.rectangle.left
                #         self.is_enough_space_right = False
                #         self.heading[0] = 0
                #         self.speed = 0
                #         continue

        #-----------------------------------
        # Check LEFT
        for key in sorted_obs['left']:
            obs = self.obstacles_around[key]
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.collision_detector_left):
                self.collided_left = True
                self.is_being_collided_now = True

                # if self.look == -1: # Obstacle is on the left, and actor also looks to the left, and hangs on the edge.
                #     if self.get_state() == 'hanging on edge' and self.influenced_by_obstacle != obs.id:
                #         self.rectangle.left = obs.rectangle.right + 2  # Drop down the actor
                #         self.set_state('release edge')
                #     else:
                #
                #         if self.movement_direction_inverter == -1:
                #             continue
                #
                #         self.potential_moving_distance = self.collision_detector_left.right - obs.rectangle.right
                #         # self.rectangle.left = obs.rectangle.right
                #         self.is_enough_space_left = False
                #         self.heading[0] = 0
                #         self.speed = 0
                #         continue
        # -----------------------------------
        # Check bottom
        for key in sorted_obs['below']:
            obs = self.obstacles_around[key]
            if obs.rectangle.colliderect(self.collision_detector_bottom):
                # if bottom_already_changed and obs.rectangle.top > self.rectangle.bottom:
                #     # Current obstacle lower than the actor's rectangle after at least one bottom collision has been registered.
                #     # Skip it.
                #     continue

                self.collided_bottom = True
                self.is_being_collided_now = True
                self.rectangle.bottom = obs.rectangle.top
                self.is_stand_on_ground = True
                self.influenced_by_obstacle = obs.id
                self.jump_attempts_counter = self.max_jump_attempts
                bottom_already_changed = True
                # break
                    # continue
        # -----------------------------------
        # Check top
        for key in sorted_obs['above']:
            obs = self.obstacles_around[key]
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.collision_detector_top):
                self.is_being_collided_now = True
                self.collided_top = True

                if self.fall_speed < 0:
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    # continue