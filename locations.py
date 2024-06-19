# from game_objects import *
# from actors_description import *
from constants import *
# import pygame



locations = {
    '01':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (2*MAXX, MAXY),
            'hostiles': {
                'demon 1': {
                	'already added': False,
                	'start xy': ((1500, 200), (1600, 200), (1700, 200)),
                },

            },
            'demolishers': {
                # HERE WILL BE A GEOMETRY DESCRIPTION OF EVERY PLATFORM AFTER level_editor.py USAGE:
                'dem rectangles': (

                ),            	
            },
            'obstacles': {
                # HERE WILL BE A GEOMETRY DESCRIPTION OF EVERY PLATFORM AFTER level_editor.py USAGE:
                'obs rectangles': (
                ((0, 0), (50, 2100), 0),  #0
                ((50, 2050), (5700, 50), 1),  #1
                ((5700, 0), (50, 2050), 2),  #2
                ((50, 1000), (850, 50), 3),  #3
                ((1200, 1000), (200, 50), 4),  #4
                ((1750, 1000), (200, 50), 5),  #5
                ((2300, 1000), (100, 50), 6),  #6
                ((2450, 1000), (50, 50), 7),  #7
                ((2550, 1000), (50, 50), 8),  #8
                ((2650, 1000), (3050, 50), 9),  #9
                ((2650, 0), (400, 700), 11),  #11
                ((3050, 0), (2650, 150), 12),  #12
                ((900, 1300), (300, 50), 13),  #13
                ((1350, 1500), (100, 550), 14),  #14
                ((2650, 1500), (100, 550), 15),  #15
                ((2900, 1700), (1450, 50), 16),  #16
                ((2575, 1525), (75, 525), 17),  #17
                ((2500, 1550), (75, 500), 18),  #18
                ((2425, 1575), (75, 475), 19),  #19
                ((2350, 1600), (75, 450), 20),  #20
                ((2275, 1625), (75, 450), 22),  #22
                ((2200, 1650), (75, 400), 23),  #23
                ((2125, 1675), (75, 375), 24),  #24
                ((1575, 1700), (550, 50), 25),  #25
                ((3150, 1050), (50, 300), 26),  #26
                ((3200, 1350), (50, 350), 27),  #27
                ((3250, 1050), (50, 300), 28),  #28
                ((3300, 1350), (50, 350), 29),  #29
                ((3350, 1050), (50, 300), 30),  #30
                ((3400, 1350), (50, 350), 31),  #31
                ((4300, 1750), (50, 50), 32),  #32
                ((4300, 1900), (50, 150), 33),  #33
                ((2900, 1050), (25, 650), 34),  #34


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
                    26: {
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
	                        # ('turn on actions set', 0), ('switch gravity', 0),  
                                 
                                 0: (('switch passability', 0), ('move', (3150,1350)),),
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
