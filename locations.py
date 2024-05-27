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
            'obstacles': {
                # 'void': {
                #     'already added': False,
                #     'stops bullets': True,
                #     'active': False,
                #     'cells': (180,181,182,86,102,118,134,150,166),
                #     'sprite name': None,
                #     'sprite snap': 'left',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'invisible obstacle',
                #     'scale': 0,
                #     'actions': ()
                # },
                # 'piles 1': {
                #     'already added': False,
                #     'stops bullets': True,
                #     'active': False,
                #     'cells': (121,122,137,153,154,155, 185,186,187,202,218,189,190,206,222),
                #     'sprite name': 'pile 1x #1',
                #     'sprite snap': 'left',
                #     'available': True,
                #     'index': None,
                #     'TTL': -1,
                #     'description': 'BIG QUESTION',
                #     'scale': 1.4,
                #     'actions': None
                # },
#, 'ghost'
#, 'move right'
#, 'move left'
#, 'collideable'
#, 'gravity affected'

                'platforms': (
                ((0, 0), (50, 2100)),  #0
                ((50, 2050), (3750, 50)),  #1
                ((3750, 0), (50, 2050)),  #2
                ((50, 0), (3700, 50)),  #3
                ((50, 950), (3500, 50)),  #4
                ((3550, 950), (200, 50), 'ghost' ),  #5
                ((1650, 600), (50, 350)),  #11
                ((1950, 600), (50, 350)),  #13
                ((300, 1050), (300, 50), 'gravity affected' ),  #14
                ((3450, 1300), (300, 150)),  #15
                ((2800, 1400), (650, 50)),  #16
                ((2750, 1400), (50, 600)),  #17
                ((2800, 1950), (100, 50)),  #18
                ((2350, 1550), (400, 50)),  #19
                ((2350, 1900), (400, 50)),  #20
                ((650, 400), (300, 50), 'ghost' ),  #21
                ((700, 800), (400, 50)),  #22
                ((1100, 800), (350, 100)),  #23

                )
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
