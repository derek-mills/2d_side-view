from constants import *
locations = {
    
    'Cellar':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (7600, 4000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 3950), (7600, 50), 1),
                ((7550, 0), (50, 3950), 2),
                ((0, 0), (50, 3950), 3),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    4: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'Hall', 'xy': (0, 0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'Hall':
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
                ((0, 1050), (1900, 50), 1),
                ((1850, 0), (50, 1050), 3),
                ((0, 850), (50, 200), 4),
                ((0, 0), (50, 850), 5),
                ((650, 800), (1300, 50), 6),
                ((750, 500), (300, 300), 7),
                ((850, 250), (650, 100), 8),
                ((350, 200), (150, 200), 9),
                ((400, 450), (50, 50), 10),
                ((400, 100), (50, 50), 11),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    4: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'Alley', 'xy': (1800, 750)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'Alley':
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
                ((0, 950), (1900, 100), 1),  #1
                ((0, 0), (50, 950), 2),  #2
                ((1850, 0), (50, 750), 3),  #3
                ((1850, 750), (50, 200), 4),  #4
                ((600, 0), (650, 200), 5),  #5
                ((800, 200), (300, 150), 6),  #6
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    6: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {}, 'disappear': False, 'make active': [1, 3, 2]},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}