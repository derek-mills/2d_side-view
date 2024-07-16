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
                ((0, 950), (5000, 50), 17),  #17
                ((4950, 550), (50, 400), 18),  #18
                ((4950, 0), (50, 550), 19),  #19
                ((0, 0), (50, 950), 20),  #20
                ((750, 850), (800, 100), 51),  #51
                ((1800, 150), (950, 200), 52),  #52
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    17: {
                        'sprite': 2,
                        'sprite elevated': False,
                        'ghost': False,
                        'actors pass through': False,
                        'actors may grab': False,
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
                    51: {
                        'sprite': 7,
                        'sprite elevated': True,
                        'ghost': False,
                        'actors pass through': False,
                        'actors may grab': False,
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
                    52: {
                        'sprite': 5,
                        'sprite elevated': False,
                        'ghost': False,
                        'actors pass through': False,
                        'actors may grab': False,
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