from weapons import *
# from game_objects import *
from random import randint
from graphics import sprites

zombie = {
    'name': 'zombie',
    'blood color': (0, 200, 0),
    'drop': ['exp' for i in range(randint(3,5))],
    'strength': 5,
    'body weight': 50,
    'health': 2000.,
    'mana replenish': .0,
    'stamina replenish': 12.,
    'height': 150,  # For level editor use only
    'width': 50,  # For level editor use only
    'resistances': {
        # Zero is total resistance, such type of damage multiples by zero.
        # Above 1 is a weakness to particular type of damage.
        'slash': 1.5,
        'pierce': 0.1,
        'smash': 1,
        'fire': 1.5
    },
    'gravity affected': True,
    # 'body': {
    #     'head': {
    #         'hardness': 100
    #     },
    # },
    'max speed': 2 + randint(1, 10) / 10,
    'max jump height': 5,
    'acceleration': .1,
    'friction': .9,
    'air acceleration': .1,
    'items': (demon_2_close, demon_2_mid, spikeball_staff),
    'animations': {
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,1,2,1,1,1,1), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,15,15,15,15,15,16,15,16,15,15,15,15), 'speed': 20,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'lie dead right': {
            'repeat': True,
            'sequence': (56,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'lie dead left': {
            'repeat': True,
            'sequence': (70,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (56,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process left': {
            'repeat': True, 'interruptable': True,
            'sequence': (20,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,), 'speed': 1,
                'activity at frames': {
                    1: {
                        'sound': 'step',
                    },
                },
                'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (52,51,50,49,48,47,46,45,44,43,42,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,90,90,90), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,), 'speed': 1,
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
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (4,4,4,4), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crawl right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,6,7,6), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (18,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'crawl left': {
            'repeat': True, 'interruptable': True,
            'sequence': (21,20,19,20), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'whip right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,75,76,76,76,77),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 3,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                },
            'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,90,89,89,89,88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75,  # 0 - 4
                         74,74,74,74,75, 75), # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                9: {
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 88,
                         89, 89, 89, 89, 88, 88),  # 0 - 4
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                9: {
                    # 'move': 10, # Slightly move actor forward,
                    'demolisher': True,
                    'demolishers set number': 0,
                },
            },
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'cast right': {
            'repeat': False, 'interruptable': True,
            'sequence': (60,60,60,60,60,60,61,62,62,62,62),  # 5 - 9
            'speed': 4,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'cast left': {
            'repeat': False, 'interruptable': True,
            'sequence': (65,65,65,65,65,65,64,63,63,63,63),  # 5 - 9
            'speed': 4,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (84, 85, 86, 87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73, 72, 71, 70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'lie decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'lie decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
    },
    # 'think type': '',
    'think type': 'chaser',
    'disappear after death': False,
    'AI controlled': True
}

demon_1 = {
    'name': 'demon 1',
    'blood color': (0, 200, 0),
    'drop': ['exp' for i in range(randint(3,5))],
    'strength': 10,
    'body weight': 50,
    'health': 200.,
    'mana replenish': .5,
    'stamina replenish': 2.,
    'height': 150,  # For level editor use only
    'width': 50,  # For level editor use only
    'resistances': {
        # Zero is total resistance, such type of damage multiples by zero.
        # Above 1 is a weakness to particular type of damage.
        'slash': 0.1,
        'pierce': 1,
        'smash': 1,
        'fire': 1
    },
    'gravity affected': True,
    # 'body': {
    #     'head': {
    #         'hardness': 100
    #     },
    # },
    'max speed': 5 + randint(1, 10) / 10,
    'max jump height': 25,
    'acceleration': .4,
    'friction': .9,
    'air acceleration': .4,
    'items': (demon_2_close, demon_2_mid, spikeball_staff),
    'animations': {
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,1,2,1,1,1,1), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,15,15,15,15,15,16,15,16,15,15,15,15), 'speed': 20,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'lie dead right': {
            'repeat': True,
            'sequence': (56,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'lie dead left': {
            'repeat': True,
            'sequence': (70,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (56,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process left': {
            'repeat': True, 'interruptable': True,
            'sequence': (20,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,), 'speed': 1,
                'activity at frames': {
                    1: {
                        'sound': 'step',
                    },
                },
                'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (52,51,50,49,48,47,46,45,44,43,42,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,90,90,90), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,), 'speed': 1,
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
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (4,4,4,4), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crawl right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,6,7,6), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (18,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'crawl left': {
            'repeat': True, 'interruptable': True,
            'sequence': (21,20,19,20), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'whip right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,75,76,76,76,77),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 3,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                },
            'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,90,89,89,89,88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75,  # 0 - 4
                         74,74,74,74,75, 75), # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                9: {
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89, 89, 89, 89, 88,
                         89, 89, 89, 89, 88, 88),  # 0 - 4
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                9: {
                    # 'move': 10, # Slightly move actor forward,
                    'demolisher': True,
                    'demolishers set number': 0,
                },
            },
            'speed': 1,
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 2
        },
        'cast right': {
            'repeat': False, 'interruptable': True,
            'sequence': (60,60,60,60,60,60,61,62,62,62,62),  # 5 - 9
            'speed': 4,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'cast left': {
            'repeat': False, 'interruptable': True,
            'sequence': (65,65,65,65,65,65,64,63,63,63,63),  # 5 - 9
            'speed': 4,
            'activity at frames': {
                7: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (84, 85, 86, 87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73, 72, 71, 70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'lie decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'lie decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
    },
    'think type': '',
    # 'think type': 'chaser',
    'disappear after death': False,
    'AI controlled': True
}

demon_2 = {
    'name': 'demon 2',
    'drop': ['exp' for i in range(randint(8,12))],
    'health': 5000.,
    'mana replenish': 50.,
    'stamina replenish': 1.,
    'blood color': (150, 50, 10),
    'strength': 15,
    'body weight': 140,
    'resistances': {
        # Zero is total resistance, such type of damage multiples by zero.
        # Above 1 is a weakness to particular type of damage.
        'slash': 0,
        'pierce': 0.5,
        'smash': 0.1,
        'fire': 0.8
    },
    'height': 150,  # For level editor use only
    'width': 50,  # For level editor use only
    'gravity affected': True,
    'body': {
        'head': {
            'hardness': 100
        },
    },
    'max speed': 5 + randint(1, 10) / 10,
    'max jump height': 27,
    'acceleration': .3,
    'friction': .9,
    'air acceleration': .3,

    'items': (demon_2_close, demon_2_mid, fireball_staff),
    'animations': {
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,1,2,1,1,1,1), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,15,15,15,15,15,16,15,16,15,15,15,15), 'speed': 20,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'lie dead right': {
                'repeat': True,
                'sequence': (14,), 'speed': 20,
                'activity at frames': {},
                'repeat from frame': 0
            },
        'lie dead left': {
            'repeat': True,
            'sequence': (17,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (56,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process left': {
            'repeat': True, 'interruptable': True,
            'sequence': (20,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,36,37,38,), 'speed': 4,
                'activity at frames': {
                    1: {
                        'sound': 'step',
                    },
                },
                'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (52,51,50,49,48,47,46,45,44,43,42,), 'speed': 4,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,90,90,90), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly right': {
                'repeat': True, 'interruptable': True,
                'sequence': (75,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly left': {
                'repeat': True, 'interruptable': True,
                'sequence': (90,), 'speed': 1,
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
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (4,4,4,4), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crawl right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,6,7,6), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (18,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'crawl left': {
            'repeat': True, 'interruptable': True,
            'sequence': (21,20,19,20), 'speed': 5,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'whip right': {
            'repeat': False,
            # 'interruptable': True,
            'sequence': (74,74,74,75,76,76,76,77,75,74,
                         78,78,78,79,80,80,80,79,79,79),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 'sequence': (74,74,74,75,76,76,76,77),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 4,
            'activity at frames': {
                3: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                13: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
                14: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
                },
            # 'demolisher offset': {
            #     1: (sprites['demon 2 76']['demolisher snap point'][0],
            #         sprites['demon 2 76']['demolisher snap point'][1]),
            #     # -1: (-65, 60),
            #     # 1: (65, 60),
            #     # -1: (-65, 60),
            # },
            'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,90,89,89,89,88,88,91,
                         94,94,94,93,92,92,92,93,93,93),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            # 'sequence': (91,91,91,90,89,89,89,88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 4,
            'activity at frames': {
                3: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                13: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
                14: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            # 'demolisher offset': {
            #     # 1: (65,60),
            #     -1: (sprites['demon 2 89']['demolisher snap point'][0],
            #          sprites['demon 2 89']['demolisher snap point'][1]),
            # },
            'repeat from frame': 0
        },
        'whip crouch right': {
            'repeat': False, 'interruptable': True,
            'sequence': (60,60,60,61,62,62,62,61),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 'sequence': (74,74,74,75,76,76,76,77),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 8,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolisher': True
                },
                },
            'demolisher offset': {
                1: (sprites['demon 2 76']['demolisher snap point'][0],
                    sprites['demon 2 76']['demolisher snap point'][1]),
                # -1: (-65, 60),
                # 1: (65, 60),
                # -1: (-65, 60),
            },
            'repeat from frame': 0
        },
        'whip crouch left': {
            'repeat': False, 'interruptable': True,
            'sequence': (78,78,78,79,80,80,80,79),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            # 74,74,74,74,74,  # 5 - 9
            # 74,74,74,75,75,  # 10 - 14
            # 74,74,74,74,74,  # 15 - 19
            # 74,74,74,74,74,  # 20 - 24
            # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 8,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolisher': True
                },
            },
            'demolisher offset': {
                # 1: (65,60),
                -1: (sprites['demon 2 89']['demolisher snap point'][0],
                     sprites['demon 2 89']['demolisher snap point'][1]),
            },
            'repeat from frame': 0
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (60,60,60,60,61,61,61,61,61,61), # 5 - 9
                         # 74,74,74,74,74,  # 5 - 9
                         # 74,74,74,75,75,  # 10 - 14
                         # 74,74,74,74,74,  # 15 - 19
                         # 74,74,74,74,74,  # 20 - 24
                         # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
            },
            # 'demolisher offset': {
            #     1: (sprites['demon 2 75']['demolisher snap point'][0],
            #         sprites['demon 2 75']['demolisher snap point'][1]),
            #
            #     # 1: (46, 36),
            #     # -1: (-46, 36),
            # },
            'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (62,62,62,62,63,63,63,63,63,63), # 5 - 9
                         # 74,74,74,74,74,  # 5 - 9
                         # 74,74,74,75,75,  # 10 - 14
                         # 74,74,74,74,74,  # 15 - 19
                         # 74,74,74,74,74,  # 20 - 24
                         # 74,74,74,75,75), # 25 - 29
            # 'demolisher offset': (46, 36),
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
            },
            'speed': 1,
            # 'demolisher offset': {
            #     -1: (sprites['demon 2 61']['demolisher snap point'][0],
            #         sprites['demon 2 88']['demolisher snap point'][1]),
            #
            #     # 1: (46, 36),
            #     # -1: (-46, 36),
            # },
            # 'sound': None, 'sound at frames': (1, 4),
            'repeat from frame': 2
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
                    'demolishers set number': 0,
                    'demolisher': True
                },
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
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (84,85,86,87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (73,72,71,70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 3
        },
        'lie decapitated left': {
            'repeat': True, 'interruptable': True,
            'sequence': (87,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'lie decapitated right': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,),
            'speed': 9,
            'activity at frames': {
                0: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
    },
    # 'think type': '',
    'think type': 'chaser',
    'disappear after death': False,
    'AI controlled': True
}

exploding_barrel = {
    'name': 'exploding barrel',
    'drop': [],
    'health': 500.,
    'mana replenish': 0.,
    'stamina replenish': 10.,
    'blood color': (0, 0, 0),
    'strength': 1,
    'body weight': 240,
    'resistances': {
        # Zero is total resistance, such type of damage multiples by zero.
        # Above 1 is a weakness to particular type of damage.
        'slash': 0.,
        'pierce': 0.1,
        'smash': 0.2,
        'fire': 5
    },
    'height': 150,  # For level editor use only
    'width': 50,  # For level editor use only
    'gravity affected': True,
    'max speed': 1,
    'max jump height': 1,
    'acceleration': .5,
    'friction': .9,
    'air acceleration': .4,

    'items': (barrel_explosion,),
    'animations': {
        'stand still right': {
                'repeat': True,
                'sequence': (0,), 'speed': 20,
                'activity at frames': {},
                'repeat from frame': 0
            },
        'almost explode right': {
                'repeat': True,
                'sequence': (1,2,1,2,1,2,1,2,1,2,1,2), 'speed': 10,
                'activity at frames': {},
                'repeat from frame': 0
            },
        'almost explode left': {
                'repeat': True,
                'sequence': (1,2,1,2,1,2,1,2,1,2,1,2), 'speed': 10,
                'activity at frames': {},
                'repeat from frame': 0
            },
        'explosion right': {
                'repeat': True,
                'sequence': (3,4,5,3,4,5,3,4,5,3,4,5), 'speed': 1,
                'activity at frames': {
                    11: {
                        'sound': True,
                        'demolishers set number': 0,
                        'demolisher': True
                    },
                },
                'repeat from frame': 0
            },
        'explosion left': {
                'repeat': True,
                'sequence': (3,4,5,3,4,5,3,4,5,3,4,5), 'speed': 1,
                'activity at frames': {
                    11: {
                        'sound': True,
                        'demolishers set number': 0,
                        'demolisher': True
                    },
                },
                'repeat from frame': 0
            },
    },
    'think type': 'exploding barrel',
    # 'think type': 'chaser',
    'disappear after death': True,
    'AI controlled': True
}

player_jake = {
    'name': 'Jake',
    'health': 1000.,
    'blood color': (255, 0, 0),
    'gravity affected': True,
    'mana replenish': .01,
    'stamina replenish': .2,
    'strength': 10,  # The more the strength, the less the inner athletic index, the more max speed and jump height.
    'body weight': 60,  # The more the weight, the more the inner athletic index, the less max speed and jump height.
    'resistances': {
        # Zero is total resistance, such type of damage multiples by zero.
        # Above 1 is a weakness to particular type of damage.
        # In the other terms, this is a just incoming damage multiplier.
        'slash': .1,
        'pierce': .1,
        'smash': .1,
        'fire': 1
    },
    # 'body': {
    #     'head': {
    #         'hardness': 100
    #     },
    # },
    'max speed': 10,  # Base value, which will be reduced upon athletic index.
    # 'max speed': 16,  # Base value, which will be reduced upon athletic index.
    'max jump height': 28, # Base value, which will be reduced upon athletic index.
    'acceleration': .6,
    'friction': .9,
    'air acceleration': .4,
    # First item in list must be an undroppable weapon.
    'items': (axe,jake_kick, small_shield, spikeball_staff, fireball_staff,pistol,whip,),
    # 'items': (whip,fireball_staff,sword,kitchen_knife,),
    'animations': {
        'stand still right': {
                'repeat': True, 'interruptable': True,
                'sequence': (1,1,1,1,1,1,2,1,2,1,1,1,1), 'speed': 20,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
            },
        'stand still left': {
            'repeat': True, 'interruptable': True,
            'sequence': (15,15,15,15,15,15,16,15,16,15,15,15,15), 'speed': 20,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'getting hurt right': {
                'repeat': True, 'interruptable': True,
                'sequence': (11,12,13,13,13,13,13), 'speed': 2,
                'activity at frames': {},
                'sound': None, 'sound at frames': (0,), 'repeat from frame': 2
            },
        'getting hurt left': {
            'repeat': True, 'interruptable': True,
            'sequence': (25,26,27,27,27,27,27), 'speed': 2,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 2
        },
        'lie dead right': {
            'repeat': True,
            'sequence': (14,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'lie dead left': {
            'repeat': True,
            'sequence': (17,), 'speed': 20,
            'activity at frames': {},
            'repeat from frame': 0
        },
        'sliding right': {
            'repeat': True, 'interruptable': True,
            'sequence': (56,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'sliding left': {
            'repeat': True, 'interruptable': True,
            'sequence': (70,), 'speed': 1,
            'activity at frames': {
                1: {
                    'sound': 'step',
                },
            },
            'repeat from frame': 0
        },
        'hopping back process right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,), 'speed': 1,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'hopping back process left': {
            'repeat': True, 'interruptable': True,
            'sequence': (20,), 'speed': 1,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'run right': {
                'repeat': True, 'interruptable': True,
                'sequence': (28,29,30,31,32,33,34,35,), 'speed': 4,
                # 'sequence': (28,29,30,31,32,33,34,35,36,37,38,), 'speed': 1,
                'activity at frames': {
                    1: {
                        'sound': 'step',
                    },
                },
                'repeat from frame': 0
            },
        'run left': {
                'repeat': True, 'interruptable': True,
                'sequence': (52,51,50,49,48,47,46,45,), 'speed': 4,
                # 'sequence': (52,51,50,49,48,47,46,45,44,43,42,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump right': {
                'repeat': True, 'interruptable': True,
                'sequence': (29,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'jump left': {
                'repeat': True, 'interruptable': True,
                'sequence': (51,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly right': {
                'repeat': True, 'interruptable': True,
                'sequence': (32,), 'speed': 1,
                'activity at frames': {},
                'sound': 'step', 'sound at frames': (1, 4), 'repeat from frame': 0
            },
        'fly left': {
                'repeat': True, 'interruptable': True,
                'sequence': (48,), 'speed': 1,
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
        'crouch right': {
            'repeat': True, 'interruptable': True,
            'sequence': (4,4,4,4), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crawl right': {
            'repeat': True, 'interruptable': True,
            'sequence': (5,6,5,7,), 'speed': 15,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'crouch left': {
            'repeat': True, 'interruptable': True,
            'sequence': (18,), 'speed': 1,
            'activity at frames': {},
            'sound': None, 'sound at frames': (0,), 'repeat from frame': 0
        },
        'crawl left': {
            'repeat': True, 'interruptable': True,
            'sequence': (21,20,21,19,), 'speed': 15,
            'activity at frames': {},
            'sound': None, 'sound at frames': (1, 4), 'repeat from frame': 0
        },
        'whip right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,75,76,76,76,76,76,77),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                5: {
                    'sound': True,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                6: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
                },
             'repeat from frame': 0
        },
        'whip left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,90,89,89,89,89,89,88),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                5: {
                    'sound': True,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                6: {
                    'sound': True,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'whip crouch right': {
            'repeat': False, 'interruptable': True,
            'sequence': (60, 60, 60, 61, 62, 62, 62, 61),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolisher': True,
                    'demolishers set number': 0,
                },
            },
            'repeat from frame': 0
        },
        'whip crouch left': {
            'repeat': False, 'interruptable': True,
            'sequence': (80, 80, 80, 79, 78, 78, 78, 79),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,75,76,76,76,),  # 0 - 4
            'speed': 2,
            'activity at frames': {
                2: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'stab left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,90,89,89,89),  # 0 - 4
            'activity at frames': {
                2: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'speed': 2,
            'repeat from frame': 2
        },
        'kick combo 1 right': {
            'repeat': False, 'interruptable': True,
            'sequence': (109,108,107,106,106,106,109,),  # 5 - 9
            'speed': 2,
            'activity at frames': {
                3: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'kick combo 2 right': {
            'repeat': False, 'interruptable': True,
            'sequence': (109,109,111,111,110,110,110,),  # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'kick combo 3 right': {
            'repeat': False, 'interruptable': True,
            'sequence': (63,63,64,64,65,65,65,64,63,63), # 5 - 9
            'speed': 2,
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'kick combo 1 left': {
            'repeat': False, 'interruptable': True,
            'sequence': (92,93,94,95,95,95,92,),  # 0 - 4
            'activity at frames': {
                3: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'speed': 2,
            'repeat from frame': 0
        },
        'kick combo 2 left': {
            'repeat': False, 'interruptable': True,
            'sequence': (92,92,96,96,97,97,97),  # 0 - 4
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
            },
            'speed': 2,
            'repeat from frame': 0
        },
        'kick combo 3 left': {
            'repeat': False, 'interruptable': True,
            'sequence': (68,68,67,67,66,66,66,66,67,68),  # 0 - 4
            'activity at frames': {
                4: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'speed': 2,
            'repeat from frame': 0
        },
        'cast right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74, 74, 74, 74, 74,  # 0 - 4
                         74, 74, 74, 74, 75, 75),  # 5 - 9
              'speed': 2,
            'activity at frames': {
                9: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },

            'repeat from frame': 0
        },
        'cast left': {
            'repeat': False, 'interruptable': True,
            'sequence': (89,89,89,89,89,89,  # 0 - 4
                         89,89,89,89,88,88),  # 5 - 9
            'speed': 3,
            'activity at frames': {
                9: {
                    'sound': True,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'hold stash left': {
            'repeat': True,
            'sequence': (10,),  # 0 - 5
            'speed': 3,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'hold stash right': {
            'repeat': True,
            'sequence': (22,),  # 0 - 5
            'speed': 3,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'carry stash left': {
            'repeat': True,
            'sequence': (8,9,10,9,),  # 0 - 5
            'speed': 3,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'carry stash right': {
            'repeat': True,
            'sequence': (22,23,24,23,),  # 0 - 5
            'speed': 3,
            'activity at frames': {
            },
            'repeat from frame': 0
        },
        'axe swing combo 2 right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,74,74,75, 76, 76, 76,76,76,76,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                5: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'axe swing combo 1 left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,91,90, 90, 89, 89, 89,89,89,89,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                6: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'axe swing combo 1 right': {
            'repeat': False, 'interruptable': True,
            'sequence': (74,74,75,76,76,76,74,74,75,76,76,76),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                2: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                3: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 3,
                    'demolisher': True
                },
                6: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                7: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                9: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 3,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'axe swing combo 2 left': {
            'repeat': False, 'interruptable': True,
            'sequence': (91,91,91,91,90, 90, 89, 89, 89,89,89,89,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
                4: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 1,
                    'demolisher': True
                },
                6: {
                    'sound': True,
                    # 'move': 10, # Slightly move actor forward,
                    'demolishers set number': 2,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'pistol shot right': {
            'repeat': False, 'interruptable': True,
            'sequence': (57,57,57,58,58,59,59,59,59),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                3: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'pistol shot left': {
            'repeat': False, 'interruptable': True,
            'sequence': (73,73,73,72,72,71,71,71,71),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                3: {
                    'sound': True,
                    # 'move': 10,  # Slightly move actor forward,
                    'demolishers set number': 0,
                    'demolisher': True
                },
            },
            'repeat from frame': 0
        },
        'protect right': {
            'repeat': True, 'interruptable': True,
            'sequence': (98,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': None,
                    # 'move': 10,  # Slightly move actor forward,
                    'protectors set number': 0,
                    'demolishers set number': 0,
                    'protector': True,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'protect left': {
            'repeat': True, 'interruptable': True,
            'sequence': (122,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': None,
                    # 'move': 10,  # Slightly move actor forward,
                    'protectors set number': 0,
                    'demolishers set number': 0,
                    'protector': True,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'protect walk right': {
            'repeat': True,
            'sequence': (98,99,100,101,102,103,104,105,106,107,108,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': None,
                    # 'move': 10,  # Slightly move actor forward,
                    'protectors set number': 0,
                    'demolishers set number': 0,
                    'protector': True,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
        'protect walk left': {
            'repeat': True,
            'sequence': (122,121,120,119,118,117,116,115,114,113,112,),  # 0 - 474, 74, 74, 74, 75, 75),  # 5 - 9
            'speed': 1,
            'activity at frames': {
                0: {
                    'sound': None,
                    # 'move': 10,  # Slightly move actor forward,
                    'protectors set number': 0,
                    'demolishers set number': 0,
                    'protector': True,
                    'demolisher': False
                },
            },
            'repeat from frame': 0
        },
    },
    'think type': '',
    'disappear after death': False,
    'AI controlled': False
}

all_hostiles = {
    demon_1['name']: demon_1,
    demon_2['name']: demon_2,
    exploding_barrel['name']: exploding_barrel,
    zombie['name']: zombie,
}

all_players = {
    # 'Jane': player_jane,
    player_jake['name']: player_jake,
    # 'Mark de Casques': player_dude
}
