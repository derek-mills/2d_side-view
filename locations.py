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
                ((600, 900), (450, 50), 58),  #58
                ((600, 850), (450, 50), 59),  #59
                ((1150, 850), (300, 100), 60),  #60
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    17: {
                        'sprite': 4,
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
                    20: {
                        'sprite': 7,
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
                    58: {
                        'sprite': 13,
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
                    59: {
                        'sprite': 12,
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
                    60: {
                        'sprite': 15,
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
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}