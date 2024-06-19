# from game_objects import *
# from actors_description import *
from constants import *
# import pygame

locations = {
    '01':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
            'size': (MAXX, MAXY),
            'hostiles': {
                # 'demon Hula': {
                #     'already added': False,
                #     'point on map': 121,
                # },
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
                ((0, 1000), (1900, 50), 0),  #0
                ((0, 0), (50, 1000), 1),  #1
                ((1900, 1000), (1900, 50), 13),  #13
                ((3750, 250), (50, 750), 14),  #14
                ((3050, 250), (700, 50), 15),  #15
                ((2700, 300), (550, 50), 16),  #16
                ((2450, 350), (500, 50), 17),  #17
                ((50, 450), (200, 550), 38),  #38
                ((1000, 650), (150, 350), 42),  #42
                ((1150, 650), (550, 50), 43),  #43
                ((450, 850), (150, 150), 47),  #47
                ((650, 650), (350, 50), 49),  #49
                ((2400, 350), (50, 400), 55),  #55
                ((1000, 0), (150, 450), 59),  #59
                ((2575, 325), (125, 25), 60),  #60
                ((2950, 275), (100, 25), 61),  #61
                ((2000, 350), (50, 400), 62),  #62
                ((2050, 700), (350, 50), 63),  #63
                ((2050, 350), (350, 25), 64),  #64
                ((2075, 400), (300, 275), 65),  #65
                ((1150, 200), (450, 25), 66),  #66
                ((1825, 975), (75, 25), 67),  #67
                ((1725, 950), (100, 50), 68),  #68
                ((1625, 925), (100, 75), 69),  #69
                ((1525, 900), (100, 100), 70),  #70
                ((1425, 925), (100, 75), 71),  #71
                ((1350, 950), (75, 50), 72),  #72
                ((1275, 975), (75, 25), 73),  #73
                ((625, 200), (375, 25), 74),  #74
                ((650, 250), (50, 400), 75),  #75
                ((1050, 450), (50, 200), 76),  #76
                ((250, 650), (400, 50), 77),  #77
                ((650, 750), (150, 250), 78),  #78
                ((850, 750), (100, 250), 79),  #79


                ),
                
                'settings': {
                    75: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': False,
                        'gravity affected': False,
                        'actors pass through': True,
                        'trigger': True,
                        'trigger description': {
	                       	'make active': 76,
                        	'disappear': True,
                        },
                        'actions': {},
                    },
                    76: {
                        'ghost': False,
                        'speed': 0.1, 'active': False,
                        'collideable': True,
                        'gravity affected': False,
                        'actors pass through': False,
                        'trigger': False,
                        'trigger description': {},
                        'actions': {
	                        # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))  
	                        # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
	                        # ('turn on actions set', 0), 
                                 0: (('switch passability', 0), ('move', (1050, 650)), ('turn on actions set', 1),),
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
