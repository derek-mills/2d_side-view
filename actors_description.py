from weapons import *
# from game_objects import *
from random import randint

demon_1 = {
    'name': 'demon 1',
    'start_xy': (1500, 200),
    'health': 1000.,
    'height': 190,
    'width': 49,
    'body state': {
        'viewing range': 600,
        'regeneration ability': 0.001,
        'blood volume': 15000,
        'blood volume replenish': .01,
        'stamina replenish': 1,
        'consciousness replenish': 10,
        'consciousness threshold': 10,
        'bleeding reduce': .01,  #
        'bleeding resistance': 0,  # Reduce bleeding, in percents.
        'max blood volume': 15000,
        'max stamina': 120,
        'max fatigue': 100,
        'max consciousness': 1000,
        'luck': 5,
        'strength': 25,
        'weight': 70,  # Kilos.
    },
    'gravity affected': True,
    'body': {
        'head': {
            'hardness': 100
        },
    },
    # 'action points': 100,
    'max speed': 2,
    # 'reflexes': randint(100, 150),
    # 'uses light source': False,
    'items': (kitchen_knife,),
    # 'avatar': 'Jake',
    'animations': {
        # 'firearm attack':
        #     {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'left': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'up': {'repeat': False, 'interruptable': False, 'sequence': (7,7,7,7,7,7,7,7,7), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'down': {'repeat': False, 'interruptable': False, 'sequence': (6,6,6,6,6,6,6,6,6), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    },
        # 'SMP attack': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 5,5, 4, 5,5, 4, 4, 4), 'speed': 1,
        #                              'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'left': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 5,5, 4, 5,5, 4, 4, 4), 'speed': 1,
        #                             'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 7, 7, 7, 7, 7, 7, 7, 7,7,7,7,7), 'speed': 1,
        #                           'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'down': {'repeat': False, 'interruptable': False, 'sequence': (6, 6, 6, 6, 6, 6, 6, 6, 6,6,6,), 'speed': 1,
        #                             'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    },
        # 'shotgun attack': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'left': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'up': {'repeat': False, 'interruptable': False, 'sequence': (7,7,7,7,7,7,7,7,7), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'down': {'repeat': False, 'interruptable': False, 'sequence': (6,6,6,6,6,6,6,6,6), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        # },
        # 'melee attack': {
        #     1: {
        #         'repeat': False, 'interruptable': False,
        #         'sequence': (32,33,33,33), 'speed': 1,
        #         'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0
        #     },
        #
        #     -1: {
        #         'repeat': False, 'interruptable': False,
        #         'sequence': (32,33,33,33), 'speed': 1,
        #         'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0
        #     },
        # },
        # 'get hurt': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (12,13,12,13,12,13,12,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'left': {'repeat': False, 'interruptable': False, 'sequence': (12,13,12,13,12,13,12,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'up': {'repeat': False, 'interruptable': False, 'sequence': (7,13,7,13,7,13,7,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'down': {'repeat': False, 'interruptable': False, 'sequence': (27,13,27,13,27,13,27,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        # },
        # 'be dead': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        # },
        # 'head explode': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        # },
        # 'lay down': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        # },
        # 'exhausted': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        # },
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,2,2,2,2,2,2), 'speed': 20,
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,16), 'speed': 50,
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },

        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,39,40), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (54,53,52,51,50,49,48,47,46,45,44,43,42), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (32,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (51,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn right': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn left': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75),  # 0 - 4
                         # 74,74,74,74,74,  # 5 - 9
                         # 74,74,74,75,75,  # 10 - 14
                         # 74,74,74,74,74,  # 15 - 19
                         # 74,74,74,74,74,  # 20 - 24
                         # 74,74,74,75,75), # 25 - 29
            'demolisher offset': (46, 36),
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 88),  # 0 - 4
                         # 89, 89, 89, 89, 89,  # 5 - 9
                         # 89, 89, 89, 88, 88,  # 10 - 14
                         # 89, 89, 89, 89, 89,  # 15 - 19
                         # 89, 89, 89, 89, 89,  # 20 - 24
                         # 89, 89, 89, 88, 88),  # 25 - 29
            'demolisher offset': (-46,36),
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
    },
    'think type': 'chaser',
    'AI controlled': True
}

player_jake = {
    'name': 'Jake',
    'health': 1000.,
    'start_xy': (200, 200),
    'height': 190,
    'width': 49,
    'body state': {
        'viewing range': 600,
        'regeneration ability': 0.001,
        'blood volume': 15000,
        'blood volume replenish': .01,
        'stamina replenish': 1,
        'consciousness replenish': 10,
        'consciousness threshold': 10,
        'bleeding reduce': .01,  #
        'bleeding resistance': 0,  # Reduce bleeding, in percents.
        'max blood volume': 15000,
        'max stamina': 120,
        'max fatigue': 100,
        'max consciousness': 1000,
        'luck': 5,
        'strength': 25,
        'weight': 70,  # Kilos.
    },
    'gravity affected': True,
    'body': {
        'head': {
            'hardness': 100
        },
    },
    # 'action points': 100,
    'max speed': 10,
    # 'reflexes': randint(100, 150),
    # 'uses light source': False,
    'items': (kitchen_knife,),
    # 'avatar': 'Jake',
    'animations': {
        # 'firearm attack':
        #     {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'left': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'up': {'repeat': False, 'interruptable': False, 'sequence': (7,7,7,7,7,7,7,7,7), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    'down': {'repeat': False, 'interruptable': False, 'sequence': (6,6,6,6,6,6,6,6,6), 'speed': 1,
        #    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #    },
        # 'SMP attack': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 5,5, 4, 5,5, 4, 4, 4), 'speed': 1,
        #                              'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'left': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 5,5, 4, 5,5, 4, 4, 4), 'speed': 1,
        #                             'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 7, 7, 7, 7, 7, 7, 7, 7,7,7,7,7), 'speed': 1,
        #                           'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    'down': {'repeat': False, 'interruptable': False, 'sequence': (6, 6, 6, 6, 6, 6, 6, 6, 6,6,6,), 'speed': 1,
        #                             'sound': 'gunshot', 'sound at frames': (2,5,8), 'repeat from frame': 0},
        #                    },
        # 'shotgun attack': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'left': {'repeat': False, 'interruptable': False, 'sequence': (4,4,5,5,4,4,4,4,4), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'up': {'repeat': False, 'interruptable': False, 'sequence': (7,7,7,7,7,7,7,7,7), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        #     'down': {'repeat': False, 'interruptable': False, 'sequence': (6,6,6,6,6,6,6,6,6), 'speed': 1,
        #               'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
        # },
        # 'melee attack': {
        #     1: {
        #         'repeat': False, 'interruptable': False,
        #         'sequence': (32,33,33,33), 'speed': 1,
        #         'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0
        #     },
        #
        #     -1: {
        #         'repeat': False, 'interruptable': False,
        #         'sequence': (32,33,33,33), 'speed': 1,
        #         'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0
        #     },
        # },
        # 'get hurt': {
        #     'right': {'repeat': False, 'interruptable': False, 'sequence': (12,13,12,13,12,13,12,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'left': {'repeat': False, 'interruptable': False, 'sequence': (12,13,12,13,12,13,12,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'up': {'repeat': False, 'interruptable': False, 'sequence': (7,13,7,13,7,13,7,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        #     'down': {'repeat': False, 'interruptable': False, 'sequence': (27,13,27,13,27,13,27,13), 'speed': 2,
        #              'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
        # },
        # 'be dead': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
        #             'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        # },
        # 'head explode': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
        #                  'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
        # },
        # 'lay down': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (27,27,28,28,29,30,30,31), 'speed': 2,
        #              'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
        # },
        # 'exhausted': {
        #     'right': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'left': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'up': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        #     'down': {'repeat': True, 'interruptable': True, 'sequence': (42,43), 'speed': 10,
        #              'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
        # },
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,2,2,2,2,2,2), 'speed': 20,
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,16), 'speed': 50,
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },

        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,39,40), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (54,53,52,51,50,49,48,47,46,45,44,43,42), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (32,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (51,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn right': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn left': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75,  # 0 - 4
                         74,74,74,74,75), # 5 - 9
                         # 74,74,74,74,74,  # 5 - 9
                         # 74,74,74,75,75,  # 10 - 14
                         # 74,74,74,74,74,  # 15 - 19
                         # 74,74,74,74,74,  # 20 - 24
                         # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 88),  # 0 - 4
                         # 89, 89, 89, 89, 89,  # 5 - 9
                         # 89, 89, 89, 88, 88,  # 10 - 14
                         # 89, 89, 89, 89, 89,  # 15 - 19
                         # 89, 89, 89, 89, 89,  # 20 - 24
                         # 89, 89, 89, 88, 88),  # 25 - 29
            # 'demolisher offset': (-46,36),
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
    },
    'think type': '',
    'AI controlled': False
}

# demon_1 = {
#     'name': 'demon Hildegarda',
#     'body state': {
#         'viewing range': 600,
#         'regeneration ability': 0,
#         'marksmanship': 10,  # The higher -- the better
#         'blood volume': 5000,
#         'max blood volume': 5000,
#         'blood volume replenish': 0.1,
#         'bleeding reduce': 0.1,  #
#         'bleeding resistance': 1,  # Reduce bleeding, in percents.
#         'weight': 80,  # Kilos.
#         'reflexes': 250,  # minimal threshold of event speed which creature able to notice (in ms)
#         'default reflexes': 250,
#         'pain resistance': 1,  # Change total pain level by multiplying total pain level to this number.
#                                # Below 1 is reducing, above 1 is increasing. The smaller the number, the stronger pain resistance.
#                                # Zero means total pain resist.
#         'max stamina': 100,
#         'max stamina default': 100,
#         'stamina replenish': 1,
#         'max fatigue': 100,
#         'consciousness replenish': 10,
#         'max consciousness': 1000,
#         'consciousness threshold': 10,
#         'luck': 5,
#         'strength': 5
#     },
#     'max speed': .4,
#     'body': {
#         'head': {
#             'hardness': 4,
#             'consistency': 10,
#             'consistency default': 10
#         },
#     },
#     'action points': 50,
#     'avatar': 'demon Hildegarda',
#     # 'avatar': 'phantom',
#     # 'avatar': 'zombie2',
#     'reflexes': randint(240, 250),
#     'uses light source': False,
#     'items': (kitchen_knife,),
#     # 'items': (pistol_9mm, brass_garden_key, tiny_heal_vial, painkillers),
#     'animations': {
#         'firearm attack': {
#             'right': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 4, 4, 4, 4), 'speed': 1,
#                                      'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'left': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 4, 4, 4, 4), 'speed': 1,
#                                     'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 7, 7, 7, 7, 7, 7, 7, 7), 'speed': 1,
#                                   'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'down': {'repeat': False, 'interruptable': False, 'sequence': (6, 6, 6, 6, 6, 6, 6, 6, 6), 'speed': 1,
#                                     'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#         },
#         'shotgun attack': {
#             'right': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 4, 4, 4, 4), 'speed': 1,
#                       'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'left': {'repeat': False, 'interruptable': False, 'sequence': (4, 4, 5, 5, 4, 4, 4, 4, 4), 'speed': 1,
#                      'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 7, 7, 7, 7, 7, 7, 7, 7), 'speed': 1,
#                    'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#             'down': {'repeat': False, 'interruptable': False, 'sequence': (6, 6, 6, 6, 6, 6, 6, 6, 6), 'speed': 1,
#                      'sound': 'gunshot', 'sound at frames': (2,), 'repeat from frame': 0},
#         },
#         'melee attack': {
#             'right': {'repeat': False, 'interruptable': False, 'sequence': (32, 33, 33, 33), 'speed': 1,
#                       'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0},
#
#             'left': {'repeat': False, 'interruptable': False, 'sequence': (32, 33, 33, 33), 'speed': 1,
#                      'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0},
#             'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 7, 7, 7), 'speed': 1,
#                    'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0},
#             'down': {'repeat': False, 'interruptable': False, 'sequence': (6, 6, 6, 6), 'speed': 1,
#                      'sound': 'swing', 'sound at frames': (1,), 'repeat from frame': 0},
#         },
#         'get hurt': {
#             'right': {'repeat': False, 'interruptable': False, 'sequence': (12, 13, 12, 13, 12, 13, 12, 13), 'speed': 2,
#                       'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
#             'left': {'repeat': False, 'interruptable': False, 'sequence': (12, 13, 12, 13, 12, 13, 12, 13), 'speed': 2,
#                      'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
#             'up': {'repeat': False, 'interruptable': False, 'sequence': (7, 13, 7, 13, 7, 13, 7, 13), 'speed': 2,
#                    'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
#             'down': {'repeat': False, 'interruptable': False, 'sequence': (27, 13, 27, 13, 27, 13, 27, 13), 'speed': 2,
#                      'sound': 'jake groan', 'sound at frames': (1,), 'repeat from frame': 0},
#         },
#         'be dead': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
#                       'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
#                    'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (40,), 'speed': 1,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#         },
#         'head explode': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
#                       'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
#                    'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (34, 35, 36, 37, 38, 39, 40), 'speed': 1,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 6},
#         },
#         'lay down': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (27, 27, 28, 28, 29, 30, 30, 31), 'speed': 2,
#                       'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (27, 27, 28, 28, 29, 30, 30, 31), 'speed': 2,
#                      'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (27, 27, 28, 28, 29, 30, 30, 31), 'speed': 2,
#                    'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (27, 27, 28, 28, 29, 30, 30, 31), 'speed': 2,
#                      'sound': None, 'sound at frames': (3,), 'repeat from frame': 7},
#         },
#         'exhausted': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (42, 43), 'speed': 10,
#                       'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (42, 43), 'speed': 10,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (42, 43), 'speed': 10,
#                    'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (42, 43), 'speed': 10,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#         },
#         'stay still': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2), 'speed': 20,
#                       'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2), 'speed': 20,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (3,), 'speed': 9,
#                    'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (0,), 'speed': 9,
#                      'sound': None, 'sound at frames': (0,), 'repeat from frame': 0},
#         },
#         'walk': {
#             'right': {'repeat': True, 'interruptable': True, 'sequence': (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 14, 15, 16), 'speed': 2,
#                       'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0},
#             'left': {'repeat': True, 'interruptable': True, 'sequence': (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 14, 15, 16), 'speed': 2,
#                      'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0},
#             'down': {'repeat': True, 'interruptable': True, 'sequence': (10, 11,), 'speed': 9,
#                      'sound': 'step', 'sound at frames': (1,), 'repeat from frame': 0},
#             'up': {'repeat': True, 'interruptable': True, 'sequence': (8, 9), 'speed': 9,
#                    'sound': 'step', 'sound at frames': (1,), 'repeat from frame': 0},
#         },
#     },
#     'thinking type': 'demon 1',
#     'AI controlled': True


all_hostiles = {
    # zombie_male_zak['name']: zombie_male_zak,
    # demon_female_1['name']: demon_female_1,
    demon_1['name']: demon_1
}

all_players = {
    # 'Jane': player_jane,
    player_jake['name']: player_jake,
    # 'Mark de Casques': player_dude
}
