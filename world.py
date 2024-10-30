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
        self.protectors = dict()
        self.protector_id: int = 0
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
        self.player_actor_hand_to_change_weapon = 'right hand'

        # CONTROLS
        self.is_key_pressed = False
        self.is_attack = False
        self.attack_time = 0
        self.is_alternate_attack = False
        self.alternate_attack_time = 0
        self.is_input_up_arrow = False
        self.is_input_down_arrow = False
        self.is_input_right_arrow = False
        self.is_input_left_arrow = False
        self.is_input_confirm = False
        self.is_input_cancel = False
        self.is_z = False
        self.is_q = False
        self.q_multiple_press_prevent = False
        self.is_e = False
        self.e_multiple_press_prevent = False
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
        self.player_is_dead_counter_to_game_over = 0  # Count this down to reach zero and show game over screen
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
        print(f'[ADDING ACTOR] ----------------------------------------------------------')
        entity = Actor()
        entity.id = self.actor_id
        entity.name = description['name']
        for resistance in description['resistances'].keys():
            entity.resistances[resistance] = description['resistances'][resistance]
        # entity.resistances = description['resistances']
        entity.disappear_after_death = description['disappear after death']
        entity.blood_color = description['blood color']

        entity.strength = description['strength']
        entity.body_weight = description['body weight']
        entity.base_max_speed = description['max speed']
        print(f'[ADDING ACTOR] {entity.base_max_speed=} {entity.body_weight=} {entity.strength=}')
        entity.base_max_jump_height = description['max jump height']
        # entity.calculate_athletics_index()
        # entity.calculate_max_jump_height_and_speed()

        entity.stats['max health'] = description['health']
        entity.stats['health'] = description['health']
        entity.stats['target health'] = description['health']
        # entity.stamina_replenish_modifier = description['stamina replenish']
        entity.default_normal_stamina_replenish = description['stamina replenish']
        entity.normal_stamina_replenish = description['stamina replenish']
        # entity.mana_replenish_modifier = description['mana replenish']
        entity.default_normal_mana_replenish = description['mana replenish']
        entity.normal_mana_replenish = description['mana replenish']
        # entity.health = description['health']
        # print(f'[add_actor] --------------------------------------------------------------')
        # print(f'[add_actor] Adding {entity.name}, id={entity.id}, {entity.stats["health"]=}')
        # for k in description:
        #     print(f'[add_actor] {k} :{description[k]}')
        entity.is_gravity_affected = description['gravity affected']

        entity.rectangle.height = sprites[entity.name + ' 0']['sprite'].get_height()
        entity.rectangle.width = int(sprites[entity.name + ' 0']['sprite'].get_width() * 0.7)  # Width of rectangle is 70% of sprite width.
        entity.rectangle_width_sit = entity.rectangle.width * 1.34
        if entity.name + ' 18' in sprites.keys():
            entity.rectangle_height_sit = sprites[entity.name + ' 18']['sprite'].get_height()
        else:
            entity.rectangle_height_sit = entity.rectangle.height

            # entity.rectangle.height = description['height']
        # entity.rectangle.width = description['width']
        entity.rectangle.center = start_xy
        # entity.rectangle.center = description['start_xy']
        # entity.rectangle.x += randint(-200, 300)
        entity.apply_measurements()
        entity.destination[0] = entity.rectangle.centerx
        entity.destination[1] = entity.rectangle.centery
        # entity.max_speed = description['max speed']

        entity.acceleration = description['acceleration']
        entity.default_acceleration = description['acceleration']
        entity.friction = description['friction']
        entity.default_friction = description['friction']
        entity.air_acceleration = description['air acceleration']
        entity.default_air_acceleration = description['air acceleration']
        # entity.default_max_speed = description['max speed']

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
        if entity.id != 0:
            entity.activate_weapon(0)
        else:
            all_weapons = list(entity.inventory['weapons'].keys())
            entity.body['right hand']['weapon'] = entity.inventory['weapons'][all_weapons[0]]
            entity.body['left hand']['weapon'] = entity.inventory['weapons'][all_weapons[1]]
            entity.current_weapon = entity.body['right hand']['weapon']['item']
        # entity.activate_weapon('WHIP')
        # entity.activate_weapon('SHORT SWORD')

        # entity.change_animation()
        # entity.process_animation_counter()

        # entity.set_state('stand still')
        # entity.max_jump_attempts = 3

        if self.location not in self.actors.keys():
            self.actors[self.location] = dict()

        if entity.id == 0:
            # This is the player actor:
            self.actors['player'] = entity

        self.actors[self.location][entity.id] = entity
        self.actor_id += 1
        print(f'[ADDING ACTOR] ----------------------E-N-D------------------------------')

    def add_item(self, item, xy):
        # print(f'[world.add_item] {item}')
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


            # # Make sprite surface for obstacle:
            # # print(self.locations[self.location]['obstacles']['settings'][entity.id]['sprite'])
            # # print(sprites[self.locations[self.location]['obstacles']['settings'][entity.id]['sprite']])
            # entity.surface = pygame.Surface((entity.rectangle.width, entity.rectangle.height)).convert_alpha()
            # tile_name = 'tile ' + str(self.locations[self.location]['obstacles']['settings'][entity.id]['sprite'])
            # # print(tile_name, sprites[tile_name]['sprite'])
            # sprite_to_fill_surface = sprites[tile_name]['sprite']
            # sz = sprite_to_fill_surface.get_size()
            # for dx in range(0, entity.rectangle.width, sz[0]):
            #     for dy in range(0, entity.rectangle.height, sz[1]):
            #         entity.surface.blit(sprite_to_fill_surface, (dx, dy))

            entity.is_force_render = self.locations[self.location]['obstacles']['settings'][entity.id]['force render'] if 'force render' in \
                                    self.locations[self.location]['obstacles']['settings'][entity.id].keys() else False
            entity.actions = self.locations[self.location]['obstacles']['settings'][entity.id]['actions']
            if entity.actions:
                # Make sprite surface for obstacle:
                # print(self.locations[self.location]['obstacles']['settings'][entity.id]['sprite'])
                # print(sprites[self.locations[self.location]['obstacles']['settings'][entity.id]['sprite']])
                entity.surface = pygame.Surface((entity.rectangle.width, entity.rectangle.height)).convert_alpha()
                tile_name = 'tile ' + str(self.locations[self.location]['obstacles']['settings'][entity.id]['sprite'])
                # print(tile_name, sprites[tile_name]['sprite'])
                sprite_to_fill_surface = sprites[tile_name]['sprite']
                sz = sprite_to_fill_surface.get_size()
                for dx in range(0, entity.rectangle.width, sz[0]):
                    for dy in range(0, entity.rectangle.height, sz[1]):
                        entity.surface.blit(sprite_to_fill_surface, (dx, dy))

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
        p.fall_speed_correction = description['fall speed correction'] if 'fall speed correction' in description.keys() else 1.0
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
        p.current_sprite = description['sprite']
        p.is_collideable = description['collides']
        p.is_gravity_affected = description['gravity affected']
        self.particles[self.location][p.id] = p

    def add_demolisher(self, description):
        demol = Demolisher()
        demol.id = self.demolisher_id
        self.demolisher_id += 1
        demol.name = 'demolisher ' + str(demol.id)
        demol.bounce = description['bounce']
        demol.bounce_factor = description['bounce factor']
        demol.flyer = description['flyer']
        demol.parent = description['parent']

        if description['static']:
            demol.snap_to_actor = demol.parent.id
        else:
            demol.snap_to_actor = -1

        # print(f'{demol.parent=}')
        if demol.parent:
            demol.parent_id = demol.parent.id
            demol.look = demol.parent.look
            demol.ttl = description['demolisher TTL'] * demol.parent.frames_changing_threshold_modifier
            if description['static']:
                for k in description['damage']:
                    demol.damage[k] = description['damage'][k] / demol.parent.frames_changing_threshold_penalty \
                                      + 2 * (abs(demol.parent.speed) + abs(demol.parent.fall_speed))
                                      # + 2 * (max(1, (abs(demol.parent.speed) + abs(demol.parent.fall_speed))))
                                      # * (abs(demol.parent.speed) + abs(demol.parent.fall_speed))
            else:
                demol.damage = description['damage']
            demol.parent_strength = demol.parent.strength
            demol.parent_weight = demol.parent.body_weight
            demol.parent_penalty = demol.parent.frames_changing_threshold_penalty
        else:
            # demol.look = 1
            demol.ttl = description['demolisher TTL']
            demol.damage = description['damage']
            demol.parent_strength = 0
            demol.parent_weight = 0
            demol.parent_penalty = 0

        demol.pierce = description['pierce']

        # Total damage amount is necessary to burn out stamina of a sneaky actor, protected by shield.
        for damage_type in demol.damage.keys():
            demol.total_damage_amount += demol.damage[damage_type]

        # Appearance:
        if description['visible']:
            if description['demolisher sprite']:
                demol.current_sprite = sprites[description['demolisher sprite']]
                demol.rectangle.width = sprites[description['demolisher sprite']]['mask rect'].width
                demol.rectangle.height = sprites[description['demolisher sprite']]['mask rect'].height
                demol.snapping_offset = {
                    'offset inside actor': description['snapping offset'],
                    'offset inside demolisher': sprites[description['demolisher sprite']]['demolisher snap point']
                }
                # demol.update(demol.parent.look, demol.parent.rectangle)
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
                    'demolisher snap point': (0, 0),
                    'mask': mask,
                    'mask rect': mask.get_rect()
                }
                demol.snapping_offset = {
                    'offset inside actor': description['snapping offset'],
                    'offset inside demolisher': demol.current_sprite['demolisher snap point']
                }
                # demol.update(demol.parent.look, demol.parent.rectangle)
        else:
            # if demol.parent.look == 1:
            #     demol.rectangle.x = demol.parent.rectangle. description['snapping offset'][0]
            demol.rectangle.width = description['rect'].width
            demol.rectangle.height = description['rect'].height
            demol.invisible = True
            demol.snapping_offset = {
                'offset inside actor': description['snapping offset'],
                'offset inside demolisher': (-demol.rectangle.width//2,0)  # if demol.look == 1 else (demol.rectangle.width, 0)
            }

        # Geometry and coordinates:
        if demol.parent:
            demol.update(demol.parent.look, demol.parent.rectangle)
            if demol.flyer:
                demol.destination_point = (self.camera.max_offset_x + MAXX, demol.rectangle.y) if demol.parent.look == 1 else (-100, demol.rectangle.y)
        else:
            demol.rectangle = description['rect']
            demol.destination_point = description['destination']
            demol.look = 1 if demol.rectangle.center < demol.destination_point else -1

        demol.aftermath = description['aftermath']
        # print(f'[add damager] {demol.damage=}')
        demol.static = description['static']
        demol.damage_reduce = description['damage reduce']
        demol.max_speed = description['speed']
        demol.speed = description['speed']
        demol.is_collideable = description['collides']
        demol.is_gravity_affected = description['gravity affected']
        # demol.attack_type = description['attack type']
        # demol.parent_strength = demol.parent.strength
        # demol.parent_weight = demol.parent.body_weight
        # demol.parent_penalty = demol.parent.frames_changing_threshold_penalty
        self.demolishers[self.location][demol.id] = demol
        # print(f'[add_demolisher] Added: {demol.id=} {demol.name} {demol.rectangle} {demol.max_speed=} {demol.destination=}')
    
    def add_protector(self, description):
        protector = Demolisher()
        protector.id = self.protector_id
        protector.type = 'protector'
        self.protector_id += 1
        protector.name = 'protector ' + str(protector.id)
        protector.bounce = description['bounce']
        protector.bounce_factor = description['bounce factor']
        protector.flyer = description['flyer']
        protector.parent = description['parent']
        protector.mana_consumption = description['mana consumption']
        # print(f'{protector.parent=}')

        if description['static']:
            protector.snap_to_actor = protector.parent.id
        else:
            protector.snap_to_actor = -1

        if protector.parent:
            protector.parent_id = protector.parent.id
            protector.look = protector.parent.look
            protector.ttl = description['protector TTL'] * protector.parent.frames_changing_threshold_modifier
            # if description['static']:
            #     for k in description['damage']:
            #         protector.damage[k] = description['damage'][k] / protector.parent.frames_changing_threshold_penalty + abs(protector.parent.speed) + abs(protector.parent.fall_speed)
            # else:
            protector.protection = description['protection']
            protector.parent_strength = protector.parent.strength
            protector.parent_weight = protector.parent.body_weight
            protector.parent_penalty = protector.parent.frames_changing_threshold_penalty
        else:
            # protector.look = 1
            protector.ttl = description['protector TTL']
            protector.protection = description['protection']
            # protector.damage = description['damage']
            protector.parent_strength = 0
            protector.parent_weight = 0
            protector.parent_penalty = 0

        protector.pierce = description['pierce']


        if description['visible']:
            if description['protector sprite']:
                protector.current_sprite = sprites[description['protector sprite']]
                protector.rectangle.width = sprites[description['protector sprite']]['mask rect'].width
                protector.rectangle.height = sprites[description['protector sprite']]['mask rect'].height
                protector.snapping_offset = {
                    'offset inside actor': description['snapping offset'],
                    'offset inside demolisher': sprites[description['protector sprite']]['demolisher snap point']
                }
                # protector.update(protector.parent.look, protector.parent.rectangle)
            else:
                # protector.current_sprite = None
                protector.rectangle.width = description['rect'].width
                protector.rectangle.height = description['rect'].height
                sprite = pygame.Surface((protector.rectangle.width, protector.rectangle.height)).convert_alpha()
                # sprite = pygame.Surface((protector.rectangle.width, protector.rectangle.height)).convert_alpha()
                sprite.fill(RED)
                # pygame.draw.circle(sprite, RED, protector.rectangle.center, protector.rectangle.width //2)
                mask = pygame.mask.from_surface(sprite.convert_alpha())
                protector.current_sprite = {
                    'sprite': sprite,
                    'sprite center': protector.rectangle.center,
                    'sprite asymmetric': None,
                    'demolisher snap point': (0, 0),
                    'mask': mask,
                    'mask rect': mask.get_rect()
                }
                protector.snapping_offset = {
                    'offset inside actor': description['snapping offset'],
                    'offset inside demolisher': protector.current_sprite['demolisher snap point']
                }
                # protector.update(protector.parent.look, protector.parent.rectangle)
        else:
            # if protector.parent.look == 1:
            #     protector.rectangle.x = protector.parent.rectangle. description['snapping offset'][0]
            protector.rectangle.width = description['rect'].width
            protector.rectangle.height = description['rect'].height
            protector.invisible = True
            protector.snapping_offset = {
                'offset inside actor': description['snapping offset'],
                'offset inside demolisher': (-protector.rectangle.width//2,0)  # if protector.look == 1 else (protector.rectangle.width, 0)
            }
        if protector.parent:
            protector.update(protector.parent.look, protector.parent.rectangle)
            if protector.flyer:
                protector.destination_point = (self.camera.max_offset_x + MAXX, protector.rectangle.y) if protector.parent.look == 1 else (-100, protector.rectangle.y)
        else:
            protector.rectangle = description['rect']
            protector.destination_point = description['destination']
            protector.look = 1 if protector.rectangle.center < protector.destination_point else -1

        # if description['static']:
        #     protector.snap_to_actor = protector.parent.id
        # else:
        #     protector.snap_to_actor = -1
        protector.aftermath = description['aftermath']
        # protector.damage = description['damage'] / protector.parent.frames_changing_threshold_penalty + abs(protector.parent.speed) + abs(protector.parent.fall_speed)
        # print(f'[add damager] {protector.damage=}')
        protector.static = description['static']
        protector.damage_reduce = description['damage reduce']
        protector.max_speed = description['speed']
        protector.speed = description['speed']
        protector.is_collideable = description['collides']
        protector.is_gravity_affected = description['gravity affected']
        # protector.attack_type = description['attack type']
        # protector.parent_strength = protector.parent.strength
        # protector.parent_weight = protector.parent.body_weight
        # protector.parent_penalty = protector.parent.frames_changing_threshold_penalty
        self.protectors[self.location][protector.id] = protector
        # self.obstacles[self.location][self.obstacle_id] = protector
        # self.obstacle_id += 1
        # print(f'[add_demolisher] Added: {protector.id=} {protector.name} {protector.rectangle} {protector.max_speed=} {protector.destination=}')

    def process(self, time_passed):
        self.time_passed = time_passed
        if self.player_is_dead_counter_to_game_over > 0:
            self.player_is_dead_counter_to_game_over -= 1
            # print(self.player_is_dead_counter_to_game_over)
            if self.player_is_dead_counter_to_game_over == 0:
                self.game_over()
        self.processing_obstacles()
        if self.location_has_been_changed:
            self.actors['player'].influenced_by_obstacle = -1
            self.location_has_been_changed = False
            return

        self.processing_human_input()
        self.processing_protectors()
        self.processing_demolishers()

        self.processing_actors()
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
            self.active_obstacles.append(k)
            # obs = self.obstacles[self.location][k]
            # if obs.rectangle.colliderect(self.camera.active_objects_rectangle):
            #     self.active_obstacles.append(k)

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
            # if obs.type == 'protector':
            #     continue
            if obs.dead:
                dead.append(obs.id)
                continue
            if obs.is_item:
                # Routines for item-like obstacles:
                if obs.item_amount_decrease_speed != 0:
                    if obs.item_amount != obs.item_amount_threshold:
                        # print('decrease amount', obs.item_amount)
                        obs.item_amount += obs.item_amount_decrease_speed
            if obs.id in self.actors['player'].activated_triggers_list:
                if obs.teleport:
                # if obs.trigger_activated:
                    # print('obs')
                    if obs.teleport_description['on touch']:
                        self.change_location(obs.teleport_description)
                        obs.trigger_activated = False
                        self.actors['player'].activated_triggers_list = list()
                        return
                    else:
                        if self.is_input_up_arrow:
                            self.change_location(obs.teleport_description)
                            self.actors['player'].activated_triggers_list = list()
                            obs.trigger_activated = False
                            return
                        else:
                            obs.trigger_activated = False
                            continue
                if obs.trigger:
                # if obs.trigger_activated:
                    # obs.trigger = False
                    if obs.is_item:
                        # print("ITEM GRABBED:", obs.item_name, all_items[obs.item_name])
                        if all_items[obs.item_name]['class'] == 'burden':
                            if self.is_input_up_arrow and self.actors['player'].get_state() == 'stand still':
                                self.actors[self.location][0].add_items_to_inventory((all_items[obs.item_name],))
                                self.actors[self.location][0].set_state('prepare carry stash')
                                dead.append(obs.id)
                                continue
                            else:
                                self.actors['player'].health_replenish()
                                self.actors['player'].mana_replenish_modifier = 10
                                self.actors['player'].stamina_replenish_modifier = 10
                        elif all_items[obs.item_name]['class'] == 'instant consume':
                            if all_items[obs.item_name]['type'] == 'stats gainer':
                                self.actors[self.location][0].stats[all_items[obs.item_name]['affects on']] += obs.item_amount
                                obs.trigger = False
                                dead.append(obs.id)
                                continue
                        else:
                            self.actors[self.location][0].add_items_to_inventory((all_items[obs.item_name],))
                            obs.trigger = False
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

                    if obs.trigger_description:
                        if obs.trigger_description['disappear']:
                            dead.append(obs.id)
                            continue

            obs.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location], self.protectors[self.location])
            obs.get_time(self.time_passed, self.game_cycles_counter)
            obs.process_()

        if dead:
            for dead_id in dead:
                del self.obstacles[self.location][dead_id]
            self.detect_active_obstacles()

    def make_explosion(self, xy):
        print(f'[process demolishers] KA-BOOM!')
        for i in range(randint(40, 50)):
            demolisher_description = {

                'snap to actor': -1,
                'demolisher sprite': None,
                'demolisher TTL': randint(150, 170),
                'rect': pygame.Rect(xy[0], xy[1], 25, 25),
                'destination': find_destination_behind_target_point(xy, (randint(xy[0] - 100, xy[0] + 100), randint(xy[1] - 100, xy[1] + 100)), MAXX),
                'bounce': False,
                'bounce factor': 0,
                'flyer': True,
                'aftermath': '',
                'damage': {
                    'fire': 100,
                    'smash': 10,
                    'pierce': 100,
                },
                'static': False,
                'parent': None,
                'damage reduce': .01,
                'pierce': True,
                'visible': False,
                'snapping offset': (0, 0),
                # 'attack type': ('fire', 'smash', 'pierce', ),
                'speed': 1.5 + randint(1, 5) / 10,
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
                p.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None, self.protectors[self.location])
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
            # if dem.is_collideable:
            #     dem.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None, self.protectors[self.location])
            dem.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, None, self.protectors[self.location])
            if dem.static:
                if dem.snap_to_actor not in self.actors[self.location].keys():
                    dead.append(dem.id)
                    continue
                actor = self.actors[self.location][dem.snap_to_actor]
                # dem.update(actor.vec_to_destination)
                dem.update(actor.look, actor.rectangle)
                # dem.update(actor.look, actor.sprite_rectangle)

            dem.get_time(self.time_passed, self.game_cycles_counter)
            dem.process_demolisher()
            # dem.process_demolisher(self.time_passed)

        for dead_id in dead:
            del self.demolishers[self.location][dead_id]
        for expl in explosions:
            self.make_explosion(expl)
    
    def processing_protectors(self):
        dead = list()
        for key in self.protectors[self.location].keys():
            protector = self.protectors[self.location][key]
            if protector.dead:
                dead.append(protector.id)
                continue
            # if protector.is_collideable:
            # protector.percept({k: self.demolishers[self.location][k] for k in self.demolishers[self.location].keys()}, None, None)
            if protector.static:
                if protector.snap_to_actor not in self.actors[self.location].keys():
                    dead.append(protector.id)
                    continue
                actor = self.actors[self.location][protector.snap_to_actor]
                # protector.update(actor.vec_to_destination)
                protector.update(actor.look, actor.rectangle)
                # protector.update(actor.look, actor.sprite_rectangle)

            protector.get_time(self.time_passed, self.game_cycles_counter)
            protector.process_protector()
            # protector.process_demolisher(self.time_passed)

        for dead_id in dead:
            del self.protectors[self.location][dead_id]

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

            # if actor.dead:
            #     continue

            if actor.dying:
                actor.dead = True
                actor.dying = False
                actor.invincibility_timer = 0
                # actor.set_state('lie dead')
                if actor.disappear_after_death:
                    dead.append(actor.id)
                if actor.id == 0:
                    self.player_is_dead_counter_to_game_over = 200
                    if actor.has_item_in_inventory(all_items['stash']):
                        actor.drop_item_from_inventory(actor.inventory['burden']['stash']['item'])
                    # continue
                else:
                    if all_hostiles[actor.name]['drop']:
                        # print(all_hostiles[actor.name]['drop'])
                        for drop in all_hostiles[actor.name]['drop']:
                            self.add_item(all_items[drop], (randint(actor.rectangle.left - 50, actor.rectangle.right + 50), actor.rectangle.top))
                    # continue

            actor.percept({k: self.obstacles[self.location][k] for k in self.active_obstacles}, self.demolishers[self.location], self.protectors[self.location])
            actor.get_time(self.time_passed, self.game_cycles_counter)

            # actor.get_target(self.actors['player'])
            # if not actor.ignore_user_input:
            #     actor.think()

            if not actor.dead and not actor.is_stunned:
                if actor.ai_controlled:
                    # routines for AI
                    actor.get_target(self.actors['player'])
                    if not actor.ignore_user_input:
                        actor.think()
                else:
                    # routines for Player actor
                    if not actor.ignore_user_input:
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

                        if self.is_q:
                        # if self.is_l_alt and not self.l_alt_multiple_press_prevent:
                        #     self.l_alt_multiple_press_prevent = True
                            self.q_multiple_press_prevent = True
                            self.is_q = False
                            if actor.look == 1:
                                actor.set_action('hop back')
                            else:
                                actor.set_action('hop forward')
                        else:
                            if actor.get_state() in ('hopping back progress', 'hopping forward progress'):
                                actor.set_action('hop action cancel')

                        if self.is_e:
                        # if self.is_l_alt and not self.l_alt_multiple_press_prevent:
                        #     self.l_alt_multiple_press_prevent = True
                            self.e_multiple_press_prevent = True
                            self.is_e = False
                            if actor.look == -1:
                                actor.set_action('hop back')
                            else:
                                actor.set_action('hop forward')
                        else:
                            if actor.get_state() in ('hopping back progress', 'hopping forward progress'):
                                actor.set_action('hop action cancel')

                        # if self.is_attack and not self.is_alternate_attack:
                        #     # self.is_attack = False
                        #     if not actor.get_state() == 'protect':
                        #         # if self.is_alternate_attack:
                        #         #     actor.current_weapon = actor.body['left hand']['weapon']['item']
                        #         # elif self.is_attack:
                        #         actor.current_weapon = actor.body['right hand']['weapon']['item']
                        #         actor.current_stamina_lost_per_attack = actor.normal_stamina_lost_per_attack * actor.current_weapon['stamina consumption']
                        #         actor.current_mana_lost_per_attack = actor.normal_mana_lost_per_attack * actor.current_weapon['mana consumption']
                        #         if actor.current_weapon['type'] == 'shields':
                        #             actor.set_action('protect')
                        #         else:
                        #             actor.set_action('attack')
                        # elif not self.is_attack and self.is_alternate_attack:
                        #     # self.is_attack = False
                        #     if not actor.get_state() == 'protect':
                        #         # if self.is_alternate_attack:
                        #         actor.current_weapon = actor.body['left hand']['weapon']['item']
                        #         # elif self.is_attack:
                        #         # actor.current_weapon = actor.body['right hand']['weapon']['item']
                        #         actor.current_stamina_lost_per_attack = actor.normal_stamina_lost_per_attack * actor.current_weapon['stamina consumption']
                        #         actor.current_mana_lost_per_attack = actor.normal_mana_lost_per_attack * actor.current_weapon['mana consumption']
                        #         if actor.current_weapon['type'] == 'shields':
                        #             print('vvvvvvvvvvvvvvvvvvvvvv')
                        #             actor.set_action('protect')
                        #         else:
                        #             actor.set_action('attack')
                        # elif self.is_attack and self.is_alternate_attack:
                        #     if not actor.get_state() == 'protect':
                        #         actor.current_weapon = actor.body['right hand']['weapon']['item']
                        #         actor.current_stamina_lost_per_attack = actor.normal_stamina_lost_per_attack * actor.current_weapon['stamina consumption']
                        #         actor.current_mana_lost_per_attack = actor.normal_mana_lost_per_attack * actor.current_weapon['mana consumption']
                        #         if actor.current_weapon['type'] == 'shields':
                        #             actor.set_action('protect')
                        #         else:
                        #             actor.set_action('attack')
                        #
                        # else:
                        #     if actor.get_state() == 'protect':
                        #
                        #         actor.set_state('stand still')

                        if self.is_attack and self.is_alternate_attack:
                            # print(self.alternate_attack_time, self.attack_time)

                            if self.alternate_attack_time > self.attack_time:
                                hand = 'left hand'
                                self.alternate_attack_time = 0
                            else:
                                hand = 'right hand'
                                self.attack_time = 0
                        else:
                            if self.is_alternate_attack:
                                hand = 'left hand'
                            elif self.is_attack:
                                hand = 'right hand'
                            else:
                                hand = None

                        if hand:
                            # One or both hands of an actor does action:
                            actor.current_weapon = actor.body[hand]['weapon']['item']
                            if actor.get_state() == 'protect' and actor.current_weapon['type'] == 'shields':
                                # print('bbbb')
                                if not actor.summoned_protectors_keep_alive:
                                    actor.summon_protector = False
                                ...
                            else:
                                actor.current_stamina_lost_per_attack = actor.normal_stamina_lost_per_attack * actor.current_weapon['stamina consumption']
                                actor.current_mana_lost_per_attack = actor.normal_mana_lost_per_attack * actor.current_weapon['mana consumption']
                                if actor.current_weapon['type'] == 'shields':
                                    actor.set_action('protect')
                                    # actor.summon_protector = True
                                else:
                                    actor.set_action('attack')
                                    while actor.summoned_protectors_keep_alive:
                                        protector_id = actor.summoned_protectors_keep_alive.pop()
                                        del self.protectors[self.location][protector_id]
                        else:
                            actor.frames_changing_threshold_modifier = 1
                            actor.frames_changing_threshold_penalty = 1
                            actor.frames_changing_threshold = actor.animations[actor.current_animation]['speed']
                            # actor.summon_protector = False
                            # if actor.get_state() == 'protect' or actor.summon_protector:
                            if self.protectors[self.location]:
                                if actor.summoned_protectors_keep_alive:
                                    actor.summon_protector = False
                                    actor.set_state('stand still')
                                    while actor.summoned_protectors_keep_alive:
                                        protector_id = actor.summoned_protectors_keep_alive.pop()
                                        del self.protectors[self.location][protector_id]
                                # else:
                                #     actor.summoned_protectors_keep_alive.clear()
                                # actor.summon_protector = False
                                # actor.set_state('stand still')
            #         else:
            #             actor.summon_protector = False
            # else:
            #     actor.summon_protector = False

            actor.process()

            while actor.drop_from_inventory:
                i = actor.drop_from_inventory.pop()
                print('[processing actors] drop items:', all_items, i)
                # self.add_item(all_items[i], (actor.rectangle.right + sprites[i]['sprite'].get_width() //2,
                #                                 actor.rectangle.bottom - sprites[i]['sprite'].get_height()))
                if actor.look == 1:
                    self.add_item(all_items[i], (actor.rectangle.left - sprites[i]['sprite'].get_width() - 20,
                                                 actor.rectangle.top - sprites[i]['sprite'].get_height() - 20))
                else:
                    self.add_item(all_items[i], (actor.rectangle.right + sprites[i]['sprite'].get_width() + 20,
                                                 actor.rectangle.top - sprites[i]['sprite'].get_height() - 20))

            if actor.has_just_stopped_demolishers:
                while actor.has_just_stopped_demolishers:
                    d_id = actor.has_just_stopped_demolishers.pop()
                    del self.demolishers[self.location][d_id]
                    # self.demolishers[self.location][d_id].become_mr_floppy()

            if actor.summon_protector:
                # actor.summon_protector = False
                while actor.summoned_protectors_description:
                    p = actor.summoned_protectors_description.pop()
                    self.add_protector(p)
                    print(f'[processing actors] {actor.name} summoned a protector.')
                    actor.summoned_protectors_keep_alive.append(self.protector_id - 1)
            else:
                while actor.summoned_protectors_keep_alive:
                    protector_id = actor.summoned_protectors_keep_alive.pop()
                    del self.protectors[self.location][protector_id]

            if actor.summon_demolisher:
                actor.summon_demolisher = False
                # actor.stamina_reduce(actor.current_stamina_lost_per_attack)
                # actor.mana_reduce(actor.current_mana_lost_per_attack)
                # for d in actor.summoned_demolishers_description:
                while actor.summoned_demolishers_description:
                    d = actor.summoned_demolishers_description.pop()
                    self.add_demolisher(d)
                # self.add_demolisher(actor.summoned_demolisher_description)


            if actor.summon_particle:
                actor.summon_particle = False
                for description in actor.summoned_particle_descriptions:
                    self.add_particle(description)
                actor.summoned_particle_descriptions = list()

        for dead_id in dead:
            # Erase actors which must be disappeared after death.
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
        for key in reversed(self.actors[self.location].keys()):
            actor = self.actors[self.location][key]
            if actor.invincibility_timer > 0 and not actor.dead:
                if self.game_cycles_counter // 2 == self.game_cycles_counter / 2:
                    continue
            # size = actor.current_sprite['sprite'].get_size()
            # Offset sprite to the left from the center of rectangle using anchor point.
            # if actor.current_sprite_flip:
            #     if actor.current_sprite['sprite asymmetric']:
            #         x = actor.rectangle.centerx - self.camera.offset_x \
            #             - size[0] + actor.current_sprite['sprite center']
            #     else:
            #         x = actor.rectangle.centerx - self.camera.offset_x \
            #             - actor.current_sprite['sprite center']
            # else:
            #     x = actor.rectangle.centerx - self.camera.offset_x - actor.current_sprite['sprite center']
            #
            # y = actor.rectangle.bottom - self.camera.offset_y - size[1]

            x = actor.sprite_x - self.camera.offset_x
            y = actor.sprite_y - self.camera.offset_y
            # tmp_mask_sprite = actor.current_sprite['mask'].to_surface()
            # self.screen.blit(tmp_mask_sprite, (x, y))

            self.screen.blit(actor.current_sprite['sprite'], (x, y))

            # Misc info:
            # self.screen.blit(fonts.all_fonts[10].render(actor.get_state() + ' dying: ' + str(actor.dying)+ ' dead: ' + str(actor.dead), True, WHITE, BLACK), (x, y))

            # # Weak spot
            # if actor.current_sprite['weak spot']:
            #     # pygame.draw.circle(self.screen, YELLOW, (actor.rectangle.x + actor.current_sprite['weak spot'][0] - self.camera.offset_x,
            #     #                                       actor.rectangle.y + actor.current_sprite['weak spot'][1] - self.camera.offset_y),
            #     #                                       10)
            #     pygame.draw.rect(self.screen, YELLOW, actor.current_sprite['weak spot rect'])
            #     # pygame.draw.rect(self.screen, YELLOW, (actor.rectangle.x + actor.current_sprite['weak spot']['offset'][0] - self.camera.offset_x,
            #     #                                       actor.rectangle.y + actor.current_sprite['weak spot']['offset'][1] - self.camera.offset_y,
            #     #                                       actor.current_sprite['weak spot']['width'], actor.current_sprite['weak spot']['height']))

            if self.is_i:
                # Rectangle frame:
                pygame.draw.rect(self.screen, GREEN, (actor.rectangle.x - self.camera.offset_x, actor.rectangle.y - self.camera.offset_y,
                                                      actor.rectangle.width, actor.rectangle.height), 5)
                # SPRITE Rectangle frame:
                pygame.draw.rect(self.screen, MAGENTA, (actor.sprite_rectangle.x - self.camera.offset_x, actor.sprite_rectangle.y - self.camera.offset_y,
                                                      actor.sprite_rectangle.width, actor.sprite_rectangle.height), 3)

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
            if actor.id != 0 and not actor.dead:
                # pygame.draw.rect(self.screen, WHITE, (actor.rectangle.x - self.camera.offset_x - 2, actor.rectangle.y - 13 - self.camera.offset_y,
                #                                      actor.rectangle.width + 4, 7), 1)
                pygame.draw.rect(self.screen, RED, (actor.rectangle.centerx - 100 - self.camera.offset_x, actor.rectangle.bottom - actor.rectangle_height_default  - 9 - self.camera.offset_y,
                                                     actor.stats['health'] * 200 // actor.stats['max health'], 3))
                pygame.draw.rect(self.screen, YELLOW, (actor.rectangle.centerx - 100 - self.camera.offset_x, actor.rectangle.bottom - actor.rectangle_height_default - 6 - self.camera.offset_y,
                                                     actor.stats['stamina'] * 200 // actor.stats['max stamina'], 3))
                pygame.draw.rect(self.screen, BLUE, (actor.rectangle.centerx - 100 - self.camera.offset_x, actor.rectangle.bottom - actor.rectangle_height_default - 3 - self.camera.offset_y,
                                                     actor.stats['mana'] * 200 // actor.stats['max mana'], 3))


    def render_demolishers(self):
        for key in self.demolishers[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            dem = self.demolishers[self.location][key]
            if dem.invisible:
                pygame.draw.rect(self.screen, MAGENTA, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
                                                      dem.rectangle.width, dem.rectangle.height),1)
                continue
            # color = (max(0, 255 - dem.ttl*4), 10,0) if dem.ttl < 50 else PINK
            # pygame.draw.rect(self.screen, color, (dem.rectangle.x - self.camera.offset_x, dem.rectangle.y - self.camera.offset_y,
            #                                       dem.rectangle.width, dem.rectangle.height),1)

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
    
    def render_protectors(self):
        for key in self.protectors[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            protector = self.protectors[self.location][key]
            if protector.invisible:
                pygame.draw.rect(self.screen, MAGENTA, (protector.rectangle.x - self.camera.offset_x, protector.rectangle.y - self.camera.offset_y,
                                                      protector.rectangle.width, protector.rectangle.height),1)
                continue
            if protector.look == 1:
                self.screen.blit(protector.current_sprite['sprite'], (protector.rectangle.x - self.camera.offset_x, protector.rectangle.y - self.camera.offset_y))
            else:
                self.screen.blit(pygame.transform.flip(protector.current_sprite['sprite'], True, False), (protector.rectangle.x - self.camera.offset_x, protector.rectangle.y - self.camera.offset_y))
    
    def render_particles(self):
        for key in self.particles[self.location].keys():
            # if key not in self.active_obstacles:
            #     continue
            p = self.particles[self.location][key]
            # color = (max(0, 255 - p.ttl*4), 10,0) if p.ttl < 50 else PINK

            if p.subtype == 'splatter':
                pygame.draw.circle(self.screen, p.color, (p.rectangle.centerx - self.camera.offset_x, p.rectangle.centery - self.camera.offset_y), p.rectangle.width)
            elif p.subtype == 'text':
                self.screen.blit(p.current_sprite, (p.rectangle.centerx - self.camera.offset_x, p.rectangle.centery - self.camera.offset_y))
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

    def render_items(self):
        for key in self.obstacles[self.location].keys():
            if key not in self.active_obstacles:
                continue
            obs = self.obstacles[self.location][key]
            if obs.is_item:
                self.screen.blit(sprites[obs.sprite]['sprite'], (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y))


    def render_obstacles(self):
        for key in self.obstacles[self.location].keys():
            if key not in self.active_obstacles:
                continue
            obs = self.obstacles[self.location][key]
            if obs.invisible or obs.is_item:
            # if obs.invisible:
                continue
            if obs.teleport:
                if not obs.teleport_description['on touch']:
                    if obs.trigger_activated:
                        pygame.draw.rect(self.screen, CYAN, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
                                                              obs.rectangle.width, obs.rectangle.height), 1)
            # if obs.is_item:
            #     self.screen.blit(sprites[obs.sprite]['sprite'], (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y))
            #     continue

            if obs.surface:
                self.screen.blit(obs.surface, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y))
                continue

            # if not obs.is_force_render:
            #     continue
            # try:
            #     self.screen.blit(sprites[obs.sprite]['sprite'], (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y))
            # except:
            #     print(obs.id, obs.sprite, sprites[obs.sprite])

            # if obs.sprite is not None:
            #     print(obs.sprite, sprites[obs.sprite])
            #     self.screen.blit(sprites[obs.sprite]['sprite'], (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y))
            #                                                      # obs.rectangle.width, obs.rectangle.height))
            #     continue

            # color = YELLOW if obs.is_ghost_platform else CYAN
            # pygame.draw.rect(self.screen, color, (obs.rectangle.x - self.camera.offset_x, obs.rectangle.y - self.camera.offset_y,
            #                                       obs.rectangle.width, obs.rectangle.height), 1)

            # if obs.active:
            #     dx = 10
            #     stats_y = 1
            #     gap = 1
            #     font_size = 10
            #     params = (
            #         ('ID: ' + str(obs.id), RED),
            #         ('ACTV: ' + str(obs.active), RED),
            #         ('TRGGRED: ' + str(obs.trigger_activated), RED),
            #         ('WAIT COUNTER    : ' + str(obs.wait_counter), RED),
            #         ('DEST REACHED    : ' + str(obs.is_destination_reached), RED),
            #         ('RECTANGLE       : ' + str(obs.rectangle), RED),
            #         ('ACTION          : ' + str(obs.actions[obs.actions_set_number][obs.current_action]), RED) if obs.current_action else ('', RED),
            #         ('NEED NEXT ACTION: ' + str(obs.need_next_action), RED),
            #         ('VEC TO DESTINTON: ' + str(obs.vec_to_destination), RED),
            #         ('DESTINATION AREA: ' + str(obs.destination_area), RED),
            #         ('DESTINATION PNT : ' + str(obs.destination_point), RED),
            #         ('DESTINATION     : ' + str(obs.destination), RED),
            #         ('GRAVITY         : ' + str(obs.is_gravity_affected), RED),
            #         # 'CR',
            #     )
            #     for p in params:
            #         if p == 'CR':
            #             dx += 300
            #             gap = 1
            #             continue
            #         self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1], WHITE),
            #                          (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
            #         gap += font_size
            #     # pygame.draw.rect(self.screen, MAGENTA, (obs.destination_area.x - self.camera.offset_x, obs.destination_area.y - self.camera.offset_y,
            #     #                                       obs.destination_area.width, obs.destination_area.height))
            #
            # else:
            #     dx = 10
            #     stats_y = 1
            #     gap = 1
            #     font_size = 10
            #     params = (
            #         ('ID: ' + str(obs.id), BLACK),
            #         ('TRGGR: ' + str(obs.trigger_activated), YELLOW),
            #         # ('GRAVITY         : ' + str(obs.is_gravity_affected), RED),
            #         # ('IN GROUND       : ' + str(obs.is_stand_on_ground), RED),
            #         # ('EDGE GRABBED    : ' + str(obs.is_edge_grabbed), RED),
            #         # ('WAIT COUNTER    : ' + str(obs.wait_counter), BLACK),
            #         # ('IDLE            : ' + str(obs.idle), BLACK),
            #     )
            #     for p in params:
            #         if p == 'CR':
            #             dx += 300
            #             gap = 1
            #             continue
            #         self.screen.blit(fonts.all_fonts[font_size].render(p[0], True, p[1]),
            #                          (obs.rectangle.x + dx - self.camera.offset_x, obs.rectangle.y + gap - self.camera.offset_y))
            #         gap += font_size


    def render_all(self):
        self.render_background()
        self.render_obstacles()
        self.render_actors()
        self.render_demolishers()
        self.render_protectors()
        self.render_particles()
        self.render_items()
        self.render_info_panel_overlay()
        if self.is_i:
            self.render_debug_info()

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
            ('HEALTH :' + str(int(self.actors['player'].stats['max health'])) + '/' + str(int(self.actors['player'].stats['health'])),
             ((int(self.actors['player'].stats['max health']),BLACK),
              (int(self.actors['player'].stats['target health']),YELLOW),
              (int(self.actors['player'].stats['health']),MAGENTA),),
             MAGENTA),
             # int(self.actors['player'].stats['health'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max health']),


            ('STAMINA:' + str(int(self.actors['player'].stats['max stamina'])) + '/' + str(int(self.actors['player'].stats['stamina'])),
             ((int(self.actors['player'].stats['max stamina']),BLACK),
              (int(self.actors['player'].stats['target stamina']),YELLOW),
              (int(self.actors['player'].stats['stamina']), GREEN if self.actors['player'].stats['stamina'] >= self.actors['player'].current_stamina_lost_per_attack else RED),),
             GREEN),
            # int(self.actors['player'].stats['stamina'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max stamina']),

            ('MANA   :' + str(int(self.actors['player'].stats['max mana'])) + '/' + str(int(self.actors['player'].stats['mana'])),
             ((int(self.actors['player'].stats['max mana']),BLACK),
              (int(self.actors['player'].stats['target mana']),YELLOW),
              (int(self.actors['player'].stats['mana']),BLUE),),

             # int(self.actors['player'].stats['mana'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max mana']),
             BLUE),

            ('EXP:' + str(int(self.actors['player'].stats['exp'])), None, VIOLET),
            # ('HEALTH:' + str(int(self.actors['player'].max_health)) + '/' + str(int(self.actors['player'].health)),int(self.actors['player'].health * max_stripes_width // self.actors['player'].max_health), RED),

        )

        # txt = fonts.all_fonts[self.info_panel_font_size].render(params[0][0], True, params[0][2])
        # txt_shadow = fonts.all_fonts[self.info_panel_font_size].render(params[0][0], True, BLACK)
        # txt_width = txt.get_width() + 50
        txt_width = 250

        background_width = self.info_panel_max_stripes_width + 10 + txt_width
        background_height = len(params) * self.info_panel_font_size + 5 + (self.info_panel_gap_between_stripes * len(params))

        # pygame.draw.rect(self.screen, BLACK, (self.info_panel_start_x - 5, self.info_panel_start_y - 5, background_width, background_height))

        for p in params:
            txt = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, p[2])
            txt_shadow = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, GRAY)
            self.screen.blit(txt_shadow, (self.info_panel_start_x + 2, self.info_panel_start_y + dy + 2))  # TEXT SHADOW
            # self.screen.blit(txt, (self.info_panel_start_x + 1, self.info_panel_start_y + dy + 1), None, BLEND_RGB_MIN)  # TEXT SHADOW
            self.screen.blit(txt, (self.info_panel_start_x, self.info_panel_start_y + dy))

            # Stripes:
            if p[1]:
                size_shrinker = 0
                for stripe in p[1]:
                    if stripe[0] > 0:
                        pygame.draw.rect(self.screen, stripe[1], (self.info_panel_start_x + txt_width + size_shrinker,
                                                                  self.info_panel_start_y + dy + size_shrinker, stripe[0] - size_shrinker*2, 10 - size_shrinker*2))
                        size_shrinker += 1
            dy += (self.info_panel_font_size + self.info_panel_gap_between_stripes)

        # Show weapons ICONS in both player's hands:
        frame_sz = sprites['axe']['sprite'].get_size()
        weapon_sprite_start_x = 10
        weapon_sprite_start_y = MAXY - frame_sz[1] - 10
        # weapon_sprite_start_x = self.info_panel_start_x + background_width + 5

        for hand in ('left hand', 'right hand'):
            s = sprites[self.actors['player'].body[hand]['weapon']['item']['sprite']]['sprite']
            sz = s.get_size()
            if hand == self.player_actor_hand_to_change_weapon:
                pygame.draw.rect(self.screen, WHITE, (weapon_sprite_start_x, weapon_sprite_start_y, frame_sz[0], frame_sz[1]), 3, 10, 10)

            self.screen.blit(s, (weapon_sprite_start_x + frame_sz[0] // 2 - sz[0] // 2,
                                 weapon_sprite_start_y + frame_sz[1] // 2 - sz[1] // 2))
            weapon_sprite_start_x += frame_sz[0]
        # self.screen.blit(sprites[self.actors['player'].current_weapon['sprite']]['sprite'], (self.info_panel_start_x, self.info_panel_start_y))

    def render_info_panel_overlay_OLD(self):
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
            ('HEALTH :' + str(int(self.actors['player'].stats['max health'])) + '/' + str(int(self.actors['player'].stats['health'])),
             int(self.actors['player'].stats['health'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max health']),
             MAGENTA),

            ('STAMINA:' + str(int(self.actors['player'].stats['max stamina'])) + '/' + str(int(self.actors['player'].stats['stamina'])),
             int(self.actors['player'].stats['stamina'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max stamina']),
             YELLOW if self.actors['player'].stats['stamina'] >= self.actors['player'].current_stamina_lost_per_attack else RED),

            ('MANA   :' + str(int(self.actors['player'].stats['max mana'])) + '/' + str(int(self.actors['player'].stats['mana'])),
             int(self.actors['player'].stats['mana'] * self.info_panel_max_stripes_width // self.actors['player'].stats['max mana']),
             BLUE),

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

        for p in params:
            txt = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, p[2])
            txt_shadow = fonts.all_fonts[self.info_panel_font_size].render(p[0], True, GRAY)
            self.screen.blit(txt_shadow, (self.info_panel_start_x + 2, self.info_panel_start_y + dy + 2))  # TEXT SHADOW
            # self.screen.blit(txt, (self.info_panel_start_x + 1, self.info_panel_start_y + dy + 1), None, BLEND_RGB_MIN)  # TEXT SHADOW
            self.screen.blit(txt, (self.info_panel_start_x, self.info_panel_start_y + dy))
            if p[1] > 0:
                pygame.draw.rect(self.screen, p[2], (self.info_panel_start_x + txt_width ,self.info_panel_start_y + dy, p[1],10))
            dy += (self.info_panel_font_size + self.info_panel_gap_between_stripes)

        # Show weapons ICONS in both player's hands:
        weapon_sprite_start_x = self.info_panel_start_x + background_width + 5
        frame_sz = sprites['axe']['sprite'].get_size()
        for hand in ('left hand', 'right hand'):
            s = sprites[self.actors['player'].body[hand]['weapon']['item']['sprite']]['sprite']
            sz = s.get_size()
            if hand == self.player_actor_hand_to_change_weapon:
                pygame.draw.rect(self.screen, WHITE, (weapon_sprite_start_x, self.info_panel_start_y, frame_sz[0], frame_sz[1]), 3, 10, 10)

            self.screen.blit(s, (weapon_sprite_start_x + frame_sz[0] // 2 - sz[0] // 2,
                                 self.info_panel_start_y + frame_sz[1] // 2 - sz[1] // 2))
            weapon_sprite_start_x += frame_sz[0]
        # self.screen.blit(sprites[self.actors['player'].current_weapon['sprite']]['sprite'], (self.info_panel_start_x, self.info_panel_start_y))

    def load(self):
        if self.location not in self.locations.keys():
            self.locations[self.location] = dict()
            self.obstacles[self.location] = dict()
            self.demolishers[self.location] = dict()
            self.protectors[self.location] = dict()
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

        # Background layers.
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

        # Key #80: left arrow
        # Key #79: right arrow
        keys = pygame.key.get_pressed()
        # print(type(keys))
        # self.press_any_key()
        # for k in keys:
            # if k:
            #     print(k, keys.index(k))
        # print(f'[human input] {keys[K_RIGHT]}')
        # print(f'[human input] {keys[79]=} {keys[80]=}')
        if keys[K_LEFT]:
            self.is_alternate_attack = True
            if self.alternate_attack_time == 0:
                self.alternate_attack_time = self.game_cycles_counter
            # print('left arrow press')
        else:
            self.is_alternate_attack = False
            self.alternate_attack_time = 0

        if keys[K_RIGHT]:
            self.is_attack = True
            if self.attack_time == 0:
                self.attack_time = self.game_cycles_counter
            # print('right arrow press')
        else:
            self.is_attack = False
            self.attack_time = 0

        # MOD KEYS:
        # mods = pygame.key.get_mods()
        # if mods & KMOD_LSHIFT:  # use whatever KMOD_ constant you want;)
        #     self.is_l_shift = True
        # elif mods & KMOD_LCTRL:
        #     self.is_l_ctrl = True
        # elif mods & KMOD_LALT:
        #     self.is_l_alt = True
        # else:
        #     self.l_alt_multiple_press_prevent = False
        #     self.is_l_ctrl = False
        #     self.is_l_shift = False
        #     self.is_l_alt = False


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit()
            # mods = pygame.key.get_mods()
            # if mods & KMOD_LSHIFT:  # use whatever KMOD_ constant you want;)
            #     self.is_l_shift = True
            # elif mods & KMOD_LCTRL:
            #     self.is_l_ctrl = True
            # elif mods & KMOD_LALT:
            #     self.is_l_alt = True
            # else:
            #     self.l_alt_multiple_press_prevent = False
            #     self.is_l_ctrl = False
            #     self.is_l_shift = False
            #     self.is_l_alt = False
            # print(self.l_shift)
            if event.type == KEYUP:
                self.is_key_pressed = False

                if event.key == K_q:
                    self.is_q = False
                    self.q_multiple_press_prevent = False
                if event.key == K_e:
                    self.is_e = False
                    self.e_multiple_press_prevent = False

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
                # if event.key == K_LEFT:
                #     self.is_alternate_attack = False

            if event.type == KEYDOWN:
                self.is_key_pressed = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    raise SystemExit()
                # # ATTACKING CHECKS
                # if event.key == K_RIGHT:
                #     self.is_attack = True
                #     self.is_alternate_attack = False
                # if event.key == K_LEFT:
                #     print('left pressed')
                #     self.is_attack = False
                #     self.is_alternate_attack = True
                if event.key == K_1:
                    self.player_actor_hand_to_change_weapon = 'left hand'
                elif event.key == K_2:
                    self.player_actor_hand_to_change_weapon = 'right hand'
                if event.key == K_BACKSPACE:
                    all_weapons = list(self.actors['player'].inventory['weapons'].keys())
                    if len(all_weapons) > 1:
                        current_index = all_weapons.index(self.actors['player'].body[self.player_actor_hand_to_change_weapon]['weapon']['item']['label'])
                        if current_index + 1 > len(all_weapons) - 1:
                            next_index = 0
                        else:
                            next_index = current_index + 1

                        # while self.actors['player'].inventory['weapons'][all_weapons[next_index]] == \
                        #       self.actors['player'].body['left hand' if self.player_actor_hand_to_change_weapon == 'right hand' else 'right hand']['weapon']: \
                        # next_index = 0 if next_index + 1 > len(all_weapons) - 1 else next_index + 1
                        self.actors['player'].body[self.player_actor_hand_to_change_weapon]['weapon'] = self.actors['player'].inventory['weapons'][all_weapons[next_index]]
                        # actor.drop_item_from_inventory(actor.inventory['burden']['stash']['item'])
                        # self.add_item(all_items[drop], (randint(actor.rectangle.left - 50, actor.rectangle.right + 50), actor.rectangle.top))
                        if self.actors['player'].body['left hand' if self.player_actor_hand_to_change_weapon == 'right hand' else 'right hand']['weapon']['item']['label'] == \
                            self.actors['player'].inventory['weapons'][all_weapons[current_index]]['item']['label']:
                            print('THE SAME!!')
                            self.actors['player'].body['left hand' if self.player_actor_hand_to_change_weapon == 'right hand' else 'right hand']['weapon'] = self.actors['player'].inventory['weapons'][all_weapons[0]]

                        self.actors['player'].drop_item_from_inventory(self.actors['player'].inventory['weapons'][all_weapons[current_index]]['item'])
                    else:
                        print(f'[processing human input] There is only one weapon left')
                # TAB
                if event.key == K_TAB:
                    all_weapons = list(self.actors['player'].inventory['weapons'].keys())
                    # print(all_weapons)
                    current_index = all_weapons.index(self.actors['player'].body[self.player_actor_hand_to_change_weapon]['weapon']['item']['label'])
                    if current_index + 1 > len(all_weapons) - 1:
                        next_index = 0
                    else:
                        next_index = current_index + 1

                    # while self.actors['player'].inventory['weapons'][all_weapons[next_index]] == \
                    #       self.actors['player'].body['left hand' if self.player_actor_hand_to_change_weapon == 'right hand' else 'right hand']['weapon']: \
                    # next_index = 0 if next_index + 1 > len(all_weapons) - 1 else next_index + 1

                    self.actors['player'].body[self.player_actor_hand_to_change_weapon]['weapon'] = self.actors['player'].inventory['weapons'][all_weapons[next_index]]

                if event.key == K_q:
                    if not self.q_multiple_press_prevent:
                        self.is_q = True
                if event.key == K_e:
                    if not self.e_multiple_press_prevent:
                        self.e_multiple_press_prevent = True
                        self.is_e = True

                # DIRECTION KEYS
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
                    # enemy_to_add = copy(all_hostiles['zombie'])  # Create a copy of enemy
                    # enemy_to_add = copy(all_hostiles['demon 1'])  # Create a copy of enemy
                    enemy_to_add = copy(all_hostiles['demon 2'])  # Create a copy of enemy
                    self.add_actor(enemy_to_add, (MAXX_DIV_2 + self.camera.offset_x, MAXY_DIV_2 + self.camera.offset_y))
                    # self.change_mode()
                    # self.is_n = False if self.is_n else True
                    # msg = 'NEW EMPTY MESSAGE FOR TEST PURPOSES.'
                    # self.info_windows[0].get_bunch_of_new_messages((msg, msg))
                    # self.add_info_window(self.calculate_info_string_xy(), [msg, ], 300, False)

                elif event.key == K_p:
                    self.is_p = False if self.is_p else True
                elif event.key == K_i:
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

            # if event.type == MOUSEBUTTONDOWN:
            #     buttons = pygame.mouse.get_pressed()
            #     if buttons[0]:
            #         self.is_mouse_button_down = True
            #         self.is_left_mouse_button_down = True
            #     if buttons[2]:
            #         self.is_mouse_button_down = True
            #         self.is_right_mouse_button_down = True
            # elif event.type == MOUSEWHEEL:
            #     # print(event)
            #     # print(event.x, event.y)
            #     # print(event.flipped)
            #     # print(event.which)
            #     self.is_mouse_wheel_rolls = True
            #     if event.y == 1:
            #         # Mouse wheel up:
            #         self.is_mouse_wheel_up = True
            #         # self.wandering_screen_target_scale += self.wandering_scale_amount
            #     elif event.y == -1:
            #         # Mouse wheel down:
            #         self.is_mouse_wheel_down = True
            # if event.type == MOUSEBUTTONUP:
            #     self.is_mouse_button_down = False
            #     if self.is_right_mouse_button_down:
            #         self.is_right_mouse_button_down = False
            #     if self.is_left_mouse_button_down:
            #         self.is_left_mouse_button_down = False

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
            (' RECT       : ' + str(self.actors['player'].rectangle), WHITE),
            (' SPRITE RECT: ' + str(self.actors['player'].sprite_rectangle), WHITE),
            ('╔ TARGET HEIGHT ╗: ' + str(self.actors['player'].target_height), YELLOW),
            ('╚ TARGET WIDTH  ╝: ' + str(self.actors['player'].target_width), YELLOW),
            (' FALL SPEED: ' + str(self.actors['player'].fall_speed), WHITE),
            (' SPEED: ' + str(self.actors['player'].speed), WHITE),
            (' MAX SPEED: ' + str(self.actors['player'].max_speed), WHITE),
            (' LOOK: ' + str(self.actors['player'].look), WHITE),
            (' MOVE INVERTER: ' + str(self.actors['player'].movement_direction_inverter), WHITE),
            (' HEADING: ' + str(self.actors['player'].heading), WHITE),
            (' IDLE COUNT: ' + str(self.actors['player'].idle_counter), (200, 100, 50)),
            (' ACTIVE FRAMES: ' + str(self.actors['player'].active_frames), (200, 100, 50)),
            (' JUMP ATTEMPTS : ' + str(self.actors['player'].jump_attempts_counter), YELLOW),
            (' JUST JUMPED   : ' + str(self.actors['player'].just_got_jumped), YELLOW),
            (' JUMP PERFORMED: ' + str(self.actors['player'].is_jump_performed), YELLOW),
            (' IGNORES INPUT: ' + str(self.actors['player'].ignore_user_input), WHITE),
            (' STAMINA MODIFIER: ' + str(self.actors['player'].stamina_replenish_modifier), WHITE),
            (' __STATE: ' + str(self.actors['player'].get_state()), CYAN),
            (' __ANIMATION: ' + str(self.actors['player'].current_animation), CYAN),
            (' COMBO NUMBER : ' + str(self.actors['player'].combo_set_number), YELLOW),
            (' COMBO COUNTER: ' + str(self.actors['player'].combo_counter), YELLOW),
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
        render_text('YOU DIED', self.screen, 150, RED, 'AlbionicRegular.ttf', 'center_x', 'center_y')
        pygame.display.flip()
        pygame.time.wait(800)
        render_text('press a key to revive', self.screen, 50, RED, 'AlbionicRegular.ttf', 'center_x', '3/4_y')  #, (-200, 0))
        pygame.display.flip()
        pygame.event.clear()
        self.press_any_key()
        self.actors['player'].stats['health'] = self.actors['player'].stats['max health']
        self.actors['player'].stats['mana'] = self.actors['player'].stats['max mana']
        self.actors['player'].dead = False
        self.actors['player'].dying = False
        self.actors['player'].animation_change_denied = False
        self.actors['player'].set_state('stand still')
        self.actors['player'].invincibility_timer = 300
        self.actors['player'].ignore_user_input = False
        for location in self.obstacles.keys():
            obstacles = self.obstacles[location]
            for obs_key in obstacles.keys():
                obs = obstacles[obs_key]
                # print(obs)
                if obs.is_item:
                    if obs.item_name == 'stash':
                        self.change_location({'new location': location,
                                              'xy': (obs.rectangle.x, obs.rectangle.bottom - self.actors['player'].rectangle.height - 10),
                                              }
                                             )

                        return

        self.change_location({'new location': 'entrance',
                              'xy': (100, locations['entrance']['size'][1] - self.actors['player'].rectangle.height * 1.5)
                              # 'xy': (100, 100)
                              }
                             )
        # pygame.quit()
        # exit()