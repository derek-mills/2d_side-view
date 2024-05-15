from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'

        # self.is_need_to_grab_edge: bool = True
        # self.edge

        self.jump_height: int = 22
        self.rectangle.height = 150
        self.rectangle_height_default = self.rectangle.height

        self.__state = 'stand still'

    def process(self, time_passed):
        self.state_machine()
        super().process(time_passed)

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state

    def set_action(self, new_action):
        # LEFT actions
        if new_action == 'left action':
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

        # RIGHT actions
        elif new_action == 'right action':
            if self.__state == 'crouch':
                if self.look == -1:
                    self.set_state('crouch turn right')
                else:
                    ...
            elif self.__state == 'stand still':
                if self.look == -1:
                    self.set_state('turn right')
                else:
                    self.set_state('run right')
        elif new_action == 'right action cancel':
            if self.__state == 'run right':
                self.set_state('stand still')

        # DOWN actions
        elif new_action == 'down action':
            if self.__state == 'stand still':
                self.set_state('crouch down')
        elif new_action == 'down action cancel':
            if self.__state == 'crouch':
                self.set_state('crouch rise')

        elif new_action == 'crouch':
            if self.__state == 'crouch down':
                self.set_state('crouch')
            else:
                self.set_state('crouch')
        elif new_action == 'crouch rise':
            self.set_state('stand still')

    def state_machine(self):
        if self.__state == 'crouch':
            ...
        elif self.__state == 'stand still':
            ...
        elif self.__state == 'crouch down':
            self.is_crouch = True
            self.rectangle.height = 90
            self.rectangle.y -= 100
            self.set_state('crouch')
        elif self.__state == 'crouch rise':
            self.is_crouch = False
            self.rectangle.y -= 150
            self.rectangle.height = self.rectangle_height_default
            self.set_state('stand still')
        elif self.__state == 'turn left':
            # self.look = -1
            self.is_move_left = True
            self.set_state('stand still')
        elif self.__state == 'turn right':
            # self.look = 1
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


    def reset_self_flags(self):
        self.is_move_left = False
        self.is_move_right = False
        self.is_jump = False