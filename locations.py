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
                'actions': {
                    0: {
                        0: (('move', (300,450)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                    },
                    
		    13: {		
                        0: (('move', (1000,600)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                        },
                        
		    4: {
		        0: (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
		    },

                },
                'settings': {
                    0: {
                        'speed': 0.1,
                    },
                    13: {
                        'speed': 0.1,
                    },
                    4: {
                        'speed': 0.1,
                    },

                }
            },
            'obstacles': {
#, 'ghost'
#, 'move right'
#, 'move left'
#, 'collideable'
#, 'gravity affected'
                # 'actions': {
                #     3: {
                #         0: (('move', (950, 750)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                #     },
                #
                #     4: {
                #         0: (('move', (250, 600)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                #     },
                #
                # },
                # 'settings': {
                #     3: {
                #         'speed': 0.1,
                #     },
                #     4: {
                #         'speed': 0.3,
                #     },
                #
                # }
                # HERE WILL BE A GEOMETRY DESCRIPTION OF EVERY PLATFORM AFTER level_editor.py USAGE:
                'obs rectangles': (
                ((0, 1000), (1900, 50), 0),  #0
                ((0, 0), (50, 1000), 1),  #1
                ((900, 975), (75, 25), 2),  #2
                ((975, 950), (75, 25), 3),  #3
                ((1050, 925), (75, 25), 4),  #4
                ((1125, 900), (75, 25), 5),  #5
                ((1200, 875), (75, 25), 6),  #6
                ((1275, 850), (75, 25), 7),  #7
                ((1350, 875), (75, 25), 8),  #8
                ((1425, 900), (75, 25), 9),  #9
                ((1500, 925), (75, 25), 10),  #10
                ((1575, 950), (75, 25), 11),  #11
                ((1650, 975), (75, 25), 12),  #12
                ((1900, 1000), (1900, 50), 13),  #13
                ((3750, 250), (50, 750), 14),  #14
                ((3050, 250), (700, 50), 15),  #15
                ((2700, 300), (550, 50), 16),  #16
                ((2450, 350), (500, 50), 17),  #17
                ((700, 750), (1100, 50), 24),  #24
                ((900, 550), (250, 50), 25),  #25
                ((1050, 300), (300, 50), 26),  #26
#                ((1050, 200), (50, 50), 'collideable' , 'gravity affected', 27),  #27
#                ((1150, 200), (50, 50), 'collideable' , 'gravity affected', 28),  #28
#                ((1250, 200), (50, 50), 'collideable' , 'gravity affected', 29),  #29
#                ((1050, 100), (250, 50), 'collideable' , 'gravity affected', 30),  #30
#                ((1100, 50), (50, 50), 'collideable' , 'gravity affected', 31),  #31

                ),
                
                'actions': {
                     19: {
                         0: (('move', (1450, 300)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                     },
                     20: {
                         0: (('move', (50, 400)), ('move', 'start'), ('wait', 2), ('repeat', 0)),
                     }
                },
                'settings': {
                    19: {
                        'speed': 0.1,
                    },
                    20: {
                        'speed': 0.1,
                    },

                }
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
