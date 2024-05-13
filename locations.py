# from game_objects import *
from actors_description import *
from constants import *
import pygame

locations = {
    'living_room_1':
        {
            'mode': 'wandering',
            'light level': 1.5,
            'lights on': True,
            # 'lights on': False,
            'description': 'Inside the Church',
            'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.6,
            'avatar scales': True,
            'actors speed scale': 0.7,
            'cell size': 100,
            'sprites type': 'walking figure',
            'sprites orientation': {
                'rotate': False,
                'east-west': True,
                'still': False
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            # 'net': False,
            'items': {
                'goo_stuff': {
                    'position': (600, 600),
                    'destination': (600, 600),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'shotgun_ammo',
                    'inventory': (shotgun_ammo,),
                    'scale': 0.5
                },
                'Mud_stuff': {
                    'position': (1000, 200),
                    'destination': (400, 600),
                    'speed': 0.09,
                    'sprite': 'question sign',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'brass_garden_key',
                    'inventory': (brass_garden_key, ),
                    'scale': 0.2
                },
            },
            'obstacles': {
                # (3, 2): {
                #     'sprite name': ' box single',
                #     'available': True,
                #     'index': None,
                #     'TTL': 100,
                #     'description': 'BIG QUESTION',
                #     'scale': 1
                # },
                3: {
                    'sprite name': 'box single',
                    'available': True,
                    'index': None,
                    'TTL': 100,
                    'description': 'BIG QUESTION',
                    'scale': 1
                },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 250,
                'start y': 50,
                'cell width': 100,
                'cell height': 100,
                'max x cells': 15,
                'max y cells': 5,
                'min cell scale': 0.5,
                'scale increase factor': 0.05,
                'default available': True,
                'not available cells': (5,),
                'points lead to other locations': {
                    0: {'location': 'village1', 'point': 3, 'on touch': False, 'need key': False, 'key': None},
                },
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
        },

    'field_1':
        {
            'mode': 'wandering',
            'light level': 1.2,
            'lights on': True,
            'music': None,
            # 'lights on': False,
            'description': 'Field behind the Central Store',
            'scale': {'max': 1.3, 'min': 0.65, 'amount': .5},
            # 'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.2,
            'avatar scales': False,
            'actors speed scale': 1,
            'cell size': 100,
            'sprites type': 'walking figure',  # 'icon'
            'sprites orientation': {
                # 'rotate': True,
                'rotate': False,
                # 'east-west': False,
                'east-west': True,
                'still': False
                # 'still': True
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            # 'isometric': False,
            # 'net': False,
            'obstacles': {
                # Possible actions:
                # ('move', (99, 102, 55)): move object through the list of given points, ignoring obstacles.
                # ('wait', 100): wait given game cycles.
                # ('repeat', 0):  if zero, repeat all preceding actions unlimited number of times, else repeat given number.
                # ('die',): get suicide.
                # ('find route', 46): build A* route to a given point considering obstacles.
                'crate #1': {
                    'already added': False,
                    'cells': (23,),
                    'sprite name': 'metal crate #1 frame 0',
                    'sprite snap': 'left',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    # 'description': 'crate id 1',
                    'scale': 1,
                    'speed': 0.1,
                    'active': True,
                    'do actions': False,
                    'action number': 0,
                    'actions': {
                        0: (('move', (23, 24, 9)), ('stop', ), ),
                    },
                    # 'use alternate actions': False,
                    # 'actions': (('switch visibility',), ('switch passability',), ),
                    # 'actions': (('move', (24, 9)), ('stop', ), ('move', (24, 23)),),
                    # 'alternate actions': (('move', (24, 23)), )
                    # 'actions': (('move', (24, 9)), ('wait', 2), ('repeat', 3), ('move', (10, )), ('wait', 100),  ('die', ))
                },
                'coffee table 1': {
                    'already added': False,
                    'cells': (68, ),
                    'sprite name': 'coffee table',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'table',
                    'scale': 1,
                    'sprite snap': 'left',
                    'speed': 0.6,
                    'active': True,
                    'do actions': False,
                    'action number': 0,
                    'actions': {
                        0: (('find route', 46), ('find route', 68), ('repeat', 0),),
                        1: (('find route', 16), ('teleport', 46), ('wait', 120), ('die',))
                    },
                },
                'coffee table 2': {
                    'already added': False,
                    'active': True,
                    'cells': (99,),
                    'sprite name': 'coffee table',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'table',
                    'scale': 1,
                    'sprite snap': 'left',
                    'speed': 0.6,
                    'do actions': False,
                    'action number': 0,
                    'actions': {
                        0: (('move', (70, )), ('wait', 12), ('move', (68, )), ('wait', 12), ('move', (99, )), ('wait', 12), ('repeat', 0)),
                        1: (('find route', 16), ('wait', 12), ('die',)),
                    }
                },
                'coffee table 3': {
                    'already added': False,
                    'active': True,
                    'cells': (135,),
                    'sprite name': 'coffee table',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'table',
                    'scale': 1,
                    'sprite snap': 'left',
                    'speed': 0.6,
                    'do actions': False,
                    'action number': 0,
                    'actions': {
                        0: (('move', (137, 139, 141, 143, 145, 147, 149)), ('switch visibility', 0), ('wait', 120), ('teleport', 135), ('switch visibility', 0), ('wait', 12), ('repeat', 0)),
                        1: (('find route', 11), ('find route', 111), ('wait', 12), ('die',))
                    }
                },
                'piles 1': {
                # (34, 38, 8): {
                    'already added': False,
                    'active': False,
                    'cells': (30, 34, 38, 8),
                    'sprite name': 'pile 1x #1',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'sprite snap': 'left',
                    'actions': ()
                },
                'glasses 1': {
                # (35, 37): {
                    'already added': False,
                    'active': False,
                    'cells': (31, 32, 33, 35, 36, 37),
                    'sprite name': 'glass 1x #1',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'sprite snap': 'left',
                    'actions': ()
                },
                'boxes single': {
                # (4, 30, 15, 12): {
                    'already added': False,
                    'active': False,
                    'cells': (4, 15, 12),
                    'sprite name': 'box single',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'sprite snap': 'left',
                    'actions': ()
                },
                'boxes 1.5': {
                    'already added': False,
                    'active': False,
                    'cells': (45, 60, 75, 88, 89, 90),
                    'sprite name': 'box 1.5x #23',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'sprite snap': 'left',
                    'actions': ()
                },
            },
            'items': {
                'crate switcher': {
                    'already added': False,
                    'position': (900, 420),
                    'destination': (900, 420),
                    'size': (40, 100),
                    'speed': 0.1,
                    'sprite': None,
                    # 'sprite': 'question sign',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        # 'furniture action trigger': True,
                        'inventory': None,
                        'multiple': True,
                        # 'objects': (('field_1', 'obstacles', 'crate #1', 'do actions'),
                        #             # ('field_1', 'obstacles', 'coffee table', 'do actions'),
                        #             ),
                        'target': ("self.obstacles[self.location]['crate #1'].do_actions = True", ),
                        # 'target': ("self.locations['field_1']['obstacles']['crate #1']['do actions'] = True", ),
#                         'target': ("""locations['field_1']['obstacles']['crate #1']['do actions'] = False if locations['field_1']['obstacles']['crate #1']['do actions'] else True
# locations['field_1']['obstacles']['crate #1']['do alternate actions'] = False if locations['field_1']['obstacles']['crate #1']['do actions'] else True""", ),
                    },
                    'TTL': -1,
                    'description': 'crate door opener',
                    'scale': 0.4
                },
                # 'total light switcher': {
                #     'position': (950, 475),
                #     'destination': (950, 475),
                #     # 'position': (870, 300),
                #     # 'destination': (870, 300),
                #     'speed': 0.1,
                #     'sprite': None,
                #     # 'sprite': 'question sign',
                #     'available': True,
                #     # 'mode': 'interact',
                #     'mode': 'on touch',
                #     'index': None,
                #     'action': {
                #         'action trigger': True,
                #         'storage': False,
                #         'inventory': None,
                #         'target': ("self.locations['field_1']['obstacles']['coffee table']['do actions'] = True",
                #                    "self.locations['field_1']['obstacles']['coffee table 2']['do actions'] = True",
                #                    "self.locations['field_1']['obstacles']['coffee table 3']['do actions'] = True",
                #                    "self.locations['village1']['lights on'] = True",
                #                    ),
                #         # 'multiple': True,
                #         'multiple': False,
                #     },
                #     'TTL': -1,
                #     'description': 'light switcher',
                #     'scale': 1
                # },
                'tables switch on': {
                    'already added': False,
                    'position': (1200, 550),
                    'destination': (1200, 550),
                    # 'position': (870, 300),
                    # 'destination': (870, 300),
                    'speed': 0.1,
                    'sprite': None,
                    # 'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                            "self.obstacles[self.location]['coffee table 1'].do_actions = True",
                            "self.obstacles[self.location]['coffee table 2'].do_actions = True",
                            "self.obstacles[self.location]['coffee table 3'].do_actions = True",
                            # "self.locations['field_1']['obstacles']['coffee table 2']['do actions'] = True",
                            # "self.locations['field_1']['obstacles']['coffee table 2']['use alternate actions'] = True",
                                   # "self.locations['field_1']['lights on'] = False if locations['field_1']['lights on'] else True",
                                   # "self.mouse_wheel_rolls = True",
                                   # "self.mouse_wheel_up = True"
                                   ),
                        # 'multiple': True,
                        'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 1
                },
                'tables killer': {
                    'already added': False,
                    'position': (950,475),
                    'destination': (950,475),
                    'speed': 0.1,
                    'sprite': None,
                    # 'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': ("self.obstacles[self.location]['coffee table 1'].do_actions = True",
                                   "self.obstacles[self.location]['coffee table 1'].action_number += 1",
                                   "self.obstacles[self.location]['coffee table 1'].current_action = -1",
                                   "self.obstacles[self.location]['coffee table 2'].do_actions = True",
                                   "self.obstacles[self.location]['coffee table 2'].action_number += 1",
                                   "self.obstacles[self.location]['coffee table 2'].current_action = -1",
                                   # "self.locations['field_1']['obstacles']['coffee table']['use alternate actions'] = True",
                                   # "self.locations['field_1']['obstacles']['coffee table 2']['do actions'] = True",
                                   # "self.locations['field_1']['obstacles']['coffee table 2']['use alternate actions'] = True",
                                   # "self.locations['field_1']['lights on'] = False if locations['field_1']['lights on'] else True",
                                   # "self.mouse_wheel_rolls = True",
                                   # "self.mouse_wheel_up = True"
                                   ),
                        # 'multiple': True,
                        'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 1
                },

                'bag': {
                    'already added': False,
                    'position': (900, 500),
                    'destination': (900, 500),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (brass_garden_key,),
                    },
                    'TTL': -1,
                    'description': 'brass_garden_key',
                    'scale': 0.1
                },
            },
            'lights': {
                'central bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 1,
                    'x': 1260,
                    'y': 460,
                    'sprite': 'light halo casual',
                    'glowing': False
                },
                'custom bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 1,
                    'x': 115,
                    'y': 558,
                    'sprite': 'light halo casual',
                    'glowing': True
                },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 500,
                'start y': 200,
                'cell width': 100,
                'cell height': 100,
                'max x cells': 15,
                'max y cells': 10,
                'min cell scale': 0.3,
                'scale increase factor': 0,
                # 'instant scale points': {
                #
                # },
                'default available': True,
                # If there is a tuple or list instead of single cell number, it means a range.
                # If a tuple or a list consists of two numbers, it means straight range from start to finish.
                # Else it is just a bunch of unavailable cell numbers:
                'not available cells': [(49, 52), 64, 80, ],
                # 'not available cells': [(49, 52), 55, (64, 80, 96) ],
                'points lead to other locations': {
                    0: {'location': 'village1', 'point': 16, 'on touch': True, 'need key': False, 'key': None},
                    74: {'location': 'apartment_01_main_room', 'point': 195, 'on touch': True, 'need key': False, 'key': None},
                    14: {'location': 'storage_room', 'point': 1, 'on touch': True, 'need key': False, 'key': None},
                },
                # 'peculiar points': {
                #     151:
                #
                # }
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
            # 3: {
            #     'leads': {'location': 'living_room_1', 'point': 0, 'on touch': False, 'need key': False, 'key': None},
            #     'connected': (13,),
            #     'available': True,
            #     'scale': .4,
            #     'rect': pygame.Rect(560, 35, 416, 214),
            #     'interactive': True,
            #     'distances': dict(),
            #     'name': 'Church of St. Farting'
            # },
    },

    'cave_1':
        {
            'mode': 'wandering',
            'light level': 1.2,
            # 'lights on': True,
            'lights on': False,
            'description': 'Field behind the Central Store',
            'scale': {'max': 1.3, 'min': 0.65, 'amount': .5},
            # 'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.2,
            'avatar scales': False,
            'actors speed scale': 0.7,
            'cell size': 100,
            'sprites type': 'walking figure',  # 'icon'
            'sprites orientation': {
                # 'rotate': True,
                'rotate': False,
                # 'east-west': False,
                'east-west': True,
                'still': False
                # 'still': True
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            # 'isometric': False,
            # 'net': False,
            'obstacles': {
                # Possible actions:
                # ('move', (99, 102, 55)): move object through the list of given points, ignoring obstacles.
                # ('wait', 100): wait given game cycles.
                # ('repeat', 0):  if zero, repeat all preceding actions unlimited number of times, else repeat given number.
                # ('die',): get suicide.
                # ('find route', 46): build A* route to a given point considering obstacles.
                # 'crate #1': {
                # # 23: {
                #     # 'active': False,
                #     'active': True,
                #     'cells': (23,),
                #     'sprite name': ' metal crate #1 frame 0',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     # 'description': 'crate id 1',
                #     'scale': 1,
                #     'speed': 0.1,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     'actions': (('move', (24, 9)), )
                #     # 'actions': (('move', (24, 9)), ('wait', 2), ('repeat', 3), ('move', (10, )), ('wait', 100),  ('die', ))
                # },
                # 'coffee table': {
                # 'already added': False,
                #     'active': True,
                #     'cells': (68, ),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     'actions': (('find route', 46), ('find route', 68), ('repeat', 0)),
                #     # 'actions': (('move', (99, )), ('wait', 12), ('move', (70, )), ('wait', 12), ('move', (68, )), ('wait', 12), ('repeat', 0)),
                #     'alternate actions': (('teleport', 0), ('wait', 100), ('die',))
                #     # 'alternate actions': (('find route', 46), ('move', (47, )), ('wait', 100), ('teleport', 0), ('wait', 100), ('die',))
                # },
                # 'coffee table 2': {
                #     'already added': False,
                #     'active': True,
                #     'cells': (99,),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     'actions': (('move', (70, )), ('wait', 12), ('move', (68, )), ('wait', 12), ('move', (99, )), ('wait', 12), ('repeat', 0)),
                #     'alternate actions': (('find route', 16), ('wait', 12), ('die',))
                # },
                # 'coffee table 3': {
                #     'already added': False,
                #     'active': True,
                #     'cells': (135,),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'actions': (('move', (137, 139, 141, 143, 145, 147, 149)), ('switch visibility', 0), ('wait', 120), ('teleport', 135), ('switch visibility', 0), ('wait', 12), ('repeat', 0)),
                #     'use alternate actions': False,
                #     'alternate actions': (('find route', 11), ('find route', 111), ('wait', 12), ('die',))
                # },
                'piles 1': {
                # (34, 38, 8): {
                    'active': False,
                    'cells': (45,),
                    'sprite name': ' pile 1x #1',
                    'sprite snap': 'left',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'actions': (('move', (24, 25, 26)), ('stop',))
                },
                'glasses 1': {
                # (35, 37): {
                    'active': False,
                    'cells': (75, 105, 135, 165, 195, 225, 255, 285),
                    'sprite name': ' glass 1x #2',
                    'sprite snap': 'left',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1,
                    'actions': (('move', (24, 25, 26)), ('stop',))
                },
                # 'boxes single': {
                # # (4, 30, 15, 12): {
                #     'active': False,
                #     'cells': (4, 15, 12),
                #     'sprite name': ' box single',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1,
                #     'actions': (('move', (24, 25, 26)), ('stop',))
                # },
                # 'boxes 1.5': {
                #     'active': False,
                #     'cells': (45, 60, 75, 88, 89, 90),
                #     'sprite name': ' box 1.5x #23',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1,
                #     'actions': (('move', (24, 25, 26)), ('repeat',))
                # },
            },
            'items': {
                # 'crate switcher': {
                #     'position': (825, 100),
                #     'destination': (825, 300),
                #     'speed': 0.1,
                #     'sprite': 'question sign',
                #     'available': True,
                #     'mode': 'interact',
                #     # 'mode': 'on touch',
                #     'index': None,
                #     'action': {
                #         'action trigger': True,
                #         'storage': False,
                #         # 'furniture action trigger': True,
                #         'inventory': None,
                #         'multiple': False,
                #         # 'objects': (('field_1', 'obstacles', 'crate #1', 'do actions'),
                #         #             # ('field_1', 'obstacles', 'coffee table', 'do actions'),
                #         #             ),
                #         'target': ("locations['field_1']['obstacles']['crate #1']['do actions']", ),
                #         'action': 'swap state',
                #     },
                #     'TTL': -1,
                #     'description': 'crate door opener',
                #     'scale': 0.4
                # },
                # 'total light switcher': {
                #     'position': (950, 475),
                #     'destination': (950, 475),
                #     # 'position': (870, 300),
                #     # 'destination': (870, 300),
                #     'speed': 0.1,
                #     'sprite': 'void',
                #     # 'sprite': 'question sign',
                #     'available': True,
                #     # 'mode': 'interact',
                #     'mode': 'on touch',
                #     'index': None,
                #     'action': {
                #         'action trigger': True,
                #         'storage': False,
                #         'inventory': None,
                #         'target': ("locations['field_1']['obstacles']['coffee table']['do actions']",
                #                    "locations['field_1']['obstacles']['coffee table 2']['do actions']",
                #                    "locations['field_1']['obstacles']['coffee table 3']['do actions']",
                #                    "locations['village1']['lights on']",
                #                    ),
                #         # 'multiple': True,
                #         'multiple': False,
                #         # 'action': 'off'
                #         'action': 'swap state'
                #     },
                #     'TTL': -1,
                #     'description': 'light switcher',
                #     'scale': 1
                # },
                # 'tables killer': {
                #     'position': (1200, 550),
                #     'destination': (1200, 550),
                #     # 'position': (870, 300),
                #     # 'destination': (870, 300),
                #     'speed': 0.1,
                #     'sprite': 'void',
                #     # 'sprite': 'question sign',
                #     'available': True,
                #     # 'mode': 'interact',
                #     'mode': 'on touch',
                #     'index': None,
                #     'action': {
                #         'action trigger': True,
                #         'storage': False,
                #         'inventory': None,
                #         'target': ("locations['field_1']['obstacles']['coffee table']['do actions']",
                #                    "locations['field_1']['obstacles']['coffee table']['use alternate actions']",
                #                    "locations['field_1']['obstacles']['coffee table 2']['do actions']",
                #                    "locations['field_1']['obstacles']['coffee table 2']['use alternate actions']",
                #                    ),
                #         'multiple': False,
                #         'action': 'True'
                #         # 'action': 'swap state'
                #     },
                #     'TTL': -1,
                #     'description': 'light switcher',
                #     'scale': 1
                # },
                'bag': {
                    'position': (900, 500),
                    'destination': (900, 500),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'sprite snap': 'left',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (brass_garden_key,),
                    },
                    'TTL': -1,
                    'description': 'brass_garden_key',
                    'scale': 0.1
                },
            },
            'lights': {
                'central bulb': {
                    'scaled_sz_x': 5,
                    'scaled_sz_y': 1,
                    'x': 1260,
                    'y': 460,
                    'sprite': 'light halo casual',
                    'glowing': True
                },
                # 'custom bulb': {
                #     'scaled_sz_x': 1,
                #     'scaled_sz_y': 1,
                #     'x': 115,
                #     'y': 558,
                #     'sprite': 'light halo casual',
                #     'glowing': True
                # },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 550,  # 500 if 550 px when cursor shows on this cell
                'start y': 175,  # 200 if 225 px
                'cell width': 100,
                'cell height': 100,
                'max x cells': 30,
                'max y cells': 20,
                'min cell scale': 0.3,
                'scale increase factor': 0,
                'default available': True,
                # If there is a tuple or list instead of single cell number, it means a range.
                # If a tuple or a list consists of two numbers, it means straight range from start to finish.
                # Else it is just a bunch of unavailable cell numbers:
                'not available cells': [1, 2, (8, 29), (38, 44), (330, 344), (360,374),(390,404), (420, 434), (450,464), (480, 494), (510, 524), (540, 554), (570, 584)],
                # 'not available cells': [(49, 52), 55, (64, 80, 96) ],
                'points lead to other locations': {
                    0: {'location': 'field_1', 'point': 74, 'on touch': False, 'need key': False, 'key': None},
                    3: {'location': 'storage_room', 'point': 38, 'on touch': True, 'need key': False, 'key': None},
                    4: {'location': 'storage_room', 'point': 30, 'on touch': True, 'need key': False, 'key': None},
                    5: {'location': 'storage_room', 'point': 22, 'on touch': True, 'need key': False, 'key': None},
                    6: {'location': 'storage_room', 'point': 14, 'on touch': True, 'need key': False, 'key': None},
                    7: {'location': 'storage_room', 'point': 6, 'on touch': True, 'need key': False, 'key': None},
                },
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
    },

    'alley_1':
        {
        'mode': 'wandering',
        'light level': 1.5,
        'lights on': True,
        'description': 'Alley.',
        'sprites type': 'walking figure',
        'actors speed scale': 0.4,
        'sprites orientation': {
            'rotate': False,
            'east-west': True,
            'still': True
        },
        # Availability of participants to pass through each other.
        'pass through': True,
        # 'pass through': False,
        # Is the map is straight net oriented, or it's type is chaotic points mesh.
        # Net-oriented maps use A* algorythm for pathfinding.
        'net': False,
        'isometric': False,
        'scale': {'max': 2.0, 'min': 1., 'amount': 0.5},
        # 'avatar scale': 0.2,
        'avatar scales': True,
        'cell size': 1,
        'points per index': dict(),
        'points per rect': dict(),
        'lights': {
            'custom bulb': {
                'scaled_sz_x': .5,
                'scaled_sz_y': .5,
                'x': 533,
                'y': 334,
                'sprite': 'light halo casual',
                'glowing': True
            },
        },
        'points': {
            0: {
                'leads': {'location': 'village1', 'point': 13, 'on touch': False, 'need key': False, 'key': None},
                'available': True,
                'connected': [1, ],
                'scale': 0.4,
                'rect': pygame.Rect(522,1277,408,71),
                'interactive': True,
                'distances': dict(),
                'name': 'entrance'
            },
            1: {
                'available': True,
                'connected': [2, 0],
                'scale': 0.35,
                'rect': pygame.Rect(554,1189,69,69),
                'interactive': True,
                'distances': dict(),
                'name': 'fontain'
            },

            2: {
                'available': True,
                'connected': [1, 3],
                'scale': 0.15,
                'rect': pygame.Rect(626,743,204,92),
                'interactive': True,
                'distances': dict(),
                'name': 'far'
            },
            3: {
                'available': True,
                'connected': [2, ],
                'scale': 0.05,
                'rect': pygame.Rect(680,456,81,96),
                'interactive': True,
                'distances': dict(),
                'name': 'the very far point'
            },
        }
    },

    'cabinet_1':
        {
        'mode': 'wandering',
        'light level': 1.5,
        'lights on': True,
        # 'lights on': False,
        'description': 'Old-fashioned cabinet.',
        'sprites type': 'walking figure',
        'actors speed scale': 2.5,
        # 'avatar scale': 1.2,
        'avatar scales': True,
        'sprites orientation': {
            'rotate': False,
            'east-west': True,
            'still': False
        },
        # Availability of participants to pass through each other.
        'pass through': True,
        # 'pass through': False,
        # Is the map is straight net oriented, or it's type is chaotic points mesh.
        # Net-oriented maps use A* algorythm for pathfinding.
        'net': False,
        'isometric': False,
        'scale': {'max': 0.51, 'min': 1.5, 'amount': .4},
        'cell size': 1,
        'points per index': dict(),
        'points per rect': dict(),
        'points': {
            0: {
                'attraction': 'bottom',
                'available': True,
                'connected': [4, ],
                'scale': 2.2,
                # 'instant scale': 1.0,
                'rect': pygame.Rect(0,1376,1032,1240),
                'interactive': True,
                'distances': dict(),
                'name': 'chair'
            },
            1: {
                'leads': {'location': 'village1', 'point': 5, 'on touch': False, 'need key': False, 'key': None},
                'attraction': 'bottom',
                'available': True,
                'connected': [0, 3],
                'scale': 4,
                # 'instant scale': 0.6,
                'rect': pygame.Rect(2427,18,277,2686),
                'interactive': True,
                'distances': dict(),
                'name': 'entrance'
            },
            3: {
                # 'leads': {'location': 'village1', 'point': 5},
                'attraction': 'bottom',
                'available': True,
                'connected': [4, 1],
                'scale': 2,
                'rect': pygame.Rect(1023,1647,627,552),
                'interactive': True,
                'distances': dict(),
                'name': 'bookshelf'
            },
            4: {
                # 'leads': {'location': 'village1', 'point': 5},
                'attraction': 'bottom',
                'available': True,
                'connected': [0, 1, 3],
                'scale': 2.2,
                'rect': pygame.Rect(1035,2445,150,162),
                'interactive': False,
                'distances': dict(),
                'name': 'middle point'
            },
        },
        'lights': {}
    },

    'village1':
        {
        'mode': 'wandering',
        'light level': 0.5,
        'lights on': False,
        'description': 'North side of the village of Doublegate',
        # 'sprites type': 'icon',
        'sprites type': 'walking figure',
        'sprites orientation': {
            'rotate': False,
            'east-west': True,
            'still': False
        },
        # Availability of participants to pass through each other.
        'pass through': True,
        # Is the map is straight net oriented, or it's type is chaotic points mesh.
        # Net-oriented maps use A* algorythm for pathfinding.
        'net': False,
        'isometric': False,
        'scale': {'max': 1.25, 'min': 0.75, 'amount': .1},
        # 'avatar scale': 0.3,
        'avatar scales': False,
        'actors speed scale': .5,
        'cell size': 100,
        'points per index': dict(),
        'points per rect': dict(),
        'items': {
            'light on': {
                'already added': False,
                'position': (1100, 533),
                'destination': (1100, 533),
                'speed': 0.1,
                'sprite': None,
                # 'sprite': 'void',
                # 'sprite': 'question sign',
                'available': True,
                # 'mode': 'interact',
                'mode': 'on touch',
                'index': None,
                'action': {
                    'action trigger': True,
                    'storage': False,
                    # 'furniture action trigger': True,
                    'inventory': None,
                    # 'multiple': True,
                    'multiple': False,
                    # 'objects': (('field_1', 'obstacles', 'crate #1', 'do actions'),
                    #             # ('field_1', 'obstacles', 'coffee table', 'do actions'),
                    #             ),
                    'target': ("locations['village1']['lights on'] = True if not locations['village1']['lights on'] else False",),
                },
                'TTL': -1,
                'description': 'light on',
                'scale': 0.4
            },
        },
        'lights': {
            'central bulb': {
                'scaled_sz_x': 1,
                'scaled_sz_y': 1,
                'x': 680,
                'y': 517,
                'sprite': 'light halo casual',
                'glowing': False
            },
            'custom bulb': {
                'scaled_sz_x': .2,
                'scaled_sz_y': .2,
                'x': 760,
                'y': 162,
                'sprite': 'light halo casual',
                'glowing': False
            },
        },
        'points': {
            0: {
                'connected': (13,),
                'available': True,
                'scale': .1,
                'rect': pygame.Rect(654, 939, 112, 69),
                'interactive': True,
                'distances': dict(),
                'name': 'Entrance'
            },
            3: {
                'leads': {'location': 'living_room_1', 'point': 0, 'on touch': False, 'need key': False, 'key': None},
                'connected': (13,),
                'available': True,
                'scale': .1,
                'rect': pygame.Rect(560, 35, 416, 214),
                'interactive': True,
                'distances': dict(),
                'name': 'Church of St. Farting'
            },

            5: {
                'leads': {'location': 'cabinet_1', 'point': 1, 'on touch': False, 'need key': False, 'key': None},
                'connected': (12,),
                'available': True,
                'scale': .1,
                # 'rect': pygame.Rect(537,435,245,255),
                'rect': pygame.Rect(575, 500, 167, 143),
                'interactive': True,
                'distances': dict(),
                'name': 'Tavern'
            },
            10: {
                'available': True,
                'scale': .1,
                'connected': (12,),
                'rect': pygame.Rect(222, 391, 44, 47),
                'interactive': True,
                'distances': dict(),
                'name': 'waypoint 10'
            },
            12: {
                'available': True,
                'scale': .1,
                'connected': (5, 13, 10),
                'rect': pygame.Rect(641, 465, 38, 36),
                'interactive': True,
                'distances': dict(),
                'name': 'waypoint 12'
            },
            13: {
                'available': True,
                'scale': .1,
                'leads': {'location': 'alley_1', 'point': 3, 'on touch': False },
                'connected': (3, 0, 12, 16),
                'rect': pygame.Rect(787, 467, 55, 55),
                'interactive': True,
                'distances': dict(),
                'name': 'waypoint 13'
            },
            16: {
                'leads': {'location': 'field_1', 'point': 1, 'on touch': False, 'need key': False, 'key': None},
                'available': True,
                'scale': .1,
                'connected': (13,),
                'rect': pygame.Rect(1181, 503, 48, 47),
                    'interactive': True,
                    'distances': dict(),
                'name': 'waypoint 16'
            },
        }
    },

    'storage_room':
        {
            'mode': 'wandering',
            'light level': 1.2,
            'lights on': True,
            # 'lights on': False,
            'description': 'Field behind the Central Store',
            'scale': {'max': 1.3, 'min': 0.65, 'amount': .09},
            # 'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.2,
            'avatar scales': False,
            'actors speed scale': 1.7,
            'cell size': 100,
            'sprites type': 'walking figure',  # 'icon'
            'sprites orientation': {
                # 'rotate': True,
                'rotate': False,
                # 'east-west': False,
                'east-west': True,
                'still': False
                # 'still': True
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            # 'isometric': False,
            # 'net': False,
            'obstacles': {
                # Possible actions:
                # ('move', (99, 102, 55)): move object through the list of given points, ignoring obstacles.
                # ('wait', 100): wait given game cycles.
                # ('repeat', 0):  if zero, repeat all preceding actions unlimited number of times, else repeat given number.
                # ('die',): get suicide.
                # ('find route', 46): build A* route to a given point considering obstacles.

                # 'crate #1': {
                # # 23: {
                #     # 'active': False,
                #     'active': True,
                #     'cells': (23,),
                #     'sprite name': ' metal crate #1 frame 0',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     # 'description': 'crate id 1',
                #     'scale': 1,
                #     'speed': 0.1,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     # 'actions': (('switch visibility',), ('switch passability',), ),
                #     'actions': (('move', (24, 9)), ('stop', ), ('move', (24, 23)),),
                #     # 'alternate actions': (('move', (24, 23)), )
                #     # 'actions': (('move', (24, 9)), ('wait', 2), ('repeat', 3), ('move', (10, )), ('wait', 100),  ('die', ))
                # },
                # 'coffee table': {
                # 'already added': False,
                #     'active': True,
                #     'cells': (68, ),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     'actions': (('find route', 46), ('find route', 68), ('repeat', 0)),
                #     # 'actions': (('move', (99, )), ('wait', 12), ('move', (70, )), ('wait', 12), ('move', (68, )), ('wait', 12), ('repeat', 0)),
                #     'alternate actions': (('teleport', 0), ('wait', 100), ('die',))
                #     # 'alternate actions': (('find route', 46), ('move', (47, )), ('wait', 100), ('teleport', 0), ('wait', 100), ('die',))
                # },
                # 'coffee table 2': {
                #     'already added': False,
                #     'active': True,
                #     'cells': (99,),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'use alternate actions': False,
                #     'actions': (('move', (70, )), ('wait', 12), ('move', (68, )), ('wait', 12), ('move', (99, )), ('wait', 12), ('repeat', 0)),
                #     'alternate actions': (('find route', 16), ('wait', 12), ('die',))
                # },
                # 'coffee table 3': {
                #     'already added': False,
                #     'active': True,
                #     'cells': (135,),
                #     'sprite name': ' coffee table',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'table',
                #     'scale': 1,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'actions': (('move', (137, 139, 141, 143, 145, 147, 149)), ('switch visibility', 0), ('wait', 120), ('teleport', 135), ('switch visibility', 0), ('wait', 12), ('repeat', 0)),
                #     'use alternate actions': False,
                #     'alternate actions': (('find route', 11), ('find route', 111), ('wait', 12), ('die',))
                # },
                # 'piles 1': {
                # # (34, 38, 8): {
                #     'active': False,
                #     'cells': (6,13,20,27,34),
                #     'sprite name': ' pile 1x #1',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1.5,
                #     'actions': (('move', (24, 25, 26)), ('stop',))
                # },
                # 'glasses 1': {
                # # (35, 37): {
                #     'active': False,
                #     'cells': (31, 32, 33, 35, 36, 37),
                #     'sprite name': ' glass 1x #1',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1,
                #     'actions': (('move', (24, 25, 26)), ('stop',))
                # },
                # 'boxes single': {
                # # (4, 30, 15, 12): {
                #     'active': False,
                #     'cells': (33,32,31,30,29,28),
                #     'sprite name': ' box single',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1.5,
                #     'actions': (('move', (24, 25, 26)), ('stop',))
                # },
                # 'boxes 1.5': {
                #     'active': False,
                #     'cells': (45, 60, 75, 88, 89, 90),
                #     'sprite name': ' box 1.5x #23',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1,
                #     'actions': (('move', (24, 25, 26)), ('repeat',))
                # },
            },
            'items': {
#                 'crate switcher': {
#                     'position': (900, 450),
#                     'destination': (900, 450),
#                     'size': (100, 50),
#                     'speed': 0.1,
#                     'sprite': 'void',
#                     # 'sprite': 'question sign',
#                     'available': True,
#                     'mode': 'interact',
#                     # 'mode': 'on touch',
#                     'index': None,
#                     'action': {
#                         'action trigger': True,
#                         'storage': False,
#                         # 'furniture action trigger': True,
#                         'inventory': None,
#                         'multiple': True,
#                         # 'objects': (('field_1', 'obstacles', 'crate #1', 'do actions'),
#                         #             # ('field_1', 'obstacles', 'coffee table', 'do actions'),
#                         #             ),
#                         # 'target': ("self.obstacles[self.location]['crate #1'].active = False", ),
#                         'target': ("locations['field_1']['obstacles']['crate #1']['do actions'] = True", ),
# #                         'target': ("""locations['field_1']['obstacles']['crate #1']['do actions'] = False if locations['field_1']['obstacles']['crate #1']['do actions'] else True
# # locations['field_1']['obstacles']['crate #1']['do alternate actions'] = False if locations['field_1']['obstacles']['crate #1']['do actions'] else True""", ),
#                     },
#                     'TTL': -1,
#                     'description': 'crate door opener',
#                     'scale': 0.4
#                 },
#                 'total light switcher': {
#                     'position': (950, 475),
#                     'destination': (950, 475),
#                     # 'position': (870, 300),
#                     # 'destination': (870, 300),
#                     'speed': 0.1,
#                     'sprite': 'void',
#                     # 'sprite': 'question sign',
#                     'available': True,
#                     # 'mode': 'interact',
#                     'mode': 'on touch',
#                     'index': None,
#                     'action': {
#                         'action trigger': True,
#                         'storage': False,
#                         'inventory': None,
#                         'target': ("locations['field_1']['obstacles']['coffee table']['do actions'] = True",
#                                    "locations['field_1']['obstacles']['coffee table 2']['do actions'] = True",
#                                    "locations['field_1']['obstacles']['coffee table 3']['do actions'] = True",
#                                    "locations['village1']['lights on'] = True",
#                                    ),
#                         # 'multiple': True,
#                         'multiple': False,
#                     },
#                     'TTL': -1,
#                     'description': 'light switcher',
#                     'scale': 1
#                 },
#                 'tables killer': {
#                     'position': (1200, 550),
#                     'destination': (1200, 550),
#                     # 'position': (870, 300),
#                     # 'destination': (870, 300),
#                     'speed': 0.1,
#                     'sprite': 'void',
#                     # 'sprite': 'question sign',
#                     'available': True,
#                     # 'mode': 'interact',
#                     'mode': 'on touch',
#                     'index': None,
#                     'action': {
#                         'action trigger': True,
#                         'storage': False,
#                         'inventory': None,
#                         'target': ("locations['field_1']['obstacles']['coffee table']['do actions'] = True",
#                                    "locations['field_1']['obstacles']['coffee table']['use alternate actions'] = True",
#                                    "locations['field_1']['obstacles']['coffee table 2']['do actions'] = True",
#                                    "locations['field_1']['obstacles']['coffee table 2']['use alternate actions'] = True",
#                                    "locations['field_1']['lights on'] = False if locations['field_1']['lights on'] else True",
#                                    "self.mouse_wheel_rolls = True",
#                                    "self.mouse_wheel_up = True"
#                                    ),
#                         # 'multiple': True,
#                         'multiple': False,
#                     },
#                     'TTL': -1,
#                     'description': 'light switcher',
#                     'scale': 1
#                 },
#                 'bag': {
#                     'position': (900, 500),
#                     'destination': (900, 500),
#                     'speed': 0.1,
#                     'sprite': 'question sign',
#                     'available': True,
#                     # 'mode': 'interact',
#                     'mode': 'on touch',
#                     'index': None,
#                     'action': {
#                         'action trigger': False,
#                         'storage': True,
#                         'multiple': False,
#                         'inventory': (brass_garden_key,),
#                     },
#                     'TTL': -1,
#                     'description': 'brass_garden_key',
#                     'scale': 0.1
#                 },
            },
            'lights': {
                'central bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 1,
                    'x': 1260,
                    'y': 460,
                    'sprite': 'light halo casual',
                    'glowing': False
                },
                'custom bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 1,
                    'x': 115,
                    'y': 558,
                    'sprite': 'light halo casual',
                    'glowing': True
                },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 900,
                'start y': 560,
                'cell width': 200,
                'cell height': 200,
                'max x cells': 8,
                'max y cells': 5,
                'min cell scale': 1,
                'scale increase factor': 0,
                'default available': True,
                # If there is a tuple or list instead of single cell number, it means a range.
                # If a tuple or a list consists of two numbers, it means straight range from start to finish.
                # Else it is just a bunch of unavailable cell numbers:
                'not available cells': (),
                # 'not available cells': [(49, 52), 55, (64, 80, 96) ],
                'points lead to other locations': {
                    0: {'location': 'field_1', 'point': 29, 'on touch': True, 'need key': False, 'key': None},
                    7: {'location': 'cave_1', 'point': 37, 'on touch': True, 'need key': False, 'key': None},
                    15: {'location': 'cave_1', 'point': 36, 'on touch': True, 'need key': False, 'key': None},
                    23: {'location': 'cave_1', 'point': 35, 'on touch': True, 'need key': False, 'key': None},
                    31: {'location': 'cave_1', 'point': 34, 'on touch': True, 'need key': False, 'key': None},
                    39: {'location': 'cave_1', 'point': 33, 'on touch': True, 'need key': False, 'key': None},
                },
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
    },

    'apartment_01_main_room':
        {
            'mode': 'wandering',
            'music': music_ambient_1,
            'light level': 1.2,
            'lights on': True,
            # 'lights on': False,
            'description': 'apartment #1',
            'scale': {'max': 1.0, 'min': 0.5, 'amount': .1},
            # 'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.2,
            'avatar scales': False,
            'actors speed scale': 1,
            'cell size': 1,  # No use. Be good to remove it in the future.
            'sprites type': 'walking figure',  # 'icon'
            'sprites orientation': {
                # 'rotate': True,
                'rotate': False,
                # 'east-west': False,
                'east-west': True,
                'still': False
                # 'still': True
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            # 'hostiles': {
            #     'ZAK': [30, 29, 28, 103, 197, 198],
            # },
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            'hostiles': {
                # 'demon Hula': {
                #     'already added': False,
                #     'point on map': 121,
                # },
                # 'demon Hildegarda': {
                #     'already added': False,
                #     'point on map': 103,
                # }

            },
            # 'isometric': False,
            # 'net': False,
            'obstacles': {
                # Possible actions:
                # ('move', (99, 102, 55)): move object through the list of given points, ignoring obstacles.
                # ('wait', 100): wait given game cycles.
                # ('repeat', 0):  if zero, repeat all preceding actions unlimited number of times, else repeat given number.
                # ('die',): get suicide.
                # ('find route', 46): build A* route to a given point considering obstacles.

                # 'pinetree 1': {
                #     'already added': False,
                #     'active': False,
                #     'cells': (74,),
                #     'sprite name': 'pinetree',
                #     'sprite snap': 'center',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'pinetree',
                #     'scale': .3,
                #     'speed': 6,
                #     'do actions': False,
                #     'actions': (),
                #     'use alternate actions': False,
                #     'alternate actions': ()
                # },
                # 'pinetree 2': {
                #     'already added': False,
                #     'active': False,
                #     'cells': (78,),
                #     'sprite name': 'pinetree',
                #     'sprite snap': 'center',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'pinetree',
                #     'scale': 1.3,
                #     'speed': 0.6,
                #     'do actions': False,
                #     'actions': (),
                #     'use alternate actions': False,
                #     'alternate actions': ()
                # },
                'void': {
                    'already added': False,
                    'stops bullets': True,
                    'active': False,
                    'cells': (180,181,182,86,102,118,134,150,166),
                    'sprite name': None,
                    'sprite snap': 'left',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'invisible obstacle',
                    'scale': 0,
                    'actions': ()
                },
                'piles 1': {
                    'already added': False,
                    'stops bullets': True,
                    'active': False,
                    'cells': (121,122,137,153,154,155, 185,186,187,202,218,189,190,206,222),
                    'sprite name': 'pile 1x #1',
                    'sprite snap': 'left',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1.4,
                    'actions': None
                },
                # # 'glasses 1': {
                # # # (35, 37): {
                # #     'active': False,
                # #     'cells': (31, 32, 33, 35, 36, 37),
                # #     'sprite name': ' glass 1x #1',
                # #     'available': True,
                # #     'index': None,
                # #     'TTL': -1,
                # #     'description': 'BIG QUESTION',
                # #     'scale': 1,
                # #     'actions': (('move', (24, 25, 26)), ('stop',))
                # # },
                # 'boxes single': {
                #     'already added': False,
                #     'stops bullets': False,
                #     'active': False,
                #     'cells': (218,185,186,201,202,217),
                #     'sprite name': 'box single',
                #     'sprite snap': 'left',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1.5,
                #     'actions': (('move', (24, 25, 26)), ('stop',))
                # },
                # 'boxes 1.5': {
                #     'already added': False,
                #     'active': False,
                #     #
                #     'cells': (175,191,207,223,239,),
                #     # 'cells': (63,79,95,111,127,143,159,175,191,207,223,239,),
                #     'sprite name': 'box 1.5x #23',
                #     'sprite snap': 'left',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1.3,
                #     'actions': (('move', (24, 25, 26)), ('repeat',))
                # },
            },
            'items': {
                'central light switcher': {
                    'already added': False,
                    'position': (837, 793),
                    'destination': (837, 793),
                    'associated point': 183,
                    # 'position': (870, 300),
                    # 'destination': (870, 300),
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'light switch #2',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                        "self.locations['apartment_01_main_room']['lights']['central bulb']['glowing'] = False if self.locations['apartment_01_main_room']['lights']['central bulb']['glowing'] else True",
                        "self.locations['apartment_01_kitchen']['lights']['main room bulb']['glowing'] = False if self.locations['apartment_01_kitchen']['lights']['main room bulb']['glowing'] else True",
                        "self.lights_generate_static_illumination()",
                        "self.scaling_static_lights_image()",
                        "self.put_sound_to_queue((sounds_all['sound_click_4'][0], sounds_all['sound_click_4'][1], self.wandering_actors[self.current_wandering_actor]))",
                        # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 0.8
                },
                'kitchen light switcher': {
                    'already added': False,
                    'position': (1271, 576),
                    'destination': (1271, 576),
                    'associated point': 87,
                    # 'position': (870, 300),
                    # 'destination': (870, 300),
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'light switch #2',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                            "self.locations['apartment_01_kitchen']['lights']['custom bulb']['glowing'] = False if self.locations['apartment_01_kitchen']['lights']['custom bulb']['glowing'] else True",
                            "self.locations['apartment_01_main_room']['lights']['kitchen bulb']['glowing'] = False if self.locations['apartment_01_main_room']['lights']['kitchen bulb']['glowing'] else True",
                            "self.lights_generate_static_illumination()",
                            "self.scaling_static_lights_image()",
                            "self.put_sound_to_queue((sounds_all['sound_click_4'][0], sounds_all['sound_click_4'][1], self.wandering_actors[self.current_wandering_actor]))",
                            # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 0.8
                },
                'bathroom door': {
                    'already added': False,
                    'position': (660, 718),
                    'destination': (660, 718),
                    'associated point': 197,
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'wooden door #1 frame 0',
                    'available': True,
                    'mode': 'interact',
                    'need key': True,
                    'key': brass_garden_key,
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                        "self.consider_location_change(self.wandering_actors[self.current_wandering_actor], 'field_1', 73)",
                        "self.load_new_location['new location'] = 'field_1'",
                        "self.put_sound_to_queue((sounds_all['sound_door_1'][0], sounds_all['sound_door_1'][1], self.wandering_actors[self.current_wandering_actor]))",
                        # "self.wandering_actor.point_on_map = 34",
                        # "self.change_location('cave_1', 34)",
                        # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'A doorway.',
                    'scale': 1
                },
                'outside door': {
                    'already added': False,
                    'position': (530, 655),
                    'destination': (530, 655),
                    'associated point': 195,
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'wooden door #1 frame 0',
                    'available': True,
                    'mode': 'interact',
                    'need key': True,
                    'key': brass_garden_key,
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                            "self.consider_location_change(self.wandering_actors[self.current_wandering_actor], 'village1', 16)",
                            "self.load_new_location['new location'] = 'village1'",
                            "self.put_sound_to_queue((sounds_all['sound_door_1'][0], sounds_all['sound_door_1'][1], self.wandering_actors[self.current_wandering_actor]))",
                            # "self.wandering_actor.point_on_map = 34",
                            # "self.change_location('cave_1', 34)",
                            # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'A doorway.',
                    'scale': 1
                },
                'front door light switcher': {
                    'already added': False,
                    'position': (763,800),
                    'destination': (763, 800),
                    'associated point': 198,
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'light switch #1',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': ("self.locations['apartment_01_main_room']['lights']['front door bulb']['glowing'] = False if self.locations['apartment_01_main_room']['lights']['front door bulb']['glowing'] else True",
                                   # "self.wandering_screen_scale_counter = self.wandering_max_scale",
                                   # "self.wandering_screen_scale = self.wandering_max_scale",
                                   # "self.screen_zoom_in()",
                                   # "self.screen_scaling()",
                                   # "self.instant_follow = True",
                                   "self.lights_generate_static_illumination()",
                                   "self.scaling_static_lights_image()",
                                   "self.put_sound_to_queue((sounds_all['sound_click_4'][0], sounds_all['sound_click_4'][1], self.wandering_actors[self.current_wandering_actor]))",
                                   # "print('light switched')"
                                   ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 0.8
                },
                'brass key': {
                    'already added': False,
                    'position': (500, 800),
                    'destination': (500, 800),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (brass_garden_key,),
                    },
                    'TTL': -1,
                    'description': 'brass_garden_key',
                    'scale': 0.2
                },
                'flashlight': {
                    'already added': False,
                    'position': (420,900),
                    'destination': (420,900),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (flashlight,),
                    },
                    'TTL': -1,
                    'description': 'Regular 3-AAA LED flash light.',
                    'scale': 0.2
                },
                'shotgun': {
                    'already added': False,
                    'position': (280,660),
                    'destination': (280,660),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (shotgun, pistol_9mm_ammo, pistol_9mm, shotgun_ammo),
                    },
                    'TTL': -1,
                    'description': 'shotgun',
                    'scale': 0.2
                },
                'shells': {
                    'already added': False,
                    'position': (1325, 977),
                    'destination': (1325, 977),
                    'speed': 0.1,
                    'sprite': 'question sign',
                    'available': True,
                    # 'mode': 'interact',
                    'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': False,
                        'storage': True,
                        'multiple': False,
                        'inventory': (shotgun_ammo, shotgun_ammo, shotgun_ammo, shotgun_ammo),
                    },
                    'TTL': -1,
                    'description': 'shotgun',
                    'scale': 0.2
                },

            },
            'lights': {
                # # 'central bulb': {
                # #     'scaled_sz_x': 2,
                # #     'scaled_sz_y': 2,
                # #     'x': 1500,
                # #     'y': 900,
                # #     'sprite': 'light halo casual',
                # #     'static': True,
                # #     'glowing': True
                # #     # 'glowing': False
                # # },
                # 'kitchen bulb': {
                #     'scaled_sz_x': .7,
                #     'scaled_sz_y': 3.5,
                #     'x': 1392,
                #     'y': 550,
                #     'sprite': 'light halo mild',
                #     'static': True,
                #     'glowing': True
                # },
                # # 'window bulb spot': {
                # #     'scaled_sz_x': .3,
                # #     'scaled_sz_y': 3,
                # #     'x': 2254,
                # #     'y': 608,
                # #     'sprite': 'light halo strong',
                # #     'static': True,
                # #     'glowing': True
                # # },
                # 'front door bulb': {
                #     'scaled_sz_x': 1,
                #     'scaled_sz_y': 1,
                #     'x': 500,
                #     'y': 560,
                #     'sprite': 'light halo mild',
                #     'static': True,
                #     'glowing': True
                # },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 1100,
                'start y': 200,
                'cell width': 150,
                'cell height': 150,
                'max x cells': 16,
                'max y cells': 15,
                'min cell scale': 1,
                'scale increase factor': 0,
                'instant scale points': {
                    # A tuple with two points is a range between point_1 and point_2;
                    # a single number is a single point;
                    # a tuple with more than two digits is just a bunch of points, not range.
                    # 1.2: ((192,198),(208,214),225,226,(227,228,229,230)),
                    # 0.6: (233,234)
                },
                'default available': True,
                # If there is a tuple or list instead of single cell number, it means a range.
                # If a tuple or a list consists of two numbers, it means straight range from start to finish.
                # Else it is just a bunch of unavailable cell numbers:
                'not available cells': [(16,24), (32,40),(48,56),(64,70), (0,9), (11,15), (80,86),(96,102),(112,118),(128,134),(144,150),(160,166),(176,182),25,41,57,73],
                # 'not available cells': [(49, 52), 55, (64, 80, 96) ],
                'points lead to other locations': {
                    71: {'location': 'apartment_01_kitchen', 'point': 30, 'on touch': True, 'need key': False, 'key': None},
                    72: {'location': 'apartment_01_kitchen', 'point': 31, 'on touch': True, 'need key': False, 'key': None},
                    # 10: {'location': 'apartment_01_kitchen', 'point': 30, 'on touch': False, 'need key': False, 'key': None},
                    10: {'location': 'level_1', 'point': 0, 'on touch': True, 'need key': False, 'key': None},
                    31: {'location': 'gen_1', 'point': 1, 'on touch': True, 'need key': False, 'key': None},
                    # 39: {'location': 'cave_1', 'point': 33, 'on touch': False, 'need key': False, 'key': None},
                },
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
    },

    'apartment_01_kitchen':
        {
            'mode': 'wandering',
            'light level': 1.2,
            # 'lights on': True,
            'lights on': False,
            'description': 'apartment #1',
            'scale': {'max': 1.0, 'min': 0.5, 'amount': .5},
            # 'scale': {'max': 1.25, 'min': 0.65, 'amount': .5},
            # 'avatar scale': 0.2,
            'avatar scales': False,
            'actors speed scale': 0.8,
            'cell size': 40,
            'sprites type': 'walking figure',  # 'icon'
            'sprites orientation': {
                # 'rotate': True,
                'rotate': False,
                # 'east-west': False,
                'east-west': True,
                'still': False
                # 'still': True
            },
            # Availability of participants to pass through each other.
            # 'pass through': True,
            'pass through': False,
            'hostiles': {
                # 'zak': [3, 5, 12],
                # 'demon Hula': {
                #     'already added': False,
                #     'point on map': 13,
                # },
                # 'demon Hildegarda': {
                #     'already added': False,
                #     'point on map': 3,
                # }
                # 'demon Hula': 2,
                # 'demon hula': [2, 10],
            },
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': True,
            'isometric': True,
            # 'isometric': False,
            # 'net': False,
            'obstacles': {
                'coffee table 1': {
                    'already added': False,
                    'active': False,
                    'cells': (5,6,7, ),
                    'sprite name': 'coffee table',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'table',
                    'scale': 1.3,
                    'sprite snap': 'left',
                    'speed': 0.6,
                    'do actions': False,
                    'action number': 0,
                    'actions': None,
                },
                'piles 1': {
                    'already added': False,
                    'active': False,
                    'cells': (0,8,16,24),
                    'sprite name': 'pile 1x #1',
                    'available': True,
                    'index': None,
                    'TTL': -1,
                    'description': 'BIG QUESTION',
                    'scale': 1.3,
                    'sprite snap': 'left',
                    'actions': None
                },
            },
            'items': {
            },
            'lights': {
                'main room bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 3.5,
                    'x': 778,
                    'y': 700,
                    'sprite': 'light halo strong',
                    'static': True,
                    'glowing': True,
                    # 'glowing': True
                },
                'custom bulb': {
                    'scaled_sz_x': 2,
                    'scaled_sz_y': 2,
                    'x': 670,
                    'y': 500,
                    'sprite': 'light halo casual',
                    'static': True,
                    'glowing': True
                },
            },
            'net settings': {
                'cell start index': 0,
                'start x': 473,
                'start y': 270,
                'cell width': 150,
                'cell height': 150,
                'max x cells': 8,
                'max y cells': 5,
                'min cell scale': 0.5,
                'scale increase factor': 0,
                'default available': True,
                # If there is a tuple or list instead of single cell number, it means a range.
                # If a tuple or a list consists of two numbers, it means straight range from start to finish.
                # Else it is just a bunch of unavailable cell numbers:
                'not available cells': [(32, 37),],
                # 'not available cells': [(49, 52), 55, (64, 80, 96) ],
                'points lead to other locations': {
                    39: {'location': 'apartment_01_main_room', 'point': 88, 'on touch': True, 'need key': False, 'key': None},
                    38: {'location': 'apartment_01_main_room', 'point': 87, 'on touch': True, 'need key': False, 'key': None},
                    # 7: {'location': 'cave_1', 'point': 37, 'on touch': False, 'need key': False, 'key': None},
                    # 15: {'location': 'cave_1', 'point': 36, 'on touch': False, 'need key': False, 'key': None},
                    # 23: {'location': 'cave_1', 'point': 35, 'on touch': False, 'need key': False, 'key': None},
                    # 31: {'location': 'cave_1', 'point': 34, 'on touch': False, 'need key': False, 'key': None},
                    # 39: {'location': 'cave_1', 'point': 33, 'on touch': False, 'need key': False, 'key': None},
                },
            },
            'points': dict(),
            'points per index': dict(),
            'points per rect': dict()
    },

    'level_1':
        {
            'mode': 'wandering',
            'light level': 0.5,
            'lights on': True,
            'description': 'North side of the village of Doublegate',
            # 'sprites type': 'icon',
            'sprites type': 'walking figure',
            'sprites orientation': {
                'rotate': False,
                'east-west': True,
                'still': False
            },
            # Availability of participants to pass through each other.
            'pass through': True,
            # Is the map is straight net oriented, or it's type is chaotic points mesh.
            # Net-oriented maps use A* algorythm for pathfinding.
            'net': False,
            'isometric': False,
            'scale': {'max': 1., 'min': 1., 'amount': .1},
            # 'avatar scale': 0.3,
            'avatar scales': False,
            'actors speed scale': 1.5,
            'cell size': 100,
            'points per index': dict(),
            'points per rect': dict(),
            'items': {
            },
            'lights': {
                'central bulb': {
                    'scaled_sz_x': 1,
                    'scaled_sz_y': 1,
                    'x': 680,
                    'y': 517,
                    'sprite': 'light halo casual',
                    'glowing': False
                },
                'custom bulb': {
                    'scaled_sz_x': .2,
                    'scaled_sz_y': .2,
                    'x': 760,
                    'y': 162,
                    'sprite': 'light halo casual',
                    'glowing': False
                },
            },
            'points': {
                0: {
                    'connected': (1,2),
                    'available': True,
                    'scale': .5,
                    'rect': pygame.Rect(47,715,178,48),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'Entrance'
                },
                1: {
                    'leads': {'location': 'living_room_1', 'point': 0, 'on touch': False, 'need key': False, 'key': None},
                    'connected': (0,),
                    'available': True,
                    'scale': .5,
                    'rect': pygame.Rect(52,681,109,35),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'Church of St. Farting'
                },

                2: {
                    'leads': {'location': 'cabinet_1', 'point': 1, 'on touch': False, 'need key': False, 'key': None},
                    'connected': (0,3),
                    'available': True,
                    'scale': .5,
                    # 'rect': pygame.Rect(537,435,245,255),
                    'rect': pygame.Rect(441,715,94,42),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'Tavern'
                },
                3: {
                    'available': True,
                    'scale': .5,
                    'connected': (2,4),
                    'rect': pygame.Rect(819,699,171,63),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'waypoint 10'
                },
                4: {
                    'available': True,
                    'scale': .5,
                    'connected': (3,5),
                    'rect': pygame.Rect(1289,709,254,54),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'waypoint 12'
                },
                5: {
                    'available': True,
                    'scale': .5,
                    'leads': {'location': 'alley_1', 'point': 3, 'on touch': False},
                    'connected': (4,),
                    'rect': pygame.Rect(1835,511,213,132),
                    'interactive': True,
                    'distances': dict(),
                    'name': 'waypoint 13'
                },

            }
        },

    # 'generated':
    #     {
    #         'mode': 'wandering',
    #         'light level': 1.0,
    #         # 'lights on': True,
    #         'lights on': False,
    #         'description': 'generated maze #1',
    #         'scale': {'max': 1.0, 'min': 0.9, 'amount': .1},
    #         'avatar scales': False,
    #         'actors speed scale': 1.2,
    #         'cell size': 40,
    #         'sprites type': 'walking figure',  # 'icon'
    #         'sprites orientation': {
    #             # 'rotate': True,
    #             'rotate': False,
    #             # 'east-west': False,
    #             'east-west': True,
    #             'still': False
    #             # 'still': True
    #         },
    #         # Availability of participants to pass through each other.
    #         # 'pass through': True,
    #         'pass through': False,
    #         'hostiles': {
    #             # 'zak': [3, 5, 12],
    #             # 'demon Hula': {
    #             #     'already added': False,
    #             #     'point on map': 13,
    #             # },
    #             # 'demon Hildegarda': {
    #             #     'already added': False,
    #             #     'point on map': 3,
    #             # }
    #             # 'demon Hula': 2,
    #             # 'demon hula': [2, 10],
    #         },
    #         # Is the map is straight net oriented, or it's type is chaotic points mesh.
    #         # Net-oriented maps use A* algorythm for pathfinding.
    #         'net': True,
    #         'isometric': True,
    #         # 'isometric': False,
    #         # 'net': False,
    #         'obstacles': {
    #
    #         },
    #         'items': {
    #         },
    #         'lights': {
    #
    #         },
    #         'net settings': {
    #             'cell start index': 0,
    #             'start x': 0,
    #             'start y': 0,
    #             'cell width': 100,
    #             'cell height': 100,
    #             'max x cells': 0,
    #             'max y cells': 0,
    #             'min cell scale': 1.,
    #             'scale increase factor': 0,
    #             'default available': True,
    #             # If there is a tuple or list instead of single cell number, it means a range.
    #             # If a tuple or a list consists of two numbers, it means straight range from start to finish.
    #             # Else it is just a bunch of unavailable cell numbers:
    #             'not available cells': list(),
    #             'points lead to other locations': dict(),
    #                 # 39: {'location': 'apartment_01_main_room', 'point': 88, 'on touch': True, 'need key': False, 'key': None},
    #                 # 38: {'location': 'apartment_01_main_room', 'point': 87, 'on touch': True, 'need key': False, 'key': None},
    #                 # 7: {'location': 'cave_1', 'point': 37, 'on touch': False, 'need key': False, 'key': None},
    #                 # 15: {'location': 'cave_1', 'point': 36, 'on touch': False, 'need key': False, 'key': None},
    #                 # 23: {'location': 'cave_1', 'point': 35, 'on touch': False, 'need key': False, 'key': None},
    #                 # 31: {'location': 'cave_1', 'point': 34, 'on touch': False, 'need key': False, 'key': None},
    #                 # 39: {'location': 'cave_1', 'point': 33, 'on touch': False, 'need key': False, 'key': None},
    #         },
    #         'points': dict(),
    #         'points per index': dict(),
    #         'points per rect': dict()
    #     },
}