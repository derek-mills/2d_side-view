from constants import *
locations = {
    
    'New map 108fe6c4-339a-11ef-9782-6dffda05a41a':
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
                ((0, 1050), (1950, 50), 1),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
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
                ((2600, 1550), (100, 2400), 4),
                ((2700, 1550), (4300, 50), 5),
                ((2650, 1500), (1100, 50), 6),
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
                ((200, 250), (100, 100), 12),
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
                ((600, 850), (250, 100), 7),  #7
                ((850, 800), (200, 150), 8),  #8
                ((1050, 750), (200, 200), 9),  #9
                ((1250, 750), (350, 50), 10),  #10
                ((1550, 800), (50, 150), 11),  #11
                ((1300, 850), (200, 50), 12),  #12
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
                    5: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {}, 'disappear': False, 'make active': [12, 11, 10]},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}