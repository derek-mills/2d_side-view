import sys

from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'
        self.inventory = dict()
        self.current_weapon = dict()
        self.current_weapon_demolishers_reveal_frames = list()
        self.is_collideable = True
        self.is_destructible = True

        # self.exp = 0
        # self.level = 0

        # self.weapon_snap_points ={
        #     'left hand': {},
        #     'right hand': {},
        # }

        self.ai_input_right_arrow = False
        self.ai_input_left_arrow = False
        self.ai_input_attack = False
        self.ai_input_jump = False

        self.acceleration = .5
        self.air_acceleration = .4
        self.jump_height: int = 22
        self.max_jump_attempts = 2

        # self.rectangle.height = 149
        # self.rectangle.width = 49
        # self.target_height = self.rectangle.h
        # self.target_width = self.rectangle.w
        # self.rectangle_height_default = self.rectangle.height
        # self.rectangle_width_default = self.rectangle.width
        # self.rectangle_height_sit = self.rectangle.height * 0.66
        # self.rectangle_width_sit = self.rectangle.width * 1.34
        # self.rectangle_height_slide = self.rectangle.width
        # self.rectangle_width_slide = self.rectangle.height

        self.__state = 'stand still'


        self.body = {
            'head': {
                # 'map rect': pygame.Rect(1,0,7,8),
                'to hit probability weight': 1,
                'available': True,
                'hardness': 2,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0,
                'bleeding': 0
            },
            'left hand': {
                # 'map rect': pygame.Rect(0,6,2,8),
                'to hit probability weight': 5,
                'status': {
                    'grab_something': False,
                    'grabbed': False
                },
                'available': True,
                'hardness': 1,
                'weapon': None,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0,
                'bleeding': 0,
            },
            'right hand': {
                'map rect': pygame.Rect(7,6,2,8),
                'to hit probability weight': 5,
                'status': {
                    'grab_something': False,
                    'grabbed': False
                },
                'available': True,
                'hardness': 1,
                'weapon': None,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0, 'bleeding': 0
            },
            'left leg': {
                'map rect': pygame.Rect(2,13, 2, 8),
                'to hit probability weight': 5,
                'available': True,
                'hardness': 1,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0,
                'bleeding': 0
            },
            'right leg': {
                'map rect': pygame.Rect(5,13,2, 8),
                'to hit probability weight': 5,
                'available': True,
                'hardness': 1,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0,
                'bleeding': 0
            },
            'torso': {
                'map rect': pygame.Rect(2,8,5,5),
                'to hit probability weight': 25,
                'hardness': 1,
                'consistency': 100,
                'consistency default': 100,
                'pain': 0,
                'bleeding': 0
            },
        }
        self.target = None

    def apply_measurements(self):
        self.target_height = self.rectangle.h
        self.target_width = self.rectangle.w
        self.rectangle_height_default = self.rectangle.height
        self.rectangle_width_default = self.rectangle.width
        self.rectangle_height_sit = self.rectangle.height * 0.66
        self.rectangle_width_sit = self.rectangle.width * 1.34
        self.rectangle_height_slide = self.rectangle.width
        self.rectangle_width_slide = self.rectangle.height

    def get_target(self, target):
        self.target = target

    def think(self):
        if self.think_type == 'chaser':
            if self.rectangle.left > self.target.rectangle.right:
                if self.rectangle.left - self.target.rectangle.right <= self.current_weapon['reach']:
                    self.ai_input_attack = True
                else:
                    self.ai_input_left_arrow = True
                    self.ai_input_right_arrow = False
            elif self.rectangle.right < self.target.rectangle.left:
                if self.target.rectangle.left - self.rectangle.right <= self.current_weapon['reach']:
                    self.ai_input_attack = True
                else:
                    self.ai_input_left_arrow = False
                    self.ai_input_right_arrow = True

        # if self.is_input_up_arrow:
        #     actor.set_action('up action')
        # else:
        #     # if actor.get_state() == 'up action':
        #     actor.set_action('up action cancel')
        #
        # if self.is_input_down_arrow:
        #     actor.set_action('down action')
        # else:
        #     # if actor.get_state() == 'down action':
        #     actor.set_action('down action cancel')

        if self.ai_input_right_arrow:
            self.set_action('right action')
        else:
            self.set_action('right action cancel')

        if self.ai_input_left_arrow:
            self.set_action('left action')
        else:
            self.set_action('left action cancel')

        if self.ai_input_jump:
            self.set_action('jump action')
        else:
            self.set_action('jump action cancel')

        # if self.is_l_alt and not self.l_alt_multiple_press_prevent:
        #     self.l_alt_multiple_press_prevent = True
        #     actor.set_action('hop back')
        # else:
        #     if actor.get_state() == 'hop back progress':
        #         actor.set_action('hop back action cancel')

        if self.ai_input_attack:
            self.ai_input_attack = False
            self.set_action('attack')

    def add_items_to_inventory(self, items):
        if not items:
            return
        # print(items)
        for item in items:
            if item['class'] not in self.inventory.keys():
                self.inventory[item['class']] = dict()
            if item['label'] in self.inventory[item['class']].keys():
                self.inventory[item['class']][item['label']]['quantity'] += 1
            else:
                self.inventory[item['class']][item['label']] = {'item': item.copy(), 'quantity': 1}

    def activate_weapon(self, uuid):
        if not self.inventory:
            return
        # print(self.inventory)
        if uuid == 0:
            all_weapons = list(self.inventory['weapons'].keys())
            self.body['right hand']['weapon'] = self.inventory['weapons'][all_weapons[0]]
        else:
            self.body['right hand']['weapon'] = self.inventory['weapons'][uuid]
        self.current_weapon = self.body['right hand']['weapon']['item']
        # print(self.current_weapon)
        # {'aimed fire': True, 'attack animation': 'stab', 'steal user input': True, 'leave particles': False, 'class': 'weapons', 'type': 'melee', 'sub-type': 'bladed', 'sound': 'sound_swing_2', 'droppable': True, 'need ammo': False, 'ammo': 0, 'label': 'KITCHEN KNIFE', 'sprite': 'kitchen knife', 'pierce': False, 'damager TTL': 200, 'damagers spread': False, 'damager static': True, 'damager radius': 1, 'damagers quantity': 1, 'damager reveal delay': 0, 'damager reveals with flash': False, 'damager brings light': False, 'damager fly speed reduce': 0, 'damager fly speed': 1.5, 'damager invisible': False, 'damager weight': 5, 'description': 'Casual kitchen knife.', 'reach': 1, 'weight': 5, 'hardness': 10, 'special': ('bleeding',)}
        # exit()

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        # print(f'[actor.set_state] new state: {new_state} {self.cycles_passed}')
        self.__state = new_state
        self.set_current_animation()

    def process(self):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
        self.state_machine()
        self.processing_rectangle_size()
        self.check_space_around()
        super().process()
        # super().process(time_passed)
        # self.reset_self_flags()

        # if (self.collided_top and self.collided_bottom) or (self.collided_right and self.collided_left):
        #     raise sys.exit()

    def set_action(self, new_action):
        # print(f'[actor set action] Setting new action: {new_action}')
        # if self.ignore_user_input:
        #     return

        # RIGHT actions
        if new_action == 'right action':
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'free', 'crouch', 'stand still', 'prone', 'run left', 'fly left', 'run right'):
                return
            if not self.is_stand_on_ground:
                if self.__state == 'jump':
                    self.is_jump_performed = True
                else:
                    self.is_jump_performed = False

                self.set_state('fly right')
            else:
                if self.__state == 'crouch':
                    if self.look == -1:
                        self.set_state('crouch turn right')
                    else:
                        self.set_state('crawl right')
                elif self.__state in ('free', 'stand still'):
                # elif self.__state == 'stand still':
                    if self.look == 1:
                        self.set_state('run right')
                    else:
                        self.set_state('turn right')
                elif self.__state == 'prone':
                    self.set_state('crawl prone right')
                elif self.__state in ('run left', 'fly left'):
                    self.set_action('left action cancel')

        elif new_action == 'right action cancel':
            if self.__state == 'crawl right':
                self.set_state('crouch')
            elif self.__state in ('run right', 'fly right'):
                # self.speed = 0
                self.set_state('stand still')
            elif self.__state == 'crawl prone right':
            # elif self.__state in ('crawl prone left', 'crawl prone right'):
                self.set_state('prone')

        # LEFT actions
        elif new_action == 'left action':
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'free', 'crouch', 'stand still', 'prone', 'run right', 'fly right', 'run left'):
            # if self.__state == 'hanging on edge'
                return
            if not self.is_stand_on_ground:
                if self.__state == 'jump':
                    self.is_jump_performed = True
                else:
                    self.is_jump_performed = False
                self.set_state('fly left')
            else:
                if self.__state == 'crouch':
                    if self.look == 1:
                        self.set_state('crouch turn left')
                    else:
                        self.set_state('crawl left')
                elif self.__state in ('free', 'stand still'):
                # elif self.__state == 'stand still':
                    if self.look == -1:
                        self.set_state('run left')
                    else:
                        self.set_state('turn left')
                elif self.__state == 'prone':
                # elif self.__state in ('prone', 'crawl prone'):
                    # self.look = -1
                    self.set_state('crawl prone left')
                elif self.__state in ('run right', 'fly right'):
                    # self.set_state('turn left')
                    self.set_action('right action cancel')

        elif new_action == 'left action cancel':
            if self.__state == 'crawl left':
                self.set_state('crouch')
            elif self.__state in ('run left', 'fly left'):
                # self.speed = 0
                self.set_state('stand still')
            elif self.__state == 'crawl prone left':
            # elif self.__state in ('crawl prone left', 'crawl prone right'):
                self.set_state('prone')

        # DOWN actions
        elif new_action == 'down action':
            # Apply filter of unwanted actions:
            if self.__state not in ('free', 'stand still', 'run right', 'run left', 'hanging on edge', 'hanging on ghost'):
                return

            if self.__state in ('hanging on edge', 'hanging on ghost'):
                self.set_state('release edge')
                return
            if self.is_stand_on_ground:
                if self.__state in ('stand still', 'run right', 'run left' ):
                    self.set_state('crouch down')
        elif new_action == 'down action cancel':
            if self.__state == 'crouch':
                if self.is_enough_height:
                    self.set_state('crouch rise')
            elif self.__state in ('crawl right', 'crawl left'):
                if self.is_enough_height:
                    self.set_state('crouch rise')

        # UP action
        elif new_action == 'up action':
            # Apply filter of unwanted actions:
            if self.__state not in ('hanging on edge', 'hanging on ghost'):
                return
            if self.__state in ('hanging on edge', 'hanging on ghost') and self.is_enough_height:
            # if self.__state == 'hanging on edge' and self.is_enough_space_above:
                self.set_state('climb on')
            # if self.__state in ('prone', 'crawl prone right', 'crawl prone left'):
            #     self.set_state('crouch down')

        # JUMP
        elif new_action == 'jump action':
            if self.is_jump_performed:
                return
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'crouch', 'crawl right', 'crawl left',
                                    # 'run right', 'run left', 'stand still', ):
                                    'run right', 'run left', 'stand still', 'fly left', 'fly right'):
                return

            if self.__state in ('crouch down', 'crouch rise', 'crouch', 'crawl right', 'crawl left') and self.is_stand_on_ground:
                if self.influenced_by_obstacle >= 0:
                    # Jump off a ghost platform:
                    if self.obstacles_around[self.influenced_by_obstacle].is_ghost_platform:
                        self.set_state('hop down from ghost')
                        return
                # self.set_new_desired_height(self.rectangle_height_slide, 0)
                # self.check_space_around()
                # if (self.look == 1 and self.is_enough_space_right) or\
                #         (self.look == -1 and self.is_enough_space_left):
                self.set_state('slide')
            else:
                if self.jump_attempts_counter == 0:
                    # self.set_state('free')
                    return
                if self.is_enough_space_above and self.__state != 'jump':
                    # self.is_grabbers_active = True
                    self.set_state('jump')
                # else:
                #     self.set_state('jump cancel')
        elif new_action == 'jump action cancel':
            # self.is_grabbers_active = False
            # if self.__state in ('jump', ):
            #     if self.just_got_jumped:
            #         self.set_state('jump cancel')
            if self.just_got_jumped:
                self.set_state('jump cancel')

        # HOP BACK
        elif new_action == 'hop back':
            # Apply filter of unwanted actions:
            if self.__state not in ('run left', 'run right', 'stand still', 'fly right', 'fly left', 'jump'):
                return
            # if self.is_stand_on_ground:
            #     if self.is_enough_space_above:
            self.set_state('hop back')
        elif new_action == 'hop back action cancel':
            # self.set_state('jump cancel')
            # self.is_grabbers_active = False
            if self.just_got_jumped:
                self.just_got_jumped = False
            self.is_abort_jump = True
            self.ignore_user_input = False
            # self.movement_direction_inverter = 1

        elif new_action == 'attack':
            # if self.is_stand_on_ground:
            if self.__state not in ('free', 'stand still', 'run right', 'run left', 'stand still', 'jump', 'crawl right', 'crawl left', \
                                    'crouch', 'fly right', 'fly left'):
                return
            self.set_state('attack')

    def state_machine(self):
        if self.__state == 'attack':                          # PREPARING ATTACK
            self.set_state(self.current_weapon['attack animation'])
            self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier']
            self.set_current_animation()
            self.ignore_user_input = self.current_weapon['ignore user input']
            if self.is_stand_on_ground:
                self.heading[0] = 0
        elif self.__state in ('stab', 'cast', 'whip'):                          # ATTACKING IN PROCESS...
            # self.speed = 0
            # print(self.frame_number, '-', self.current_frame)
            # if self.current_weapon_demolishers_reveal_frames:
            #     if self.frame_number == self.current_weapon_demolishers_reveal_frames[0]:
            #         self.summon_demolisher = True
            if self.animation_sequence_done:
                self.ignore_user_input = False
                # self.heading[0] = 0
                self.set_state('stand still')
        elif self.__state == 'crouch down':                       # CROUCH DOWN PROCESS
            self.is_crouch = True
            self.is_grabbers_active = False
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.set_new_desired_width(self.rectangle_width_sit, 3)
            self.set_state('crouch')
        elif self.__state == 'crouch':                          # CROUCH
            self.speed = 0
            self.heading[0] = 0
        elif self.__state == 'crouch turn left':                # CROUCH TURN RIGHT
            self.look = -1
            self.set_state('crouch')
        elif self.__state == 'crouch turn right':               # CROUCH TURN LEFT
            self.look = 1
            self.set_state('crouch')
        elif self.__state == 'crouch rise':  # CROUCH UP PROCESS
            self.is_crouch = False
            self.speed = 0
            self.set_new_desired_height(self.rectangle_height_default, 9)
            self.check_space_around()
            if self.is_enough_height:
                self.is_jump_performed = False
                self.set_state('stand still')
            else:
                self.set_state('crouch down')
                self.state_machine()
        elif self.__state == 'crawl right':
            # self.look = 1
            self.speed = self.max_speed // 3
            # self.heading[0] = 1
        elif self.__state == 'crawl left':
            # self.look = 1
            self.speed = self.max_speed // 3
            # self.heading[0] = -1
        elif self.__state == 'free':
            # self.heading[0] = 0
            ...
        elif self.__state == 'jump':
            # print('try to jump...')
            if not self.just_got_jumped:
                self.just_got_jumped = True
                self.jump_attempts_counter -= 1
                if self.fall_speed > -2:
                    self.is_grabbers_active = True
                self.is_jump = True
                self.influenced_by_obstacle = -1
                self.jump_height = self.max_jump_height
            else:
                if self.is_stand_on_ground:
                    self.is_jump_performed = True
                    self.heading[0] = 0
                    # self.just_got_jumped = True
                    # self.is_abort_jump = True
                    # self.is_jump_performed = False
                    self.set_state('stand still')
                    # self.set_state('jump cancel')
            self.is_abort_jump = False
        elif self.__state == 'jump cancel':                     # CANCEL JUMP
            self.just_got_jumped = False
            self.is_abort_jump = True
            self.is_jump_performed = False
            # self.set_new_desired_height(self.rectangle_height_default, 5)
            # self.set_new_desired_width(self.rectangle_width_default, 5)
            if self.is_stand_on_ground:
                self.set_state('stand still')
            else:
                if self.look == 1:
                    self.set_state('fly right')
                else:
                    self.set_state('fly left')
            # self.set_state('stand still')
        elif self.__state == 'hop back':                        # HOP BACK
            if self.is_stand_on_ground:
                if self.is_enough_space_above:
                    self.ignore_user_input = True
                    self.is_grabbers_active = False
                    if not self.just_got_jumped:
                        self.just_got_jumped = True
                        self.jump_attempts_counter -= 1
                        self.is_jump = True
                        self.influenced_by_obstacle = -1
                        self.jump_height = self.max_jump_height // 2
                        self.speed = self.max_speed
                        self.movement_direction_inverter = -1
                        self.heading[0] = 0
                        self.idle_counter = 20
                    self.is_abort_jump = False
                    self.set_state('hopping back process')
            else:
                self.set_state('release edge')
            # else:
            #     self.set_state('stand still')
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
        elif self.__state == 'slide':                           # SLIDE PREPARING
            self.speed = self.max_speed * 2.5
            self.set_new_desired_height(self.rectangle_height_slide, 0)
            self.set_new_desired_width(self.rectangle_width_slide, 6)
            self.is_grabbers_active = False
            self.check_space_around()
            if (self.look == 1 and self.is_enough_space_right) or\
                    (self.look == -1 and self.is_enough_space_left):
                self.ignore_user_input = True
                self.set_state('sliding')
            else:
                self.speed = 0
                # self.speed = self.max_speed // 2
                self.set_new_desired_height(self.rectangle_height_sit)
                self.set_new_desired_width(self.rectangle_width_sit, 4)
                # self.set_rect_width(self.rectangle_width_sit)
                # self.set_rect_height(self.rectangle_height_sit)
                self.set_state('crouch')
        elif self.__state == 'sliding':                         # SLIDING PROCESS
            self.heading[0] = 0
            if self.speed == 0:
                self.set_state('slide rise')
        elif self.__state == 'slide rise':                      # RISING AFTER SLIDE IS OVER
            self.ignore_user_input = False
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.check_space_around()
            if self.is_enough_height:
                self.set_new_desired_width(self.rectangle_width_sit,10)
                self.set_state('crouch')
            else:
                self.set_new_desired_height(self.rectangle_height_slide, 0)
                self.set_state('prone')
        elif self.__state == 'crawl prone left':
            self.speed = self.max_speed // 3
            self.look = -1
            self.heading[0] = -1
            # print('sdsdsdsdsdsds')
            # self.set_new_desired_height(self.rectangle_height_slide, 0)
            # self.check_space_around()
        elif self.__state == 'crawl prone right':
            self.speed = self.max_speed // 3
            self.look = 1
            self.heading[0] = 1
            # print('sdsdsdsdsdsds')
            # self.set_new_desired_height(self.rectangle_height_slide, 0)
            # self.check_space_around()
        elif self.__state == 'prone':
            self.speed = 0
            self.heading[0] = 0
            self.set_new_desired_height(self.rectangle_height_sit, 0)
            self.check_space_around()
            if self.is_enough_height:
                self.set_state('crouch down')
            else:
                self.set_new_desired_height(self.rectangle_height_slide, 0)
            # self.set_new_desired_height(self.rectangle_height_slide, 0)
        elif self.__state == 'stand still':                     # STANDING STILL
            self.heading[0] = 0
            # self.just_got_jumped = False
            # self.is_abort_jump = True
            # self.is_grabbers_active = True
            self.is_grabbers_active = False
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,10)
                self.check_space_around()
                if not self.is_enough_height:
                    self.set_state('crouch down')
                    self.state_machine()
                    return
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,10)
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
        elif self.__state == 'fly left':                        # IN MID-AIR FLY LEFT
            if self.is_stand_on_ground:
                self.set_state('stand still')
                return
            if self.look == 1 and self.speed > 0:
                # Actor moves to the opposite direction.
                # Need to slow him down.
                self.heading[0] = 0
                self.is_grabbers_active = False
            else:
                self.look = -1
                self.heading[0] = -1
                self.is_grabbers_active = True
                if self.rectangle.height != self.rectangle_height_default:
                    self.set_new_desired_height(self.rectangle_height_default,5)
                if self.rectangle.width != self.rectangle_width_default:
                    self.set_new_desired_width(self.rectangle_width_default,5)
            # if self.is_stand_on_ground:
            #     self.set_state('stand still')
            #     return
            # # if self.look == 1
            # self.look = -1
            # self.heading[0] = -1
            # self.is_grabbers_active = True
            # if self.rectangle.height != self.rectangle_height_default:
            #     self.set_new_desired_height(self.rectangle_height_default,5)
            # if self.rectangle.width != self.rectangle_width_default:
            #     self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'run left':                        # RUN LEFT
            self.look = -1
            self.heading[0] = -1
            # self.is_grabbers_active = True
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'fly right':                        # IN MID-AIR MOVE RIGHT
            if self.is_stand_on_ground:
                self.set_state('stand still')
                return
            if self.look == -1 and self.speed > 0:
                # Actor moves to the opposite direction.
                # Need to slow him down.
                self.heading[0] = 0
                self.is_grabbers_active = False
            else:
                self.look = 1
                self.heading[0] = 1
                self.is_grabbers_active = True
                if self.rectangle.height != self.rectangle_height_default:
                    self.set_new_desired_height(self.rectangle_height_default,5)
                if self.rectangle.width != self.rectangle_width_default:
                    self.set_new_desired_width(self.rectangle_width_default,5)
            # self.look = 1
            # self.heading[0] = 1
            # self.is_grabbers_active = True
            # if self.rectangle.height != self.rectangle_height_default:
            #     self.set_new_desired_height(self.rectangle_height_default,5)
            # if self.rectangle.width != self.rectangle_width_default:
            #     self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'run right':                        # RUN RIGHT
            self.look = 1
            self.heading[0] = 1
            # self.is_grabbers_active = True
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.__state == 'has just grabbed edge':            # GRAB THE EDGE
            self.potential_moving_distance = 0
            self.is_grabbers_active = False
            self.is_edge_grabbed = True
            self.fall_speed = 0
            self.heading[0] = 0
            self.speed = 0
            self.rectangle.width = self.rectangle_width_default
            self.rectangle.height = self.rectangle_height_default
            # self.set_new_desired_height(self.rectangle_height_default)
            # self.set_new_desired_width(self.rectangle_width_default)
            # self.processing_rectangle_size()
            self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            if self.look == -1:
                self.rectangle.left = self.obstacles_around[self.influenced_by_obstacle].rectangle.right + 1
                self.is_enough_space_left = False
            else:
                self.rectangle.right = self.obstacles_around[self.influenced_by_obstacle].rectangle.left - 1
                self.is_enough_space_right = False
            self.jump_attempts_counter = 0
            # self.jump_attempts_counter = self.max_jump_attempts
            self.set_state('hanging on edge')
        elif self.__state == 'hanging on edge':                 # HANGING ON THE EDGE
            self.just_got_jumped = False
            self.is_abort_jump = True
            # self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        # elif self.__state == 'hanging on ghost':                # HANGING ON THE GHOST PLATFORM
        #     self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        #     if self.idle_counter > 0:
        #         self.idle_counter -= 1
        #     else:
        #         self.ignore_user_input = False
        elif self.__state == 'hop down from ghost':             # PREPARE TO HOP DOWN FROM THE GHOST PLATFORM
            self.potential_moving_distance = 0
            # self.is_edge_grabbed = True
            # self.ignore_user_input = True
            # self.idle_counter = 25
            self.fall_speed = 0
            self.heading[0] = 0
            self.speed = 0
            # self.set_new_desired_height(self.rectangle_height_default, 5)
            # self.set_new_desired_width(self.rectangle_width_default, 5)

            self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.bottom + 1
            # self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
            self.reset_self_flags()
            self.jump_attempts_counter = 0
            self.influenced_by_obstacle = -1
            self.set_state('jump cancel')
            # self.set_state('hanging on ghost')
        elif self.__state == 'release edge':                    # RELEASE
            self.is_edge_grabbed = False
            self.is_grabbers_active = False
            self.rectangle.y += self.look * -10
            # self.rectangle.y += self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[1] * -4
            self.influenced_by_obstacle = -1
            self.speed = 0
            self.ignore_user_input = False
            # if self.is_stand_on_ground:
            self.set_state('stand still')
        elif self.__state == 'climb on':                        # START CLIMBING ON AN OBSTACLE
            self.ignore_user_input = True
            self.is_jump_performed = False
            self.set_new_desired_height(self.rectangle_height_sit // 2, 6)
            self.set_state('climb on raise')
        elif self.__state == 'climb on raise':                        # START CLIMBING ON AN OBSTACLE
            if self.rectangle.height <= self.rectangle_height_sit // 2:
                self.check_space_around()
                if self.is_enough_height:
                    self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
                    self.rectangle.centerx += 1 * self.look  # Slightly pushing an actor far from the edge of an obstacle to let his bottom collider do the job.
                    self.ignore_user_input = False
                    self.is_edge_grabbed = False
                    self.set_state('stand still')
                    # self.set_state('crouch down')
                else:
                    self.set_state('hanging on edge')
            else:
                self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top

    def reset_self_flags(self):
        self.is_move_left = False
        self.is_move_right = False
        self.is_move_up = False
        self.is_move_down = False
        self.is_jump = False
        # self.is_edge_grabbed = False

