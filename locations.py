# from game_objects import *
# from actors_description import *
from constants import *
# import pygame

locations = {
    '01':
        {
            'music': music_ambient_1,
            'description': 'apartment #1',
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


                'platforms': (
                ((0, 0), (50, 950)),  #0
                ((2150, 600), (150, 50), 'ghost' , 'move left' ),  #2
                ((1550, 50), (50, 50), 'collideable' , 'gravity affected' ),  #3
                ((1500, 250), (200, 100), 'move left' ),  #4
                ((2050, 0), (50, 500)),  #5
                ((2200, 0), (50, 500)),  #6
                ((2350, 0), (50, 500)),  #7
                ((2500, 0), (50, 500)),  #8
                ((2650, 0), (50, 500)),  #9
                ((2800, 0), (50, 500)),  #10
                ((2950, 0), (50, 500)),  #11
                ((3100, 0), (50, 500)),  #12
                ((3200, 450), (150, 50)),  #13
                ((3450, 450), (150, 50)),  #14
                ((3700, 450), (150, 50)),  #15
                ((3950, 450), (150, 50)),  #16
                ((4200, 450), (150, 50)),  #17
                ((4450, 450), (150, 50)),  #18
                ((4700, 450), (150, 50)),  #19
                ((4950, 450), (150, 50)),  #20
                ((5200, 450), (150, 50)),  #21
                ((0, 950), (950, 100)),  #22
                ((1800, 750), (3950, 50)),  #23
                ((2875, 1875), (2875, 25)),  #24
                ((3425, 1675), (100, 200)),  #25
                ((3525, 1700), (75, 175)),  #26
                ((3600, 1725), (75, 150)),  #27
                ((3675, 1750), (75, 125)),  #28
                ((3750, 1775), (75, 100)),  #29
                ((3825, 1800), (75, 75)),  #30
                ((3900, 1825), (50, 50)),  #31
                ((3950, 1850), (50, 25)),  #32
                ((2850, 1450), (100, 300)),  #33
                ((1750, 1025), (50, 200)),  #34
                ((1800, 1050), (50, 200)),  #35
                ((1850, 1075), (50, 200)),  #36
                ((1900, 1100), (50, 200)),  #37
                ((1950, 1125), (50, 200)),  #38
                ((2000, 1150), (50, 200)),  #39
                ((2050, 1175), (50, 200)),  #40
                ((2100, 1200), (50, 200)),  #41
                ((2150, 1225), (50, 200)),  #42
                ((2200, 1250), (50, 200)),  #43
                ((2250, 1275), (50, 200)),  #44
                ((2300, 1300), (50, 200)),  #45
                ((2350, 1325), (50, 200)),  #46
                ((2400, 1350), (50, 200)),  #47
                ((2450, 1375), (50, 200)),  #48
                ((2500, 1400), (50, 200)),  #49
                ((2550, 1425), (50, 200)),  #50
                ((2600, 1450), (250, 175)),  #51
                ((2950, 1450), (2600, 50)),  #52
                ((5700, 800), (50, 1075)),  #53
                ((325, 925), (100, 25)),  #54
                ((425, 900), (125, 50)),  #55
                ((550, 875), (100, 75)),  #56
                ((650, 850), (75, 100)),  #57
                ((725, 825), (75, 125)),  #58
                ((800, 800), (50, 150)),  #59
                ((850, 775), (50, 175)),  #60
                ((900, 750), (50, 200)),  #61
                ((950, 725), (50, 275)),  #62
                ((1000, 700), (50, 300)),  #63
                ((950, 1000), (800, 50)),  #64
                ((450, 450), (500, 50)),  #65
                ((1050, 725), (50, 275)),  #66
                ((1100, 750), (50, 250)),  #67
                ((1150, 775), (50, 225)),  #68
                ((1200, 800), (50, 200)),  #69
                ((1250, 825), (75, 175)),  #70
                ((1325, 850), (75, 150)),  #71
                ((1400, 875), (75, 125)),  #72
                ((1475, 900), (75, 100)),  #74
                ((1550, 925), (50, 75)),  #75
                ((1600, 950), (50, 50)),  #76
                ((1650, 975), (25, 25)),  #77

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
