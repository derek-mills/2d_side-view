from entity import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'obstacle'
        self.is_ghost_platform: bool = False
        self.max_speed = .2
        self.is_being_collided_now: bool = False
        self.let_actors_pass_through: bool = False
        self.idle = False

        self.active_flag = False
        self.active = False
        self.actions = dict()
        self.actions_set_number = 0
        self.current_action = -1
        self.need_next_action = True
        self.wait_counter = 0
        self.repeat_counter = -1
        self.teleport = False
        self.teleport_description = dict()
        self.trigger = False
        self.trigger_activated: bool = False
        self.trigger_description = dict()

    def process_(self):
        if self.active:
            if self.idle:
                return
            if self.wait_counter > 0:
                self.wait_counter -= 1
                # if self.wait_counter == 0:
                #     self.need_next_action = True
                return
            if self.need_next_action:
                self.need_next_action = False
                self.next_action()
                return
            # print(self.actions[self.actions_set_number])
            # print(self.actions[self.actions_set_number][self.current_action])
            # print(self.actions_set_number, self.current_action)

            if self.actions[self.actions_set_number][self.current_action][0] == 'repeat':
                self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'move':
                self.fly()
                if self.is_destination_reached:
                    self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'die':
                self.die()
            elif self.actions[self.actions_set_number][self.current_action][0] == 'stop':
                self.active = False
                self.need_next_action = False
                return
            elif self.actions[self.actions_set_number][self.current_action][0] == 'wait':
                self.wait_counter = self.actions[self.actions_set_number][self.current_action][1]
                self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'turn on actions set':
                if self.actions[self.actions_set_number][self.current_action][1] != 0:
                    self.actions_set_number = self.actions[self.actions_set_number][self.current_action][1]
                else:
                    self.actions_set_number += 1
                self.current_action = -1
                self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'switch visibility':
                self.invisible = False if self.invisible else True
                self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'switch passability':
                self.is_collideable = False if self.is_collideable else True
                print(f'[obs process] {self.name} changed collision status: {self.is_collideable=}')
                self.need_next_action = True
            elif self.actions[self.actions_set_number][self.current_action][0] == 'switch gravity':
                self.is_gravity_affected = False if self.is_gravity_affected else True
                # print(f'[obs process] {self.name} changed collision status: {self.is_collideable=}')
                self.need_next_action = True
        super().process()
        # super().process(time_passed)


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

    def reset_actions(self):
        self.actions = None
        self.current_action = -1
        self.need_next_action = False
        self.wait_counter = 0
        self.repeat_counter = -1

    def next_action(self):
        print('ENTERING NEXT ACTION')

        if not self.actions:
            return
        if self.actions[self.actions_set_number][self.current_action][0] == 'repeat':
            if self.actions[self.actions_set_number][self.current_action][1] == 0:
                # print('return to first action')
                self.current_action = 0
                # return
            else:
                if self.repeat_counter > 0:
                    self.repeat_counter -= 1
                    if self.repeat_counter == 0:
                        self.current_action += 1
                    else:
                        self.current_action = 0
                else:
                    self.repeat_counter = self.actions[self.actions_set_number][self.current_action][1]
            # self.need_next_action = True
        else:
            self.current_action += 1

        if self.current_action == len(self.actions[self.actions_set_number]):
            # End of action sequence reached.
            print('ENd reached '*5)
            self.active = False
            self.current_action = -1
            return

        # print(f'{self.actions[self.current_action]=}')

        if self.actions[self.actions_set_number][self.current_action][0] == 'move':
            self.is_destination_reached = False
            if self.actions[self.actions_set_number][self.current_action][1] == 'start point':
                self.destination_point = self.origin_xy
                self.destination_area.update(0,0,0,0)
            elif self.actions[self.actions_set_number][self.current_action][1] == 'start area':
                self.destination_area.update(0,0, 100, 100)
                self.destination_area.center = self.origin_xy
                # self.destination_area.update(self.origin_xy[0], self.origin_xy[1], 100, 100)
            else:
                if len(self.actions[self.actions_set_number][self.current_action][1]) == 4:
                    # Destination described by four digits, so this is a square area, not a single point:
                    self.destination_area.update(self.actions[self.actions_set_number][self.current_action][1])
                else:
                    # Destination is just a single point:
                    self.destination_point = self.actions[self.actions_set_number][self.current_action][1]
                    self.destination_area.update(0, 0, 0, 0)
        print('current_action:', self.actions[self.actions_set_number][self.current_action])
        # elif self.actions[self.actions_set_number][self.current_action][0] == 'die':
        #     self.die()
        # elif self.actions[self.actions_set_number][self.current_action][0] == 'stop':
        #     self.active = False
        # elif self.actions[self.actions_set_number][self.current_action][0] == 'wait':
        #     self.wait_counter = self.actions[self.actions_set_number][self.current_action][1]
        # elif self.actions[self.actions_set_number][self.current_action][0] == 'switch visibility':
        #     self.invisible = False if self.invisible else True
        # elif self.actions[self.actions_set_number][self.current_action][0] == 'switch passability':
        #     self.is_collideable = False if self.is_collideable else True
        #     print(f'[next_action] {self.name} changed collision status: {self.is_collideable=}')
