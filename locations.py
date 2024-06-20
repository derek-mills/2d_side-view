from constants import *

locations = {
    '1':
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
            'obstacles': {  #((0, 1000), (7650, 50), 1),  #1
                'obs rectangles': (
                ), # OBSTACLE RECTANGLES SECTION END
                
                'settings': {
                    16: {
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
                        		'new location': 'Mansion hall',
                        		'xy': (100, 100),
                        	},
                        	'disappear': False,
                        },
                        'actions': {},
                    },                 
                },

            },
            'items': {
                },
    },




}
