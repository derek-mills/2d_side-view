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
                ((0, 50), (50, 850), 2),  #2
                ((0, 1050), (1950, 50), 3),  #3
                ((1900, 50), (50, 1000), 4),  #4
                ((0, 900), (50, 150), 5),  #5
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    5: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 1', 'xy': (2850.0, 1800.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
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
                ((2950, 0), (50, 1800), 2),
                ((0, 0), (50, 1800), 3),
                ((0, 1800), (50, 150), 4),
                ((2950, 1800), (50, 150), 5),
                ((400, 1550), (2300, 50), 6),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    5: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 2', 'xy': (100.0, 800.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}
