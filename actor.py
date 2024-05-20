from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'

        self.acceleration = 1
        self.jump_height: int = 22

        self.rectangle.height = 150
        self.rectangle_height_default = self.rectangle.height
        self.rectangle_width_default = self.rectangle.width
        self.rectangle_height_sit = 90
        self.rectangle_width_sit = self.rectangle.width
        self.rectangle_height_slide = 45
        self.rectangle_width_slide = 130

        self.ignore_user_input: bool = False

        self.__state = 'stand still'


    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        print(f'[actor.set_state] new state: {new_state}')
        self.__state = new_state

    def process(self, time_passed):
        self.state_machine()
        super().process(time_passed)

    def set_rect_height(self, height):
        floor = self.rectangle.bottom
        self.rectangle.height = height
        self.rectangle.bottom = floor

    def set_rect_width(self, width):
        floor = self.rectangle.bottom
        center = self.rectangle.centerx
        right = self.rectangle.right
        left = self.rectangle.left
        self.rectangle.width = width
        if self.speed > 0:
            if self.look == 1:
                self.rectangle.left = left
            else:
                self.rectangle.right = right
        else:
            self.rectangle.centerx = center
        self.rectangle.bottom = floor

    def set_action(self, new_action):
        if self.ignore_user_input:
            return

        # RIGHT actions
        if new_action == 'right action':
            if self.__state == 'crouch':
                if self.look == -1:
                    self.set_state('crouch turn right')
                else:
                    ...
            elif self.__state == 'stand still':
                if self.look == 1:
                    self.set_state('run right')
                else:
                    self.set_state('turn right')
            elif self.__state == 'run left':
                # self.set_state('turn left')
                self.set_action('right action cancel')
        elif new_action == 'right action cancel':
            if self.__state == 'run right':
                self.set_state('stand still')

        # LEFT actions
        elif new_action == 'left action':
            if self.__state == 'crouch':
                if self.look == 1:
                    self.set_state('crouch turn left')
                else:
                    ...
            elif self.__state == 'stand still':
                if self.look == -1:
                    self.set_state('run left')
                else:
                    self.set_state('turn left')
            elif self.__state == 'run right':
                # self.set_state('turn left')
                self.set_action('left action cancel')
        elif new_action == 'left action cancel':
            if self.__state == 'run left':
                self.set_state('stand still')

        # DOWN actions
        elif new_action == 'down action':
            if self.__state == 'hanging on edge':
                self.set_state('release edge')
            # if self.is_edge_grabbed:
            #     self.is_edge_grabbed = False
            #     self.set_state('stand still')
            elif self.__state == 'stand still' and self.is_stand_on_ground:
                self.set_state('crouch down')

        elif new_action == 'down action cancel':
            if self.__state == 'crouch':
                if self.is_enough_space_above:
                    self.set_state('crouch rise')

        # UP action
        elif new_action == 'up action':
            if self.__state == 'hanging on edge' and self.is_enough_space_above:
                self.set_state('climb on')

        # JUMP
        elif new_action == 'jump action':
            # self.set_state('jump')
            if self.__state == 'crouch' and self.is_stand_on_ground:
                if self.influenced_by_obstacle:
                    # Jump off a ghost platform:
                    # print('sdad')
                    if self.obstacles_around[self.influenced_by_obstacle].is_ghost_platform:
                        self.rectangle.centery = self.obstacles_around[self.influenced_by_obstacle].rectangle.bottom + 20
                        self.set_state('crouch rise')
                        return

                if (self.look == 1 and self.is_enough_space_right) or\
                        (self.look == -1 and self.is_enough_space_left):
                    self.set_state('slide')
                # self.set_state('slide')

            elif self.__state == 'hanging on edge':
                ...
                # self.set_state('climb on')
            # elif self.is_stand_on_ground:
            else:
                if not self.just_got_jumped:
                    self.just_got_jumped = True
                    self.jump_attempts_counter -= 1
                    self.is_jump = True
                    self.influenced_by_obstacle = None
                self.is_abort_jump = False

        elif new_action == 'jump action cancel':
            # self.set_state('jump cancel')
            if self.just_got_jumped:
                self.just_got_jumped = False
            self.is_abort_jump = True

    def state_machine(self):
        # CROUCH
        if self.__state == 'crouch down':
            self.is_crouch = True
            self.set_rect_height(self.rectangle_height_sit)
            self.set_rect_width(self.rectangle_width_sit)
            self.set_state('crouch')
        elif self.__state == 'crouch':
            ...
        elif self.__state == 'crouch rise':
            self.is_crouch = False
            self.set_rect_height(self.rectangle_height_default)
            self.set_rect_width(self.rectangle_width_default)
            self.set_state('stand still')
        # SLIDE
        elif self.__state == 'slide':
            # self.speed *=
            self.speed = self.max_speed * 1.5
            self.set_rect_width(self.rectangle_width_slide)
            self.set_rect_height(self.rectangle_height_slide)
            self.check_space_around()
            if (self.look == 1 and self.is_enough_space_right) or\
                    (self.look == -1 and self.is_enough_space_left):
                self.set_state('sliding')
                self.ignore_user_input = True
            else:
                self.speed = self.max_speed
                self.set_rect_width(self.rectangle_width_sit)
                self.set_rect_height(self.rectangle_height_sit)
                self.set_state('crouch')

        elif self.__state == 'sliding':
            # self.set_rect_width(self.rectangle_width_slide)
            # self.set_rect_height(self.rectangle_height_slide)
            if self.speed == 0:
                self.set_state('slide rise')
        elif self.__state == 'slide rise':
            self.ignore_user_input = False
            self.set_rect_width(self.rectangle_width_sit)
            self.set_rect_height(self.rectangle_height_sit)
            self.set_state('crouch')
            # self.set_state('stand still')
        elif self.__state == 'stand still':
            ...
        elif self.__state == 'turn left':
            self.is_move_left = True
            self.set_state('stand still')
        elif self.__state == 'turn right':
            self.is_move_right = True
            self.set_state('stand still')
        elif self.__state == 'crouch turn left':
            self.look = -1
            self.set_state('crouch')
        elif self.__state == 'crouch turn right':
            self.look = 1
            self.set_state('crouch')
        elif self.__state == 'run left':
            self.is_move_left = True
        elif self.__state == 'run right':
            self.is_move_right = True
        elif self.__state == 'has just grabbed edge':
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
        elif self.__state == 'hanging on edge':
            ...
        elif self.__state == 'release edge':
            self.is_edge_grabbed = False
            self.influenced_by_obstacle = None
            if self.is_stand_on_ground:
                self.set_state('stand still')
        elif self.__state == 'climb on':
            # self.jump_attempts_counter = self.max_jump_attempts
            self.jump_attempts_counter = 0
            self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            self.rectangle.centerx += 10 * self.look
            self.is_edge_grabbed = False
            # self.influenced_by_obstacle = None
            self.set_state('crouch')


    def reset_self_flags(self):
        self.is_move_left = False
        self.is_move_right = False
        self.is_jump = False