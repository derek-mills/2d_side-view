from constants import *
locations = {
    
    '7d':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (5000, 2000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 1950), (1800, 50), 1),
                ((2100, 1950), (2900, 50), 2),
                ((4950, 1600), (50, 350), 3),
                ((4950, 0), (50, 1600), 4),
                ((0, 0), (50, 1950), 5),
                ((50, 0), (4900, 50), 6),
                ((1800, 1950), (300, 50), 7),
                ((1600, 1550), (200, 400), 8),
                ((2100, 1550), (200, 400), 9),
                ((1525, 1550), (75, 25), 10),
                ((1450, 1575), (150, 25), 11),
                ((1375, 1600), (225, 25), 12),
                ((1250, 1625), (350, 25), 13),
                ((1150, 1650), (450, 25), 14),
                ((1050, 1675), (550, 25), 15),
                ((975, 1700), (625, 25), 16),
                ((900, 1725), (700, 25), 17),
                ((850, 1750), (750, 25), 18),
                ((800, 1775), (800, 25), 19),
                ((750, 1800), (850, 25), 20),
                ((725, 1825), (875, 25), 21),
                ((700, 1850), (900, 25), 22),
                ((675, 1875), (925, 25), 23),
                ((650, 1900), (950, 25), 24),
                ((625, 1925), (975, 25), 25),
                ((2150, 950), (100, 600), 26),
                ((2100, 50), (200, 900), 27),
                ((1600, 50), (200, 900), 28),
                ((2300, 1550), (150, 400), 29),
                ((2450, 1750), (100, 100), 30),
                ((2300, 550), (600, 100), 31),
                ((2900, 450), (550, 100), 32),
                ((3450, 200), (350, 250), 33),
                ((3550, 450), (150, 750), 34),
                ((3500, 1200), (250, 100), 35),
                ((3600, 1300), (50, 250), 36),
                ((2650, 200), (800, 50), 37),
                ((2550, 100), (100, 250), 38),
                ((2300, 150), (250, 150), 39),
                ((3800, 450), (100, 100), 40),
                ((3350, 550), (200, 50), 41),
                ((3700, 550), (200, 50), 42),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    7: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': True,
                        'teleport description': {'new location': 'room 1', 'xy': (300.0, 0.0)},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    '2':
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
                ((0, 950), (1950, 50), 1),
                ((0, 0), (50, 950), 2),
                ((1900, 0), (50, 950), 3),
                ((50, 450), (750, 50), 4),
                ((300, 0), (50, 450), 15),
                ((50, 500), (750, 50), 16),
                ((50, 550), (750, 50), 17),
                ((50, 600), (750, 50), 18),
                ((50, 650), (750, 50), 19),
                ((50, 700), (750, 50), 20),
                ((50, 750), (750, 50), 21),
                ((50, 800), (750, 50), 22),
                ((50, 850), (750, 50), 23),
                ((50, 900), (750, 50), 24),
                ((950, 400), (400, 300), 25),
                ((450, 100), (350, 50), 26),
                ((400, 0), (50, 50), 27),
                ((1000, 800), (150, 150), 28),
                ((1200, 800), (150, 150), 29),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    15: {
                        'ghost': False,
                        'actors pass through': True,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'make active': [25, 24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    16: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (100, 500)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    17: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (150, 550)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    18: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (200, 600)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    19: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (250, 650)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    20: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (300, 700)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    21: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (350, 750)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    22: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (400, 800)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    23: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (450, 850)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    24: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: (('move', (500, 900)), ('stop', 0))},
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [24, 23, 22, 21, 20, 19, 18, 17, 16], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    25: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: [('move', (950, 50)), ('wait', 30), ('switch gravity', 0), ('stop', 0)]},
                        'collideable': True,
                        'gravity affected': False,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    26: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': True,
                        'gravity affected': True,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    27: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': True,
                        'gravity affected': True,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    28: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': True,
                        'gravity affected': True,
                        'invisible': False,
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'teleport': False,
                        'teleport description': {'new location': '', 'xy': [0, 0]},
                  },
                    29: {
                        'ghost': False,
                        'actors pass through': False,
                        'speed': 0.2,
                        'active': False,
                        'actions': {0: []},
                        'collideable': True,
                        'gravity affected': True,
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
    '64e4a58e-3dbd-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (10000, 1080),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 0), (10000, 50), 3),  #3
                ((0, 50), (50, 900), 4),  #4
                ((9450, 350), (550, 50), 5),  #5
                ((9950, 50), (50, 300), 6),  #6
                ((9250, 400), (250, 50), 7),  #7
                ((9075, 425), (175, 25), 8),  #8
                ((9350, 375), (100, 25), 9),  #9
                ((9500, 400), (50, 350), 10),  #10
                ((9000, 450), (500, 25), 11),  #11
                ((8850, 475), (650, 25), 12),  #12
                ((8775, 500), (725, 25), 13),  #13
                ((8650, 525), (850, 25), 14),  #14
                ((8500, 550), (1000, 25), 15),  #15
                ((8350, 600), (1150, 150), 16),  #16
                ((8400, 575), (1100, 25), 17),  #17
                ((1050, 50), (50, 750), 19),  #19
                ((1550, 50), (50, 750), 21),  #21
                ((1800, 50), (50, 200), 23),  #23
                ((4150, 50), (100, 100), 27),  #27
                ((4350, 50), (50, 300), 28),  #28
                ((4500, 50), (100, 50), 29),  #29
                ((4425, 50), (50, 75), 30),  #30
                ((4275, 50), (25, 450), 31),  #31
                ((4325, 175), (25, 400), 32),  #32
                ((4625, 50), (50, 500), 33),  #33
                ((4725, 50), (50, 75), 34),  #34
                ((4750, 125), (25, 350), 35),  #35
                ((4175, 150), (50, 275), 36),  #36
                ((4200, 425), (25, 125), 37),  #37
                ((4450, 125), (25, 450), 38),  #38
                ((4525, 100), (50, 475), 39),  #39
                ((4800, 50), (50, 100), 40),  #40
                ((4800, 150), (25, 175), 41),  #41
                ((4875, 50), (100, 100), 42),  #42
                ((4900, 150), (50, 100), 43),  #43
                ((5000, 50), (25, 25), 44),  #44
                ((5050, 50), (50, 75), 45),  #45
                ((5425, 650), (50, 300), 46),  #46
                ((5475, 650), (250, 50), 47),  #47
                ((5725, 650), (50, 300), 48),  #48
                ((6125, 625), (300, 25), 50),  #50
                ((6125, 50), (25, 575), 52),  #52
                ((0, 950), (50, 150), 53),  #53
                ((50, 1050), (9950, 50), 54),  #54
                ((9950, 400), (50, 650), 55),  #55
                ((5450, 50), (50, 600), 56),  #56
                ((5700, 50), (50, 600), 57),  #57
                ((1050, 800), (50, 250), 58),  #58
                ((1550, 800), (50, 250), 59),  #59
                ((2650, 50), (50, 400), 61),  #61
                ((3150, 50), (50, 400), 62),  #62
                ((8050, 700), (300, 50), 63),  #63
                ((8300, 650), (50, 50), 64),  #64
                ((8325, 625), (25, 25), 65),  #65
                ((8275, 675), (25, 25), 66),  #66
                ((950, 800), (50, 250), 67),  #67
                ((1450, 800), (50, 250), 69),  #69
                ((1450, 550), (50, 200), 71),  #71
                ((800, 250), (50, 800), 72),  #72
                ((550, 1050), (250, 50), 73),  #73
                ((600, 150), (150, 150), 74),  #74
                ((350, 550), (300, 50), 75),  #75
                ((2150, 800), (50, 250), 89),  #89
                ((2150, 750), (50, 50), 90),  #90
                ((2150, 700), (50, 50), 91),  #91
                ((2150, 650), (50, 50), 92),  #92
                ((2150, 600), (50, 50), 93),  #93
                ((2150, 550), (50, 50), 94),  #94
                ((2150, 500), (50, 50), 95),  #95
                ((2150, 450), (50, 50), 96),  #96
                ((2150, 400), (50, 50), 97),  #97
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