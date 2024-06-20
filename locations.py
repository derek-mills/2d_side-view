# IMPORTANT NOTE:
# To modify level content edit locations_template.py file only!
# locations.py will be overwritten after the level editor has done saving.

# from game_objects import *

# from actors_description import *
from constants import *
# import pygame


locations = {
    '01':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (5500,MAXY),
            'hostiles': {
                'demon 1': {
                	'already added': False,
                	'start xy': ((1500, 200), (1600, 200), (1700, 200)),
                },
                # 'demon Hildegarda': {
                #     'already added': False,
                #     'point on map': 103,
                # }

            },
            'demolishers': {
                # HERE WILL BE A GEOMETRY DESCRIPTION OF EVERY PLATFORM AFTER level_editor.py USAGE:
                'dem rectangles': (

                ),            	
            },
            'obstacles': {
                # HERE WILL BE A GEOMETRY DESCRIPTION OF EVERY PLATFORM AFTER level_editor.py USAGE:
                'obs rectangles': (
                ((0, 900), (5450, 150), 0),  #0
                ((0, 0), (50, 900), 2),  #2
                ((5100, 550), (350, 50), 3),  #3
                ((5300, 0), (150, 550), 4),  #4
                ((50, 0), (5250, 50), 5),  #5
                ((300, 600), (150, 50), 6),  #6


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
                    6: {
                        'ghost': False,
                        'speed': 1., 'active': True,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': False,
                        'exotic movement': 'sin',
                        'invisible': False,                        
                        'trigger': False,
                        'trigger description': {},
                        'actions': {
	                        # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))  
	                        # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
	                        # ('turn on actions set', 0), ('switch gravity', 0),  
                                 
                                 0: (('move', (1800,0, 150, 1500)), ('move', 'start area'), ('repeat', 0)),
                                 1: (('move', (0, 0)),),
                             }
		            },
                    28: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': True,
                        'gravity affected': False,
                        'actors pass through': False,
                        'invisible': False,                                                
                        'trigger': False,
                        'trigger description': {},
                        'actions': {
	                        # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))  
	                        # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
	                        # ('turn on actions set', 0), 
                                 #0: (('switch passability', 0), ('move', (1050, 650)), ('turn on actions set', 1),),
                                 0: (('switch passability', 0), ('wait', 30), ('move', (3250, 1350)),),
                                 1: (('move', (1550, 500)),),
                             }
		            },		
                    30: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': True,
                        'gravity affected': False,
                        'actors pass through': False,
                        'invisible': False,                                                
                        'trigger': False,
                        'trigger description': {},
                        'actions': {
	                        # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))  
	                        # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
	                        # ('turn on actions set', 0), 
                                 #0: (('switch passability', 0), ('move', (1050, 650)), ('turn on actions set', 1),),
                                 0: (('switch passability', 0), ('wait', 40), ('move', (3350, 1350)),),
                                 1: (('move', (1550, 500)),),
                             }
		            },
                },
                ####################################
            },
            'items': {
                'central light switcher': {
                    'already added': False,
                    'position': (837, 793),
                    'destination': (837, 793),
                    'associated point': 183,
                    # 'position': (870, 300),
                    # 'destination': (870, 300),
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'light switch #2',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                        "self.locations['apartment_01_main_room']['lights']['central bulb']['glowing'] = False if self.locations['apartment_01_main_room']['lights']['central bulb']['glowing'] else True",
                        "self.locations['apartment_01_kitchen']['lights']['main room bulb']['glowing'] = False if self.locations['apartment_01_kitchen']['lights']['main room bulb']['glowing'] else True",
                        "self.lights_generate_static_illumination()",
                        "self.scaling_static_lights_image()",
                        "self.put_sound_to_queue((sounds_all['sound_click_4'][0], sounds_all['sound_click_4'][1], self.wandering_actors[self.current_wandering_actor]))",
                        # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 0.8
                },
                'kitchen light switcher': {
                    'already added': False,
                    'position': (1271, 576),
                    'destination': (1271, 576),
                    'associated point': 87,
                    # 'position': (870, 300),
                    # 'destination': (870, 300),
                    'speed': 0.1,
                    # 'sprite': 'void',
                    'sprite': 'light switch #2',
                    'available': True,
                    'mode': 'interact',
                    # 'mode': 'on touch',
                    'index': None,
                    'action': {
                        'action trigger': True,
                        'storage': False,
                        'inventory': None,
                        'target': (
                            "self.locations['apartment_01_kitchen']['lights']['custom bulb']['glowing'] = False if self.locations['apartment_01_kitchen']['lights']['custom bulb']['glowing'] else True",
                            "self.locations['apartment_01_main_room']['lights']['kitchen bulb']['glowing'] = False if self.locations['apartment_01_main_room']['lights']['kitchen bulb']['glowing'] else True",
                            "self.lights_generate_static_illumination()",
                            "self.scaling_static_lights_image()",
                            "self.put_sound_to_queue((sounds_all['sound_click_4'][0], sounds_all['sound_click_4'][1], self.wandering_actors[self.current_wandering_actor]))",
                            # "print('light switched')"
                        ),
                        'multiple': True,
                        # 'multiple': False,
                    },
                    'TTL': -1,
                    'description': 'light switcher',
                    'scale': 0.8
                },
            },
    },

}
