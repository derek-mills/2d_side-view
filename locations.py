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
                ((550, 875), (600, 50), 34),  #34
                ((600, 800), (550, 50), 35),  #35
                ((650, 725), (500, 50), 36),  #36
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    36: {
                        'sprite': 0,
                        'ghost': True,
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
                    35: {
                        'ghost': True,
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
                    34: {
                        'ghost': True,
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