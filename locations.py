from constants import *
locations = {

    '89d86630-390f-11ef-aa3e-63422c966797':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (1920, 1000), 
            'hostiles': {
            },
            'demolishers': {
                'dem rectangles': (
                ),
            },
            'obstacles': {  
	        #((0, 1000), (7650, 50), 1),  #1
                'obs rectangles': ( 
                ), # OBSTACLE RECTANGLES SECTION END

                'settings': {
                #     16: {
                #         'ghost': False,
                #         'speed': 0.1, 'active': False,
                #         'collideable': False,
                #         'gravity affected': False,
                #         'actors pass through': True,
                #         'invisible': True,
                #         'trigger': True,
                #         'trigger description': {
                #            	#'make active': (26,28,30),
                #         	'change location': {
                #         		'new location': 'Mansion hall',
                #         		'xy': (100, 100),
                #         	},
                #         	'disappear': False,
                #         },
                #         'actions': {},
                #     },
                # },

                #  6: {
                #     'ghost': False,
                #     'speed': 1., 'active': True,
                #     'collideable': False,
                #     'gravity affected': False,
                #     'actors pass through': False,
                #     'exotic movement': 'sin',
                #     'invisible': False,
                #     'trigger': False,
                #     'trigger description': {},
                #     'actions': {
                #         # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))
                #         # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
                #         # ('turn on actions set', 0), ('switch gravity', 0),
                #
                #              0: (('move', (1800,0, 150, 1500)), ('move', 'start area'), ('repeat', 0)),
                #              1: (('move', (0, 0)),),
                #          }
                },

            },
            'items': {
                },
    },


    
    'b6430b68-38fa-11ef-aa3e-63422c966797':
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
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    'a1d4c0e2-38da-11ef-aa3e-63422c966797':
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
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
    '9ba1c670-38da-11ef-aa3e-63422c966797':
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
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
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
                ((50, 750), (700, 50), 8),
                ((750, 500), (50, 300), 9),
                ((800, 500), (400, 50), 10),
                ((1200, 500), (50, 300), 11),
                ((1750, 250), (50, 550), 15),
                ((1250, 750), (500, 50), 16),
                ((800, 750), (400, 50), 17),
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    5: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 1', 'xy': (2850.0, 1800.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                    6: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 1', 'xy': (2850.0, 1750.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                    4: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': '8f731f90-376b-11ef-aa3e-63422c966797', 'xy': (100, 850)}, 'disappear': False, 'make active': None},
                        'actions': {},
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
                ((0, 1950), (3000, 50), 1),  #1
                ((400, 1550), (2300, 50), 6),  #6
                ((2950, 1750), (50, 200), 7),  #7
                ((2950, 0), (50, 1750), 8),  #8
                ((0, 0), (50, 1950), 9),  #9
                ((1650, 0), (1300, 50), 15),  #15
                ((50, 750), (350, 50), 19),  #19
                ((450, 950), (400, 50), 20),  #20
                ((900, 1150), (350, 50), 21),  #21
                ((2300, 50), (400, 1250), 22),  #22
                ((400, 1650), (2300, 250), 23),  #23
                ((2700, 1150), (100, 150), 24),  #24
                ((2850, 600), (100, 150), 25),  #25
                ((2700, 250), (100, 50), 26),  #26
                ((1300, 900), (250, 200), 27),  #27
                  ), # OBSTACLE RECTANGLES SECTION END
                'settings': {
                    5: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 2', 'xy': (100.0, 800.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                    7: {
                        'ghost': False,
                        'speed': 0.0,
                        'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {'change location': {'new location': 'room 2', 'xy': (100.0, 850.0)}, 'disappear': False, 'make active': None},
                        'actions': {},
                  },
                  } # OBSTACLE SETTINGS SECTION END
              },
            'items': {},
    },
}