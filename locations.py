from constants import *
locations = {
    
    'stairway':
        {
            'music': 'music/ambient_1.mp3',
            'description': 'apartment #1',
            'size': (1500, 5000),
            'hostiles': {
              },
            'demolishers': {
                'dem rectangles': (
                  ), # DEMOLISHERS RECTANGLE SECTION END
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 4950), (1500, 50), 1),  #1
                ((-100, 4750), (50, 200), 2),  #2
                ((1450, 4750), (50, 200), 3),  #3
                ((50, 4450), (450, 50), 6),  #6
                ((50, 3950), (450, 50), 7),  #7
                ((50, 3450), (450, 50), 9),  #9
                ((1000, 3450), (450, 50), 14),  #14
                ((1000, 3950), (450, 50), 15),  #15
                ((1000, 4450), (450, 50), 16),  #16
                ((0, 4450), (50, 300), 17),  #17
                ((0, 4250), (50, 200), 18),  #18
                ((0, 3950), (50, 300), 19),  #19
                ((0, 3750), (50, 200), 20),  #20
                ((0, 3450), (50, 300), 21),  #21
                ((1450, 4450), (50, 300), 22),  #22
                ((1450, 4250), (50, 200), 23),  #23
                ((1450, 3950), (50, 300), 24),  #24
                ((1450, 3750), (50, 200), 25),  #25
                ((1450, 3450), (50, 300), 26),  #26
                ((0, 3250), (50, 200), 27),  #27
                ((0, 2950), (50, 300), 28),  #28
                ((50, 2950), (450, 50), 29),  #29
                ((0, 2750), (50, 200), 30),  #30
                ((0, 2450), (50, 300), 31),  #31
                ((50, 2450), (450, 50), 32),  #32
                ((0, 2250), (50, 200), 33),  #33
                ((0, 1950), (50, 300), 34),  #34
                ((50, 1950), (450, 50), 35),  #35
                ((0, 1750), (50, 200), 36),  #36
                ((0, 1450), (50, 300), 37),  #37
                ((50, 1450), (450, 50), 38),  #38
                ((0, 1250), (50, 200), 39),  #39
                ((0, 950), (50, 300), 40),  #40
                ((50, 950), (450, 50), 41),  #41
                ((0, 750), (50, 200), 42),  #42
                ((0, 450), (50, 300), 43),  #43
                ((50, 450), (450, 50), 44),  #44
                ((0, 250), (50, 200), 45),  #45
                ((0, 0), (50, 250), 46),  #46
                ((50, 0), (1450, 50), 47),  #47
                ((1450, 50), (50, 200), 48),  #48
                ((1450, 250), (50, 200), 49),  #49
                ((1000, 450), (450, 50), 50),  #50
                ((1450, 450), (50, 300), 51),  #51
                ((1450, 3250), (50, 200), 52),  #52
                ((1000, 2950), (450, 50), 53),  #53
                ((1450, 2950), (50, 300), 54),  #54
                ((1000, 2450), (450, 50), 55),  #55
                ((1450, 2450), (50, 300), 56),  #56
                ((1450, 2750), (50, 200), 57),  #57
                ((1000, 1950), (450, 50), 58),  #58
                ((1450, 1950), (50, 300), 59),  #59
                ((1450, 2250), (50, 200), 60),  #60
                ((1000, 1450), (450, 50), 61),  #61
                ((1450, 1450), (50, 300), 62),  #62
                ((1450, 1750), (50, 200), 63),  #63
                ((1000, 950), (450, 50), 64),  #64
                ((1450, 750), (50, 200), 65),  #65
                ((1450, 950), (50, 300), 66),  #66
                ((1450, 1250), (50, 200), 68),  #68
                ((-100, 4950), (100, 50), 69),  #69
                ((-100, 4700), (100, 50), 70),  #70
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    2: {
                        'sprite elevated': False,
                        'sprite': 0,
                        'force render': False,
                        'ghost': False,
                        'actors pass through': True,
                        'actors may grab': False,
                        'speed': 0.2,
                        'collideable': False,
                        'gravity affected': False,
                        'invisible': True,
                        'teleport': True,
                        'teleport description': {'new location': 'hall', 'xy': (1900.0, 800.0)},
                        'trigger': False,
                        'trigger description': {'make active': [(0, 'self', 0)], 'disappear': False},
                        'active': False,
                        'actions': {0: []},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
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
                ((2050, 750), (50, 200), 2),
                ((-100, 750), (50, 200), 3),
                ((0, 0), (50, 750), 4),
                ((50, 0), (1950, 50), 5),
                ((1950, 50), (50, 700), 6),
                ((-100, 950), (100, 50), 7),
                ((-100, 700), (100, 50), 8),
                ((2000, 950), (100, 50), 9),
                ((2000, 700), (100, 50), 10),
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
                    2: {
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
                        'teleport description': {'new location': 'stairway', 'xy': (50.0, 4800.0)},
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
                ((0, 2450), (2000, 50), 1),
                ((1850, 2200), (150, 50), 2),
                ((0, 0), (50, 2450), 3),
                ((1750, 0), (250, 50), 4),
                ((1950, 50), (50, 200), 5),
                ((1800, 450), (200, 50), 6),
                ((1750, 350), (50, 150), 7),
                ((1950, 500), (50, 250), 8),
                ((1950, 250), (50, 200), 9),
                ((1950, 750), (50, 200), 10),
                ((1800, 950), (200, 50), 11),
                ((1750, 850), (50, 150), 12),
                ((1950, 1000), (50, 250), 13),
                ((1950, 1250), (50, 200), 14),
                ((1800, 1450), (200, 50), 15),
                ((1750, 1350), (50, 150), 16),
                ((1950, 1500), (50, 700), 17),
                ((2050, 2250), (50, 200), 18),
                ((2000, 2450), (100, 50), 20),
                ((2000, 2200), (100, 50), 21),
                ((50, 0), (1700, 50), 22),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    18: {
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
                        'teleport description': {'new location': 'hall', 'xy': (50.0, 800.0)},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}