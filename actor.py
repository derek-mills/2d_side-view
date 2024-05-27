from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'

        self.acceleration = .5
        self.air_acceleration = .4
        self.jump_height: int = 22
        self.default_max_speed = 10
        self.max_jump_attempts = 2
        self.max_speed = 10

        self.rectangle.height = 149
        self.rectangle.width = 49
        self.target_height = self.rectangle.h
        self.target_width = self.rectangle.w
        self.rectangle_height_default = self.rectangle.height
        self.rectangle_width_default = self.rectangle.width
        self.rectangle_height_sit = self.rectangle.height * 0.6
        self.rectangle_width_sit = self.rectangle.width * 1.4
        self.rectangle_height_slide = self.rectangle.width
        self.rectangle_width_slide = self.rectangle.height
        # self.rectangle_height_slide = self.rectangle.height // 3
        # self.rectangle_width_slide = self.rectangle.height // 4 * 3

        self.ignore_user_input: bool = False

        self.__state = 'stand still'


    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        # print(f'[actor.set_state] new state: {new_state}')
        self.__state = new_state

    def process(self, time_passed):
        self.state_machine()
        super().process(time_passed)
        self.reset_self_flags()

    # def set_rect_height(self, height):
    #     floor = self.rectangle.bottom
    #     self.rectangle.height = height
    #     self.rectangle.bottom = floor
    #
    # def set_rect_width(self, width):
    #     floor = self.rectangle.bottom
    #     center = self.rectangle.centerx
    #     right = self.rectangle.right
    #     left = self.rectangle.left
    #     self.rectangle.width = width
    #     if self.speed > 0:
    #         if self.look == 1:
    #             self.rectangle.left = left
    #         else:
    #             self.rectangle.right = right
    #     else:
    #         self.rectangle.centerx = center
    #     self.rectangle.bottom = floor

    def set_action(self, new_action):
        # print(f'[actor set action] Setting new action: {new_action}')
        # if self.ignore_user_input:
        #     return

        # RIGHT actions
        if new_action == 'right action':
            if self.__state == 'crouch':
                if self.look == -1:
                    self.set_state('crouch turn right')
                else:
                    self.set_state('crawl right')
            elif self.__state == 'stand still':
                if self.look == 1:
                    self.set_state('run right')
                else:
                    self.set_state('turn right')
            elif self.__state == 'run left':
                # self.set_state('turn left')
                self.set_action('right action cancel')
        elif new_action == 'right action cancel':
            if self.__state == 'crawl right':
                self.set_state('crouch')
            elif self.__state == 'run right':
                self.set_state('stand still')

        # LEFT actions
        elif new_action == 'left action':
            if self.__state == 'crouch':
                if self.look == 1:
                    self.set_state('crouch turn left')
                else:
                    self.set_state('crawl left')
            elif self.__state == 'stand still':
                if self.look == -1:
                    self.set_state('run left')
                else:
                    self.set_state('turn left')
            elif self.__state == 'run right':
                # self.set_state('turn left')
                self.set_action('left action cancel')
        elif new_action == 'left action cancel':
            if self.__state == 'crawl left':
                self.set_state('crouch')
            elif self.__state == 'run left':
                self.set_state('stand still')

        # DOWN actions
        elif new_action == 'down action':
            # if self.__state in ('hanging on edge', 'hanging on ghost'):
            #     self.set_state('release edge')
            #     return
            if self.is_stand_on_ground:
                if self.__state in ('stand still', 'run right', 'run left' ):
                    self.set_state('crouch down')

        elif new_action == 'down action cancel':
            if self.__state == 'crouch':
                if self.is_enough_space_above:
                    self.set_state('crouch rise')
            elif 'crawl' in self.__state:
                if self.is_enough_space_above:
                    self.set_state('crouch rise')

        # UP action
        elif new_action == 'up action':
            if self.__state == 'hanging on edge' and self.is_enough_space_above:
                self.set_state('climb on')

        # JUMP
        elif new_action == 'jump action':
            if self.jump_attempts_counter == 0:
                return
            # if self.__state == 'jump':
            #     return
            if self.__state in ('crouch', 'crawl right', 'crawl left') and self.is_stand_on_ground:
                if self.influenced_by_obstacle:
                    # Jump off a ghost platform:
                    # print('sdad')
                    if self.obstacles_around[self.influenced_by_obstacle].is_ghost_platform:
                        self.set_state('hop down from ghost')
                        return
                if (self.look == 1 and self.is_enough_space_right) or\
                        (self.look == -1 and self.is_enough_space_left):
                    self.set_state('slide')
            elif self.__state == 'hanging on ghost':
                self.set_state('release edge')
            elif self.__state == 'hanging on edge':
                self.set_state('release edge')
            else:
                self.set_state('jump')
        elif new_action == 'jump action cancel':
            if self.just_got_jumped:
                self.set_state('jump cancel')

        # HOP BACK
        elif new_action == 'hop back':
            if self.is_stand_on_ground:
                self.set_state('hop back')
        elif new_action == 'hop back action cancel':
            # self.set_state('jump cancel')
            if self.just_got_jumped:
                self.just_got_jumped = False
            self.is_abort_jump = True
            self.ignore_user_input = False
            # self.movement_direction_inverter = 1

    def state_machine(self):
        if self.__state == 'crouch down':                       # CROUCH DOWN PROCESS
            self.is_crouch = True
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.set_new_desired_width(self.rectangle_width_sit, 3)
            # self.set_rect_height(self.rectangle_height_sit)
            # self.set_rect_width(self.rectangle_width_sit)
            self.set_state('crouch')
        elif self.__state == 'crouch':                          # CROUCH
            self.speed = 0
            self.heading[0] = 0
        elif self.__state == 'crouch rise':  # CROUCH UP PROCESS
            self.is_crouch = False
            self.speed = 0
            self.set_state('stand still')
            self.check_space_around()
            if not self.is_enough_space_above:
                self.set_state('crouch down')
        # elif self.__state == 'crawl stop':
        elif self.__state == 'crawl right':
            # self.look = 1
            self.speed = self.max_speed // 3
            # self.heading[0] = 1
        elif self.__state == 'crawl left':
            # self.look = 1
            self.speed = self.max_speed // 3
            # self.heading[0] = -1
        elif self.__state == 'jump':
            if not self.just_got_jumped:
                self.just_got_jumped = True
                self.jump_attempts_counter -= 1
                self.is_jump = True
                self.influenced_by_obstacle = None
                self.jump_height = self.max_jump_height
                self.set_new_desired_height(self.rectangle_height_default + 15, 1)
                self.set_new_desired_width(self.rectangle_width_default - 15, 1)
            self.is_abort_jump = False
        elif self.__state == 'jump cancel':                     # CANCEL JUMP
            self.just_got_jumped = False
            self.is_abort_jump = True
            self.set_new_desired_height(self.rectangle_height_default, 1)
            self.set_new_desired_width(self.rectangle_width_default, 1)
            self.set_state('stand still')
        elif self.__state == 'slide':                           # SLIDE PREPARING
            self.speed = self.max_speed * 2.5
            self.set_new_desired_height(self.rectangle_height_slide, 10)
            self.set_new_desired_width(self.rectangle_width_slide, 6)
            # self.set_rect_width(self.rectangle_width_slide)
            # self.set_rect_height(self.rectangle_height_slide)
            self.check_space_around()
            if (self.look == 1 and self.is_enough_space_right) or\
                    (self.look == -1 and self.is_enough_space_left):
                self.ignore_user_input = True
                self.set_state('sliding')
            else:
                self.speed = 0
                # self.speed = self.max_speed // 2
                self.set_new_desired_height(self.rectangle_height_sit, 3)
                self.set_new_desired_width(self.rectangle_width_sit, 2)
                # self.set_rect_width(self.rectangle_width_sit)
                # self.set_rect_height(self.rectangle_height_sit)
                self.set_state('crouch')
        elif self.__state == 'hop back':                        # HOP BACK
            self.ignore_user_input = True
            if not self.just_got_jumped:
                self.just_got_jumped = True
                self.jump_attempts_counter -= 1
                self.is_jump = True
                self.influenced_by_obstacle = None
                self.jump_height = self.max_jump_height // 2
                self.speed = self.max_speed
                self.movement_direction_inverter = -1
                self.heading[0] = 0
                self.idle_counter = 30
            self.is_abort_jump = False
            self.set_state('hopping back process')
        elif self.__state == 'hopping back process':            # HOPPING BACK PROCESS
            if self.idle_counter > 0:
                self.idle_counter -= 1
            else:
                if self.speed <= 0:
                    self.ignore_user_input = False
                    if self.just_got_jumped:
                        self.just_got_jumped = False
                    self.is_abort_jump = True
                    # self.movement_direction_inverter = 1
                    # self.set_state('crouch')
                    self.set_state('stand still')
        elif self.__state == 'sliding':                         # SLIDING PROCESS
            self.heading[0] = 0
            if self.speed == 0:
                self.set_state('slide rise')
        elif self.__state == 'slide rise':                      # RISING AFTER SLIDE IS OVER
            self.check_space_around()
            if self.is_enough_space_above:
                self.ignore_user_input = False
                self.set_new_desired_height(self.rectangle_height_sit, 5)
                self.set_new_desired_width(self.rectangle_width_sit,10)
                # self.set_rect_width(self.rectangle_width_sit)
                # self.set_rect_height(self.rectangle_height_sit)
                self.set_state('crouch')
            else:
                self.speed = self.max_speed // 3
                if self.is_enough_space_above:
                    self.set_state('crouch down')

                # self.set_state('autocrawling')
        elif self.__state == 'stand still':                     # STANDING STILL
            self.heading[0] = 0
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'turn left':                       # TURN LEFT
            if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
            else:
                self.look = -1
                self.heading[0] = -1
                self.set_state('stand still')

            # self.is_move_left = True
            # self.look = -1
            # print('jj')
            # self.set_state('stand still')
        elif self.__state == 'turn right':                      # TURN RIGHT
            if self.look == -1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
            else:
                self.look = 1
                self.heading[0] = 1
                self.set_state('stand still')

            # self.is_move_right = True
            # self.look = 1
            # self.set_state('stand still')
        elif self.__state == 'crouch turn left':                # CROUCH TURN RIGHT
            self.look = -1
            self.set_state('crouch')
        elif self.__state == 'crouch turn right':               # CROUCH TURN LEFT
            self.look = 1
            self.set_state('crouch')
        elif self.__state == 'run left':                        # RUN LEFT
            self.look = -1
            self.heading[0] = -1
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'run right':                        # RUN RIGHT
            self.look = 1
            self.heading[0] = 1
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'has just grabbed edge':            # GRAB THE EDGE
            self.potential_moving_distance = 0
            self.is_edge_grabbed = True
            self.fall_speed = 0
            self.heading[0] = 0
            self.speed = 0
            self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            if self.look == -1:
                self.rectangle.left = self.obstacles_around[self.influenced_by_obstacle].rectangle.right
                self.is_enough_space_left = False
            else:
                self.rectangle.right = self.obstacles_around[self.influenced_by_obstacle].rectangle.left
                self.is_enough_space_right = False
            # self.jump_attempts_counter = 3
            # self.jump_attempts_counter = self.max_jump_attempts
            self.set_state('hanging on edge')
        elif self.__state == 'hop down from ghost':             # HOP DOWN THE GHOST PLATFORM
            # self.rectangle.centery = self.obstacles_around[self.influenced_by_obstacle].rectangle.bottom + 20
            self.potential_moving_distance = 0
            self.is_edge_grabbed = True
            self.ignore_user_input = True
            self.idle_counter = 25
            self.fall_speed = 0
            self.heading[0] = 0
            self.speed = 0
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.set_new_desired_width(self.rectangle_width_sit, 5)
            # self.rectangle.height = self.rectangle_height_default
            self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.bottom
            self.reset_self_flags()
            # if self.look == -1:
            #     self.rectangle.left = self.obstacles_around[self.influenced_by_obstacle].rectangle.right
            #     self.is_enough_space_left = False
            # else:
            #     self.rectangle.right = self.obstacles_around[self.influenced_by_obstacle].rectangle.left
            #     self.is_enough_space_right = False
            # self.jump_attempts_counter = 3
            # self.jump_attempts_counter = self.max_jump_attempts
            self.set_state('hanging on ghost')
        elif self.__state == 'hanging on edge':                 # HANGING ON THE EDGE
            self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        elif self.__state == 'hanging on ghost':                # HANGING ON THE GHOST PLATFORM
            self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            if self.idle_counter > 0:
                self.idle_counter -= 1
            else:
                self.ignore_user_input = False
        elif self.__state == 'release edge':                    # RELEASE
            self.is_edge_grabbed = False
            self.influenced_by_obstacle = None
            self.speed = 0
            self.ignore_user_input = False
            if self.is_stand_on_ground:
                self.set_state('stand still')
        elif self.__state == 'climb on':                        # START CLIMBING ON AN OBSTACLE
            self.ignore_user_input = True
            self.set_new_desired_height(self.rectangle_height_sit // 2, 4)
            self.set_state('climb on raise')
        elif self.__state == 'climb on raise':                        # START CLIMBING ON AN OBSTACLE
            if self.rectangle.height <= self.rectangle_height_sit // 2:
                self.ignore_user_input = False
                if self.influenced_by_obstacle:
                    self.jump_attempts_counter = 0
                    self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
                    self.rectangle.centerx += 20 * self.look
                    self.is_edge_grabbed = False
                    # self.influenced_by_obstacle = None
                    self.set_state('stand still')
                else:
                    self.set_state('stand still')
            else:
                self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top

    def reset_self_flags(self):
        self.is_move_left = False
        self.is_move_right = False
        self.is_move_up = False
        self.is_move_down = False
        self.is_jump = False