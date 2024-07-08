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
                ((0, 0), (1950, 50), 1),  #1
                ((0, 1050), (1950, 50), 3),  #3
                ((1900, 50), (50, 1000), 4),  #4
                ((0, 850), (50, 200), 6),  #6
                ((0, 50), (50, 800), 7),  #7
                ((50, 750), (700, 50), 8),  #8
                ((750, 500), (50, 300), 9),  #9
                ((800, 500), (400, 50), 10),  #10
                ((1200, 500), (50, 300), 11),  #11
                ((1750, 250), (50, 550), 15),  #15
                ((1250, 750), (500, 50), 16),  #16
                ((800, 750), (400, 50), 17),  #17
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    10: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.0,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': True,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': False,
                        'trigger description': {'make active': [11, 10, 9, 8, 7, 6, 4, 3, 1], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                    9: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.0,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': True,
                        'trigger description': {'make active': [6, 7, 8], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
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
                ((0, 1950), (3000, 50), 1),
                ((2950, 1750), (50, 200), 7),
                ((2950, 0), (50, 1750), 8),
                ((0, 0), (50, 1950), 9),
                ((1650, 0), (1300, 50), 15),
                ((50, 750), (350, 50), 19),
                ((450, 950), (400, 50), 20),
                ((900, 1150), (350, 50), 21),
                ((2300, 50), (400, 1250), 22),
                ((2700, 1150), (100, 150), 24),
                ((2850, 600), (100, 150), 25),
                ((2700, 250), (100, 50), 26),
                ((1300, 900), (250, 200), 27),
                ((450, 1750), (2100, 200), 31),
                ((800, 400), (50, 550), 32),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}