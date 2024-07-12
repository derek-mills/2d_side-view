from constants import *
locations = {
    
    '64e4a58e-3dbd-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (10000, 1080),
            'hostiles': {
            	(700, 850): {
                    'name': 'demon 1',
                    'health': 1000,
                    'max speed': 10,
                    'height': 400,
            	},

            	(750, 850): {
                    'name': 'demon 1',
                    'health': 1,
                    'max speed': 1,
                    'height': 200,
            	},

              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 0), (10000, 50), 3),  #3
                ((0, 50), (50, 900), 4),  #4
                ((1050, 50), (50, 750), 19),  #19
                ((1550, 50), (50, 750), 21),  #21
                ((1650, 50), (50, 200), 23),  #23
                ((5425, 650), (50, 300), 46),  #46
                ((5475, 650), (250, 50), 47),  #47
                ((5725, 650), (50, 300), 48),  #48
                ((0, 950), (50, 150), 53),  #53
                ((50, 1050), (9950, 50), 54),  #54
                ((5450, 50), (50, 600), 56),  #56
                ((5700, 50), (50, 600), 57),  #57
                ((1050, 800), (50, 250), 58),  #58
                ((1550, 800), (50, 250), 59),  #59
                ((950, 800), (50, 250), 67),  #67
                ((1450, 800), (50, 250), 69),  #69
                ((1300, 850), (50, 200), 71),  #71
                ((800, 250), (50, 800), 72),  #72
                ((550, 1050), (250, 50), 73),  #73
                ((600, 150), (150, 150), 74),  #74
                ((350, 550), (300, 50), 75),  #75
                ((9950, 50), (50, 1000), 98),  #98
                ((600, 600), (200, 100), 99),  #99
                ((3150, 150), (250, 100), 100),  #100
                ((6450, 50), (700, 600), 101),  #101
                ((5750, 600), (700, 50), 102),  #102
                ((7150, 600), (650, 50), 103),  #103
                ((2350, 50), (800, 600), 104),  #104
                ((1700, 150), (650, 100), 105),  #105
                ((2200, 650), (50, 400), 106),  #106
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    4: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 2', 'xy': (1800.0, 'keep y')},
                  },
                    58: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.5,
                        'active': False,
                        'actions': {0: [('move', (1050, 450)), ('stop', (0, 0))], 1: [('move', (1050, 800)), ('stop', (0, 0))]},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    67: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'make active': [(58, 'self', 0)], 'disappear': True},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    69: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'make active': [(58, 'self', 1)], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    59: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.5,
                        'active': False,
                        'actions': {0: [('move', (1550, 450)), ('stop', (0, 0))]},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    71: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'make active': [(59, 'self', 0)], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    72: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': True,
                        'trigger description': {'make active': [(22, 'room 2', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: [('move', (0, 0)), ('stop', (0, 0))]},
                  },
                    73: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': True,
                        'trigger description': {'make active': [(74, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: []},
                  },
                    74: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'collideable': True,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'active': False,
                        'actions': {0: [('switch gravity', 0), ('stop', 0)]},
                  },
                    75: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': False,
                        'trigger description': {'make active': [(0, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                    106: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': True,
                        'trigger description': {'make active': [(104, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                  },
                    104: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'collideable': True,
                        'gravity affected': False,
                        'invisible': False,
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                        'trigger': False,
                        'trigger description': {'make active': [(0, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: [('switch gravity', 0), ('stop', 0)]},
                  },
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
            	(600, 850): {
                    'name': 'demon 1',
                    'health': 110,
                    'max speed': 5,
                    'height': 300,

              },
            	(650, 850): {
                    'name': 'demon 1',
                    'health': 2,
                    'max speed': 2,
                    'height': 100,

              },
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
                ((900, 800), (50, 250), 21),
                ((1400, 50), (150, 1000), 22),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    6: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 1', 'xy': (2850.0, 1750.0)},
                  },
                    4: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': '64e4a58e-3dbd-11ef-a7e0-f5ed2070cb71', 'xy': (100.0, 'keep y')},
                  },
                    22: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: [('move', (1400, -500)), ('stop', (0, 0))]},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
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
                ((2950, 1750), (50, 200), 7),
                ((2950, 0), (50, 1750), 8),
                ((0, 0), (50, 1950), 9),
                ((1650, 0), (1300, 50), 15),
                ((2300, 50), (400, 1250), 22),
                ((2700, 1150), (100, 150), 24),
                ((2850, 600), (100, 150), 25),
                ((2700, 250), (100, 50), 26),
                ((450, 1750), (2100, 200), 31),
                ((800, 400), (50, 550), 32),
                ((700, 0), (950, 400), 38),
                ((450, 950), (1200, 50), 39),
                ((1900, 1250), (400, 50), 40),
                ((900, 400), (750, 550), 42),
                ((50, 950), (400, 50), 48),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    32: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: [('move', (0, 0)), ('die', 0)]},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'make active': [42], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    7: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.0,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 2', 'xy': (100.0, 850.0)},
                  },
                    42: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: [('move', (900, 0)), ('die', 0)]},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [42], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}