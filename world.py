# import pygame
import pygame.draw

from actors_description import *
from actor import *
from obstacle import *
from demolisher import *
from particle import *
from items import all_items
# from constants import *
import fonts
import camera
from locations import *
from load_content import load_animations
from misc_tools import *  #black_out, black_in
# import pickle
from random import choice
from copy import copy
class World(object):
    def __init__(self):
        # Entities
        self.obstacles = dict()
        self.obstacle_id: int = 0
        self.active_obstacles = list()
        self.max_obs_id_in_current_location: int = 0
        self.demolishers = dict()
        self.demolisher_id: int = 0
        self.actors = dict()
        self.actor_id: int = 0
        self.items = dict()
        self.item_id: int = 0
        self.particles = dict()
        self.particle_id: int = 0

        self.locations = dict()
        self.location: str = ''
        self.location_has_been_changed = False
        self.is_new_location_loading: bool = True
        self.new_location_description = dict()
        self.obstacles_changes_pending = dict()

        # CONTROLS
        self.is_key_pressed = False
        self.is_attack = False
        self.is_input_up_arrow = False
        self.is_input_down_arrow = False
        self.is_input_right_arrow = False
        self.is_input_left_arrow = False
        self.is_input_confirm = False
        self.is_input_cancel = False
        self.is_z = False
        self.is_p = False
        self.is_i = False
        self.is_x = False
        self.is_n = False
        self.is_b = False
        self.is_jump_button = False
        self.jump_button_multiple_press_prevent = False
        self.is_attack_button = False
        self.attack_button_multiple_press_prevent = False
        self.is_l_shift = False
        self.is_l_ctrl = False
        self.is_l_alt = False
        self.l_alt_multiple_press_prevent = False
        self.is_mouse_button_down = False
        self.is_left_mouse_button_down = False
        self.is_right_mouse_button_down = False
        self.is_mouse_wheel_rolls = False
        self.is_mouse_wheel_up = False
        self.is_mouse_wheel_down = False
        self.mouse_xy = list()  #
        self.is_mouse_hovers_item: bool = False
        self.mouse_hovers_item: int = 0
        self.is_mouse_hovers_actor: bool = False
        self.mouse_hovers_actor: int = 0

        self.screen = None
        self.camera = camera.Camera()
        # self.camera.setup(MAXX*2, MAXY)
        self.time_passed: int = 0
        self.game_cycles_counter: int = 0
        self.is_quit:bool = False

        # GRAPHIC
        self.backgrounds = dict()
        # Info panel:
        self.info_panel_start_x = 10
        self.info_panel_start_y = 10
        self.info_panel_max_stripes_width = 500
        self.info_panel_gap_between_stripes = 1
        self.info_panel_font_size = 20


    def set_screen(self, surface):
        self.screen = surface


    def add_actor(self, description, start_xy):
        entity = Actor()
        entity.id = self.actor_id
        entity.name = description['name']
        entity.blood_color = description['blood color']
        entity.stats['max health'] = description['health']
        # entity.max_health = description['health']
        entity.stats['health'] = description['health']
        # entity.health = description['health']
        # print(f'[add_actor] --------------------------------------------------------------')
        # print(f'[add_actor] Adding {entity.name}, id={entity.id}, {entity.stats["health"]=}')
        # for k in description:
        #     print(f'[add_actor] {k} :{description[k]}')
        entity.is_gravity_affected = description['gravity affected']

        entity.rectangle.height = sprites[entity.name + ' 0']['sprite'].get_height()
        entity.rectangle.width = int(sprites[entity.name + ' 0']['sprite'].get_width() * 0.7)  # Width of rectangle is 70% of sprite width.
        entity.rectangle_width_sit = entity.rectangle.width * 1.34
        entity.rectangle_height_sit = sprites[entity.name + ' 18']['sprite'].get_height()

        # entity.rectangle.height = description['height']
        # entity.rectangle.width = description['width']
        entity.rectangle.center = start_xy
        # entity.rectangle.center = description['start_xy']
        # entity.rectangle.x += randint(-200, 300)
        entity.apply_measurements()
        entity.destination[0] = entity.rectangle.centerx
        entity.destination[1] = entity.rectangle.centery
        entity.max_speed = description['max speed']
        entity.default_max_speed = description['max speed']

        entity.animations = description['animations']
        entity.animation_descriptor = entity.name  # for ex.: 'player1'
        load_animations(entity)
        entity.set_state('stand still')
        entity.set_current_animation()
        # print(entity.get_state(), entity.current_animation)
        # exit()
        entity.frames_changing_threshold = entity.animations[entity.current_animation]['speed']
        # entity.frames_changing_threshold = entity.animations[entity.current_animation][entity.look]['speed']
        entity.animation_sequence = entity.animations[entity.current_animation]['sequence']
        # entity.animation_sequence = entity.animations[entity.current_animation][entity.look]['sequence']
        entity.set_current_sprite()

        entity.ai_controlled = description['AI controlled']
        entity.think_type = description['think type']
        entity.add_items_to_inventory(description['items'])
        entity.activate_weapon(0)
        # entity.activate_weapon('WHIP')
        # entity.activate_weapon('SHORT SWORD')

        # entity.change_animation()
        # entity.process_animation_counter()

        entity.set_state('stand still')
        # entity.max_jump_attempts = 3

        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()

        if entity.id == 0:
            # This is the player actor:
            self.actors['player'] = entity

        self.actors[self.location][entity.id] = entity
        self.actor_id += 1

    def add_item(self, item, xy):
        entity = Obstacle()
        self.item_id += 1
        # self.max_obs_id_in_current_location += 1
        # self.obstacle_id += 1
        # entity.id = self.max_obs_id_in_current_location
        # entity.id = self.obstacle_id + self.max_obs_id_in_current_location
        # entity.id = xy[-1]
        entity.id = self.item_id * 100
        # entity.id = str(self.item_id) + ' item'
        entity.rectangle.topleft = xy
        entity.origin_xy = xy
        entity.max_speed = 5
        # entity.speed = 5
        # entity.is_jump = True
        entity.is_force_render = True
        entity.sprite = item['sprite']
        entity.rectangle.width = sprites[entity.sprite]['sprite'].get_size()[0]
        entity.rectangle.height = sprites[entity.sprite]['sprite'].get_size()[1]
        entity.invisible = False
        entity.trigger = True
        entity.is_collideable = True
        entity.is_gravity_affected = True
        entity.let_actors_pass_through = True
        entity.is_item = True
        entity.item_name = item['label']
        entity.item_amount = item['amount']
        entity.item_amount_threshold = item['amount threshold']
        entity.item_amount_decrease_speed = item['amount decrease speed']
        # self.items[self.location][entity.id] = entity
        self.obstacles[self.location][entity.id] = entity

    def add_item_safe(self, item, xy):
        entity = Obstacle()
        # self.item_id += 1
        # self.max_obs_id_in_current_location += 1
        self.obstacle_id += 1
        # entity.id = self.max_obs_id_in_current_location
        entity.id = self.obstacle_id + self.max_obs_id_in_current_location
        # entity.id = self.item_id
        # entity.id = str(self.item_id) + ' item'
        entity.rectangle.topleft = xy
        entity.origin_xy = xy
        entity.max_speed = 5
        entity.is_force_render = True
        entity.sprite = item['sprite']
        entity.rectangle.width = sprites[entity.sprite]['sprite'].get_size()[0]
        entity.rectangle.height = sprites[entity.sprite]['sprite'].get_size()[1]
        entity.invisible = False
        entity.trigger = True
        entity.is_collideable = True
        entity.is_gravity_affected = True
        entity.let_actors_pass_through = True
        entity.is_item = True
        entity.item_name = item['label']
        entity.item_amount = item['amount']
        entity.item_amount_threshold = item['amount threshold']
        entity.item_amount_decrease_speed = item['amount decrease speed']
        # self.items[self.location][entity.id] = entity
        self.obstacles[self.location][entity.id] = entity

    def add_obstacle(self, description):
        entity = Obstacle()
        entity.id = description[-1]
        self.obstacle_id = description[-1]
        entity.rectangle.topleft = description[0]
        entity.origin_xy = description[0]
        entity.rectangle.width = description[1][0]
        entity.rectangle.height = description[1][1]
        if entity.id in self.locations[self.location]['obstacles']['settings'].keys():
            entity.exotic_movement = self.locations[self.location]['obstacles']['settings'][entity.id]['exotic movement'] \
                if 'exotic movement' in self.locations[self.location]['obstacles']['settings'][entity.id] else None

            entity.active = self.locations[self.location]['obstacles']['settings'][entity.id]['active']
            entity.is_force_render = self.locations[self.location]['obstacles']['settings'][entity.id]['force render'] if 'force render' in \
                                    self.locations[self.location]['obstacles']['settings'][entity.id].keys() else False
            entity.actions = self.locations[self.location]['obstacles']['settings'][entity.id]['actions']
            entity.trigger = self.locations[self.location]['obstacles']['settings'][entity.id]['trigger']
            entity.trigger_description = self.locations[self.location]['obstacles']['settings'][entity.id]['trigger description']
            entity.teleport = self.locations[self.location]['obstacles']['settings'][entity.id]['teleport']
            entity.teleport_description = self.locations[self.location]['obstacles']['settings'][entity.id]['teleport description']
            entity.let_actors_pass_through = self.locations[self.location]['obstacles']['settings'][entity.id]['actors pass through']
            entity.is_ghost_platform = self.locations[self.location]['obstacles']['settings'][entity.id]['ghost']
            entity.is_collideable = self.locations[self.location]['obstacles']['settings'][entity.id]['collideable']
            entity.is_gravity_affected = self.locations[self.location]['obstacles']['settings'][entity.id]['gravity affected']
            entity.invisible = self.locations[self.location]['obstacles']['settings'][entity.id]['invisible']
            entity.max_speed = self.locations[self.location]['obstacles']['settings'][entity.id]['speed']
            entity.let_actors_grab = self.locations[self.location]['obstacles']['settings'][entity.id]['actors may grab'] if 'actors may grab' in \
                                      self.locations[self.location]['obstacles']['settings'][entity.id].keys() else False
            if 'item' in self.locations[self.location]['obstacles']['settings'][entity.id].keys():
                entity.is_item = self.locations[self.location]['obstacles']['settings'][entity.id]['item']
                entity.item_name = self.locations[self.location]['obstacles']['settings'][entity.id]['item name']['name']
                if entity.item_name:
                    # print(entity.item_name)
                    entity.item_amount = all_items[entity.item_name]['amount']
                    entity.item_amount_threshold = all_items[entity.item_name]['amount threshold']
                    entity.item_amount_decrease_speed = all_items[entity.item_name]['amount decrease speed']
                # entity.item_name = self.locations[self.location]['obstacles']['settings'][entity.id]['item name']['name'] if 'item name' in \
                #                       self.locations[self.location]['obstacles']['settings'][entity.id].keys() else ''
            # print(f'[add_obstacle] Added active obstacle: {entity.actions=} {entity.is_gravity_affected=}')
        # Add an obstacle to the world storage:
        # if self.location not in self.obstacles.keys():
        #     self.obstacles[self.location] = dict()
        self.obstacles[self.location][entity.id] = entity
        # if entity.id == 20:
        # print(f'[add_obstacle] Added obstacle: {entity.id=} {entity.is_collideable=} {entity.is_gravity_affected=}')
        # self.obstacle_id += 1


    def add_particle(self, description):
        p = Particle()
        p.id = self.particle_id
        self.particle_id += 1
        p.ttl = description['particle TTL']
        p.rectangle.width = description['width']
        p.rectangle.height = description['height']
        p.rectangle.center = description['xy']
        p.bounce = description['bounce']
        p.bounce_factor = description['bounce factor']
        p.subtype = description['subtype']
        p.color = description['color']
        p.look = description['look']
        # p.max_jump_height = description['jump height']
        p.fall_speed = -description['jump height'] if description['jump height'] > 0 else 0
        p.max_speed = description['speed']
        p.speed = description['speed']
        p.is_collideable = description['collides']
        p.is_gravity_affected = description['gravity affected']
        self.particles[self.location][p.id] = p

    def add_demolisher(self, description):
        demol = Demolisher()
        # demol.id = description[-1]
        demol.id = self.demolisher_id
        self.demolisher_id += 1
        demol.name = 'demolisher ' + str(demol.id)
        demol.ttl = description['demolisher TTL']

        if description['demolisher sprite']:
            demol.current_sprite = sprites[description['demolisher sprite']]
            demol.rectangle.width = sprites[description['demolisher sprite']]['mask rect'].width
            demol.rectangle.height = sprites[description['demolisher sprite']]['mask rect'].height
        else:
            # demol.current_sprite = None
            demol.rectangle.width = description['rect'].width
            demol.rectangle.height = description['rect'].height
            sprite = pygame.Surface((demol.rectangle.width, demol.rectangle.height)).convert_alpha()
            # sprite = pygame.Surface((demol.rectangle.width, demol.rectangle.height)).convert_alpha()
            sprite.fill(RED)
            # pygame.draw.circle(sprite, RED, demol.rectangle.center, demol.rectangle.width //2)
            mask = pygame.mask.from_surface(sprite.convert_alpha())
            demol.current_sprite = {
                'sprite': sprite,
                'sprite center': demol.rectangle.center,
                'sprite asymmetric': None,
                'mask': mask,
                'mask rect': mask.get_rect()
            }
        demol.bounce = description['bounce']
        demol.bounce_factor = description['bounce factor']
        demol.flyer = description['flyer']
        demol.parent = description['parent']


        if description['snap to actor'] >= 0:
            demol.snap_to_actor = description['snap to actor']
            actor = self.actors[self.location][description['snap to actor']]
            demol.parent_id = actor.id
            demol.snapping_offset = description['snapping offset']
            # demol.snapping_offset = actor.animations[actor.current_animation]['demolisher offset'][actor.look]
            demol.update(actor.look, actor.rectangle)
            if demol.flyer:
                demol.destination = (self.camera.max_offset_x + MAXX, demol.rectangle.y) if actor.look == 1 else (-100, demol.rectangle.y)
            demol.look = actor.look
        else:
            demol.rectangle.topleft = description['rect'].topleft
            demol.snapping_offset = [0, 0]
            demol.parent_id = -1
            demol.snap_to_actor = -1
            demol.look = description['look'] if 'look' in description.keys() else 1
            demol.destination_point = description['destination'] if 'destination' in description.keys() else (0, 0)
        demol.aftermath = description['aftermath']
        demol.damage = description['damage']
        demol.static = description['static']
        demol.damage_reduce = description['damage reduce']
        demol.max_speed = description['speed']
        demol.speed = description['speed']
        demol.is_collideable = description['collides']
        demol.is_gravity_affected = description['gravity affected']
        # demol.rectangle.y += randint(-150, 150)

        # self.demolishers[self.location][self.demolisher_id] = ent
        self.demolishers[self.location][demol.id] = demol
        # print(f'[add_demolisher] Added: {demol.id=} {demol.name} {demol.rectangle} {demol.max_speed=} {demol.destination=}')

    # def process(self):
    def process(self, time_passed):
        self.time_passed = time_passed
        self.processing_obstacles()
        if self.location_has_been_changed:
            self.actors['player'].influenced_by_obstacle = -1
            self.location_has_been_changed = False
            return
        self.processing_human_input()
        # self.processing_player_actor()
        self.processing_actors()
        if self.actors['player'].dead:
            self.game_over()
        self.processing_demolishers()
        self.processing_particles()

        # Applying camera offset:
        if self.actors['player'].influenced_by_obstacle >= 0 and  self.obstacles[self.location][self.actors['player'].influenced_by_obstacle].active:
            x_offset_speed = 2
            y_offset_speed = 5
            # y_offset_speed = 5 if self.obstacles[self.location][self.actors['player'].influenced_by_obstacle].vec_to_destination[1] > 0 else -5

            # x_offset_speed = round(self.obstacles[self.location][self.actors['player'].influenced_by_obstacle].vec_to_destination[0])
            # y_offset_speed = round(self.obstacles[self.location][self.actors['player'].influenced_by_obstacle].vec_to_destination[1])
        else:
            x_offset_speed = self.actors['player'].speed  # * self.actors['player'].look
            y_offset_speed = 2 if not self.actors['player'].is_stand_on_ground and abs(self.actors['player'].fall_speed) < 5 \
                               else abs(self.actors['player'].fall_speed)
            # y_offset_speed = abs(self.actors['player'].fall_speed)        # if self.actors['player'].speed > 0:

        if self.actors['player'].rectangle.bottom > self.camera.rectangle.bottom:
            y_offset_speed *= 2
        else:
            if self.actors['player'].rectangle.top < self.camera.rectangle.top:
                y_offset_speed *= 2

        self.camera.apply_offset((self.actors['player'].rectangle.centerx, self.actors['player'].rectangle.top),
                                 x_offset_speed, y_offset_speed)
                                 # self.actors['player'].speed * 0.9, self.actors['player'].fall_speed)

        self.detect_active_obstacles()

        self.render_all()

    def detect_active_obstacles(self):
        self.active_obstacles = list()
        for k in self.obstacles[self.location].keys():
            obs = self.obstacles[self.location][k]
            if obs.rectangle.colliderect(self.camera.active_objects_rectangle):
            # if obs.rectangle.colliderect(self.camera.rectangle):
                self.active_obstacles.append(k)

    # def detect_active_actors(self):
    #     self.active_actors = list()
    #     for k in self.obstacles[self.location].keys():
    #         obs = self.obstacles[self.location][k]
    #         if obs.rectangle.colliderect(self.camera.rectangle):
    #             self.active_obstacles.append(k

    def change_location(self, new_location):
        # print('Before location change:', self.actors.keys())
        self.location_has_been_changed = True
        self.location = new_location['new location']
        self.demolishers = dict()
        self.demolishers[self.location] = dict()

        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()
            self.actors[self.location][0] = self.actors['player']
        if new_location['xy'][0] == 'keep x':
            x = self.actors['player'].rectangle.x
        else:
            x = new_location['xy'][0]
        if new_location['xy'][1] == 'keep y':
            y = self.actors['player'].rectangle.y
        else:
            y = new_location['xy'][1]
        self.actors['player'].rectangle.centerx = x
        self.actors['player'].rectangle.y = y
        # self.actors['player'].rectangle.topleft = (x, y)
        # if self.actors['player'].get_state() in ('slide', 'sliding'):
        #     self.actors['player'].set_state('slide rise')
        self.load()
        self.detect_active_obstacles()


        # print('After location change:', self.actors.keys())

    # def processing_items(self):
    #     dead = list()
    #     for key in self.items[self.location]:
    #         i = self.items[self.location][key]
    #         if i.dead:
    #             dead.append(i.id)
    #             continue
    #         # if i.is_item:
    #         # Routines for item-like obstacles:
    #         if i.item_amount_decrease_speed != 0:
    #             if i.item_amount != i.item_amount_threshold:
    #                 # print('decrease amount', obs.item_amount)
    #                 i.item_amount += i.item_amount_decrease_speed


    def processing_obstacles(self):
        dead = list()
        for key in self.active_obstacles:
            obs = self.obstacles[self.location][key]
            if obs.dead:
                dead.append(obs.id)
                continue
            if obs.is_item:
                # Routines for item-like obstacles:
                if obs.item_amount_decrease_speed != 0:
                    if obs.item_amount != obs.item_amount_threshold:
                        # print('decrease amount', obs.item_amount)
                        obs.item_amount += obs.item_amount_decrease_speed
            if obs.teleport:
                if obs.trigger_activated:
                    # print('obs')
                    if obs.teleport_description['on touch']:
                        self.change_location(obs.teleport_description)
                        obs.trigger_activated = False
                        return
                    else:
                        if self.is_input_up_arrow:
                            self.change_location(obs.teleport_description)
                            obs.trigger_activated = False
                            return
                        else:
                            obs.trigger_activated = False
                            continue
            if obs.trigger:
                if obs.trigger_activated:
                    obs.trigger = False
                    if obs.is_item:
                        # print("ITEM GRABBED:", obs.item_name, all_items[obs.item_name])
                        if all_items[obs.item_name]['class'] == 'instant consume':
                            if all_items[obs.item_name]['type'] == 'stats gainer':
                                self.actors[self.location][0].stats[all_items[obs.item_name]['affects on']] += obs.item_amount
                                # self.actors[self.location][0].stats[all_items[obs.item_name]['affects on']] += all_items[obs.item_name]['amount']
                        else:
                            self.actors[self.location][0].add_items_to_inventory((all_items[obs.item_name],))
                            # self.actors[self.location][0].add_items_to_inventory((all_items[obs.item_name],))
                        dead.append(obs.id)
                        continue
                    else:
                        if obs.trigger_description['make active'] is not None:
                            for obstacle_to_be_activated in obs.trigger_description['make active']:
                                make_active_id = obstacle_to_be_activated[0]
                                if make_active_id not in self.obstacles[self.location].keys():
                                    continue
                                obs_loc = self.location if obstacle_to_be_activated[1] == 'self' else obstacle_to_be_activated[1]
                                if obs_loc not in self.obstacles.keys():
                                    self.obstacles_changes_pending[obs_loc] = dict()
                                    self.obstacles_changes_pending[obs_loc][make_active_id] = dict()
                                    self.obstacles_changes_pending[obs_loc][make_active_id]['activate actions set'] = obstacle_to_be_activated[2]
                                #     self.locations[obs_loc]['obstacles']['settings'][make_active_id]['active'] = True
                                    continue
                                activate_actions_set = obstacle_to_be_activated[2]

                                self.obstacles[obs_loc][make_active_id].active = True
                                self.obstacles[obs_loc][make_active_id].need_next_acton = True
                                self.obstacles[obs_loc][make_active_id].actions_set_number = activate_actions_set
                                self.obstacles[obs_loc][make_active_id].current_action = None
                                # self.obstacles[self.location][make_active_id].current_action = -1
                                # self.obstacles[self.location][make_active_id].process_()
                                # self.obstacles[self.location][make_active_id].next_action()

                    if obs.trigger_description['disappear']:
                        dead.append(obs.id)
                        continue
            obs.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location])
            obs.get_time(self.time_passed, self.game_cycles_counter)
            # if obs.id == 25:
            #     print('obs #25 world process')
            obs.process_()

        if dead:
            for dead_id in dead:
                del self.obstacles[self.location][dead_id]
            self.detect_active_obstacles()

    def make_explosion(self, xy):
        # print(f'[process demolishers] KA-BOOM!')
        for i in range(randint(40, 50)):
            demolisher_description = {

                'snap to actor': -1,
                'demolisher sprite': None,
                'demolisher TTL': randint(150, 170),
                'rect': pygame.Rect(xy[0], xy[1], 5, 5),
                'destination': find_destination_behind_target_point(xy, (randint(xy[0] - 100, xy[0] + 100), randint(xy[1] - 100, xy[1] + 100)), MAXX),
                'bounce': False,
                'bounce factor': 0,
                'flyer': True,
                'aftermath': '',
                'damage': 10,
                'static': False,
                'parent': '',
                'damage reduce': .01,
                'speed': 0.5 + randint(1, 5) / 10,
                'collides': True,
                'gravity affected': False
            }
            # dest = demolisher_description['destination']
            # print(f'[process demolishers] Adding frag #{i}: {dest=}')
            self.add_demolisher(demolisher_description)

    def processing_particles(self):
        dead = list()
        # explosions = list()
        for key in self.particles[self.location].keys():
            p = self.particles[self.location][key]
            if p.dead:
                # if p.aftermath == 'explode':
                #     # print(f'[process polishers] KA-BOOM!')
                #     explosions.append(p.rectangle.center)
                #     # self.make_explosion(p.rectangle.center)
                dead.append(p.id)
                continue
            if p.is_collideable:
                p.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None)
            # if p.static:
            #     if p.snap_to_actor not in self.actors[self.location].keys():
            #         dead.append(p.id)
            #         continue
            #     actor = self.actors[self.location][p.snap_to_actor]
            #     p.update(actor.look, actor.rectangle)

            p.get_time(self.time_passed, self.game_cycles_counter)
            p.process_particle()

        for dead_id in dead:
            del self.particles[self.location][dead_id]
        # for expl in explosions:
        #     self.make_explosion(expl)

    def processing_demolishers(self):
        dead = list()
        explosions = list()
        for key in self.demolishers[self.location].keys():
            dem = self.demolishers[self.location][key]
            if dem.dead:
                if dem.aftermath == 'explode':
                    # print(f'[process demolishers] KA-BOOM!')
                    explosions.append(dem.rectangle.center)
                    # self.make_explosion(dem.rectangle.center)
                dead.append(dem.id)
                continue
            if dem.is_collideable:
                dem.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None)
            if dem.static:
                if dem.snap_to_actor not in self.actors[self.location].keys():
                    dead.append(dem.id)
                    continue
                actor = self.actors[self.location][dem.snap_to_actor]
                dem.update(actor.look, actor.rectangle)

            dem.get_time(self.time_passed, self.game_cycles_counter)
            dem.process_demolisher()
            # dem.process_demolisher(self.time_passed)

        for dead_id in dead:
            del self.demolishers[self.location][dead_id]
        for expl in explosions:
            self.make_explosion(expl)

    def processing_player_actor(self):
        actor = self.actors['player']
        if actor.dead:
            self.game_over()

        actor.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location])

        if not actor.ignore_user_input:
            if self.is_input_up_arrow:
                actor.set_action('up action')
            else:
                # if actor.get_state() == 'up action':
                actor.set_action('up action cancel')

            if self.is_input_down_arrow:
                actor.set_action('down action')
            else:
                # if actor.get_state() == 'down action':
                actor.set_action('down action cancel')

            if self.is_input_right_arrow:
                actor.set_action('right action')
            else:
                # if actor.get_state() == 'right action':
                actor.set_action('right action cancel')

            if self.is_input_left_arrow:
                actor.set_action('left action')
            else:
                # if actor.get_state() == 'left action':
                actor.set_action('left action cancel')

            if self.is_jump_button:
                actor.set_action('jump action')
            else:
                actor.set_action('jump action cancel')

            if self.is_l_alt and not self.l_alt_multiple_press_prevent:
                self.l_alt_multiple_press_prevent = True
                actor.set_action('hop back')
            else:
                if actor.get_state() == 'hop back progress':
                    actor.set_action('hop back action cancel')

            if self.is_attack:
                self.is_attack = False
                actor.set_action('attack')

        actor.get_time(self.time_passed, self.game_cycles_counter)
        actor.process()

        if actor.summon_demolisher:
            actor.summon_demolisher = False
            self.add_demolisher(actor.summoned_demolisher_description)

    def processing_actors(self):
        dead = list()
        for key in self.actors[self.location].keys():
            # if key == 0:
            #     continue
            actor = self.actors[self.location][key]
            # print(actor.name)
            # if not actor.rectangle.colliderect(self.camera.active_objects_rectangle):
            #     continue

            if actor.dead:
                dead.append(actor.id)
                if all_hostiles[actor.name]['drop']:
                    # print(all_hostiles[actor.name]['drop'])
                    for drop in all_hostiles[actor.name]['drop']:
                        self.add_item(all_items[drop], (randint(actor.rectangle.left - 50, actor.rectangle.right + 50), actor.rectangle.top))
                continue

            actor.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location])

            # actor.get_target(self.actors['player'])
            # if not actor.ignore_user_input:
            #     actor.think()

            if actor.ai_controlled:
                actor.get_target(self.actors['player'])
                if not actor.ignore_user_input:
                    actor.think()
            else:
                if not actor.ignore_user_input:  # routines for Player actor
                # if key == 0 and not actor.ignore_user_input:  # routines for Player actor
                    if self.is_input_up_arrow:
                        actor.set_action('up action')
                    else:
                        # if actor.get_state() == 'up action':
                        actor.set_action('up action cancel')

                    if self.is_input_down_arrow:
                        actor.set_action('down action')
                    else:
                        # if actor.get_state() == 'down action':
                        actor.set_action('down action cancel')

                    if self.is_input_right_arrow:
                        actor.set_action('right action')
                    else:
                        # if actor.get_state() == 'right action':
                        actor.set_action('right action cancel')

                    if self.is_input_left_arrow:
                        actor.set_action('left action')
                    else:
                        # if actor.get_state() == 'left action':
                        actor.set_action('left action cancel')

                    if self.is_jump_button:
                        actor.set_action('jump action')
                    else:
                        actor.set_action('jump action cancel')

                    if self.is_l_alt and not self.l_alt_multiple_press_prevent:
                        self.l_alt_multiple_press_prevent = True
                        actor.set_action('hop back')
                    else:
                        if actor.get_state() == 'hop back progress':
                            actor.set_action('hop back action cancel')

                    if self.is_attack:
                        self.is_attack = False
                        actor.set_action('attack')

            actor.get_time(self.time_passed, self.game_cycles_counter)
            # actor.mask_update((self.camera.offset_x, self.camera.offset_y))
            actor.process()

            if actor.summon_demolisher:
                actor.summon_demolisher = False
                self.add_demolisher(actor.summoned_demolisher_description)

            if actor.summon_particle:
                actor.summon_particle = False
                for description in actor.summoned_particle_descriptions:
                    self.add_particle(description)
                actor.summoned_particle_descriptions = list()

        for dead_id in dead:
            del self.actors[self.location][dead_id]

    def render_background_(self):
        # pygame.draw.rect(self.screen, GRAY, (0,0,MAXX, MAXY))

        # self.screen.blit(self.backgrounds[self.location]['back layer 0']['image'], (0, 0))
        # print(self.camera.offset_x, self.camera.offset_y)

        for layer_key in self.backgrounds[self.location]['background layers'].keys():
            sub_surf = self.backgrounds[self.location]['background layers'][layer_key]['image'].subsurface(
                             (-self.camera.offset_x * self.backgrounds[self.location]['background layers'][layer_key]['offset x corrector'],
                              -self.camera.offset_y * self.backgrounds[self.location]['background layers'][layer_key]['offset y corrector'], MAXX, MAXY))
            self.screen.blit(sub_surf, (0, 0))

        # sub_surf = self.backgrounds[self.location]['ground level']['image'].subsurface(self.camera.offset_x, self.camera.offset_y, MAXX, MAXY)
        # self.screen.blit(sub_surf, (0,0))

        self.screen.blit(self.backgrounds[self.location]['ground level']['image'], (-self.camera.offset_x, -self.camera.offset_y))

    def render_background(self):
        if self.camera.max_x < MAXX or self.camera.max_y < MAXY:
            pygame.draw.rect(self.screen, BLACK, (0,0,MAXX, MAXY))

        # self.screen.blit(self.backgrounds[self.location]['back layer 0']['image'], (0, 0))
        # print(self.camera.offset_x, self.camera.offset_y)

        for layer_key in self.backgrounds[self.location]['background layers'].keys():
            self.screen.blit(self.backgrounds[self.location]['background layers'][layer_key]['image'],
                             (-self.camera.offset_x * self.backgrounds[self.location]['background layers'][layer_key]['offset x corrector'],
                              -self.camera.offset_y * self.backgrounds[self.location]['background layers'][layer_key]['offset y corrector']))

        self.screen.blit(self.backgrounds[self.location]['ground level']['image'], (-self.camera.offset_x, -self.camera.offset_y))

    def render_player_actor(self):
        actor = self.actors['player']
        size = actor.current_sprite['sprite'].get_size()
        # Offset sprite to the left from the center of rectangle using anchor point.
        if actor.current_sprite_flip:
            if actor.current_sprite['sprite asymmetric']:
                x = actor.rectangle.centerx - self.camera.offset_x \
                    - size[0] + actor.current_sprite['sprite center']
            else:
                x = actor.rectangle.centerx - self.camera.offset_x \
                    - actor.current_sprite['sprite center']
        else:
            x = actor.rectangle.centerx - self.camera.offset_x - actor.current_sprite['sprite center']

        y = actor.rectangle.bottom - self.camera.offset_y - size[1]

        self.screen.blit(actor.current_sprite['sprite'], (x, y))

        pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - self.camera.offset_y,
                                              actor.rectangle.width, actor.rectangle.height), 5)
        # Colliders rects:
        # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_right.x - self.camera.offset_x, actor.collision_detector_right.y - self.camera.offset_y,
        #                                       actor.collision_detector_right.width, actor.collision_detector_right.height))
        # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_left.x - self.camera.offset_x, actor.collision_detector_left.y - self.camera.offset_y,
        #                                       actor.collision_detector_left.width, actor.collision_detector_left.height))
        # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_top.x - self.camera.offset_x, actor.collision_detector_top.y - self.camera.offset_y,
        #                                       actor.collision_detector_top.width, actor.collision_detector_top.height))
        # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_bottom.x - self.camera.offset_x, actor.collision_detector_bottom.y - self.camera.offset_y,
        #                                       actor.collision_detector_bottom.width, actor.collision_detector_bottom.height))
        # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_right.x - self.camera.offset_x, actor.collision_detector_bottom_right.y - self.camera.offset_y,
        #                                       actor.collision_detector_bottom_right.width, actor.collision_detector_bottom_right.height))
        # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_left.x - self.camera.offset_x, actor.collision_detector_bottom_left.y - self.camera.offset_y,
        #                                       actor.collision_detector_bottom_left.width, actor.collision_detector_bottom_left.height))
        pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_right.x - self.camera.offset_x, actor.collision_grabber_right.y - self.camera.offset_y,
                                              actor.collision_grabber_right.width, actor.collision_grabber_right.height))
        pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_left.x - self.camera.offset_x, actor.collision_grabber_left.y - self.camera.offset_y,
                                              actor.collision_grabber_left.width, actor.collision_grabber_left.height))

        # The eye
        gaze_direction_mod = 0 if actor.look == -1 else actor.rectangle.width - 10
        pygame.draw.rect(self.screen, CYAN, (actor.rectangle.x + gaze_direction_mod - self.camera.offset_x, actor.rectangle.centery - 10 - self.camera.offset_y,
                                              10, 20))

    def render_actors(self):
        for key in self.actors[self.location].keys():
            actor = self.actors[self.location][key]
            if actor.invincibility_timer > 0:
                if self.game_cycles_counter // 2 == self.game_cycles_counter / 2:
                    continue
            size = actor.current_sprite['sprite'].get_size()
            # Offset sprite to the left from the center of rectangle using anchor point.
            if actor.current_sprite_flip:
                if actor.current_sprite['sprite asymmetric']:
                    x = actor.rectangle.centerx - self.camera.offset_x \
                        - size[0] + actor.current_sprite['sprite center']
                else:
                    x = actor.rectangle.centerx - self.camera.offset_x \
                        - actor.current_sprite['sprite center']
            else:
                x = actor.rectangle.centerx - self.camera.offset_x - actor.current_sprite['sprite center']

            y = actor.rectangle.bottom - self.camera.offset_y - size[1]

            # self.screen.blit(actor.current_sprite['mask'].to_surface(), (actor.current_sprite['current mask rect'].x - self.camera.offset_x,
            #                                                              actor.current_sprite['current mask rect'].y - self.camera.offset_y,))
            self.screen.blit(actor.current_sprite['sprite'], (x, y))


            # # Weak spot
            # if actor.current_sprite['weak spot']:
            #     # pygame.draw.circle(self.screen, YELLOW, (actor.rectangle.x + actor.current_sprite['weak spot'][0] - self.camera.offset_x,
            #     #                                       actor.rectangle.y + actor.current_sprite['weak spot'][1] - self.camera.offset_y),
            #     #                                       10)
            #     pygame.draw.rect(self.screen, YELLOW, actor.current_sprite['weak spot rect'])
            #     # pygame.draw.rect(self.screen, YELLOW, (actor.rectangle.x + actor.current_sprite['weak spot']['offset'][0] - self.camera.offset_x,
            #     #                                       actor.rectangle.y + actor.current_sprite['weak spot']['offset'][1] - self.camera.offset_y,
            #     #                                       actor.current_sprite['weak spot']['width'], actor.current_sprite['weak spot']['height']))


            # # Rectangle frame:
            # pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - self.camera.offset_y,
            #                                       actor.rectangle.width, actor.rectangle.height), 5)
            # # Colliders rects:
            # # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_right.x - self.camera.offset_x, actor.collision_detector_right.y - self.camera.offset_y,
            # #                                       actor.collision_detector_right.width, actor.collision_detector_right.height))
            # # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_left.x - self.camera.offset_x, actor.collision_detector_left.y - self.camera.offset_y,
            # #                                       actor.collision_detector_left.width, actor.collision_detector_left.height))
            # # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_top.x - self.camera.offset_x, actor.collision_detector_top.y - self.camera.offset_y,
            # #                                       actor.collision_detector_top.width, actor.collision_detector_top.height))
            # # pygame.draw.rect(self.screen, DARK_ORANGE, (actor.collision_detector_bottom.x - self.camera.offset_x, actor.collision_detector_bottom.y - self.camera.offset_y,
            # #                                       actor.collision_detector_bottom.width, actor.collision_detector_bottom.height))
            # # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_right.x - self.camera.offset_x, actor.collision_detector_bottom_right.y - self.camera.offset_y,
            # #                                       actor.collision_detector_bottom_right.width, actor.collision_detector_bottom_right.height))
            # # pygame.draw.rect(self.screen, MAGENTA, (actor.collision_detector_bottom_left.x - self.camera.offset_x, actor.collision_detector_bottom_left.y - self.camera.offset_y,
            # #                                       actor.collision_detector_bottom_left.width, actor.collision_detector_bottom_left.height))
            # pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_right.x - self.camera.offset_x, actor.collision_grabber_right.y - self.camera.offset_y,
            #                                       actor.collision_grabber_right.width, actor.collision_grabber_right.height))
            # pygame.draw.rect(self.screen, CYAN, (actor.collision_grabber_left.x - self.camera.offset_x, actor.collision_grabber_left.y - self.camera.offset_y,
            #                                       actor.collision_grabber_left.width, actor.collision_grabber_left.height))
            #
            # # The eye
            # gaze_direction_mod = 0 if actor.look == -1 else actor.rectangle.width - 10
            # pygame.draw.rect(self.screen, CYAN, (actor.rectangle.x + gaze_direction_mod - self.camera.offset_x, actor.rectangle.centery - 10 - self.camera.offset_y,
            #                                       10, 20))
            # Enemies Health bar.
            if actor.id != 0:
                pygame.draw.rect(self.screen, WHITE, (actor.rectangle.x - self.camera.offset_x - 2, actor.rectangle.y - 12 - self.camera.offset_y,
                                                     actor.rectangle.width + 4, 7), 1)
                pygame.draw.rect(self.screen, RED, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - 10 - self.camera.offset_y,
                                                     actor.stats['health'] * actor.rectangle.width // actor.stats['max health'], 3))


    def render_demolishers(self):
        for key in self.demolishers[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            dem = self.demolishers[self.location][key]
            # color = (max(0, 255 - dem.ttl*4), 10,0) if dem.ttl < 50 else PINK
            # pygame.draw.rect(self.screen, color, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
            #                                       dem.rectangle.width, dem.rectangle.height))

            # self.screen.blit(fonts.all_fonts[20].render(str(dem.id) + ' ' + str(dem.speed) + ' ' + str(dem.rectangle.y), True, CYAN),
            #                  (dem.rectangle.x - self.camera.offset_x, dem.rectangle.bottom - self.camera.offset_y + dem.id * 20))

            # if dem.current_sprite:
            #     if dem.look == 1:
            #         self.screen.blit(dem.current_sprite['sprite'], (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y))
            #     else:
            #         self.screen.blit(pygame.transform.flip(dem.current_sprite['sprite'], True, False), (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y))
            # else:
            #     color = (max(0, 255 - dem.ttl*4), 10,0) if dem.ttl < 50 else PINK
            #     pygame.draw.rect(self.screen, color, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
            #                                           dem.rectangle.width, dem.rectangle.height))
            if dem.look == 1:
                self.screen.blit(dem.current_sprite['sprite'], (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y))
            else:
                self.screen.blit(pygame.transform.flip(dem.current_sprite['sprite'], True, False), (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y))
    
    def render_particles(self):
        for key in self.particles[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            p = self.particles[self.location][key]
            # color = (max(0, 255 - p.ttl*4), 10,0) if p.ttl < 50 else PINK
            if p.subtype == 'splatter':
                pygame.draw.circle(self.screen, p.color, (p.rectangle.centerx - self.camera.offset_x, p.rectangle.centery - self.camera.offset_y), p.rectangle.width)
            else:
                pygame.draw.rect(self.screen, p.color, (p.rectangle.x - self.camera.offset_x, p.rectangle.y - self.camera.offset_y,
                                                        p.rectangle.width, p.rectangle.height))

            # self.screen.blit(fonts.all_fonts[20].render(str(p.id) + ' ' + str(p.speed) + ' ' + str(p.rectangle.y), True, CYAN),
            #                  (p.rectangle.x - self.camera.offset_x, p.rectangle.bottom - self.camera.offset_y + p.id * 20))

            # if p.current_sprite:
            #     if p.look == 1:
            #         self.screen.blit(p.current_sprite['sprite'], (p.rectangle.x - self.camera.offset_x, p.rectangle.y - self.camera.offset_y))
            #     else:
            #         self.screen.blit(pygame.transform.flip(p.current_sprite['sprite'], True, False), (p.rectangle.x - self.camera.offset_x, p.rectangle.y - self.camera.offset_y))
            # else:
            #     color = (max(0, 255 - p.ttl*4), 10,0) if p.ttl < 50 else PINK
            #     pygame.draw.rect(self.screen, color, (p.rectangle.x - self.camera.offset_x, p.rectangle.y - self.camera.offset_y,
            #                                           p.rectangle.width, p.rectangle.height))
            # self.screen.blit(p.current_sprite['sprite'], (p.rectangle.x - self.camera.offset_x, p.rectangle.y - self.camera.offset_y))

    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            if key not in self.active_obstacles:
                continue
            obs = self.obstacles[self.location][key]
            if obs.teleport:
                if not obs.teleport_description['on touch']:
                    if obs.trigger_activated:
                        pygame.draw.rect(self.screen, CYAN, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                              obs.rectangle.width, obs.rectangle.height), 1)

            if not obs.is_force_render:
                continue
            if obs.sprite:
                self.screen.blit(sprites[obs.sprite]['sprite'], (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))
                continue
            # if obs.invisible:
            #     continue
            color = YELLOW if obs.is_ghost_platform else CYAN
            pygame.draw.rect(self.screen, color, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                  obs.rectangle.width, obs.rectangle.height))
            if obs.active:
                dx = 10
                stats_y = 1
                gap = 1
                font_size = 10
                params = (
                    ('ID: ' + str(obs.id), RED),
                    ('ACTV: ' + str(obs.active), RED),
                    ('TRGGRED: ' + str(obs.trigger_activated), RED),
                    ('WAIT COUNTER    : ' + str(obs.wait_counter), RED),
                    ('DEST REACHED    : ' + str(obs.is_destination_reached), RED),
                    ('RECTANGLE       : ' + str(obs.rectangle), RED),
                    ('ACTION          : ' + str(obs.actions[obs.actions_set_number][obs.current_action]), RED) if obs.current_action else ('', RED),
                    ('NEED NEXT ACTION: ' + str(obs.need_next_action), RED),
                    ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), RED),
                    ('DESTINATION AREA: ' + str(obs.destination_area), RED),
                    ('DESTINATION PNT : ' + str(obs.destination_point), RED),
                    ('DESTINATION     : ' + str(obs.destination), RED),
                    ('GRAVITY         : ' + str(obs.is_gravity_affected), RED),
                    # 'CR',
                )
                for p in params:
                    if p == 'CR':
                        dx += 300
                        gap = 1
                        continue
                    self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], WHITE),
                                     (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
                    gap += font_size
                # pygame.draw.rect(self.screen, MAGENTA, (obs.destination_area.x - self.camera.offset_x, obs.destination_area.y - self.camera.offset_y,
                #                                       obs.destination_area.width, obs.destination_area.height))

            else:
                dx = 10
                stats_y = 1
                gap = 1
                font_size = 10
                params = (
                    ('ID: ' + str(obs.id), BLACK),
                    ('TRGGR: ' + str(obs.trigger_activated), YELLOW),
                    # ('GRAVITY         : ' + str(obs.is_gravity_affected), RED),
                    # ('IN GROUND       : ' + str(obs.is_stand_on_ground), RED),
                    # ('EDGE GRABBED    : ' + str(obs.is_edge_grabbed), RED),
                    # ('WAIT COUNTER    : ' + str(obs.wait_counter), BLACK),
                    # ('IDLE            : ' + str(obs.idle), BLACK),
                )
                for p in params:
                    if p == 'CR':
                        dx += 300
                        gap = 1
                        continue
                    self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1]),
                                     (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
                    gap += font_size


    def render_all(self):
        self.render_background()
        self.render_obstacles()
        self.render_demolishers()
        self.render_actors()
        self.render_particles()
        # self.render_player_actor()
        # self.render_debug_info()
        self.render_info_panel_overlay()

    def render_info_panel_overlay(self):
        # Player stats:
        # start_x = 50
        # start_y = 50
        # # start_y = MAXY - 100
        # max_stripes_width = 500
        # gap_between_stripes = 10
        # font_size = 12
        # info_panel_gap_between_stripes = self.info_panel_gap_between_stripes
        dy = 0
        params = (
            ('HEALTH :' + str(int(self.actors['player'].stats['max health'])) + '/' + str(int(self.actors['player'].stats['health'])),int(self.actors['player'].stats['health'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max health']),
             MAGENTA),
            ('STAMINA:' + str(int(self.actors['player'].stats['max stamina'])) + '/' + str(int(self.actors['player'].stats['stamina'])),int(self.actors['player'].stats['stamina'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max stamina']),
             YELLOW if self.actors['player'].stats['stamina'] >= self.actors['player'].current_stamina_lost_per_attack else RED),
            ('MANA   :' + str(int(self.actors['player'].stats['max mana'])) + '/' + str(int(self.actors['player'].stats['mana'])),int(self.actors['player'].stats['mana'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max mana']), BLUE),
            ('EXP:' + str(int(self.actors['player'].stats['exp'])), 0, VIOLET),
            # ('HEALTH:' + str(int(self.actors['player'].max_health)) + '/' + str(int(self.actors['player'].health)),int(self.actors['player'].health * max_stripes_width // self.actors['player'].max_health), RED),

        )

        # txt = fonts.all_fonts[self.info_panel_font_size].render(params[0][0], True, params[0][2])
        # txt_shadow = fonts.all_fonts[self.info_panel_font_size].render(params[0][0], True, BLACK)
        # txt_width = txt.get_width() + 50
        txt_width = 250

        background_width = self.info_panel_max_stripes_width + 10 + txt_width
        background_height = len(params) * self.info_panel_font_size + 5 + (self.info_panel_gap_between_stripes * len(params))

        pygame.draw.rect(self.screen, BLACK, (self.info_panel_start_x - 5, self.info_panel_start_y - 5, background_width, background_height))
        self.screen.blit(sprites[self.actors['player'].current_weapon['sprite']]['sprite'], (self.info_panel_start_x, self.info_panel_start_y))
        for p in params:
            txt = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, p[2])
            txt_shadow = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, GRAY)
            self.screen.blit(txt_shadow, (self.info_panel_start_x + 2, self.info_panel_start_y + dy + 2))  # TEXT SHADOW
            # self.screen.blit(txt, (self.info_panel_start_x + 1, self.info_panel_start_y + dy + 1), None, BLEND_RGB_MIN)  # TEXT SHADOW
            self.screen.blit(txt, (self.info_panel_start_x, self.info_panel_start_y + dy))
            if p[1] > 0:
                pygame.draw.rect(self.screen, p[2], (self.info_panel_start_x + txt_width ,self.info_panel_start_y + dy, p[1],10))
            dy += (self.info_panel_font_size + self.info_panel_gap_between_stripes)

    def load(self):
        if self.location not in self.locations.keys():
            self.locations[self.location] = dict()
            self.obstacles[self.location] = dict()
            self.demolishers[self.location] = dict()
            self.particles[self.location] = dict()
            # self.actors[self.location] = dict()
            # print(f'{self.location=}')
            # print(self.locations)
            # print(locations)
            self.locations[self.location] = locations[self.location]
            for obs_rect in self.locations[self.location]['obstacles']['obs rectangles']:
                if obs_rect[-1] in self.locations[self.location]['obstacles']['settings'].keys() and 'item' in self.locations[self.location]['obstacles']['settings'][obs_rect[-1]].keys():
                    if self.locations[self.location]['obstacles']['settings'][obs_rect[-1]]['item']:
                        # Add item, not obstacle
                        self.add_item(all_items[self.locations[self.location]['obstacles']['settings'][obs_rect[-1]]['item name']['name']],
                                      obs_rect[0])
                        continue
                # Add obstacle.
                self.add_obstacle(obs_rect)
            # Apply changes to active obstacles if such action has been pended:
            if self.location in self.obstacles_changes_pending.keys():
                for k in self.obstacles_changes_pending[self.location].keys():
                    print(f'[load] pending actions for obs # {k}')
                    obs_to_be_changed = self.obstacles[self.location][k]
                    obs_to_be_changed.active = True
                    obs_to_be_changed.need_next_acton = True
                    obs_to_be_changed.actions_set_number = self.obstacles_changes_pending[self.location][k]['activate actions set']
                    obs_to_be_changed.current_action = None
                del self.obstacles_changes_pending[self.location]
            for dem in self.locations[self.location]['demolishers']['dem rectangles']:
                self.add_demolisher(dem)

            for enemy_xy in self.locations[self.location]['hostiles'].keys():
                enemy_description = self.locations[self.location]['hostiles'][enemy_xy]
                enemy_name = self.locations[self.location]['hostiles'][enemy_xy]['name']
                enemy_to_add = copy(all_hostiles[enemy_name])  # Create a copy of enemy
                for k in enemy_description.keys():
                    if k == 'name':
                        continue
                    if k in enemy_to_add.keys():
                        enemy_to_add[k] = enemy_description[k]
                self.add_actor(enemy_to_add, enemy_xy)

        self.camera.setup(self.locations[self.location]['size'][0], self.locations[self.location]['size'][1])
        self.camera.apply_offset((self.actors['player'].rectangle.centerx, self.actors['player'].rectangle.top),
                                 0, 0, True)

        if self.location not in self.backgrounds.keys():
            self.backgrounds[self.location] = dict()
            # layers_out = False
            layer_number = 0
            self.backgrounds[self.location]['background layers'] = dict()
            while True:
                self.backgrounds[self.location]['background layers'][layer_number] = dict()
                try:
                    self.backgrounds[self.location]['background layers'][layer_number]['image'] = pygame.image.load('img/backgrounds/' + self.location + '_back_' + str(layer_number)+'.png').convert()
                except FileNotFoundError:
                    del self.backgrounds[self.location]['background layers'][layer_number]
                    break
                # self.backgrounds[self.location]['back level 1']['whole image'] = pygame.image.load('img/backgrounds/' + self.location + '_back_1.png')
                self.backgrounds[self.location]['background layers'][layer_number]['size'] = self.backgrounds[self.location]['background layers'][layer_number]['image'].get_size()
                self.backgrounds[self.location]['background layers'][layer_number]['offset x corrector'] = \
                    0.01 * (100 * (self.backgrounds[self.location]['background layers'][layer_number]['size'][0] - MAXX) / self.camera.max_offset_x) if self.camera.max_offset_x > 0 else 1
                self.backgrounds[self.location]['background layers'][layer_number]['offset y corrector'] = \
                    0.01 * (100 * (self.backgrounds[self.location]['background layers'][layer_number]['size'][1] - MAXY) / self.camera.max_offset_y) if self.camera.max_offset_y > 0 else 1
                # self.backgrounds[self.location]['back level 1']['offset x corrector'] = (100 - MAXX * 100 / self.backgrounds[self.location]['back level 1']['size'][0]) * 0.01
                # self.backgrounds[self.location]['back level 1']['offset y corrector'] = (100 - MAXY * 100 / self.backgrounds[self.location]['back level 1']['size'][1]) * 0.01
                # self.backgrounds[self.location]['back level 1']['offset x corrector'] = self.backgrounds[self.location]['back level 1']['size'][0] / self.camera.max_x
                # self.backgrounds[self.location]['back level 1']['offset y corrector'] = self.backgrounds[self.location]['back level 1']['size'][1] / self.camera.max_y
                # print('BACK OFFSETS of layer #', layer_number)
                # print(self.backgrounds[self.location]['background layers'][layer_number]['offset x corrector'])
                # print(self.backgrounds[self.location]['background layers'][layer_number]['offset y corrector'])
                layer_number += 1
            # print(self.backgrounds[self.location])

            self.backgrounds[self.location]['ground level'] = dict()
            self.backgrounds[self.location]['ground level']['image'] = pygame.image.load('img/backgrounds/' + self.location + '_ground.png').convert()
            self.backgrounds[self.location]['ground level']['bounding rect'] = self.backgrounds[self.location]['ground level']['image'].get_bounding_rect()
            # self.backgrounds[self.location]['ground level']['cropped image'] = self.backgrounds[self.location]['ground level']['whole image'].subsurface(self.backgrounds[self.location]['ground level']['bounding rect'])

        self.max_obs_id_in_current_location = max(self.obstacles[self.location].keys()) + 1

    def processing_human_input(self):
        # self.mouse_xy = pygame.mouse.get_pos()
        # self.mouse_xy_absolute = pygame.mouse.get_pos()
        # self.mouse_xy_index = self.define_index_for_point(self.mouse_xy)
        # if self.mode == 'wandering':
        #     self.mouse_xy = (self.mouse_xy[0] + self.offset_x) // self.wandering_screen_scale, \
        #                     (self.mouse_xy[1] + self.offset_y) // self.wandering_screen_scale

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit()
            mods = pygame.key.get_mods()
            if mods & KMOD_LSHIFT:  # use whatever KMOD_ constant you want;)
                self.is_l_shift = True
            elif mods & KMOD_LCTRL:
                self.is_l_ctrl = True
            elif mods & KMOD_LALT:
                self.is_l_alt = True
            else:
                self.l_alt_multiple_press_prevent = False
                self.is_l_ctrl = False
                self.is_l_shift = False
                self.is_l_alt = False
            # print(self.l_shift)
            if event.type == KEYUP:
                self.is_key_pressed = False
                if event.key == K_d:
                    self.is_input_right_arrow = False
                if event.key == K_a:
                    self.is_input_left_arrow = False
                if event.key == K_w:
                    self.is_input_up_arrow = False
                if event.key == K_s:
                    self.is_input_down_arrow = False
                if event.key == K_UP:
                # if event.key == K_SPACE:
                    self.is_jump_button = False
                    self.jump_button_multiple_press_prevent = False
                # if event.key == K_RIGHT:
                #     self.is_attack = False
            if event.type == KEYDOWN:
                self.is_key_pressed = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    raise SystemExit()
                if event.key == K_RIGHT:
                    self.is_attack = True
                if event.key == K_TAB:
                    lst = list(self.actors['player'].inventory['weapons'].keys())
                    indx =  lst.index(self.actors['player'].current_weapon['label'])
                    if indx + 1 > len(lst) - 1:
                        self.actors['player'].activate_weapon(0)
                    else:
                        self.actors['player'].activate_weapon(lst[indx+1])
                if event.key == K_d:
                    self.is_input_right_arrow = True
                if event.key == K_a:
                    self.is_input_left_arrow = True
                if event.key == K_w:
                    self.is_input_up_arrow = True
                if event.key == K_s:
                    self.is_input_down_arrow = True
                if event.key == K_UP:
                # if event.key == K_SPACE:
                    if not self.jump_button_multiple_press_prevent:
                        self.is_jump_button = True
                    # self.is_attack_button = True
                # if event.key == K_F5:
                #     self.need_quick_save = True
                # elif event.key == K_F8:
                #     self.need_quick_load = True
                #     # quick_save(self, self.locations)
                # elif event.key == K_F3:
                #     self.music_on = False if self.music_on else True
                #     if not self.music_on:
                #         pygame.mixer.music.fadeout(2000)
                elif event.key == K_z:
                    # Cool stuff with if-then-else expression compress:
                    self.is_z = False if self.is_z else True
                elif event.key == K_x:
                    # self.change_mode()
                    self.is_x = False if self.is_x else True
                    # self.screen_follows_actor = False if self.screen_follows_actor else True
                # elif event.key == K_b:
                #     # self.change_mode()
                #     self.b = False if self.b else True
                # elif event.key == K_f:
                #     self.follow_mode = False if self.follow_mode else True
                # elif event.key == K_l:
                #     # self.change_mode()
                #     self.locations[self.location]['lights on'] = False if self.locations[self.location]['lights on'] else True
                # elif event.key == K_l:
                #     # self.change_mode()
                #     self.lights_on = False if self.lights_on else True
                # elif event.key == K_m:
                #     self.need_to_show_minimap = False if self.need_to_show_minimap else True
                elif event.key == K_n:
                    enemy_to_add = copy(all_hostiles['demon 2'])  # Create a copy of enemy
                    self.add_actor(enemy_to_add, (MAXX_DIV_2 + self.camera.offset_x, MAXY_DIV_2 + self.camera.offset_y))
                    # self.change_mode()
                    # self.is_n = False if self.is_n else True
                    # msg = 'NEW EMPTY MESSAGE FOR TEST PURPOSES.'
                    # self.info_windows[0].get_bunch_of_new_messages((msg, msg))
                    # self.add_info_window(self.calculate_info_string_xy(), [msg, ], 300, False)

                elif event.key == K_p:
                    # Cool stuff with if-then-else expression compress:
                    self.is_p = False if self.is_p else True
                elif event.key == K_i:
                    # Cool stuff with if-then-else expression compress:
                    self.is_i = False if self.is_i else True
                # elif event.key == K_SPACE:
                #     self.change_player_actors()
                # elif event.key == K_e:
                # # elif event.key == K_KP_ENTER:
                #     # elif event.key == K_SPACE:
                #     # self.input_confirm = True
                #     self.wandering_actor.end_turn()
                #     self.player_turn = False
                # elif event.key == K_c:
                #     self.skip_actor()
                # elif event.key == K_TAB:
                #     self.need_to_show_party_inventory = True if not self.need_to_show_party_inventory else False
            if event.type == MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    self.is_mouse_button_down = True
                    self.is_left_mouse_button_down = True
                if buttons[2]:
                    self.is_mouse_button_down = True
                    self.is_right_mouse_button_down = True
            elif event.type == MOUSEWHEEL:
                # print(event)
                # print(event.x, event.y)
                # print(event.flipped)
                # print(event.which)
                self.is_mouse_wheel_rolls = True
                if event.y == 1:
                    # Mouse wheel up:
                    self.is_mouse_wheel_up = True
                    # self.wandering_screen_target_scale += self.wandering_scale_amount
                elif event.y == -1:
                    # Mouse wheel down:
                    self.is_mouse_wheel_down = True
            if event.type == MOUSEBUTTONUP:
                self.is_mouse_button_down = False
                if self.is_right_mouse_button_down:
                    self.is_right_mouse_button_down = False
                if self.is_left_mouse_button_down:
                    self.is_left_mouse_button_down = False

    def render_debug_info(self):
        stats_x = 1
        stats_y = 1
        # stripes_width = 500
        gap = 1
        font_size = 12
        # m_hover_item = 'None' if not self.mouse_hovers_item else self.items[self.mouse_hovers_item].name
        # m_hover_actor = 'None' if not self.mouse_hovers_actor else self.wandering_actors[self.mouse_hovers_actor].name + ' ' + str(self.wandering_actors[self.mouse_hovers_actor].id)
        # m_hover_cell = 'None' if self.point_mouse_cursor_shows is None else str(self.locations[self.location]['points'][self.point_mouse_cursor_shows]['rect'].center)
        params = (
            #
            ('LOCATION: ' + str(self.location), GREEN),
            ('SCREEN OFFSETS: ' + str(self.camera.offset_x) + ' ' + str(self.camera.offset_y), GREEN),
            ('', WHITE),
            (' RECT: ' + str(self.actors['player'].rectangle), WHITE),
            ('╔ TARGET HEIGHT ╗: ' + str(self.actors['player'].target_height), YELLOW),
            ('╚ TARGET WIDTH  ╝: ' + str(self.actors['player'].target_width), YELLOW),
            (' FALL SPEED: ' + str(self.actors['player'].fall_speed), WHITE),
            (' SPEED: ' + str(self.actors['player'].speed), WHITE),
            (' LOOK: ' + str(self.actors['player'].look), WHITE),
            (' HEADING: ' + str(self.actors['player'].heading), WHITE),
            (' IDLE COUNT: ' + str(self.actors['player'].idle_counter), (200, 100, 50)),
            (' ACTIVE FRAMES: ' + str(self.actors['player'].active_frames), (200, 100, 50)),
            (' JUMP ATTEMPTS : ' + str(self.actors['player'].jump_attempts_counter), YELLOW),
            (' JUST JUMPED   : ' + str(self.actors['player'].just_got_jumped), YELLOW),
            (' JUMP PERFORMED: ' + str(self.actors['player'].is_jump_performed), YELLOW),
            (' IGNORES INPUT: ' + str(self.actors['player'].ignore_user_input), WHITE),
            (' __STATE: ' + str(self.actors['player'].get_state()), CYAN),
            (' STAND ON GROUND: ' + str(self.actors['player'].is_stand_on_ground), WHITE),
            ('HEIGHT SPACE: ' + str(self.actors['player'].is_enough_height), GREEN),
            (' ABOVE SPACE: ' + str(self.actors['player'].is_enough_space_above), GREEN),
            (' BELOW SPACE: ' + str(self.actors['player'].is_enough_space_below), GREEN),
            (' RIGHT SPACE: ' + str(self.actors['player'].is_enough_space_right), GREEN),
            (' LEFT SPACE: ' + str(self.actors['player'].is_enough_space_left), GREEN),
            (' IS GRABBING: ' + str(self.actors['player'].is_edge_grabbed), WHITE),
            (' INFLUENCED BY PLATFORM #: ' + str(self.actors['player'].influenced_by_obstacle), WHITE),
            (' WEAPON: ' + str(self.actors['player'].current_weapon['label']) + ' | ALL WEAPONS: ' + str(self.actors['player'].inventory['weapons'].keys()), PINK),
            ('', WHITE),
            (' ACTORS: ' + str(self.actors[self.location].keys()), WHITE),
            # (str([str(self.demolishers[self.location][k].id) + str(self.demolishers[self.location][k].rectangle.topleft) for k in self.demolishers[self.location].keys()]),GRAY),
        )
        for p in params:
            self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], BLACK), (stats_x, stats_y + gap))
            gap += font_size

    # def processing_collisions(self, checking_unit):
    #     # checking_unit.is_enough_space_left = True
    #     # checking_unit.is_enough_space_right = True
    #     checking_unit.is_enough_space_above = True
    #     checking_unit.is_enough_space_below = True
    #     checking_unit.is_stand_on_ground = False
    #     # checking_unit.is_edge_grabbed = False
    #
    #     for key in self.obstacles[self.location].keys():
    #         obs = self.obstacles[self.location][key]
    #
    #         # # Check enough spaces right and left:
    #         # if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.rectangle.width - checking_unit.speed - 2, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
    #         #     checking_unit.is_enough_space_left = False
    #         # if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.rectangle.width + checking_unit.speed + 2, checking_unit.rectangle.height - 35):
    #         #     checking_unit.is_enough_space_right = False
    #
    #         if checking_unit.fall_speed < 0:
    #             # CHECK TOP
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.top - abs(checking_unit.fall_speed),
    #                                          checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed)):
    #                 checking_unit.rectangle.top = obs.rectangle.bottom
    #                 checking_unit.is_enough_space_above = False
    #                 checking_unit.fall_speed = 0
    #                 checking_unit.is_stand_on_ground = False
    #                 continue
    #         else:
    #             # CHECK BOTTOM
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left + 2, checking_unit.rectangle.bottom,
    #                                          checking_unit.rectangle.width - 4, abs(checking_unit.fall_speed) + 1):
    #                 checking_unit.rectangle.bottom = obs.rectangle.top
    #                 checking_unit.is_stand_on_ground = True
    #                 checking_unit.fall_speed = 0
    #                 checking_unit.is_enough_space_below = False
    #                 checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                 self.is_attack_button = False
    #                 continue
    #
    #         # CHECK LEFT
    #         if checking_unit.look == -1:
    #             if obs.rectangle.colliderect(checking_unit.rectangle.left - checking_unit.speed - 10, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
    #                     # Grab over the top of an obstacle.
    #                     if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
    #                     # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
    #                         checking_unit.is_edge_grabbed = True
    #                         checking_unit.rectangle.top = obs.rectangle.top
    #                         checking_unit.fall_speed = 0
    #                         checking_unit.is_stand_on_ground = True
    #                         checking_unit.rectangle.left = obs.rectangle.right  # - 2
    #                         checking_unit.is_enough_space_left = False
    #                         checking_unit.heading[0] = 0
    #                         checking_unit.speed = 0
    #                         checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                         return
    #
    #                     # # Bounce from the wall
    #                     # if self.is_attack_button and self.is_input_left_arrow:
    #                     # # if self.is_attack_button and checking_unit.speed > 0:
    #                     #     checking_unit.look = 1
    #                     #     checking_unit.jump_attempts_counter = 1
    #                     #     checking_unit.rectangle.left = obs.rectangle.right  # - 2
    #                     #     checking_unit.is_jump = True
    #                     #     if checking_unit.speed > 0:
    #                     #         checking_unit.speed *= .8
    #                     #     else:
    #                     #         checking_unit.speed = checking_unit.max_speed * 0.7
    #                     #
    #                     #     # checking_unit.speed *= .8
    #                     #     return
    #
    #                     checking_unit.rectangle.left = obs.rectangle.right
    #                     checking_unit.is_enough_space_left = False
    #                     checking_unit.heading[0] = 0
    #                     checking_unit.speed = 0
    #                     continue
    #
    #         # CHECK RIGHT
    #         if checking_unit.look == 1:
    #             if obs.rectangle.colliderect(checking_unit.rectangle.right, checking_unit.rectangle.top, checking_unit.speed + 10, checking_unit.rectangle.height - 35):
    #                 # Grab over the top of an obstacle.
    #                 if obs.rectangle.top >= checking_unit.rectangle.top > (obs.rectangle.top - 30) and checking_unit.fall_speed > 0:
    #                 # if checking_unit.rectangle.top <= obs.rectangle.top and checking_unit.fall_speed > 0:
    #                     checking_unit.is_edge_grabbed = True
    #                     checking_unit.rectangle.top = obs.rectangle.top
    #                     checking_unit.fall_speed = 0
    #                     checking_unit.is_stand_on_ground = True
    #                     checking_unit.rectangle.right = obs.rectangle.left  # - 2
    #                     checking_unit.is_enough_space_right = False
    #                     checking_unit.heading[0] = 0
    #                     checking_unit.speed = 0
    #                     checking_unit.jump_attempts_counter = checking_unit.max_jump_attempts
    #                     return
    #
    #                 # # Bounce from the wall
    #                 # if self.is_attack_button and self.is_input_right_arrow:
    #                 #     # if self.is_attack_button and checking_unit.speed > 0:
    #                 #     checking_unit.look = -1
    #                 #     checking_unit.jump_attempts_counter = 1
    #                 #     checking_unit.is_jump = True
    #                 #     if checking_unit.speed > 0:
    #                 #         checking_unit.speed *= .8
    #                 #     else:
    #                 #         checking_unit.speed = checking_unit.max_speed * 0.7
    #                 #     checking_unit.rectangle.right = obs.rectangle.left  # - 2
    #                 #     return
    #
    #                 checking_unit.rectangle.right = obs.rectangle.left
    #                 checking_unit.is_enough_space_right = False
    #                 checking_unit.heading[0] = 0
    #                 checking_unit.speed = 0
    #                 continue

    @staticmethod
    def press_any_key():
        command = None
        while command is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit()
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    command = 'key pressed'

    @staticmethod
    def press_any_key_passed():
        # command = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                # command = 'key pressed'
                # print('ok')
                return True
            # else:
            #     return False

    def game_over(self):
        print("--== G A M E   O V E R ==--")
        # self.info_windows[0].get_new_message('All survivors have died.')
        # self.info_windows[0].get_new_message("--== G A M E   O V E R ==--")
        # from misc_tools import render_text
        black_out(self.screen, self.screen, 10)
        render_text('GAME OVER', self.screen, 150, RED, 'AlbionicRegular.ttf', ('center_x', 'center_y'))
        pygame.display.flip()
        self.press_any_key()
        pygame.quit()
        exit()