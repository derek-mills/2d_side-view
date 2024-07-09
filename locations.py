from constants import *
locations = {
    
    '64e4a58e-3dbd-11ef-a7e0-f5ed2070cb71':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (10000, 1000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 950), (10000, 50), 1),
                ((9950, 400), (50, 550), 2),
                ((0, 0), (10000, 50), 3),
                ((0, 50), (50, 900), 4),
                ((9450, 350), (550, 50), 5),
                ((9950, 50), (50, 300), 6),
                ((9250, 400), (250, 50), 7),
                ((9075, 425), (175, 25), 8),
                ((9350, 375), (100, 25), 9),
                ((9500, 400), (50, 350), 10),
                ((9000, 450), (500, 25), 11),
                ((8850, 475), (650, 25), 12),
                ((8775, 500), (725, 25), 13),
                ((8650, 525), (850, 25), 14),
                ((8500, 550), (1000, 25), 15),
                ((8350, 600), (1150, 150), 16),
                ((8400, 575), (1100, 25), 17),
                ((800, 550), (50, 400), 18),
                ((1050, 50), (50, 750), 19),
                ((1300, 550), (50, 400), 20),
                ((1550, 50), (50, 750), 21),
                ((1800, 550), (50, 400), 22),
                ((1800, 50), (50, 200), 23),
                ((2050, 50), (50, 850), 24),
                ((2650, 600), (300, 350), 25),
                ((3250, 550), (350, 400), 26),
                ((4150, 50), (100, 100), 27),
                ((4350, 50), (50, 300), 28),
                ((4500, 50), (100, 50), 29),
                ((4425, 50), (50, 75), 30),
                ((4275, 50), (25, 450), 31),
                ((4325, 175), (25, 400), 32),
                ((4625, 50), (50, 500), 33),
                ((4725, 50), (50, 75), 34),
                ((4750, 125), (25, 350), 35),
                ((4175, 150), (50, 275), 36),
                ((4200, 425), (25, 125), 37),
                ((4450, 125), (25, 450), 38),
                ((4525, 100), (50, 475), 39),
                ((4800, 50), (50, 100), 40),
                ((4800, 150), (25, 175), 41),
                ((4875, 50), (100, 100), 42),
                ((4900, 150), (50, 100), 43),
                ((5000, 50), (25, 25), 44),
                ((5050, 50), (50, 75), 45),
                ((5425, 650), (50, 300), 46),
                ((5475, 650), (250, 50), 47),
                ((5725, 650), (50, 300), 48),
                ((6575, 450), (25, 500), 49),
                ((6125, 625), (300, 25), 50),
                ((6250, 450), (325, 25), 51),
                ((6125, 50), (25, 575), 52),
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
                ((0, 0), (1950, 50), 1),  #1
                ((0, 1050), (1950, 50), 3),  #3
                ((1900, 50), (50, 1000), 4),  #4
                ((0, 850), (50, 200), 6),  #6
                ((0, 50), (50, 800), 7),  #7
                ((600, 750), (50, 300), 18),  #18
                ((650, 750), (300, 50), 19),  #19
                ((900, 800), (50, 250), 21),  #21
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
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': True,
                        'teleport description': {'new location': '64e4a58e-3dbd-11ef-a7e0-f5ed2070cb71', 'xy': (100.0, 'keep y')},
                        'trigger': False,
                        'trigger description': {'make active': [], 'disappear': False},
                        'active': False,
                        'actions': {0: (('move', (0, 0, 100, 1000)), ('move', 'start area'), ('repeat', 0))},
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
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}
