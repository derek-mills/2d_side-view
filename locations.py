# from game_objects import *
# from actors_description import *
from constants import *
# import pygame



locations = {
    'dkajshkasjdh298123 sad':
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
                'obs rectangles': (
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((100, 750), (1750, 100), 4),  #4
                ((0, 900), (1900, 100), 5),  #5
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                },

            },
            'items': {
                },
    },


    'Mappppp':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (3000, 1200), 
            'hostiles': {
            },
            'demolishers': {
                'dem rectangles': (
                ),            	
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 900), (1900, 100), 5),  #5
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                },

            },
            'items': {
                },
    },


    'ahdahdui2313123123':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (5000, 2000), 
            'hostiles': {
            },
            'demolishers': {
                'dem rectangles': (
                ),            	
            },
            'obstacles': {
                'obs rectangles': (
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((100, 750), (1750, 100), 4),  #4
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                },

            },
            'items': {
                },
    },


    '212ddsd':
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
                'obs rectangles': (
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((100, 750), (1750, 100), 4),  #4
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((200, 500), (450, 200), 0),  #0
                ((900, 450), (250, 300), 1),  #1
                ((1250, 450), (200, 200), 2),  #2
                ((150, 800), (600, 150), 3),  #3                
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                },

            },
            'items': {
                },
    },


    'sdad':
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
                'obs rectangles': (
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((100, 750), (1750, 100), 4),  #4
                ((0, 900), (1900, 100), 5),  #5
                ((250, 300), (300, 250), 1),  #1
                ((650, 500), (300, 50), 2),  #2
                ((1000, 500), (150, 50), 3),  #3
                ((1250, 450), (200, 200), 2),  #2
                ((550, 150), (150, 100), 7),  #7
                ((900, 150), (150, 100), 8),  #8
                ((850, 300), (100, 50), 10),  #10
                ((500, 350), (150, 350), 11),  #11
                ((800, 500), (100, 200), 12),  #12
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                    34: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'invisible': True,                        
                        'trigger': True,
                        'trigger description': {
	                       	'make active': (26,28,30),
                        	'disappear': True,
                        },
                        'actions': {},
                    },
                },

            },
            'items': {
                },
    },



}
