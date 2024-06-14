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
                ((1900, 1000), (1900, 50), 13),  #13
                ((3750, 250), (50, 750), 14),  #14
                ((3050, 250), (700, 50), 15),  #15
                ((2700, 300), (550, 50), 16),  #16
                ((2450, 350), (500, 50), 17),  #17
                ((50, 450), (200, 550), 38),  #38
                ((1000, 650), (150, 350), 42),  #42
                ((1150, 650), (550, 50), 43),  #43
                ((1700, 500), (100, 200), 44),  #44
                ((1800, 650), (250, 50), 45),  #45
                ((2050, 450), (100, 250), 46),  #46
                ((450, 850), (150, 150), 47),  #47
                ((650, 250), (550, 50), 48),  #48
                ((650, 650), (350, 50), 49),  #49
                ((700, 450), (50, 200), 'collideable' , 'gravity affected' , 50),  #50
                ((725, 325), (250, 25), 'collideable' , 'gravity affected' , 51),  #51
                ((725, 375), (25, 50), 'collideable' , 'gravity affected' , 52),  #52
                ((775, 375), (25, 50), 'collideable' , 'gravity affected' , 53),  #53
                ((825, 450), (150, 25), 'collideable' , 'gravity affected' , 54),  #54


                ),
                
                'actions': {
                     49: {
                         0: (('move', (250, 600)), ),
                     },

                },
                'settings': {
                    49: {
                        'speed': 0.1,
                    },

                }
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
