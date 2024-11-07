import sys

from entity import *

class Actor(Entity):
    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.type = 'actor'
        self.inventory = dict()
        self.drop_from_inventory = list()
        self.current_weapon = dict()
        self.current_weapon_demolishers_reveal_frames = list()
        self.is_collideable = True
        self.is_destructible = True

        self.ai_input_right_arrow = False
        self.ai_input_left_arrow = False
        self.ai_input_attack = False
        self.ai_input_jump = False
        self.next_ranged_weapon_usage_counter = 0
        # self.previously_used_weapon = ''
        # self.force_use_previous_weapon = False
        # self.force_mana_reduce = False
        # self.force_mana_reduce_amount: int = 0
        # self.force_stamina_reduce = False
        # self.force_stamina_reduce_amount: int = 0

        # self.acceleration = .5
        # self.air_acceleration = .4
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
        # self.rectangle_height_sit = self.rectangle.height * 0.66
        # self.rectangle_width_sit = self.rectangle.width * 1.34
        self.rectangle_height_slide = self.rectangle.width
        self.rectangle_width_slide = self.rectangle.height


    def get_target(self, target):
        self.target = target

    def add_items_to_inventory(self, items):
        if not items:
            return
        for item in items:
            print(f'[add_items_to_inventory], {self.name} prepare to get an item: {item["description"]}')
            if item['class'] not in self.inventory.keys():
                self.inventory[item['class']] = dict()
            if item['label'] in self.inventory[item['class']].keys():
                self.inventory[item['class']][item['label']]['quantity'] += 1
            else:
                self.inventory[item['class']][item['label']] = {'item': item.copy(), 'quantity': 1}

            # if 'weight' in item.keys():
            #     self.body_weight += item['weight']
            #     print(f'[add item to inv] {self.name}\'s weight becomes: {self.body_weight}')
            #     self.calculate_athletics_index()
            #     self.calculate_max_jump_height_and_speed()
            #     self.calculate_speed()

    def calculate_weight(self):
        # print(f'[calc weight] {self.body["right hand"]["weapon"]}')
        self.body_weight = self.body_weight_netto + self.body['right hand']['weapon']['item']['weight'] if self.body['right hand']['weapon'] else 0 \
                                                  + self.body['left hand']['weapon']['item']['weight'] if self.body['left hand']['weapon'] else 0
        self.calculate_athletics_index()
        self.calculate_max_jump_height_and_speed()
        self.calculate_speed()

    def remove_item_from_inventory(self, item):
        if item['class'] in self.inventory.keys():
            if item['label'] in self.inventory[item['class']].keys():
                self.inventory[item['class']][item['label']]['quantity'] -= 1
                if self.inventory[item['class']][item['label']]['quantity'] == 0:
                    del self.inventory[item['class']][item['label']]
                    if len(self.inventory[item['class']]) == 0:
                        del self.inventory[item['class']]
                    # if 'weight' in  item.keys():
                    #     self.body_weight -=  item['weight']
                    #     print(f'[remove item from inv] {self.name}\'s weight becomes: {self.body_weight}')
                    #     self.calculate_athletics_index()
                    #     self.calculate_max_jump_height_and_speed()
                    #     self.calculate_speed()
    def drop_item_from_inventory(self, item):
        if item['class'] in self.inventory.keys():
            if item['label'] in self.inventory[item['class']].keys():
                if item['droppable']:
                    print(f'[drop_item_from_inventory] {item["label"]}')
                    self.drop_from_inventory.append(item['label'])
                    self.inventory[item['class']][item['label']]['quantity'] -= 1
                    if self.inventory[item['class']][item['label']]['quantity'] == 0:
                        del self.inventory[item['class']][item['label']]
                        if len(self.inventory[item['class']]) == 0:
                            del self.inventory[item['class']]
                    if 'weight' in item.keys():
                        self.body_weight -= item['weight']
                        print(f'[drop item to inv] {self.name}\'s weight reduces by {item["weight"]}: {self.body_weight}')
                        self.calculate_athletics_index()
                        self.calculate_max_jump_height_and_speed()
                        self.calculate_speed()

    def has_item_in_inventory(self, item):
        if item['class'] in self.inventory.keys():
            if item['label'] in self.inventory[item['class']].keys():
                return True
            else:
                return False
        else:
            return False

    def activate_weapon(self, uuid):
        if not self.inventory:
            return
        # print(self.inventory['weapons']['jake kick'])
        if type(uuid) is int:
            all_weapons = list(self.inventory['weapons'].keys())
            if self.current_weapon:
                # print(f'{self.inventory["weapons"][all_weapons[uuid]]["item"]["label"]=}')
                # print(f'{self.current_weapon["label"]=}')
                if self.current_weapon['label'] == self.inventory["weapons"][all_weapons[uuid]]["item"]["label"]:
                    return
                self.previously_used_weapon = self.current_weapon['label']
            self.body['right hand']['weapon'] = self.inventory['weapons'][all_weapons[uuid]]
            # self.body['left hand']['weapon'] = self.inventory['weapons']['jake kick']
            # self.body['right hand']['weapon'] = self.inventory['weapons'][all_weapons[0]]
        else:
            if self.current_weapon:
                if self.current_weapon['label'] == self.inventory["weapons"][uuid]["item"]["label"]:
                    return
                self.previously_used_weapon = self.current_weapon['label']
            self.body['right hand']['weapon'] = self.inventory['weapons'][uuid]
            # self.body['left hand']['weapon'] = self.inventory['weapons'][uuid + 1]


        self.current_weapon = self.body['right hand']['weapon']['item']
        # print('------------------------------')
        # print(self.current_weapon['demolishers'])
        self.current_stamina_lost_per_attack = self.normal_stamina_lost_per_attack * self.current_weapon['stamina consumption']
        self.current_mana_lost_per_attack = self.normal_mana_lost_per_attack * self.current_weapon['mana consumption']
        # print('[activate_weapon]', self.name, self.current_weapon)
        # print(self.current_weapon)
        # {'aimed fire': True, 'attack animation': 'stab', 'steal user input': True, 'leave particles': False, 'class': 'weapons', 'type': 'melee', 'sub-type': 'bladed', 'sound': 'sound_swing_2', 'droppable': True, 'need ammo': False, 'ammo': 0, 'label': 'KITCHEN KNIFE', 'sprite': 'kitchen knife', 'pierce': False, 'damager TTL': 200, 'damagers spread': False, 'damager static': True, 'damager radius': 1, 'damagers quantity': 1, 'damager reveal delay': 0, 'damager reveals with flash': False, 'damager brings light': False, 'damager fly speed reduce': 0, 'damager fly speed': 1.5, 'damager invisible': False, 'damager weight': 5, 'description': 'Casual kitchen knife.', 'reach': 1, 'weight': 5, 'hardness': 10, 'special': ('bleeding',)}
        # exit()

    # def activate_weapon_old(self, uuid):
    #     if not self.inventory:
    #         return
    #
    #     if type(uuid) is int:
    #         all_weapons = list(self.inventory['weapons'].keys())
    #         if self.current_weapon:
    #             # print(f'{self.inventory["weapons"][all_weapons[uuid]]["item"]["label"]=}')
    #             # print(f'{self.current_weapon["label"]=}')
    #             if self.current_weapon['label'] == self.inventory["weapons"][all_weapons[uuid]]["item"]["label"]:
    #                 return
    #             self.previously_used_weapon = self.current_weapon['label']
    #         self.body['right hand']['weapon'] = self.inventory['weapons'][all_weapons[uuid]]
    #         # self.body['right hand']['weapon'] = self.inventory['weapons'][all_weapons[0]]
    #     else:
    #         if self.current_weapon:
    #             if self.current_weapon['label'] == self.inventory["weapons"][uuid]["item"]["label"]:
    #                 return
    #             self.previously_used_weapon = self.current_weapon['label']
    #         self.body['right hand']['weapon'] = self.inventory['weapons'][uuid]
    #
    #
    #     self.current_weapon = self.body['right hand']['weapon']['item']
    #     # print('------------------------------')
    #     # print(self.current_weapon['demolishers'])
    #     self.current_stamina_lost_per_attack = self.normal_stamina_lost_per_attack * self.current_weapon['stamina consumption']
    #     self.current_mana_lost_per_attack = self.normal_mana_lost_per_attack * self.current_weapon['mana consumption']
    #     # print('[activate_weapon]', self.name, self.current_weapon)
    #     # print(self.current_weapon)
    #     # {'aimed fire': True, 'attack animation': 'stab', 'steal user input': True, 'leave particles': False, 'class': 'weapons', 'type': 'melee', 'sub-type': 'bladed', 'sound': 'sound_swing_2', 'droppable': True, 'need ammo': False, 'ammo': 0, 'label': 'KITCHEN KNIFE', 'sprite': 'kitchen knife', 'pierce': False, 'damager TTL': 200, 'damagers spread': False, 'damager static': True, 'damager radius': 1, 'damagers quantity': 1, 'damager reveal delay': 0, 'damager reveals with flash': False, 'damager brings light': False, 'damager fly speed reduce': 0, 'damager fly speed': 1.5, 'damager invisible': False, 'damager weight': 5, 'description': 'Casual kitchen knife.', 'reach': 1, 'weight': 5, 'hardness': 10, 'special': ('bleeding',)}
    #     # exit()

    def get_state(self):
        return self.__state

    # def got_enough_mana(self):
    #     if self.current_weapon['mana consumption'] <= self.stats['mana']:
    #         return True
    #     else:
    #         return False

    def set_state(self, new_state):
        # print(f'[actor.set_state] {self.name} (#{self.id}) got new state: {new_state} at {self.cycles_passed} ({self.movement_direction_inverter=})')
        self.__state = new_state
        # self.set_current_animation()

    def process(self):
        # if self.force_mana_reduce:
        #     self.mana_reduce(self.force_mana_reduce_amount)
        #     self.force_mana_reduce = False
        #     self.force_mana_reduce_amount = 0
        #
        # if self.force_stamina_reduce:
        #     self.stamina_reduce(self.force_stamina_reduce_amount)
        #     self.force_stamina_reduce = False
        #     self.force_stamina_reduce_amount = 0

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        if self.stun_counter > 0:
            self.stun_counter -= 1
            self.is_stunned = True
        else:
            self.is_stunned = False

        if self.combo_counter > 0:
            self.combo_counter -= 1
        else:
            self.combo_set_number = 0

        self.state_machine()
        self.apply_rectangle_according_to_sprite()
        self.processing_rectangle_size()
        self.stamina_replenish()
        self.mana_replenish()
        self.check_space_around()

        super().process()

    def set_action(self, new_action):
        # print(f'[actor set action] Setting new action: {new_action}')
        # if self.ignore_user_input:
        #     return

        # RIGHT actions
        if new_action == 'right action':
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'free', 'crouch', 'stand still', 'prone',
                                    'run left', 'fly left', 'run right', 'hold stash',):
                return
            if not self.is_stand_on_ground:
                if self.__state == 'jump':
                    self.is_jump_performed = True
                else:
                    self.is_jump_performed = False

                self.set_state('fly right')
            else:
                if self.__state == 'hold stash':
                    self.set_state('carry stash right')
                elif self.__state == 'crouch':
                    if self.look == -1:
                        self.set_state('crouch turn right')
                #     else:
                #         self.set_state('crawl right')
                elif self.__state in ('free', 'stand still'):
                # elif self.__state == 'stand still':
                    if self.look == 1:
                        self.set_state('prepare run right')
                    else:
                        self.set_state('turn right')
                # elif self.__state == 'prone':
                #     self.set_state('crawl prone right')
                elif self.__state in ('run left', 'fly left'):
                    self.set_action('left action cancel')

        elif new_action == 'right action cancel':
            if self.__state == 'carry stash right':
                self.set_state('hold stash')
            # elif self.__state == 'crawl right':
            #     self.set_state('crouch')
            elif self.__state in ('run right', 'fly right'):
                self.set_state('stand still')
            # elif self.__state == 'crawl prone right':
            #     self.set_state('prone')

        # LEFT actions
        elif new_action == 'left action':
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'free', 'crouch', 'stand still', 'prone',
                                    'run right', 'fly right', 'run left', 'hold stash',):
                return
            if not self.is_stand_on_ground:
                if self.__state == 'jump':
                    self.is_jump_performed = True
                else:
                    self.is_jump_performed = False
                self.set_state('fly left')
            else:
                if self.__state == 'hold stash':
                    self.set_state('carry stash left')

                elif self.__state == 'crouch':
                    if self.look == 1:
                        self.set_state('crouch turn left')
                #     else:
                #         self.set_state('crawl left')
                elif self.__state in ('free', 'stand still'):
                    if self.look == -1:
                        self.set_state('prepare run left')
                    else:
                        self.set_state('turn left')
                # elif self.__state == 'prone':
                #     self.set_state('crawl prone left')
                elif self.__state in ('run right', 'fly right'):
                    self.set_action('right action cancel')

        elif new_action == 'left action cancel':
            if self.__state == 'carry stash left':
                self.set_state('hold stash')
            # elif self.__state == 'crawl left':
            #     self.set_state('crouch')
            elif self.__state in ('run left', 'fly left'):
                self.set_state('stand still')
            # elif self.__state == 'crawl prone left':
            #     self.set_state('prone')

        # DOWN actions
        elif new_action == 'down action':
            # Apply filter of unwanted actions:
            if self.__state not in ('free', 'stand still', 'run right', 'run left',
                                    'hanging on edge', 'hanging on ghost',
                                    'carry stash left', 'carry stash right', 'hold stash'):
                return

            if self.__state in ('carry stash left', 'carry stash right', 'hold stash'):
                self.set_state('drop stash')
                return
            elif self.__state in ('hanging on edge', 'hanging on ghost'):
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
                self.set_state('climb on')

        # JUMP
        elif new_action == 'jump action':
            if self.is_jump_performed:
                return
            # Apply filter of unwanted actions:
            if self.__state not in ('jump', 'crouch', 'crawl right', 'crawl left',
                                    'run right', 'run left', 'stand still', 'fly left', 'fly right'):
                return

            if self.__state in ('crouch down', 'crouch rise', 'crouch', 'crawl right', 'crawl left') and self.is_stand_on_ground:
                if self.influenced_by_obstacle >= 0:
                    # Jump off a ghost platform:
                    if self.obstacles_around[self.influenced_by_obstacle].is_ghost_platform:
                        self.set_state('hop down from ghost')
                        return
                self.set_state('slide')
            else:
                if self.jump_attempts_counter == 0:
                    return
                if self.is_enough_space_above and self.__state != 'jump':
                    self.set_state('jump')
        elif new_action == 'jump action cancel':
            if self.just_got_jumped:
                self.set_state('jump cancel')

        # HOP BACK
        elif new_action == 'hop back':
            # Apply filter of unwanted actions:
            if not self.is_stand_on_ground:
                return
            self.movement_direction_inverter = -1
            self.set_state('hopping prepare')
        # HOP FORWARD
        elif new_action == 'hop forward':
            # Apply filter of unwanted actions:
            if not self.is_stand_on_ground:
                return
            self.set_state('hopping prepare')
        elif new_action == 'hop action cancel':
            if self.just_got_jumped:
                self.just_got_jumped = False
            self.is_abort_jump = True
            self.ignore_user_input = False

        elif new_action == 'protect':
            if self.__state in ('free', 'stand still', 'run right', 'run left', 'fly right',
                                'fly left','turn right', 'turn left'):

                self.set_state('protect')

        elif new_action == 'attack':
            if self.stats['stamina'] <= self.current_stamina_lost_per_attack:
                # print(f'[state machine] NOT ENOUGH STAMINA.')
                self.frames_changing_threshold_penalty = 2.  # x2 times slower animation
            else:
                self.frames_changing_threshold_penalty = 1.

            if self.stats['mana'] <= self.current_mana_lost_per_attack:
                # print(f'[state machine] NOT ENOUGH MANA')
                return
            if self.__state not in ('free', 'stand still', 'run right', 'run left',
                                    'jump', 'protect',
                                    'crouch', 'fly right', 'fly left', 'turn right', 'turn left'):
                return
            # print(f'[set action] attack')
            if self.__state in ('crawl left', 'crouch', 'crawl right'):
                if self.current_weapon['has crouch attack']:
                    if self.look == 1:
                        self.set_state('prepare crouch attack right')
                    else:
                        self.set_state('prepare crouch attack left')
            else:
                self.set_state('prepare attack')
                # print(f'[set action] {self.name} prepares to attack.')

    def state_machine(self):
        state = self.get_state()
        if state == 'stand still':                     # STANDING STILL
            self.set_current_animation()
            self.heading[0] = 0
            self.normal_stamina_replenish = self.default_normal_stamina_replenish
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
        elif state == 'drop stash':                          #
            self.drop_item_from_inventory(self.inventory['burden']['stash']['item'])
            self.set_state('stand still')
        elif state == 'prepare carry stash':                          #
            self.set_state('hold stash')
        elif state == 'hold stash':  #
            self.set_current_animation()
            self.speed = 0
            self.heading[0] = 0
        elif state == 'carry stash right':  #
            self.set_current_animation()
            # self.speed = 5
            self.speed = self.max_speed // 2
            self.look = 1
        elif state == 'carry stash left':  #
            self.set_current_animation()
            # self.speed = 5
            self.speed = self.max_speed // 2
            self.look = -1
        # elif state == 'stunned':
        #     if self.is_stunned:
        #         if 'stunned' not in self.current_animation:
        #             self.set_current_animation()
        #
        #     else:
        #         # 'Stunned' state has been switched off
        #         self.set_state('stand still')
        elif state == 'protect':
            self.set_current_animation()
            self.normal_stamina_replenish = 0.01
            self.heading[0] = 0
        # elif state == 'protect':
        #     if self.stats['mana'] > 3:
        #         self.set_current_animation()
        #         self.normal_stamina_replenish = 0.01
        #         self.heading[0] = 0
        #     else:
        #         self.summon_protector = False
        #         self.summoned_protectors_description = list()
        #         self.set_state('stand still')
        elif state == 'prepare attack':                          # PREPARING ATTACK
            # print(f'[state machine] {self.name} prepares attack.')
            self.stamina_reduce(self.current_stamina_lost_per_attack)
            self.mana_reduce(self.current_mana_lost_per_attack)
            self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
                                                      self.frames_changing_threshold_penalty
            self.combo_counter = self.current_weapon['combo next step threshold']
            self.combo_set_number += 1
            if self.combo_set_number > self.current_weapon['combo steps quantity']:
                self.combo_set_number = 1
            self.ignore_user_input = self.current_weapon['ignore user input']
            # if self.is_stand_on_ground:
            #     self.heading[0] = 0
            self.set_state(self.current_weapon['attack animation'])
            self.set_current_animation()
        elif state == 'prepare crouch attack left':                          # PREPARING ATTACK
            self.set_state(self.current_weapon['attack animation'] + ' crouch left')
            self.set_current_animation()
            self.stamina_reduce(self.current_stamina_lost_per_attack)
            self.mana_reduce(self.current_mana_lost_per_attack)
            self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
                                                      self.frames_changing_threshold_penalty
            self.ignore_user_input = self.current_weapon['ignore user input']
            if self.is_stand_on_ground:
                self.heading[0] = 0
        elif state == 'prepare crouch attack right':                          # PREPARING ATTACK
            self.set_state(self.current_weapon['attack animation'] + ' crouch right')
            self.set_current_animation()
            self.stamina_reduce(self.current_stamina_lost_per_attack)
            self.mana_reduce(self.current_mana_lost_per_attack)
            self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
                                                      self.frames_changing_threshold_penalty
            self.ignore_user_input = self.current_weapon['ignore user input']
            if self.is_stand_on_ground:
                self.heading[0] = 0
        elif state in ('stab', 'cast', 'axe swing', 'whip',
                       'whip crouch right', 'whip crouch left',
                       'kick', 'pistol shot', 'punch'):                          # ATTACKING IN PROCESS...
            # print(f'[state machine] {self.name} attacking.')
            if self.is_stand_on_ground:
                self.heading[0] = 0
            if self.animation_sequence_done:
                # print(f'[state machine] attack is done.')
                self.ignore_user_input = False
                # if self.force_use_previous_weapon:
                #     self.force_use_previous_weapon = False
                #     self.activate_weapon(self.previously_used_weapon)
                if 'crouch' in state:
                # if self.__state in ('whip crouch right', 'whip crouch left'):
                    self.set_state('crouch')
                else:
                    self.set_state('stand still')
        elif state == 'crouch down':                       # CROUCH DOWN PROCESS
            self.is_crouch = True
            self.is_grabbers_active = False
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.set_new_desired_width(self.rectangle_width_sit, 3)
            self.set_state('crouch')
        elif state == 'crouch':                          # CROUCH
            self.set_current_animation()
            self.speed = 0
            self.heading[0] = 0
        elif state == 'crouch turn left':                # CROUCH TURN RIGHT
            self.look = -1
            self.set_state('crouch')
        elif state == 'crouch turn right':               # CROUCH TURN LEFT
            self.look = 1
            self.set_state('crouch')
        elif state == 'crouch rise':  # CROUCH UP PROCESS
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
        # elif self.get_state() == 'crawl right':
        #     # self.look = 1
        #     self.speed = self.max_speed // 3
        #     # self.heading[0] = 1
        # elif self.get_state() == 'crawl left':
        #     # self.look = 1
        #     self.speed = self.max_speed // 3
        #     # self.heading[0] = -1
        elif state == 'free':
            # self.heading[0] = 0
            ...
        elif state == 'jump':
            # print('try to jump...')
            if not self.just_got_jumped:
                self.just_got_jumped = True
                self.jump_attempts_counter -= 1
                if self.jump_attempts_counter == 0:
                    # Stamina reduces while jumping only if there are no jump attempts left.
                    # If actor jumps a single hops, stamina remains unchanged.
                    self.stamina_reduce(self.normal_stamina_lost_per_second_jump)
                if self.fall_speed > -2:
                    self.is_grabbers_active = True
                self.is_jump = True
                self.influenced_by_obstacle = -1
                self.jump_height = self.max_jump_height
                self.set_current_animation()
            else:
                if self.is_stand_on_ground:
                    self.is_jump_performed = True
                    self.heading[0] = 0
                    self.set_state('stand still')
                    # self.set_state('jump cancel')
            self.is_abort_jump = False
        elif state == 'jump cancel':                     # CANCEL JUMP
            self.just_got_jumped = False
            self.is_abort_jump = True
            self.is_jump_performed = False
            if self.is_stand_on_ground:
                self.set_state('stand still')
            else:
                if self.look == 1:
                    self.set_state('fly right')
                else:
                    self.set_state('fly left')
        elif state == 'hopping prepare':                        # HOP BACK
            self.heading[0] = 0
            if self.is_enough_space_above:
                self.ignore_user_input = True
                self.ai_input_right_arrow = False
                self.ai_input_left_arrow = False
                self.ai_input_attack = False
                self.ai_input_jump = False
                self.is_grabbers_active = False
                self.is_move_right: bool = False
                self.is_move_left: bool = False
                self.is_move_up: bool = False
                self.is_move_down: bool = False
                self.is_jump: bool = False
                self.is_crouch: bool = False
                self.is_abort_jump: bool = False
                self.is_jump_performed: bool = False
                if not self.just_got_jumped:
                    self.stamina_reduce(self.normal_stamina_lost_per_hop_back)
                    self.just_got_jumped = True
                    self.jump_attempts_counter -= 1
                    self.is_jump = True
                    self.influenced_by_obstacle = -1
                    self.jump_height = min(5 * self.hop_back_jump_height_modifier, 15)
                    # self.jump_height = self.max_jump_height * 0.6
                    self.speed = min(5 * self.hop_back_jump_height_modifier, 30)
                    # print(f'[state machine] hop back prepare: {self.hop_back_jump_height_modifier=} {self.jump_height=} {self.speed=}')
                    #self.movement_direction_inverter = -1
                    # self.heading[0] = 0
                    self.idle_counter = 25
                    # self.invincibility_timer = 20
                    self.hop_back_jump_height_modifier = self.default_hop_back_jump_height_modifier
                self.is_abort_jump = False

                if self.dead:
                    # self.heading[0] = 0
                    if self.has_got_a_critical_hit:
                        self.set_state('lie decapitated')
                    else:
                        self.set_state('lie dead')
                else:
                    if self.get_state() == 'hanging on edge':
                        self.set_state('release edge')
                    else:
                        self.set_state('hopping process')
                # print(f'[state_machine] "hopping prepare" routine ends: {self.movement_direction_inverter=}')
            # else:
            #     self.set_state('release edge')
            # else:
            #     self.set_state('stand still')
        elif state == 'hopping process':            # HOPPING BACK PROCESS
            if self.idle_counter > 0:
                self.idle_counter -= 1
            else:
                if self.speed <= 0:
                    self.ignore_user_input = False
                    if self.just_got_jumped:
                        self.just_got_jumped = False
                    self.is_abort_jump = True
                    self.animation_change_denied = False
                    if not self.dead:
                        if self.scheduled_state:
                            self.set_state(self.scheduled_state)
                            self.scheduled_state = ''
                        else:
                            # self.animation_change_denied = False
                            self.set_state('stand still')
                    else:
                        if self.has_got_a_critical_hit:
                            # self.animation_change_denied = False
                            self.set_state('lie decapitated')
                            self.set_current_animation()
                            self.animation_change_denied = True
                        else:
                            # self.animation_change_denied = False
                            self.set_state('lie dead')
                            self.set_current_animation()
                            self.animation_change_denied = True
                    # print(f'[state_machine] "hopping process" routine ends: {self.movement_direction_inverter=}')
        # elif self.get_state() == 'hop forward':                        # HOP BACK
        #     self.heading[0] = 0
        #     self.speed = 0
        #     # if self.is_stand_on_ground:
        #     if self.is_enough_space_above:
        #         self.ignore_user_input = True
        #         self.ai_input_right_arrow = False
        #         self.ai_input_left_arrow = False
        #         self.ai_input_attack = False
        #         self.ai_input_jump = False
        #         self.is_grabbers_active = False
        #         self.is_move_right: bool = False
        #         self.is_move_left: bool = False
        #         self.is_move_up: bool = False
        #         self.is_move_down: bool = False
        #         self.is_jump: bool = False
        #         self.is_crouch: bool = False
        #         self.is_abort_jump: bool = False
        #         self.is_jump_performed: bool = False
        #         if not self.just_got_jumped:
        #             self.stamina_reduce(self.normal_stamina_lost_per_hop_back)
        #             self.just_got_jumped = True
        #             self.jump_attempts_counter -= 1
        #             self.is_jump = True
        #             self.influenced_by_obstacle = -1
        #             self.jump_height = min(5 * self.hop_back_jump_height_modifier, 15)
        #             # self.jump_height = self.max_jump_height * 0.6
        #             self.speed = min(5 * self.hop_back_jump_height_modifier, 30)
        #             # print(f'[state machine] hop back prepare: {self.hop_back_jump_height_modifier=} {self.jump_height=} {self.speed=}')
        #             # self.movement_direction_inverter = -1
        #             # self.heading[0] = 0
        #             self.idle_counter = 20
        #             # self.invincibility_timer = 20
        #             self.hop_back_jump_height_modifier = self.default_hop_back_jump_height_modifier
        #         self.is_abort_jump = False
        #
        #         if self.dead:
        #             # self.heading[0] = 0
        #             self.set_state('lie dead')
        #         else:
        #             if self.get_state() == 'hanging on edge':
        #                 self.set_state('release edge')
        #             else:
        #                 self.set_state('hopping forward process')
        #             # else:
        #             #     self.set_state('crouch down')
        #         # return
        #
        #
        #     # else:
        #     #     self.set_state('release edge')
        #     # else:
        #     #     self.set_state('stand still')
        # elif self.get_state() == 'hopping forward process':            # HOPPING BACK PROCESS
        #     if self.idle_counter > 0:
        #         self.idle_counter -= 1
        #         # self.invincibility_timer -= 1
        #     else:
        #         if self.speed <= 0:
        #             self.ignore_user_input = False
        #             if self.just_got_jumped:
        #                 self.just_got_jumped = False
        #             self.is_abort_jump = True
        #             # self.movement_direction_inverter = 1
        #             # self.set_state('crouch')
        #             if not self.dead:
        #                 self.set_state('stand still')
        #             else:
        #                 self.set_state('lie dead')
        elif state == 'slide':                           # SLIDE PREPARE
            if self.stats['stamina'] < self.normal_stamina_lost_per_slide or\
               self.look == 1 and not self.is_enough_space_right or\
               self.look == -1 and not self.is_enough_space_left:
                # self.set_state('crouch')
                self.speed = self.max_speed * 2
                self.idle_counter = 10
            else:
                self.speed = self.max_speed * 3

            # if self.stats['stamina'] < self.normal_stamina_lost_per_slide or\
            #    self.look == 1 and not self.is_enough_space_right or\
            #    self.look == -1 and not self.is_enough_space_left:
            #     self.set_state('crouch')
            #     return
            self.set_state('sliding')
            self.set_current_animation()
            # self.speed = self.max_speed * 4
            self.set_new_desired_height(self.rectangle_height_slide, 0)
            self.set_new_desired_width(self.rectangle_width_slide, 6)
            self.is_grabbers_active = False
            self.check_space_around()
            self.ignore_user_input = True
            self.rectangle.top  -= 50
            self.stamina_reduce(self.normal_stamina_lost_per_slide)

            # if self.stats['stamina'] < self.normal_stamina_lost_per_slide:
            #     self.set_state('crouch')
            #     return
            # self.speed = self.max_speed * 4
            # self.set_new_desired_height(self.rectangle_height_slide, 0)
            # # self.set_new_desired_width(self.sprite_rectangle.w, 6)
            # self.set_new_desired_width(self.rectangle_width_slide, 6)
            # self.is_grabbers_active = False
            # self.check_space_around()
            # if (self.look == 1 and self.is_enough_space_right) or\
            #         (self.look == -1 and self.is_enough_space_left):
            #     self.ignore_user_input = True
            #     self.rectangle.top  -= 50
            #     self.set_state('sliding')
            #     self.stamina_reduce(self.normal_stamina_lost_per_slide)
            # else:
            #     self.speed = 0
            #     # self.speed = self.max_speed // 2
            #     self.set_new_desired_height(self.rectangle_height_sit)
            #     self.set_new_desired_width(self.rectangle_width_sit, 4)
            #     # self.set_rect_width(self.rectangle_width_sit)
            #     # self.set_rect_height(self.rectangle_height_sit)
            #     self.set_state('crouch')
        elif state == 'sliding':                         # SLIDING PROCESS
            self.heading[0] = 0
            if self.speed == 0:
                if self.idle_counter > 0:
                    self.idle_counter -= 1
                else:
                    self.set_state('slide rise')
        elif state == 'slide rise':                      # RISING AFTER SLIDE IS OVER
            self.ignore_user_input = False
            self.set_new_desired_height(self.rectangle_height_sit, 5)
            self.check_space_around()
            if self.is_enough_height:
                self.set_new_desired_width(self.rectangle_width_sit,10)
                self.set_state('crouch')
            else:
                self.set_new_desired_height(self.rectangle_height_slide, 0)
                self.set_state('prone')
        # elif self.get_state() == 'crawl prone left':
        #     self.speed = self.max_speed // 3
        #     self.look = -1
        #     self.heading[0] = -1
        #     # print('sdsdsdsdsdsds')
        #     # self.set_new_desired_height(self.rectangle_height_slide, 0)
        #     # self.check_space_around()
        # elif self.get_state() == 'crawl prone right':
        #     self.speed = self.max_speed // 3
        #     self.look = 1
        #     self.heading[0] = 1
        #     # print('sdsdsdsdsdsds')
        #     # self.set_new_desired_height(self.rectangle_height_slide, 0)
        #     # self.check_space_around()
        elif state == 'prone':
            self.speed = 0
            self.heading[0] = 0
            self.set_new_desired_height(self.rectangle_height_sit, 0)
            self.check_space_around()
            if self.is_enough_height:
                self.set_state('crouch down')
            else:
                self.set_new_desired_height(self.rectangle_height_slide, 0)
            # self.set_new_desired_height(self.rectangle_height_slide, 0)
        elif state == 'turn left':                       # TURN LEFT
            self.set_current_animation()
            if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
                # self.look = -1
            else:
                self.look = -1
                self.heading[0] = -1
                self.set_state('stand still')
        elif state == 'turn right':                      # TURN RIGHT
            self.set_current_animation()
            if self.look == -1 and self.speed > 0:  # Actor looks to the other side and runs.
                # Switch off heading to force actor start reducing his speed and slow it down to zero.
                # After that self is going to be able to start acceleration to proper direction.
                self.heading[0] = 0
                # self.look = 1
            else:
                self.look = 1
                self.heading[0] = 1
                self.set_state('stand still')

        elif state == 'fly left':                        # IN MID-AIR FLY LEFT
            if self.is_stand_on_ground:
                self.set_state('stand still')
                return
            self.set_current_animation()
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
        elif state == 'prepare run left':                        # RUN LEFT
            self.set_state('run left')
            self.set_current_animation()
        elif state == 'run left':                        # RUN LEFT
            self.look = -1
            self.heading[0] = -1
            # self.is_grabbers_active = True
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif state == 'fly right':                        # IN MID-AIR MOVE RIGHT
            if self.is_stand_on_ground:
                self.set_state('stand still')
                return
            self.set_current_animation()
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
        elif state == 'prepare run right':                        # RUN RIGHT
            self.set_state('run right')
            self.set_current_animation()
        elif state == 'run right':                        # RUN RIGHT
            self.look = 1
            self.heading[0] = 1
            # self.is_grabbers_active = True
            if self.rectangle.height != self.rectangle_height_default:
                self.set_new_desired_height(self.rectangle_height_default,5)
            if self.rectangle.width != self.rectangle_width_default:
                self.set_new_desired_width(self.rectangle_width_default,5)
        elif self.get_state() == 'has just grabbed edge':            # GRAB THE EDGE
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
        elif self.get_state() == 'hanging on edge':                 # HANGING ON THE EDGE
            self.just_got_jumped = False
            self.is_abort_jump = True
            # self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        # elif self.get_state() == 'hanging on ghost':                # HANGING ON THE GHOST PLATFORM
        #     self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
        #     if self.idle_counter > 0:
        #         self.idle_counter -= 1
        #     else:
        #         self.ignore_user_input = False
        elif self.get_state() == 'hop down from ghost':             # PREPARE TO HOP DOWN FROM THE GHOST PLATFORM
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
        elif self.get_state() == 'release edge':                    # RELEASE
            self.is_edge_grabbed = False
            self.is_grabbers_active = False
            self.rectangle.y += self.look * -10
            # self.rectangle.y += self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[1] * -4
            self.influenced_by_obstacle = -1
            self.speed = 0
            self.ignore_user_input = False
            # if self.is_stand_on_ground:
            self.set_state('stand still')
        elif self.get_state() == 'climb on':                        # START CLIMBING ON AN OBSTACLE
            self.ignore_user_input = True
            self.is_jump_performed = False
            self.set_new_desired_height(self.rectangle_height_sit // 2, 6)
            self.set_state('climb on raise')
        elif self.get_state() == 'climb on raise':                        # START CLIMBING ON AN OBSTACLE
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
        elif state == 'dying':
            # print(f'[state machine] {self.name} state: *DYING*.')
            self.animation_change_denied = False
            self.ignore_user_input = True
            self.summon_protector = False
            if self.think_type == 'exploding barrel':
                self.invincibility_timer = 1000
                self.set_state('almost explode')
                self.set_current_animation()
            else:
                self.dying = True
                if self.has_got_a_critical_hit:
                    self.set_state('decapitated')
                    self.set_current_animation()
                    self.animation_change_denied = True
                else:
                    self.set_new_desired_height(self.sprite_rectangle.height)
                    self.set_state('lie dead')
                    self.set_current_animation()
                    self.animation_change_denied = True
        elif state == 'lie dead':                        #
            self.heading = [0, 0]
            if self.idle_counter > 0:
                self.idle_counter -= 1
            else:
                if self.speed <= 0:
                    self.ignore_user_input = False
                    if self.just_got_jumped:
                        self.just_got_jumped = False
                    self.is_abort_jump = True
        elif state == 'decapitated':
            if self.animation_sequence_done:
                self.heading = [0, 0]
                self.set_new_desired_height(self.sprite_rectangle.height)
                self.set_state('lie decapitated')
                self.set_current_animation()
        elif state == 'lie decapitated':
            if self.idle_counter > 0:
                self.idle_counter -= 1
                # self.invincibility_timer -= 1
            else:
                self.heading = [0, 0]
                if self.speed <= 0:
                    # self.ignore_user_input = False
                    if self.just_got_jumped:
                        self.just_got_jumped = False
                    self.is_abort_jump = True
        elif state == 'almost explode':
            # print(f'[state machine] {self.name} is going to explode.')
            # print(f'[state machine] {self.name} state: *ALMOST EXPLODE*.')
            self.animation_change_denied = True
            if self.animation_sequence_done:
                self.set_state('explosion')
                self.animation_change_denied = False
                self.set_current_animation()
        elif state == 'explosion':
            self.animation_change_denied = True
            if self.animation_sequence_done:
                print(f'[state machine] {self.name} state: *EXPLOSION*.')
                self.dying = True
        elif state == 'prepare to get hurt and hopping':
            if not self.dead:
                self.summon_protector = False
                self.set_current_animation('getting hurt')
                self.ignore_user_input = True
                self.animation_change_denied = True
                self.scheduled_state = 'getting hurt'
            self.set_state('hopping prepare')
        # elif self.get_state() == 'hopping process while get hurt':
        #     if not self.is_stunned:
        #         if self.speed <= 0:
        #             self.ignore_user_input = False
        #             if self.just_got_jumped:
        #                 self.just_got_jumped = False
        #             self.is_abort_jump = True
        #             # self.movement_direction_inverter = 1
        #             # self.set_state('crouch')
        #             if not self.dead:
        #                 if self.scheduled_state:
        #                     self.set_state(self.scheduled_state)
        #                     self.scheduled_state = ''
        #                 else:
        #                     self.set_state('stand still')
        #             else:
        #                 if self.has_got_a_critical_hit:
        #                     self.set_state('lie decapitated')
        #                 else:
        #                     self.set_state('lie dead')
        elif state == 'prepare to get hurt':
            if not self.dead:
                self.ignore_user_input = True
                # self.summon_protector = False
                # self.summoned_protectors_description = list()
                self.set_state('getting hurt')
                self.set_current_animation()
        elif state == 'getting hurt':
            if self.is_stand_on_ground:
                self.heading[0] = 0
            if self.animation_sequence_done:
                self.ignore_user_input = False
                self.animation_change_denied = False
                self.set_state('stand still')

    # def state_machine(self):
    #     state = self.get_state()
    #     if self.get_state() == 'drop stash':                          #
    #         self.drop_item_from_inventory(self.inventory['burden']['stash']['item'])
    #         self.set_state('stand still')
    #     elif self.get_state() == 'prepare carry stash':                          #
    #         # self.speed = self.max_speed // 3
    #         self.set_state('hold stash')
    #     elif self.get_state() == 'hold stash':  #
    #         self.speed = 0
    #         self.heading[0] = 0
    #     elif self.get_state() == 'carry stash right':  #
    #         self.speed = 5
    #         # self.speed = self.max_speed // 3
    #         self.look = 1
    #     elif self.get_state() == 'carry stash left':  #
    #         self.speed = 5
    #         # self.speed = self.max_speed // 3
    #         self.look = -1
    #     elif self.get_state() == 'prepare kick':                          # PREPARING kick ATTACK
    #         self.activate_weapon('jake kick')
    #         self.set_state('prepare attack')
    #         self.force_use_previous_weapon = True
    #     elif self.get_state() == 'prepare attack':                          # PREPARING ATTACK
    #         self.set_state(self.current_weapon['attack animation'])
    #         self.stamina_reduce(self.current_stamina_lost_per_attack)
    #         self.mana_reduce(self.current_mana_lost_per_attack)
    #         self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
    #                                                   self.frames_changing_threshold_penalty
    #
    #         self.combo_counter = self.current_weapon['combo next step threshold']
    #         self.combo_set_number += 1
    #         if self.combo_set_number > self.current_weapon['combo steps quantity']:
    #             self.combo_set_number = 1
    #
    #         self.set_current_animation()
    #         self.ignore_user_input = self.current_weapon['ignore user input']
    #
    #         if self.is_stand_on_ground:
    #             self.heading[0] = 0
    #         # self.heading[0] = 0
    #     elif self.get_state() == 'protect':
    #         self.normal_stamina_replenish = 0.08
    #         # self.stamina_replenish_modifier = 0.3
    #         self.heading[0] = 0
    #     elif self.get_state() == 'prepare crouch attack left':                          # PREPARING ATTACK
    #         self.set_state(self.current_weapon['attack animation'] + ' crouch left')
    #         self.stamina_reduce(self.current_stamina_lost_per_attack)
    #         self.mana_reduce(self.current_mana_lost_per_attack)
    #         self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
    #                                                   self.frames_changing_threshold_penalty
    #         self.set_current_animation()
    #         self.ignore_user_input = self.current_weapon['ignore user input']
    #         if self.is_stand_on_ground:
    #             self.heading[0] = 0
    #     elif self.get_state() == 'prepare crouch attack right':                          # PREPARING ATTACK
    #         self.set_state(self.current_weapon['attack animation'] + ' crouch right')
    #         self.stamina_reduce(self.current_stamina_lost_per_attack)
    #         self.mana_reduce(self.current_mana_lost_per_attack)
    #         self.frames_changing_threshold_modifier = self.current_weapon['animation speed modifier'] * \
    #                                                   self.frames_changing_threshold_penalty
    #         self.set_current_animation()
    #         self.ignore_user_input = self.current_weapon['ignore user input']
    #         if self.is_stand_on_ground:
    #             self.heading[0] = 0
    #     elif self.get_state() in ('stab', 'cast', 'axe swing', 'whip',
    #                               'whip crouch right', 'whip crouch left',
    #                               'kick', 'pistol shot'):                          # ATTACKING IN PROCESS...
    #                               # 'kick', 'protect', 'pistol shot'):                          # ATTACKING IN PROCESS...
    #         if self.animation_sequence_done:
    #             # print(f'[state machine] attack is done.')
    #             self.ignore_user_input = False
    #             # if self.force_use_previous_weapon:
    #             #     self.force_use_previous_weapon = False
    #             #     self.activate_weapon(self.previously_used_weapon)
    #             if self.__state in ('whip crouch right', 'whip crouch left'):
    #                 self.set_state('crouch')
    #             else:
    #                 self.set_state('stand still')
    #     elif self.get_state() == 'crouch down':                       # CROUCH DOWN PROCESS
    #         self.is_crouch = True
    #         self.is_grabbers_active = False
    #         self.set_new_desired_height(self.rectangle_height_sit, 5)
    #         self.set_new_desired_width(self.rectangle_width_sit, 3)
    #         self.set_state('crouch')
    #     elif self.get_state() == 'crouch':                          # CROUCH
    #         self.speed = 0
    #         self.heading[0] = 0
    #     elif self.get_state() == 'crouch turn left':                # CROUCH TURN RIGHT
    #         self.look = -1
    #         self.set_state('crouch')
    #     elif self.get_state() == 'crouch turn right':               # CROUCH TURN LEFT
    #         self.look = 1
    #         self.set_state('crouch')
    #     elif self.get_state() == 'crouch rise':  # CROUCH UP PROCESS
    #         self.is_crouch = False
    #         self.speed = 0
    #         self.set_new_desired_height(self.rectangle_height_default, 9)
    #         self.check_space_around()
    #         if self.is_enough_height:
    #             self.is_jump_performed = False
    #             self.set_state('stand still')
    #         else:
    #             self.set_state('crouch down')
    #             self.state_machine()
    #     elif self.get_state() == 'crawl right':
    #         # self.look = 1
    #         self.speed = self.max_speed // 3
    #         # self.heading[0] = 1
    #     elif self.get_state() == 'crawl left':
    #         # self.look = 1
    #         self.speed = self.max_speed // 3
    #         # self.heading[0] = -1
    #     elif self.get_state() == 'free':
    #         # self.heading[0] = 0
    #         ...
    #     elif self.get_state() == 'jump':
    #         # print('try to jump...')
    #         if not self.just_got_jumped:
    #             self.just_got_jumped = True
    #             self.jump_attempts_counter -= 1
    #             if self.jump_attempts_counter == 0:
    #                 # Stamina reduces while jumping only if there are no jump attempts left.
    #                 # If actor jumps a single hops, stamina remains unchanged.
    #                 self.stamina_reduce(self.normal_stamina_lost_per_second_jump)
    #             if self.fall_speed > -2:
    #                 self.is_grabbers_active = True
    #             self.is_jump = True
    #             self.influenced_by_obstacle = -1
    #             self.jump_height = self.max_jump_height
    #         else:
    #             if self.is_stand_on_ground:
    #                 self.is_jump_performed = True
    #                 self.heading[0] = 0
    #                 # self.just_got_jumped = True
    #                 # self.is_abort_jump = True
    #                 # self.is_jump_performed = False
    #                 self.set_state('stand still')
    #                 # self.set_state('jump cancel')
    #         self.is_abort_jump = False
    #     elif self.get_state() == 'jump cancel':                     # CANCEL JUMP
    #         self.just_got_jumped = False
    #         self.is_abort_jump = True
    #         self.is_jump_performed = False
    #         # self.set_new_desired_height(self.rectangle_height_default, 5)
    #         # self.set_new_desired_width(self.rectangle_width_default, 5)
    #         if self.is_stand_on_ground:
    #             self.set_state('stand still')
    #         else:
    #             if self.look == 1:
    #                 self.set_state('fly right')
    #             else:
    #                 self.set_state('fly left')
    #         # self.set_state('stand still')
    #     elif self.get_state() == 'hopping prepare':                        # HOP BACK
    #         self.heading[0] = 0
    #         # self.speed = 0
    #         # if self.is_stand_on_ground:
    #         # if self.movement_direction_inverter == -1 and not self.is_enough_space_left:
    #         #     return
    #         # if self.movement_direction_inverter == 1 and not self.is_enough_space_right:
    #         #     return
    #         if self.is_enough_space_above:
    #             self.ignore_user_input = True
    #             self.ai_input_right_arrow = False
    #             self.ai_input_left_arrow = False
    #             self.ai_input_attack = False
    #             self.ai_input_jump = False
    #             self.is_grabbers_active = False
    #             self.is_move_right: bool = False
    #             self.is_move_left: bool = False
    #             self.is_move_up: bool = False
    #             self.is_move_down: bool = False
    #             self.is_jump: bool = False
    #             self.is_crouch: bool = False
    #             self.is_abort_jump: bool = False
    #             self.is_jump_performed: bool = False
    #             if not self.just_got_jumped:
    #                 self.stamina_reduce(self.normal_stamina_lost_per_hop_back)
    #                 self.just_got_jumped = True
    #                 self.jump_attempts_counter -= 1
    #                 self.is_jump = True
    #                 self.influenced_by_obstacle = -1
    #                 self.jump_height = min(5 * self.hop_back_jump_height_modifier, 15)
    #                 # self.jump_height = self.max_jump_height * 0.6
    #                 self.speed = min(5 * self.hop_back_jump_height_modifier, 30)
    #                 # print(f'[state machine] hop back prepare: {self.hop_back_jump_height_modifier=} {self.jump_height=} {self.speed=}')
    #                 #self.movement_direction_inverter = -1
    #                 # self.heading[0] = 0
    #                 self.idle_counter = 25
    #                 # self.invincibility_timer = 20
    #                 self.hop_back_jump_height_modifier = self.default_hop_back_jump_height_modifier
    #             self.is_abort_jump = False
    #
    #             if self.dead:
    #                 # self.heading[0] = 0
    #                 if self.has_got_a_critical_hit:
    #                     self.set_state('lie decapitated')
    #                 else:
    #                     self.set_state('lie dead')
    #             else:
    #                 if self.get_state() == 'hanging on edge':
    #                     self.set_state('release edge')
    #                 else:
    #                     self.set_state('hopping process')
    #             print(f'[state_machine] "hopping prepare" routine ends: {self.movement_direction_inverter=}')
    #         # else:
    #         #     self.set_state('release edge')
    #         # else:
    #         #     self.set_state('stand still')
    #     elif self.get_state() == 'hopping process':            # HOPPING BACK PROCESS
    #         if self.idle_counter > 0:
    #             self.idle_counter -= 1
    #             # self.invincibility_timer -= 1
    #         else:
    #             if self.speed <= 0:
    #                 self.ignore_user_input = False
    #                 # self.animation_change_denied = False
    #                 if self.just_got_jumped:
    #                     self.just_got_jumped = False
    #                 self.is_abort_jump = True
    #                 # self.movement_direction_inverter = 1
    #                 # self.set_state('crouch')
    #                 if not self.dead:
    #                     if self.scheduled_state:
    #                         self.set_state(self.scheduled_state)
    #                         self.scheduled_state = ''
    #                     else:
    #                         self.animation_change_denied = False
    #                         self.set_state('stand still')
    #                 else:
    #                     if self.has_got_a_critical_hit:
    #                         self.animation_change_denied = False
    #                         self.set_state('lie decapitated')
    #                     else:
    #                         self.animation_change_denied = False
    #                         self.set_state('lie dead')
    #                 print(f'[state_machine] "hopping process" routine ends: {self.movement_direction_inverter=}')
    #     # elif self.get_state() == 'hop forward':                        # HOP BACK
    #     #     self.heading[0] = 0
    #     #     self.speed = 0
    #     #     # if self.is_stand_on_ground:
    #     #     if self.is_enough_space_above:
    #     #         self.ignore_user_input = True
    #     #         self.ai_input_right_arrow = False
    #     #         self.ai_input_left_arrow = False
    #     #         self.ai_input_attack = False
    #     #         self.ai_input_jump = False
    #     #         self.is_grabbers_active = False
    #     #         self.is_move_right: bool = False
    #     #         self.is_move_left: bool = False
    #     #         self.is_move_up: bool = False
    #     #         self.is_move_down: bool = False
    #     #         self.is_jump: bool = False
    #     #         self.is_crouch: bool = False
    #     #         self.is_abort_jump: bool = False
    #     #         self.is_jump_performed: bool = False
    #     #         if not self.just_got_jumped:
    #     #             self.stamina_reduce(self.normal_stamina_lost_per_hop_back)
    #     #             self.just_got_jumped = True
    #     #             self.jump_attempts_counter -= 1
    #     #             self.is_jump = True
    #     #             self.influenced_by_obstacle = -1
    #     #             self.jump_height = min(5 * self.hop_back_jump_height_modifier, 15)
    #     #             # self.jump_height = self.max_jump_height * 0.6
    #     #             self.speed = min(5 * self.hop_back_jump_height_modifier, 30)
    #     #             # print(f'[state machine] hop back prepare: {self.hop_back_jump_height_modifier=} {self.jump_height=} {self.speed=}')
    #     #             # self.movement_direction_inverter = -1
    #     #             # self.heading[0] = 0
    #     #             self.idle_counter = 20
    #     #             # self.invincibility_timer = 20
    #     #             self.hop_back_jump_height_modifier = self.default_hop_back_jump_height_modifier
    #     #         self.is_abort_jump = False
    #     #
    #     #         if self.dead:
    #     #             # self.heading[0] = 0
    #     #             self.set_state('lie dead')
    #     #         else:
    #     #             if self.get_state() == 'hanging on edge':
    #     #                 self.set_state('release edge')
    #     #             else:
    #     #                 self.set_state('hopping forward process')
    #     #             # else:
    #     #             #     self.set_state('crouch down')
    #     #         # return
    #     #
    #     #
    #     #     # else:
    #     #     #     self.set_state('release edge')
    #     #     # else:
    #     #     #     self.set_state('stand still')
    #     # elif self.get_state() == 'hopping forward process':            # HOPPING BACK PROCESS
    #     #     if self.idle_counter > 0:
    #     #         self.idle_counter -= 1
    #     #         # self.invincibility_timer -= 1
    #     #     else:
    #     #         if self.speed <= 0:
    #     #             self.ignore_user_input = False
    #     #             if self.just_got_jumped:
    #     #                 self.just_got_jumped = False
    #     #             self.is_abort_jump = True
    #     #             # self.movement_direction_inverter = 1
    #     #             # self.set_state('crouch')
    #     #             if not self.dead:
    #     #                 self.set_state('stand still')
    #     #             else:
    #     #                 self.set_state('lie dead')
    #     elif self.get_state() == 'slide':                           # SLIDE PREPARE
    #         if self.stats['stamina'] < self.normal_stamina_lost_per_slide or\
    #            self.look == 1 and not self.is_enough_space_right or\
    #            self.look == -1 and not self.is_enough_space_left:
    #             # self.set_state('jump cancel')
    #             self.set_state('crouch')
    #             return
    #         self.speed = self.max_speed * 4
    #         self.set_new_desired_height(self.rectangle_height_slide, 0)
    #         # self.set_new_desired_width(self.sprite_rectangle.w, 6)
    #         self.set_new_desired_width(self.rectangle_width_slide, 6)
    #         self.is_grabbers_active = False
    #         self.check_space_around()
    #         self.ignore_user_input = True
    #         self.rectangle.top  -= 50
    #         self.set_state('sliding')
    #         self.stamina_reduce(self.normal_stamina_lost_per_slide)
    #
    #         # if self.stats['stamina'] < self.normal_stamina_lost_per_slide:
    #         #     self.set_state('crouch')
    #         #     return
    #         # self.speed = self.max_speed * 4
    #         # self.set_new_desired_height(self.rectangle_height_slide, 0)
    #         # # self.set_new_desired_width(self.sprite_rectangle.w, 6)
    #         # self.set_new_desired_width(self.rectangle_width_slide, 6)
    #         # self.is_grabbers_active = False
    #         # self.check_space_around()
    #         # if (self.look == 1 and self.is_enough_space_right) or\
    #         #         (self.look == -1 and self.is_enough_space_left):
    #         #     self.ignore_user_input = True
    #         #     self.rectangle.top  -= 50
    #         #     self.set_state('sliding')
    #         #     self.stamina_reduce(self.normal_stamina_lost_per_slide)
    #         # else:
    #         #     self.speed = 0
    #         #     # self.speed = self.max_speed // 2
    #         #     self.set_new_desired_height(self.rectangle_height_sit)
    #         #     self.set_new_desired_width(self.rectangle_width_sit, 4)
    #         #     # self.set_rect_width(self.rectangle_width_sit)
    #         #     # self.set_rect_height(self.rectangle_height_sit)
    #         #     self.set_state('crouch')
    #     elif self.get_state() == 'sliding':                         # SLIDING PROCESS
    #         self.heading[0] = 0
    #         # self.set_new_desired_width(self.sprite_rectangle.w * 0.9, 6)
    #         if self.speed == 0:
    #             self.set_state('slide rise')
    #     elif self.get_state() == 'slide rise':                      # RISING AFTER SLIDE IS OVER
    #         self.ignore_user_input = False
    #         self.set_new_desired_height(self.rectangle_height_sit, 5)
    #         self.check_space_around()
    #         if self.is_enough_height:
    #             self.set_new_desired_width(self.rectangle_width_sit,10)
    #             self.set_state('crouch')
    #         else:
    #             self.set_new_desired_height(self.rectangle_height_slide, 0)
    #             self.set_state('prone')
    #     elif self.get_state() == 'crawl prone left':
    #         self.speed = self.max_speed // 3
    #         self.look = -1
    #         self.heading[0] = -1
    #         # print('sdsdsdsdsdsds')
    #         # self.set_new_desired_height(self.rectangle_height_slide, 0)
    #         # self.check_space_around()
    #     elif self.get_state() == 'crawl prone right':
    #         self.speed = self.max_speed // 3
    #         self.look = 1
    #         self.heading[0] = 1
    #         # print('sdsdsdsdsdsds')
    #         # self.set_new_desired_height(self.rectangle_height_slide, 0)
    #         # self.check_space_around()
    #     elif self.get_state() == 'prone':
    #         self.speed = 0
    #         self.heading[0] = 0
    #         self.set_new_desired_height(self.rectangle_height_sit, 0)
    #         self.check_space_around()
    #         if self.is_enough_height:
    #             self.set_state('crouch down')
    #         else:
    #             self.set_new_desired_height(self.rectangle_height_slide, 0)
    #         # self.set_new_desired_height(self.rectangle_height_slide, 0)
    #     elif self.get_state() == 'stand still':                     # STANDING STILL
    #         self.heading[0] = 0
    #         self.animation_change_denied = False
    #         self.normal_stamina_replenish = self.default_normal_stamina_replenish
    #         # self.frames_changing_threshold_modifier = 1
    #         # self.just_got_jumped = False
    #         # self.is_abort_jump = True
    #         # self.is_grabbers_active = True
    #         self.is_grabbers_active = False
    #         if self.rectangle.height != self.rectangle_height_default:
    #             self.set_new_desired_height(self.rectangle_height_default,10)
    #             self.check_space_around()
    #             if not self.is_enough_height:
    #                 self.set_state('crouch down')
    #                 self.state_machine()
    #                 return
    #         if self.rectangle.width != self.rectangle_width_default:
    #             self.set_new_desired_width(self.rectangle_width_default,10)
    #     # elif self.get_state() == 'turn left':                       # TURN LEFT
    #     #     if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
    #     #         # Switch off heading to force actor start reducing his speed and slow it down to zero.
    #     #         # After that self is going to be able to start acceleration to proper direction.
    #     #         self.heading[0] = 0
    #     #         # self.look = -1
    #     #     else:
    #     #         self.look = -1
    #     #         self.heading[0] = -1
    #     #         self.set_state('stand still')
    #     # elif self.get_state() == 'turn right':                      # TURN RIGHT
    #     #     if self.speed > 0:
    #     #         # if self.look == -1:  # and self.speed > 0:  # Actor looks to the other side and runs.
    #     #         #     # Switch off heading to force actor start reducing his speed and slow it down to zero.
    #     #         #     # After that self is going to be able to start acceleration to proper direction.
    #     #         #     self.heading[0] = 0
    #     #         self.heading[0] = 0
    #     #         # self.look = 1
    #     #     else:
    #     #         self.look = 1
    #     #         self.heading[0] = 1
    #     #         self.set_state('stand still')
    #     # Movement directions change routines backup:
    #     elif self.get_state() == 'turn left':                       # TURN LEFT
    #         if self.look == 1 and self.speed > 0:  # Actor looks to the other side and runs.
    #             # Switch off heading to force actor start reducing his speed and slow it down to zero.
    #             # After that self is going to be able to start acceleration to proper direction.
    #             self.heading[0] = 0
    #             # self.look = -1
    #         else:
    #             self.look = -1
    #             self.heading[0] = -1
    #             self.set_state('stand still')
    #     elif self.get_state() == 'turn right':                      # TURN RIGHT
    #         if self.look == -1 and self.speed > 0:  # Actor looks to the other side and runs.
    #             # Switch off heading to force actor start reducing his speed and slow it down to zero.
    #             # After that self is going to be able to start acceleration to proper direction.
    #             self.heading[0] = 0
    #             # self.look = 1
    #         else:
    #             self.look = 1
    #             self.heading[0] = 1
    #             self.set_state('stand still')
    #
    #     elif self.get_state() == 'fly left':                        # IN MID-AIR FLY LEFT
    #         if self.is_stand_on_ground:
    #             self.set_state('stand still')
    #             return
    #         if self.look == 1 and self.speed > 0:
    #             # Actor moves to the opposite direction.
    #             # Need to slow him down.
    #             self.heading[0] = 0
    #             self.is_grabbers_active = False
    #         else:
    #             self.look = -1
    #             self.heading[0] = -1
    #             self.is_grabbers_active = True
    #             if self.rectangle.height != self.rectangle_height_default:
    #                 self.set_new_desired_height(self.rectangle_height_default,5)
    #             if self.rectangle.width != self.rectangle_width_default:
    #                 self.set_new_desired_width(self.rectangle_width_default,5)
    #         # if self.is_stand_on_ground:
    #         #     self.set_state('stand still')
    #         #     return
    #         # # if self.look == 1
    #         # self.look = -1
    #         # self.heading[0] = -1
    #         # self.is_grabbers_active = True
    #         # if self.rectangle.height != self.rectangle_height_default:
    #         #     self.set_new_desired_height(self.rectangle_height_default,5)
    #         # if self.rectangle.width != self.rectangle_width_default:
    #         #     self.set_new_desired_width(self.rectangle_width_default,5)
    #     elif self.get_state() == 'run left':                        # RUN LEFT
    #         self.look = -1
    #         self.heading[0] = -1
    #         # self.is_grabbers_active = True
    #         if self.rectangle.height != self.rectangle_height_default:
    #             self.set_new_desired_height(self.rectangle_height_default,5)
    #         if self.rectangle.width != self.rectangle_width_default:
    #             self.set_new_desired_width(self.rectangle_width_default,5)
    #     elif self.get_state() == 'fly right':                        # IN MID-AIR MOVE RIGHT
    #         if self.is_stand_on_ground:
    #             self.set_state('stand still')
    #             return
    #         if self.look == -1 and self.speed > 0:
    #             # Actor moves to the opposite direction.
    #             # Need to slow him down.
    #             self.heading[0] = 0
    #             self.is_grabbers_active = False
    #         else:
    #             self.look = 1
    #             self.heading[0] = 1
    #             self.is_grabbers_active = True
    #             if self.rectangle.height != self.rectangle_height_default:
    #                 self.set_new_desired_height(self.rectangle_height_default,5)
    #             if self.rectangle.width != self.rectangle_width_default:
    #                 self.set_new_desired_width(self.rectangle_width_default,5)
    #         # self.look = 1
    #         # self.heading[0] = 1
    #         # self.is_grabbers_active = True
    #         # if self.rectangle.height != self.rectangle_height_default:
    #         #     self.set_new_desired_height(self.rectangle_height_default,5)
    #         # if self.rectangle.width != self.rectangle_width_default:
    #         #     self.set_new_desired_width(self.rectangle_width_default,5)
    #     elif self.get_state() == 'run right':                        # RUN RIGHT
    #         self.look = 1
    #         self.heading[0] = 1
    #         # self.is_grabbers_active = True
    #         if self.rectangle.height != self.rectangle_height_default:
    #             self.set_new_desired_height(self.rectangle_height_default,5)
    #         if self.rectangle.width != self.rectangle_width_default:
    #             self.set_new_desired_width(self.rectangle_width_default,5)
    #     elif self.get_state() == 'has just grabbed edge':            # GRAB THE EDGE
    #         self.potential_moving_distance = 0
    #         self.is_grabbers_active = False
    #         self.is_edge_grabbed = True
    #         self.fall_speed = 0
    #         self.heading[0] = 0
    #         self.speed = 0
    #         self.rectangle.width = self.rectangle_width_default
    #         self.rectangle.height = self.rectangle_height_default
    #         # self.set_new_desired_height(self.rectangle_height_default)
    #         # self.set_new_desired_width(self.rectangle_width_default)
    #         # self.processing_rectangle_size()
    #         self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #         if self.look == -1:
    #             self.rectangle.left = self.obstacles_around[self.influenced_by_obstacle].rectangle.right + 1
    #             self.is_enough_space_left = False
    #         else:
    #             self.rectangle.right = self.obstacles_around[self.influenced_by_obstacle].rectangle.left - 1
    #             self.is_enough_space_right = False
    #         self.jump_attempts_counter = 0
    #         # self.jump_attempts_counter = self.max_jump_attempts
    #         self.set_state('hanging on edge')
    #     elif self.get_state() == 'hanging on edge':                 # HANGING ON THE EDGE
    #         self.just_got_jumped = False
    #         self.is_abort_jump = True
    #         # self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #     # elif self.get_state() == 'hanging on ghost':                # HANGING ON THE GHOST PLATFORM
    #     #     self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #     #     if self.idle_counter > 0:
    #     #         self.idle_counter -= 1
    #     #     else:
    #     #         self.ignore_user_input = False
    #     elif self.get_state() == 'hop down from ghost':             # PREPARE TO HOP DOWN FROM THE GHOST PLATFORM
    #         self.potential_moving_distance = 0
    #         # self.is_edge_grabbed = True
    #         # self.ignore_user_input = True
    #         # self.idle_counter = 25
    #         self.fall_speed = 0
    #         self.heading[0] = 0
    #         self.speed = 0
    #         # self.set_new_desired_height(self.rectangle_height_default, 5)
    #         # self.set_new_desired_width(self.rectangle_width_default, 5)
    #
    #         self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.bottom + 1
    #         # self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #         self.reset_self_flags()
    #         self.jump_attempts_counter = 0
    #         self.influenced_by_obstacle = -1
    #         self.set_state('jump cancel')
    #         # self.set_state('hanging on ghost')
    #     elif self.get_state() == 'release edge':                    # RELEASE
    #         self.is_edge_grabbed = False
    #         self.is_grabbers_active = False
    #         self.rectangle.y += self.look * -10
    #         # self.rectangle.y += self.obstacles_around[self.influenced_by_obstacle].vec_to_destination[1] * -4
    #         self.influenced_by_obstacle = -1
    #         self.speed = 0
    #         self.ignore_user_input = False
    #         # if self.is_stand_on_ground:
    #         self.set_state('stand still')
    #     elif self.get_state() == 'climb on':                        # START CLIMBING ON AN OBSTACLE
    #         self.ignore_user_input = True
    #         self.is_jump_performed = False
    #         self.set_new_desired_height(self.rectangle_height_sit // 2, 6)
    #         self.set_state('climb on raise')
    #     elif self.get_state() == 'climb on raise':                        # START CLIMBING ON AN OBSTACLE
    #         if self.rectangle.height <= self.rectangle_height_sit // 2:
    #             self.check_space_around()
    #             if self.is_enough_height:
    #                 self.rectangle.bottom = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #                 self.rectangle.centerx += 1 * self.look  # Slightly pushing an actor far from the edge of an obstacle to let his bottom collider do the job.
    #                 self.ignore_user_input = False
    #                 self.is_edge_grabbed = False
    #                 self.set_state('stand still')
    #                 # self.set_state('crouch down')
    #             else:
    #                 self.set_state('hanging on edge')
    #         else:
    #             self.rectangle.top = self.obstacles_around[self.influenced_by_obstacle].rectangle.top
    #     elif self.get_state() == 'dying':
    #         # print(f'[state machine] {self.name} state: *DYING*.')
    #         # if self.animation_sequence_done:
    #         self.animation_change_denied = False
    #         if self.think_type == 'exploding barrel':
    #             self.set_state('almost explode')
    #         else:
    #             self.dying = True
    #             if self.has_got_a_critical_hit:
    #                 self.set_state('decapitated')
    #             else:
    #                 self.set_state('lie dead')
    #     elif self.get_state() == 'lie dead':                        #
    #         self.set_new_desired_height(self.sprite_rectangle.height)
    #         self.animation_change_denied = False
    #         self.heading = [0, 0]
    #         if self.idle_counter > 0:
    #             self.idle_counter -= 1
    #             # self.invincibility_timer -= 1
    #         else:
    #             if self.speed <= 0:
    #                 self.ignore_user_input = False
    #                 if self.just_got_jumped:
    #                     self.just_got_jumped = False
    #                 self.is_abort_jump = True
    #     elif self.get_state() == 'decapitated':
    #         self.animation_change_denied = False
    #         if self.animation_sequence_done:
    #             self.set_state('lie decapitated')
    #     elif self.get_state() == 'lie decapitated':
    #         self.set_new_desired_height(self.sprite_rectangle.height)
    #         self.animation_change_denied = False
    #         self.heading = [0, 0]
    #         if self.idle_counter > 0:
    #             self.idle_counter -= 1
    #             # self.invincibility_timer -= 1
    #         else:
    #             if self.speed <= 0:
    #                 self.ignore_user_input = False
    #                 if self.just_got_jumped:
    #                     self.just_got_jumped = False
    #                 self.is_abort_jump = True
    #     elif self.get_state() == 'almost explode':
    #         # print(f'[state machine] {self.name} is going to explode.')
    #         # print(f'[state machine] {self.name} state: *ALMOST EXPLODE*.')
    #         self.invincibility_timer = 100
    #         self.animation_change_denied = False
    #         if self.animation_sequence_done:
    #             self.set_state('explosion')
    #     elif self.get_state() == 'explosion':
    #         self.animation_change_denied = False
    #         if self.animation_sequence_done:
    #             print(f'[state machine] {self.name} state: *EXPLOSION*.')
    #             self.dying = True
    #     elif self.get_state() == 'prepare to get hurt and hopping':
    #         self.set_current_animation('getting hurt')
    #         self.animation_change_denied = True
    #         self.scheduled_state = 'getting hurt'
    #         self.set_state('hopping prepare')
    #     # elif self.get_state() == 'hopping process while get hurt':
    #     #     if not self.is_stunned:
    #     #         if self.speed <= 0:
    #     #             self.ignore_user_input = False
    #     #             if self.just_got_jumped:
    #     #                 self.just_got_jumped = False
    #     #             self.is_abort_jump = True
    #     #             # self.movement_direction_inverter = 1
    #     #             # self.set_state('crouch')
    #     #             if not self.dead:
    #     #                 if self.scheduled_state:
    #     #                     self.set_state(self.scheduled_state)
    #     #                     self.scheduled_state = ''
    #     #                 else:
    #     #                     self.set_state('stand still')
    #     #             else:
    #     #                 if self.has_got_a_critical_hit:
    #     #                     self.set_state('lie decapitated')
    #     #                 else:
    #     #                     self.set_state('lie dead')
    #     elif self.get_state() == 'prepare to get hurt':
    #         self.ignore_user_input = True
    #         self.set_state('getting hurt')
    #     elif self.get_state() == 'getting hurt':
    #         if not self.is_stunned:
    #             if self.animation_sequence_done:
    #                 self.ignore_user_input = False
    #                 self.animation_change_denied = False
    #                 self.set_state('stand still')

    def reset_self_flags(self):
        self.is_move_left = False
        self.is_move_right = False
        self.is_move_up = False
        self.is_move_down = False
        self.is_jump = False
        # self.is_edge_grabbed = False

    def think(self):
        if self.think_type == 'chaser':
            # Change weapon depends on target vicinity:
            # print('[think]', list(self.inventory['weapons'].keys()))
            # if not self.animation_sequence_done:
            #     return
            if self.rectangle.centerx > self.target.rectangle.centerx:
                self.ai_input_left_arrow = True
                self.ai_input_right_arrow = False
                self.ai_input_attack = False
                self.look = -1
            else:
                self.ai_input_left_arrow = False
                self.ai_input_right_arrow = True
                self.ai_input_attack = False
                self.look = 1

            if self.sprite_rectangle.colliderect(self.target.sprite_rectangle):
                # Smash actor immediately:
                self.activate_weapon(0)  # Activate close combat weapon (always has index 0).
                self.ai_input_attack = True
            else:

                if abs(self.rectangle.centerx - self.target.rectangle.centerx) <= self.current_weapon['reach']:

                    if self.rectangle.centery >= self.target.rectangle.centery:
                        # self.activate_weapon(0)  # Activate close combat weapon (always has index 0).
                        if self.get_state() != 'jump':
                            self.ai_input_jump = True
                            # print('wanna jump')
                        else:
                            self.activate_weapon(0)  # Activate close combat weapon (always has index 0).
                            self.ai_input_attack = True
                            # print('wanna attack in the air')
                    else:
                        self.activate_weapon(1)  # Activate middle-ranged weapon (always has index 1).
                        self.ai_input_attack = True
                        # print('wanna attack')
                    # if self.get_state() == 'jump':
                    #     self.ai_input_attack = True
                else:
                    # if randint(0, 50) == 1:
                    if self.next_ranged_weapon_usage_counter > 0:
                        self.next_ranged_weapon_usage_counter -= 1
                    else:
                        self.next_ranged_weapon_usage_counter = randint(100, 120)
                        if self.stats['mana'] >= self.current_mana_lost_per_attack:
                            self.activate_weapon(2)  # Activate ranged weapon (always has index 2).
                            self.ai_input_attack = True
                            self.ai_input_left_arrow = False
                            self.ai_input_right_arrow = False
                        # if self.stats['mana'] < self.current_mana_lost_per_attack:
                        #     self.activate_weapon(1)
                        # else:
                        #     self.ai_input_attack = True
                        #     self.ai_input_left_arrow = False
                        #     self.ai_input_right_arrow = False
        elif self.think_type == 'exploding barrel':
            if self.fall_speed > 20:  # barrel explodes if it falls from the height of 4 blocks (50 pixels * 4)
                self.set_state('almost explode')
            # if self.get_state() == 'dying':
            #     print(f'[think] A barrel consider to be dying.')
            #     self.set_state('almost explode')
            #     # self.ai_input_attack = True
            #     self.think_type = ''

        if self.ai_input_jump:
            # self.ai_input_jump = False
            self.set_action('jump action')
            # return
        else:
            self.set_action('jump action cancel')

        if self.ai_input_right_arrow:
            self.set_action('right action')
            # return
        else:
            self.set_action('right action cancel')

        if self.ai_input_left_arrow:
            self.set_action('left action')
            # return
        else:
            self.set_action('left action cancel')

        if self.ai_input_attack:
            self.ai_input_attack = False
            self.set_action('attack')