from constants import *

locations = {

    'Attic room':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (1920, 1080), 
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

                # 'settings': {
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
                # },

            },
            'items': {
                },
    },



    'Hall':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (1920, 1080), 
            'hostiles': {
            },
            'demolishers': {
                'dem rectangles': (
                ),
            },
            'obstacles': {  
	        #((0, 1000), (7650, 50), 1),  #1
                'obs rectangles': ( 
                ((0, 1050), (1900, 50), 1),  #1
                ((1850, 0), (50, 1050), 3),  #3
                ((0, 850), (50, 200), 4),  #4
                ((0, 0), (50, 850), 5),  #5
                ((650, 800), (1300, 50), 6),  #6
                ((400, 850), (250, 50), 7),  #7
                ((275, 900), (125, 25), 8),  #8
                ((150, 925), (125, 25), 9),  #9
                ), # OBSTACLE RECTANGLES SECTION END

                'settings': {
                    4: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {
                           	#'make active': (26,28,30),
                        	'change location': {
                        		'new location': 'Alley',
                        		'xy': (1750, 800),
                        	},
                        	'disappear': False,
                        },
                        'actions': {},
                    },
                },

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
                # },

            },
            'items': {
                },
    },



    'Alley':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (1920, 1080), 
            'hostiles': {
            },
            'demolishers': {
                'dem rectangles': (
                ),
            },
            'obstacles': {  
	        #((0, 1000), (7650, 50), 1),  #1
                'obs rectangles': ( 
                ((0, 950), (1900, 100), 1),  #1
                ((0, 0), (50, 950), 2),  #2
                ((1850, 0), (50, 750), 3),  #3
                ((1850, 750), (50, 200), 4),  #4
                ((650, 200), (600, 100), 5),  #5
                ((700, 300), (50, 450), 6),  #6
                ((1150, 300), (50, 450), 7),  #7
                ((900, 650), (100, 50), 8),  #8
                ), # OBSTACLE RECTANGLES SECTION END
	    'settings': {
                    4: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,
                        'trigger': True,
                        'trigger description': {
                           	#'make active': (26,28,30),
                        	'change location': {
                        		'new location': 'Hall',
                        		'xy': (100, 900),
                        	},
                        	'disappear': False,
                        },
                        'actions': {},
                    },
                },

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
                # },

            },
            'items': {
                },
    },



}
