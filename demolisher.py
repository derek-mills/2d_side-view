# from obstacle import *
# import pygame

from entity import *
from misc_tools import check_lines_intersection
from pygame import Rect

class Demolisher(Entity):
# class Demolisher(Obstacle):

    def __init__(self):
        super().__init__()
        # self.id: int = 0
        self.type = 'demolisher'
        self.acceleration = 0.1
        # self.air_acceleration = 0
        # self.max_speed = 0
        self.snap_to_actor: int = 0  # Active actor which cause this demolisher to be glued.
        self.snapping_offset = dict()
        # self.snapping_offset = list()
        self.protection = dict()
        self.damage = dict()
        self.push = False
        self.mana_consumption: int = 0
        self.stamina_consumption: int = 0
        self.impact_recoil: bool = True    # This demolisher causes stunning of own parent if it hits a protector.

        # Total damage amount is necessary to burn out stamina of a sneaky actor, protected by shield.
        self.total_damage_amount: float = 0.

        # self.damage: float = 0.
        self.damage_reduce: float = 0.
        self.parent_id: int = -1
        self.parent = None  # Instance of parent Entity() class.
        self.static = True
        self.attack_type = list()
        self.bounce = False
        self.bounce_factor: float = 0.  # Vertical and horizontal speed reducing after every bounce.
        self.aftermath: str = ''  # Description of the demolisher behavior after TTL timer runs out.
        self.flyer = False
        # self.speed = 5
        self.floppy = False     # If Demolisher becomes floppy, it is unable to make harm to anybody.
        # self.rectangle = Rect(0, 0, 50, 50)

    # def update(self, update_distance):
    #     self.rectangle.x += update_distance[0]
    #     self.rectangle.y += update_distance[1]

    # def update__(self, snap_side, snap_rect):
    #     # print(f"[demolisher update] Enter: {snap_side=} {snap_rect=} {self.rectangle=}")
    #     if snap_side == 1:  # Snapping to the actor's right side
    #         self.rectangle.left = snap_rect.centerx + self.snapping_offset[0]
    #         self.rectangle.top = snap_rect.centery + self.snapping_offset[1]
    #     else:
    #         self.rectangle.right = snap_rect.centerx + self.snapping_offset[0]
    #         self.rectangle.top = snap_rect.centery + self.snapping_offset[1]
    #     # print(f"[demolisher update] Exit with: {self.rectangle=}")
    #     # print(f"[demolisher update] ---------------------------")

    def update(self):
        self.rectangle.centerx = self.parent.rectangle.centerx + self.parent.current_sprite['demolisher snap point'][0] \
                                 - self.snapping_offset['offset inside demolisher'][0] * self.parent.look # * self.parent.movement_direction_inverter #

        self.rectangle.centery = self.parent.rectangle.centery + self.parent.current_sprite['demolisher snap point'][1] \
                                 - self.snapping_offset['offset inside demolisher'][1]
        # print(f'[demolisher update] {self.snapping_offset["offset inside actor"]=} {offset_inside_rect=}')



        # if self.parent.look == -1:
        # # if self.parent.movement_direction_inverter * self.parent.look == -1:
        #     self.rectangle.centerx = self.parent.rectangle.centerx + self.parent.current_sprite['demolisher snap point'][0] \
        #                              - self.snapping_offset['offset inside demolisher'][0] * -1
        #     self.rectangle.centery = self.parent.rectangle.centery + self.parent.current_sprite['demolisher snap point'][1] \
        #                              - self.snapping_offset['offset inside demolisher'][1]
        # elif self.parent.look == 1:
        # # elif self.parent.movement_direction_inverter * self.parent.look == 1:
        #     self.rectangle.centerx = self.parent.rectangle.centerx + self.parent.current_sprite['demolisher snap point'][0] \
        #                              - self.snapping_offset['offset inside demolisher'][0]
        #     self.rectangle.centery = self.parent.rectangle.centery + self.parent.current_sprite['demolisher snap point'][1] \
        #                              - self.snapping_offset['offset inside demolisher'][1]

        # if snap_side == 1:  # Snapping to the actor's right side
        #     self.rectangle.centerx = snap_rect.centerx + offset_inside_rect[0] \
        #                              - self.snapping_offset['offset inside demolisher'][0]
        #     self.rectangle.centery = snap_rect.centery + offset_inside_rect[1] \
        #                              - self.snapping_offset['offset inside demolisher'][1]
        #     # self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
        #     #                          - self.snapping_offset['offset inside demolisher'][0]
        #     # self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
        #     #                          - self.snapping_offset['offset inside demolisher'][1]
        #
        # else:
        #     self.rectangle.centerx = snap_rect.centerx + offset_inside_rect[0] \
        #                              - self.snapping_offset['offset inside demolisher'][0] * -1
        #     self.rectangle.centery = snap_rect.centery + offset_inside_rect[1] \
        #                              - self.snapping_offset['offset inside demolisher'][1]

    def update_old(self, snap_side, snap_rect, offset_inside_rect):
        # print(f'[demolisher update] {self.snapping_offset["offset inside actor"]=} {offset_inside_rect=}')
        if snap_side == 1:  # Snapping to the actor's right side
            self.rectangle.centerx = snap_rect.centerx + offset_inside_rect[0] \
                                     - self.snapping_offset['offset inside demolisher'][0]
            self.rectangle.centery = snap_rect.centery + offset_inside_rect[1] \
                                     - self.snapping_offset['offset inside demolisher'][1]
            # self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
            #                          - self.snapping_offset['offset inside demolisher'][0]
            # self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
            #                          - self.snapping_offset['offset inside demolisher'][1]

        else:
            self.rectangle.centerx = snap_rect.centerx + offset_inside_rect[0] \
                                     - self.snapping_offset['offset inside demolisher'][0] * -1
            self.rectangle.centery = snap_rect.centery + offset_inside_rect[1] \
                                     - self.snapping_offset['offset inside demolisher'][1]

    def update_very_old(self, snap_side, snap_rect):
        # self.rectangle.centerx = snap_rect.centerx + self.snapping_offset[snap_side][0]
        # self.rectangle.centery = snap_rect.centery + self.snapping_offset[snap_side][1]

        if snap_side == 1:  # Snapping to the actor's right side
            self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
                                     - self.snapping_offset['offset inside demolisher'][0]
            self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
                                     - self.snapping_offset['offset inside demolisher'][1]
            # self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
            #                          + abs(self.snapping_offset['offset inside demolisher'][0])
            # self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
            #                          + abs(self.snapping_offset['offset inside demolisher'][1])

        else:
            self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
                                     - self.snapping_offset['offset inside demolisher'][0] * -1
            self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
                                     - self.snapping_offset['offset inside demolisher'][1]
            # self.rectangle.centerx = snap_rect.centerx + self.snapping_offset['offset inside actor'][0] \
            #                          - self.snapping_offset['offset inside demolisher'][0] * -1
            # self.rectangle.centery = snap_rect.centery + self.snapping_offset['offset inside actor'][1] \
            #                          + abs(self.snapping_offset['offset inside demolisher'][1])


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
                # # self.summoned_sounds.append(self.sounds['obstacle hit'])

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
                # self.summoned_sounds.append(self.sounds['obstacle hit'])

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
                # self.summoned_sounds.append(self.sounds['obstacle hit'])

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
                # self.summoned_sounds.append(self.sounds['obstacle hit'])

                if self.fall_speed < 0:
                    self.potential_falling_distance = obs.rectangle.bottom - self.collision_detector_top.bottom
                    self.is_stand_on_ground = False
                    self.fall_speed = 0
                    # continue

    def detect_collisions_with_obstacles_simple(self):
        # return
        self.is_being_collided_now = False

        for key in self.obstacles_around.keys():
            obs = self.obstacles_around[key]
            obs.is_being_collided_now = False
            if obs.is_ghost_platform:
                continue
            if obs.rectangle.colliderect(self.rectangle):
                self.is_being_collided_now = True
                # self.summoned_sounds.append(self.sounds['obstacle hit'])

                return

    def become_mr_floppy(self):
        self.floppy = True

    def detect_collisions_with_protectors(self):
        if self.floppy:
            # print(f'[detect collision with protectors] {self.id} IS FLOPPY...')
            return
        if self.protectors_around:
            # print(f'[detect collision with protectors] {self.id} collision check starting...')
            hit_detected = False
            for k in self.protectors_around.keys():
                p = self.protectors_around[k]
                if self.parent:
                    if self.parent.id == p.parent.id:
                        continue
                if self.flyer:
                    protector_lines = (
                        (p.rectangle.topleft, p.rectangle.bottomleft),
                        (p.rectangle.topright, p.rectangle.bottomright)
                    )
                    self_trace_has_been_passed = (self.previous_location,
                                                  self.rectangle.topleft)
                    # print(f'[detect collision with protectors {self.id}] trace={self_trace_has_been_passed}')
                    # print(f'[detect collision with protectors {self.id}] protector={protector_diagonals}')
                    # print()
                    for diagonal in protector_lines:
                        if check_lines_intersection(self_trace_has_been_passed, diagonal):
                            hit_detected = True
                            # print('HIT')
                            # print(f'[detect collision with protectors {self.id}] trace={self_trace_has_been_passed} protector={protector_diagonals}')
                            break
                else:
                    if self.rectangle.colliderect(p.rectangle):
                    # if self.rectangle.colliderect(p.rectangle) and self.look != p.parent.look:
                        hit_detected = True

                if hit_detected:
                    # self.summoned_sounds.append(p.sounds[self.type])

                    self.summoned_particle_descriptions.append({
                        'sprite': 'sparkles',
                        'particle TTL': 3,
                        'width': 21,
                        'height': 22,
                        'xy': (p.rectangle.centerx, self.rectangle.y),
                        'bounce': False,
                        'bounce factor': 0.,
                        'subtype': 'sprite',
                        'color': self.blood_color,
                        'look': self.look,
                        # 'look': self.look * -1,  # Splatter always fly in the opposite direction
                        'speed': 1,
                        'jump height': 0,
                        'collides': False,
                        'gravity affected': False
                    })

                    # print(f'[detect collision with protectors] {self.id} collided with {p.name}, {p.look=}, {self.look=}')

                    # self.parent.make_all_following_demolishers_floppy = True
                    if self.impact_recoil:
                        # Strike back own parent, because demolisher get hit to the shield.
                        if self.parent:
                            print(f'[demolisher detect w\protectors ({self.name} {self.id})] strikes back parent: {self.parent.name}')
                            self.parent.set_state('prepare to get hurt')
                            self.parent.stun_counter = 40 # How many cycles attacking actor will be recovering from recoil.
                            self.parent.state_machine()

                    if not self.floppy:
                        self.summoned_sounds.append(p.sounds[self.type])
                        # Reduce all damaging abilities according to protector's might:
                        damage_to_owner_of_protector = dict()
                        for damage_type in self.damage:
                            damage_to_owner_of_protector[damage_type] = self.damage[damage_type] * p.protection[damage_type]
                            self.damage[damage_type] = self.damage[damage_type] * p.protection[damage_type] if damage_type != "fire" else self.damage[damage_type]
                            # self.damage[damage_type] *= p.protection[damage_type]


                        if self.id not in p.parent.got_immunity_to_demolishers:
                            p.parent.got_immunity_to_demolishers.append(self.id)
                        # p.parent.mana_reduce(p.mana_consumption * p.parent.normal_mana_lost_per_defend)
                        p.parent.stamina_reduce(p.stamina_consumption * p.parent.normal_stamina_lost_per_defend)
                        p.parent.get_damage(damage_to_owner_of_protector, 1)
                        # p.parent.get_damage(self.damage, 1)
                        if p.parent.total_damage_has_got > 0:
                            if p.parent.stats['stamina'] > 0:
                            # if p.parent.stats['stamina'] > 0 and p.parent.stats['mana'] > 0:
                                p.parent.invincibility_timer = self.default_invincibility_timer
                            if self.id not in p.parent.got_immunity_to_demolishers:
                                p.parent.got_immunity_to_demolishers.append(self.id)
                            # print(f'[detect demolishers] {p.parent.got_immunity_to_demolishers}')
                            p.parent.set_state('prepare to get hurt')
                            p.parent.state_machine()
                            p.parent.summon_info_blob(str(int(p.parent.total_damage_has_got)), YELLOW if p.parent.id == 0 else WHITE, self.parent.look if self.parent else 1)

                        if self.bounce:
                            print(f'[demolisher detect w\protectors ({self.name} {self.id})] bounces.')
                            self.is_being_collided_now = True
                            self.parent_id = -1
                            self.parent = None
                            if self.rectangle.centerx > p.rectangle.centerx:
                                self.collided_left = True
                            else:
                                self.collided_right = True
                        else:
                            self.dead = True
                        self.become_mr_floppy()
                    break

    def process_protector(self):
    # def process_demolisher(self, time_passed):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                # if self.aftermath == 'disappear':
                self.die()
                return
        # if self.damage_reduce > 0:
        #     for damage_type in self.damage.keys():
        #         self.damage[damage_type] -= self.damage_reduce
        # if self.is_collideable:
        #     # print('Demolisher check collisions with ', self.obstacles_around.keys())
        #     self.calculate_colliders()
        #     self.detect_collisions_with_obstacles()
        #     if self.is_being_collided_now:
        #         if self.bounce:
        #             self.speed *= self.bounce_factor
        #             if self.collided_left:
        #                 self.look = 1
        #             elif self.collided_right:
        #                 self.look = -1
        #             elif self.collided_bottom:
        #                 self.fall_speed *= -self.bounce_factor  # Bounce up from the floor.
        #                 self.is_stand_on_ground = False
        #         else:
        #             self.die()
        #             return
        if not self.static:
            self.calculate_speed()
            if self.flyer:
                self.fly()
                # self.fly(time_passed)
            else:
                self.move()
                # self.move(time_passed)
            if self.is_gravity_affected:
                self.calculate_fall_speed()  # Discover speed and potential fall distance
                self.fall()

    def process_demolisher(self):
    # def process_demolisher(self, time_passed):
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl == 0:
                # if self.aftermath == 'disappear':
                self.die()
                return
        if self.damage_reduce > 0:
            for damage_type in self.damage.keys():
                self.damage[damage_type] -= self.damage_reduce

        # if self.is_collideable:
        #     # print('Demolisher check collisions with ', self.obstacles_around.keys())
        #     self.calculate_colliders()
        #     self.detect_collisions_with_obstacles()
        # self.detect_collisions_with_protectors()
        #
        # if self.is_being_collided_now:
        #     if self.bounce:
        #         if self.fall_speed > 1:
        #             self.summoned_sounds.append(self.sounds['obstacle hit'])
        #         self.floppy = False
        #         self.speed *= self.bounce_factor
        #         if self.collided_left:
        #             self.look = 1
        #         elif self.collided_right:
        #             self.look = -1
        #         elif self.collided_bottom:
        #             self.fall_speed *= -self.bounce_factor  # Bounce up from the floor.
        #             self.is_stand_on_ground = False
        #     else:
        #         self.summoned_sounds.append(self.sounds['obstacle hit'])
        #         self.die()
        #         return

        if not self.static:
            self.calculate_speed()
            if self.flyer:
                self.fly()
                # self.fly(time_passed)
            else:
                self.move()
                # self.move(time_passed)
            if self.is_gravity_affected:
                self.calculate_fall_speed()  # Discover speed and potential fall distance
                self.fall()

        if self.is_collideable:
            # print('Demolisher check collisions with ', self.obstacles_around.keys())
            self.calculate_colliders()
            self.detect_collisions_with_obstacles()
        self.detect_collisions_with_protectors()

        if self.is_being_collided_now:
            if self.bounce:
                if self.fall_speed > 1:
                    self.summoned_sounds.append(self.sounds['obstacle hit'])
                self.floppy = False
                self.speed *= self.bounce_factor
                if self.collided_left:
                    self.look = 1
                elif self.collided_right:
                    self.look = -1
                elif self.collided_bottom:
                    self.fall_speed *= -self.bounce_factor  # Bounce up from the floor.
                    self.is_stand_on_ground = False
            else:
                self.summoned_sounds.append(self.sounds['obstacle hit'])
                self.die()
                return
