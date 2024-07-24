from constants import *
locations = {
    
    'anothertest':
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
                ((0, 850), (1950, 150), 19),
                ((300, 500), (100, 150), 20),
                ((500, 250), (100, 500), 21),
                ((700, 200), (50, 550), 22),
                ((950, 250), (50, 450), 23),
                ((1200, 50), (150, 500), 24),
                ((1450, 200), (50, 400), 25),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    19: {
                        'sprite': 0,
                        'sprite elevated': True,
                        'force render': False,
                        'invisible': False,
                        'ghost': False,
                        'speed': 0.2,
                        'actors may grab': False,
                        'actors pass through': False,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'trigger': True,
                        'trigger description': {'make active': [(20, 'self', 0), (21, 'self', 0), (22, 'self', 0)], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'test1':
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
                ((0, 950), (1950, 50), 1),  #1
                ((0, 400), (50, 500), 2),  #2
                ((450, 450), (300, 250), 3),  #3
                ((1100, 450), (350, 250), 4),  #4
                ((950, 150), (50, 150), 5),  #5
                ((800, 550), (150, 200), 6),  #6
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    4: {
                        'sprite elevated': False,
                        'sprite': 0,
                        'force render': False,
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
                    3: {
                        'sprite elevated': False,
                        'sprite': 0,
                        'force render': False,
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
                    2: {
                        'sprite': 0,
                        'sprite elevated': False,
                        'force render': False,
                        'invisible': False,
                        'ghost': False,
                        'speed': 0.2,
                        'actors may grab': False,
                        'actors pass through': False,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'trigger': False,
                        'trigger description': {'make active': [(1, 'self', 0), (2, 'self', 0), (3, 'self', 0), (4, 'self', 0)], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    1: {
                        'sprite': 0,
                        'sprite elevated': False,
                        'force render': False,
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
                    6: {
                        'sprite elevated': False,
                        'sprite': 0,
                        'force render': False,
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