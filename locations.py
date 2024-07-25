from constants import *
locations = {
    
    'hall':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (2000, 1000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 950), (2000, 50), 1),
                ((1950, 750), (50, 200), 2),
                ((-100, 750), (50, 200), 3),
                ((0, 0), (50, 750), 4),
                ((50, 0), (1950, 50), 5),
                ((1950, 50), (50, 700), 6),
                ((-100, 950), (100, 50), 7),
                ((-100, 700), (100, 50), 8),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    3: {
                        'sprite': 0,
                        'sprite elevated': False,
                        'force render': False,
                        'invisible': True,
                        'ghost': False,
                        'speed': 0.2,
                        'actors may grab': False,
                        'actors pass through': True,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'trigger': False,
                        'trigger description': {'make active': [(0, 'self', 0)], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'entrance', 'xy': (1900.0, 2300.0)},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'entrance':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (2000, 2500),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 2450), (2000, 50), 1),  #1
                ((1850, 2200), (150, 50), 2),  #2
                ((0, 0), (50, 2450), 3),  #3
                ((1750, 0), (250, 50), 4),  #4
                ((1950, 50), (50, 200), 5),  #5
                ((1800, 450), (200, 50), 6),  #6
                ((1750, 350), (50, 150), 7),  #7
                ((1950, 500), (50, 250), 8),  #8
                ((1950, 250), (50, 200), 9),  #9
                ((1950, 750), (50, 200), 10),  #10
                ((1800, 950), (200, 50), 11),  #11
                ((1750, 850), (50, 150), 12),  #12
                ((1950, 1000), (50, 250), 13),  #13
                ((1950, 1250), (50, 200), 14),  #14
                ((1800, 1450), (200, 50), 15),  #15
                ((1750, 1350), (50, 150), 16),  #16
                ((1950, 1500), (50, 700), 17),  #17
                ((2050, 2250), (50, 200), 18),  #18
                ((2000, 2450), (100, 50), 20),  #20
                ((2000, 2200), (100, 50), 21),  #21
                ((50, 0), (1700, 50), 22),  #22
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    18: {
                        'sprite': 0,
                        'sprite elevated': False,
                        'force render': False,
                        'ghost': False,
                        'actors pass through': True,
                        'actors may grab': False,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': True,
                        'teleport description': {'new location': 'hall', 'xy': (50.0, 800.0)},
                        'trigger': False,
                        'trigger description': {'make active': [(0, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: []},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}