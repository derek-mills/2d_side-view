from constants import *
locations = {
    
    'room 2':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (1920, 1080),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 0), (1950, 50), 1),
                ((0, 1050), (1950, 50), 3),
                ((1900, 50), (50, 1000), 4),
                ((0, 850), (50, 200), 6),
                ((0, 50), (50, 800), 7),
                ((600, 750), (50, 300), 18),
                ((650, 750), (300, 50), 19),
                ((950, 400), (50, 400), 20),
                ((900, 800), (50, 250), 21),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    6: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 1', 'xy': (2850.0, 1750.0)},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'room 1':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (3000, 2000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 1950), (3000, 50), 1),  #1
                ((2950, 1750), (50, 200), 7),  #7
                ((2950, 0), (50, 1750), 8),  #8
                ((0, 0), (50, 1950), 9),  #9
                ((1650, 0), (1300, 50), 15),  #15
                ((50, 750), (350, 50), 19),  #19
                ((450, 950), (400, 50), 20),  #20
                ((2300, 50), (400, 1250), 22),  #22
                ((2700, 1150), (100, 150), 24),  #24
                ((2850, 600), (100, 150), 25),  #25
                ((2700, 250), (100, 50), 26),  #26
                ((450, 1750), (2100, 200), 31),  #31
                ((800, 400), (50, 550), 32),  #32
                ((800, 0), (850, 400), 34),  #34
                ((800, 1000), (1500, 50), 35),  #35
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    32: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 2', 'xy': (100.0, 850.0)},
                  },
                    7: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': True,
                        'teleport description': {'new location': 'room 2', 'xy': (100.0, 850.0)},
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}