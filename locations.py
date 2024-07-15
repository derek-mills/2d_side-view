from constants import *
locations = {
    
    '4cb6277c-424e-11ef-b7ff-bfb4330f33e3':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (5000, 1000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 975), (5000, 25), 1),  #1
                ((0, 0), (25, 975), 2),  #2
                ((4975, 0), (25, 975), 3),  #3
                ((800, 775), (225, 200), 4),  #4
                ((850, 650), (125, 125), 5),  #5
                ((1025, 800), (200, 175), 6),  #6
                ((1225, 850), (175, 125), 7),  #7
                ((750, 925), (50, 50), 8),  #8
                ((575, 950), (175, 25), 9),  #9
                ((1400, 875), (150, 100), 10),  #10
                ((1550, 900), (50, 75), 11),  #11
                ((1600, 925), (250, 50), 12),  #12
                ((1850, 950), (125, 25), 13),  #13
                ((975, 700), (25, 75), 14),  #14
                ((2200, 950), (450, 25), 15),  #15
                ((2250, 450), (350, 500), 16),  #16
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    16: {
                        'ghost': False,
                        'actors pass through': False,
                        'actors may grab': True,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
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
