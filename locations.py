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
                ((2150, 600), (150, 50), 'ghost' , 'move left' ),  #1
                ((1550, 50), (50, 50), 'collideable' , 'gravity affected' ),  #2
                ((1500, 250), (200, 100), 'move left' ),  #3
                ((2050, 0), (50, 500)),  #4
                ((2200, 0), (50, 500)),  #5
                ((2350, 0), (50, 500)),  #6
                ((2500, 0), (50, 500)),  #7
                ((2650, 0), (50, 500)),  #8
                ((2800, 0), (50, 500)),  #9
                ((2950, 0), (50, 500)),  #10
                ((3100, 0), (50, 500)),  #11
                ((3200, 450), (150, 50)),  #12
                ((3450, 450), (150, 50)),  #13
                ((3700, 450), (150, 50)),  #14
                ((3950, 450), (150, 50)),  #15
                ((4200, 450), (150, 50)),  #16
                ((4450, 450), (150, 50)),  #17
                ((4700, 450), (150, 50)),  #18
                ((4950, 450), (150, 50)),  #19
                ((5200, 450), (150, 50)),  #20
                ((0, 950), (950, 100)),  #21
                ((1800, 750), (3950, 50)),  #22
                ((2875, 1875), (2875, 25)),  #23
                ((3425, 1675), (100, 200)),  #24
                ((3525, 1700), (75, 175)),  #25
                ((3600, 1725), (75, 150)),  #26
                ((3675, 1750), (75, 125)),  #27
                ((3750, 1775), (75, 100)),  #28
                ((3825, 1800), (75, 75)),  #29
                ((3900, 1825), (50, 50)),  #30
                ((3950, 1850), (50, 25)),  #31
                ((2850, 1450), (100, 300)),  #32
                ((1750, 1025), (50, 200)),  #33
                ((1800, 1050), (50, 200)),  #34
                ((1850, 1075), (50, 200)),  #35
                ((1900, 1100), (50, 200)),  #36
                ((1950, 1125), (50, 200)),  #37
                ((2000, 1150), (50, 200)),  #38
                ((2050, 1175), (50, 200)),  #39
                ((2100, 1200), (50, 200)),  #40
                ((2150, 1225), (50, 200)),  #41
                ((2200, 1250), (50, 200)),  #42
                ((2250, 1275), (50, 200)),  #43
                ((2300, 1300), (50, 200)),  #44
                ((2350, 1325), (50, 200)),  #45
                ((2400, 1350), (50, 200)),  #46
                ((2450, 1375), (50, 200)),  #47
                ((2500, 1400), (50, 200)),  #48
                ((2550, 1425), (50, 200)),  #49
                ((2600, 1450), (250, 175)),  #50
                ((2950, 1450), (2600, 50)),  #51
                ((5700, 800), (50, 1075)),  #52
                ((325, 925), (100, 25)),  #53
                ((425, 900), (125, 50)),  #54
                ((550, 875), (100, 75)),  #55
                ((650, 850), (75, 100)),  #56
                ((725, 825), (75, 125)),  #57
                ((800, 800), (50, 150)),  #58
                ((850, 775), (50, 175)),  #59
                ((900, 750), (50, 200)),  #60
                ((950, 725), (50, 275)),  #61
                ((1000, 700), (50, 300)),  #62
                ((950, 1000), (800, 50)),  #63
                ((450, 450), (500, 50), 'move right' ),  #64
                ((1050, 725), (50, 275)),  #65
                ((1100, 750), (50, 250)),  #66
                ((1150, 775), (50, 225)),  #67
                ((1200, 800), (50, 200)),  #68
                ((1250, 825), (75, 175)),  #69
                ((1325, 850), (75, 150)),  #70
                ((1400, 875), (75, 125)),  #71
                ((1475, 900), (75, 100)),  #72
                ((1550, 925), (50, 75)),  #73
                ((1600, 950), (50, 50)),  #74
                ((1650, 975), (25, 25)),  #75
                ((250, 650), (250, 50), 'move right'),  #76

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
