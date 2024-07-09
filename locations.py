from constants import *
locations = {
    
    '63e20b98-3d97-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (3500, 3500),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 3450), (3150, 50), 1),  #1
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'de7126d8-3d96-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (1920, 1000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'c6bd7a96-3d96-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (0, 0),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'c5b44120-3d96-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (0, 0),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'bca6a154-3d96-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (0, 0),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
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
                ((2300, 50), (400, 1250), 22),
                ((2700, 1150), (100, 150), 24),
                ((2850, 600), (100, 150), 25),
                ((2700, 250), (100, 50), 26),
                ((450, 1750), (2100, 200), 31),
                ((800, 400), (50, 550), 32),
                ((800, 0), (850, 400), 34),
                ((800, 1000), (1500, 50), 35),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    32: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                    31: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': True},
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}