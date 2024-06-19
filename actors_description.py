from weapons import *
# from game_objects import *
from random import randint

demon_1 = {
    'name': 'demon 1',
    # 'start_xy': (1500, 200),
    'health': 100.,
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
    'max speed': 2,
    'items': (whip,),
    'animations': {
        'whip right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74, 74, 74, 74, 74, 74, 74, 75),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 89, 89, 89, 88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,2,2,2,2,2,2), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,16), 'speed': 50,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },

        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,39,40), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (54,53,52,51,50,49,48,47,46,45,44,43,42), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (32,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (51,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn right': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn left': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'activity at frames': {},
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
            # 'demolisher offset': (46, 36),
            'activity at frames': {
                4: {
                    'sound': True,
                    'move': 10,
                    'demolisher': True
                },
                9: {
                    'move': 10,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'speed': 2,
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
            'activity at frames': {
                4: {
                    'sound': True,
                    'move': 10,
                    'demolisher': True
                },
                9: {
                    'move': 10,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'speed': 2,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
    },
    'think type': 'chaser',
    'AI controlled': True
}

player_jake = {
    'name': 'Jake',
    'health': 1000.,
    # 'start_xy': (200, 200),
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
    'items': (whip,fireball_staff,sword,kitchen_knife,),
    # 'avatar': 'Jake',
    'animations': {
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,2,2,2,2,2,2), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,16), 'speed': 50,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,39,40), 'speed': 1,
                'activity at frames': {
                    1: {
                        'sound': 'step',
                    },
                },
                'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (54,53,52,51,50,49,48,47,46,45,44,43,42), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (32,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (51,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn right': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'turn left': {
                'repeat': True, 'interruptable': True,
                'sequence': (0,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,71,72,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'whip right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74, 74, 74, 74, 74,74,74,75),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolisher': True
                },
                },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89,89,89,89,89,89,89,88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75,  # 0 - 4
                         74,74,74,74,75, 75), # 5 - 9
                         # 74,74,74,74,74,  # 5 - 9
                         # 74,74,74,75,75,  # 10 - 14
                         # 74,74,74,74,74,  # 15 - 19
                         # 74,74,74,74,74,  # 20 - 24
                         # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    'move': 10,
                    'demolisher': True
                },
                9: {
                    'move': 10,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 88,
                         89, 89, 89, 89, 88, 88),  # 0 - 4
                         # 89, 89, 89, 89, 89,  # 5 - 9
                         # 89, 89, 89, 88, 88,  # 10 - 14
                         # 89, 89, 89, 89, 89,  # 15 - 19
                         # 89, 89, 89, 89, 89,  # 20 - 24
                         # 89, 89, 89, 88, 88),  # 25 - 29
            # 'demolisher offset': (-46,36),
            'activity at frames': {
                4: {
                    'sound': True,
                    'move': 10,
                    'demolisher': True
                },
                9: {
                    'move': 10,
                    'demolisher': True
                },
            },
            'speed': 1,
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'cast right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74, 74, 74, 74, 74,  # 0 - 4
                         74, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 2,
            'activity at frames': {
                9: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
        'cast left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89,89,89,89,89,89,  # 0 - 4
                         89,89,89,89,88,88),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 3,
            'activity at frames': {
                9: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                1: (46, 36),
                -1: (-46, 36),
            },
            'repeat from frame': 0
        },
    },
    'think type': '',
    'AI controlled': False
}


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
