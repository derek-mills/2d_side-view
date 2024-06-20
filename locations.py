# from game_objects import *
# from actors_description import *
from constants import *
# import pygame



locations = {
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
                ((600, 750), (800, 100), 0),  #0
                ((150, 500), (400, 150), 1),  #1
                ((50, 850), (350, 100), 2),  #2
                ),
                
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
                ((600, 750), (800, 100), 0),  #0
                ((150, 500), (400, 150), 1),  #1
                ((50, 850), (350, 100), 2),  #2
                ((200, 500), (450, 200), 0),  #0
                ((900, 450), (250, 300), 1),  #1
                ((1250, 450), (200, 200), 2),  #2
                ),
                
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
