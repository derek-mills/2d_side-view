import pygame
from constants import *

menu_buttons_height = 100
menu_buttons_width = 300
menu_small_buttons_height = 50
menu_small_buttons_width = 100
menu_buttons_spacing = 10
menu_headers_height = 100
menu_headers_width = MAXX_DIV_2
menu_screen_edge_margin = 50

menu_elements_bindings = {
    'top header': (MAXX_DIV_2 - menu_headers_width // 2, menu_screen_edge_margin,
                   menu_headers_width, menu_headers_height),
    'central header': (MAXX_DIV_2 - menu_headers_width // 2, MAXY_DIV_2 - menu_headers_height // 2,
                       menu_headers_width, menu_headers_height),
    'central right button': (MAXX_DIV_2 + menu_screen_edge_margin, MAXY_DIV_2 + menu_headers_height // 2 + menu_screen_edge_margin,
                             menu_buttons_width, menu_buttons_height),
    'central left button': (MAXX_DIV_2 - menu_screen_edge_margin - menu_buttons_width, MAXY_DIV_2 + menu_headers_height // 2 + menu_screen_edge_margin,
                            menu_buttons_width, menu_buttons_height),
    'bottom right button': (MAXX - (menu_buttons_width + menu_screen_edge_margin),
                            MAXY - (menu_buttons_height + menu_screen_edge_margin),
                            menu_buttons_width, menu_buttons_height),
    'bottom left button': (menu_screen_edge_margin, MAXY - (menu_buttons_height + menu_screen_edge_margin),
                           menu_buttons_width, menu_buttons_height),
}

menu_structure = {
     '_template_menu_item_': {
        'rectangle': None,
        'label': '',
        'value': None,
        'description': '',
        'target': '',
        'on hover action': None,
        'LMB action': None,
        'active': False,
        'after action': None
    },

    'map single selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE MAP TO LOAD:',
            'description': 'map single selection',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'generate list from': '*locations.locations.keys()',
        'predefined keys': {
            'LMB action': 'return value',
            'value': '$description',
            'label': '$description',
            # 'description': '*item',
            'active': True
        },
    },

    'obs single selection': {
        'generate list from': '*self.obstacles[location].keys()',
        'predefined keys': {
            'LMB action': 'return value',
            'value': '$description',
            'label': 'Obstacle #: $description',
            'active': True
        },
    },

    'obs multiple selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE SEVERAL OBSTACLES:',
            'description': 'obs multiple selection',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'generate list from': '*self.obstacles[self.location].keys()',
        'predefined keys': {
            'LMB action': 'append value',
            'value': '$description',
            'target': "self.menu_structure['obs multiple selection']['ok']['value']",
            'label': '$description',
            'active': True,
            'after action': 'keep going'
        },
        'ok': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[CONFIRM]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': list(),
            'description': 'multiple obstacles list',
            'active': True,
            'also affects on': None,
            'after action': None
        },
    },

    'teleport/trigger': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE TYPE:',
            'description': 'teleport/trigger',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'trigger': {
            'rectangle': None,
            'label': '[ACTION TRIGGER]',
            'on hover action': 'submenu',
            'submenu name': 'obs multiple selection',
            'value': 'obs multiple selection',
            'description': 'trigger',
            'LMB action': None,
            'active': True,
            'after action': None
        },
        'teleport': {
            'rectangle': None,
            'label': '[TELEPORT]',
            'on hover action': 'submenu',
            'value': 'map single selection',
            'description': 'teleport',
            'LMB action': None,
            'active': True,
            'after action': None
        },
    },
    
    'obstacle edit': {
        'header': {
            'rectangle': None,
            'label': 'INTRODUCE OBSTACLE AS:',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'trigger': {
            'rectangle': None,
            'label': '[MAKE EVENT INITIATOR] >',
            'on hover action': 'submenu',
            'submenu name': 'teleport/trigger',
            'value': 'teleport/trigger',
            # 'on hover action': ('submenu', 'teleport/trigger'),
            'LMB action': None,
            'active': True,
            'after action': None
        },
        'moving platform': {
            'rectangle': None,
            'label': '[MAKE MOVING PLATFORM]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': 'make moving platform',
            'active': True,
            'after action': None
        },
        'custom': {
            'rectangle': None,
            'label': '[CUSTOM PROPERTIES EDIT] >',
            'on hover action': 'submenu',
            'submenu name': 'custom obs properties',
            'value': 'custom obs properties',
            # 'on hover action': ('submenu', 'custom obs properties'),
            'LMB action': None,
            # 'LMB action': ('return value', 'custom'),
            'active': True,
            'after action': None
        },
    },

    'custom obs properties': {
        'header': {
            'rectangle': menu_elements_bindings['central header'],
            'label': 'EDIT OBSTACLE PROPERTIES:',
            'on hover action': None,
            'description': 'custom obs properties',
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'ghost': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'ghost',
            'on hover action': None,
            'LMB action': 'switch state',
            'description': 'ghost',
            'value': ("menu_structure['custom obs properties']['ok']['value']['ghost']",),
            # 'LMB action': ['switch state', {'ghost': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'speed': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'speed',
            'on hover action': None,
            'LMB action': 'input number',
            'value': "menu_structure['custom obs properties']['ok']['value']['speed']",
            # 'LMB action': ('input number', {'speed': 0}),
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'active': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'active',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['active']",),
            # 'LMB action': ['switch state', {'active': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'collideable': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'collideable',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['collideable']",),
            # 'LMB action': ['switch state', {'collideable': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'gravity affected': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'gravity affected',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['gravity affected']",),
            # 'LMB action': ['switch state', {'gravity affected': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'invisible': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'invisible',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['invisible']",),
            # 'value': {'invisible': False},
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'trigger': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['trigger']",),
            # 'LMB action': ['switch state', {'trigger': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'actors pass through': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'actors pass through',
            'on hover action': None,
            'LMB action': 'switch state',
            'value': ("menu_structure['custom obs properties']['ok']['value']['actors pass through']",),
            # 'LMB action': ['switch state', {'actors pass through': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'trigger description': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger description',
            'on hover action': 'submenu',
            'LMB action': None,
            'submenu name': 'trigger description',
            'value': 'trigger description',
            # 'value': menu_structure['custom obs properties']['ok']['value']['trigger description'],
            # 'LMB action': ['submenu', 'trigger description'],
            # 'LMB action': ['input string', {'trigger description': {}}],
            'active': True,
            'also affects on': None,
            'after action': None
            # obs_settings[]
        },
        'actions': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'actions',
            'on hover action': None,
            'LMB action': 'input string',
            'value': "menu_structure['custom obs properties']['ok']['value']['actions']",
            # 'LMB action': ['input string', {'actions': {}}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'ok': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[CONFIRM]',
            'on hover action': None,
            'LMB action': 'return value',
            'description': 'return custom obs properties',
            'value': {
                'ghost': False,
                'speed': 0.,
                'active': False,
                'collideable': False,
                'gravity affected': False,
                'invisible': False,
                'trigger': False,
                'actors pass through': False,
                'trigger description': {
                    'make active': list(),
                    'change location': {
                        'new location': '',
                        'xy': [0, 0]
                    },
                    'disappear': False
                },
                'actions': {
                    #         # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))
                    #         # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
                    #         # ('turn on actions set', 0), ('switch gravity', 0),
                    #
                    #              0: (('move', (1800,0, 150, 1500)), ('move', 'start area'), ('repeat', 0)),
                    #              1: (('move', (0, 0)),),
                },
            },

            'active': True,
            'after action': None
        },
    },
    
    'trigger description': {
        'header': {
            'rectangle': menu_elements_bindings['central header'],
            'label': 'TRIGGER DESCRIPTION:',
            'on hover action': None,
            'description': 'trigger description',
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'make active': {
            'rectangle': menu_elements_bindings['central header'],
            'label': '[Make some other obstacles active] >',
            'on hover action': 'submenu',
            'submenu name': 'obs multiple selection',
            # 'value': ("menu_structure['trigger description']['ok']['value']['make active']",),
            'LMB action': None,
            'active': True,
            'after action': None
        },
        'ok': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[CONFIRM]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': {
                'make active': list(),
                'change location': {
                    'new location': '',
                    'xy': [0, 0],
                },
                'disappear': False
            },
            'active': True,
            'after action': None
        },
    },

    'initial setup': {
        'header': {
            'rectangle': pygame.Rect(menu_elements_bindings['central header']),
            'label': 'EDIT EXISTING OR CREATE NEW?',
            'on hover action': None,
            'description': 'initial setup',
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'existing': {
            'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
            'label': '[LOAD]',
            'on hover action': None,
            'description': 'map single selection',
            'LMB action': 'submenu',  # Return string type of 'load'
            'value': 'map single selection',  # Return string type of 'load'
            # 'LMB action': 'return value',  # Return string type of 'load'
            # 'value': 'load',  # Return string type of 'load'
            'active': True,
            'after action': None
        },
        'new': {
            'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
            'label': '[CREATE NEW MAP]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': 'new',
            'description': 'new',
            'active': True,
            'after action': None
        },
        'quit': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
            'label': 'QUIT',
            'on hover action': None,
            'description': 'quit',
            'LMB action': 'exec',
            'value': 'pygame.quit()\nraise SystemExit()',
            'active': True,
            'after action': None
        },
    },

    'main menu': {
        'header': {
            'rectangle': pygame.Rect(menu_elements_bindings['central header']),
            'label': 'Hit ESC to quit',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'new': {
            'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
            'label': '[CREATE NEW MAP]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': 'new',
            'description': 'new',
            'active': True,
            'after action': None
        },
        'save': {
            'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
            'label': '[SAVE]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': 'save',
            # 'LMB action': ('exec', 'save()'),
            'active': True,
            'after action': None
        },
        'load': {
            'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
            'label': '[LOAD]',
            'on hover action': None,
            'LMB action': 'submenu',
            'value': "map single selection",
            # 'LMB action': 'return value',
            # 'value': "load",
            'active': True,
            'after action': None
        },
        'resize': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
            'label': '[RESIZE MAP]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': "resize",
            # 'LMB action': ('exec', "x = create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')\ny = create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')\ncamera.setup(int(x), int(y))\ncreate_snap_mesh()"),
            'active': True,
            'after action': None
        },
        'quit': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom left button']),
            'label': '[QUIT TO DOS...]',
            'on hover action': None,
            'LMB action': 'return value',
            'value': "quit",
            # 'LMB action': ('exec', "reset_menu()"),
            'active': True,
            'after action': None
        },
    },
}

# menu_structure = {
#     '_template_menu_item_': {
#         'rectangle': None,
#         'label': '',
#         'value': None,
#         'on hover action': None,
#         'LMB action': None,
#         'active': False,
#         'after action': None
#     },
#     'map single selection': {
#           'generate list from': 'locations.locations.keys()',
#           'predefined keys': {
#               'LMB action': 'return value',
#               'value': '@str(item)',
#               'label': '@str(item)',
#               'active': True
#           }
#     },
#     'obs single selection': {
#         'generate list from': 'obstacles[location].keys()',
#         'predefined keys': {
#             'LMB action': 'return value',
#             'value': '@str(item)',
#             'label': 'Obstacle #: @str(item)',
#             'active': True
#         },
#     },
#     'obs multiple selection': {
#         # 'target object': list(),
#         'generate list from': 'obstacles[location].keys()',
#         'predefined keys': {
#                 'LMB action': 'return value',
#                 'value': '@str(item)',
#                 # 'LMB action': ('return value', '@item'),
#                 'label': 'Obstacle #: @str(item)',
#                 'active': True,
#                 'after action': 'keep going'
#         },
#         'ok': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': '[CONFIRM]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': 'obs selection done',
#             'active': True,
#             'also affects on': None,
#             'after action': None
#         },
#     },
#     'teleport/trigger': {
#         'header': {
#             'rectangle': None,
#             'label': 'CHOOSE TYPE:',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'trigger': {
#             'rectangle': None,
#             'label': '[ACTION TRIGGER]',
#             'on hover action': 'submenu',
#             'value': 'obs multiple selection',
#             # 'on hover action': ('submenu', 'obs multiple selection'),
#             'LMB action': None,
#             'active': True,
#             'after action': None
#         },
#         'teleport': {
#             'rectangle': None,
#             'label': '[TELEPORT]',
#             'on hover action': 'submenu',
#             'value': 'map single selection',
#             # 'on hover action': ('submenu', 'map single selection'),
#             'LMB action': None,
#             'active': True,
#             'after action': None
#         },
#     },
#     'obstacle edit': {
#         'header': {
#             'rectangle': None,
#             'label': 'INTRODUCE OBSTACLE AS:',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'trigger': {
#             'rectangle': None,
#             'label': '[MAKE EVENT INITIATOR] >',
#             'on hover action': 'submenu',
#             'value': 'teleport/trigger',
#             # 'on hover action': ('submenu', 'teleport/trigger'),
#             'LMB action': None,
#             'active': True,
#             'after action': None
#         },
#         'moving platform': {
#             'rectangle': None,
#             'label': '[MAKE MOVING PLATFORM]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': 'make moving platform',
#             'active': True,
#             'after action': None
#         },
#         'custom': {
#             'rectangle': None,
#             'label': '[CUSTOM PROPERTIES EDIT] >',
#             'on hover action': 'submenu',
#             'value': 'custom obs properties',
#             # 'on hover action': ('submenu', 'custom obs properties'),
#             'LMB action': None,
#             # 'LMB action': ('return value', 'custom'),
#             'active': True,
#             'after action': None
#         },
#     },
#     'custom obs properties': {
#         'header': {
#             'rectangle': menu_elements_bindings['central header'],
#             'label': 'EDIT OBSTACLE PROPERTIES:',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'ghost': {
#             'rectangle': pygame.Rect(0,0,0,0),
#             'label': 'ghost',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'ghost': False},
#             # 'LMB action': ['switch state', {'ghost': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'speed': {
#             'rectangle': pygame.Rect(0,0,0,0),
#             'label': 'speed',
#             'on hover action': None,
#             'LMB action': 'input number',
#             'value': {'speed': 0},
#             # 'LMB action': ('input number', {'speed': 0}),
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'active': {
#             'rectangle': pygame.Rect(0,0,0,0),
#             'label': 'active',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'active': False},
#             # 'LMB action': ['switch state', {'active': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'collideable': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'collideable',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'collideable': False},
#             # 'LMB action': ['switch state', {'collideable': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'gravity affected': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'gravity affected',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'gravity affected': False},
#             # 'LMB action': ['switch state', {'gravity affected': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'invisible': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'invisible',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': menu_structure['custom obs properties']['ok']['value']['invisible'],
#             # 'value': {'invisible': False},
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#         },
#         'trigger': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'trigger',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'trigger': False},
#             # 'LMB action': ['switch state', {'trigger': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#             # obs_settings[]
#         },
#         'actors pass through': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'actors pass through',
#             'on hover action': None,
#             'LMB action': 'switch state',
#             'value': {'actors pass through': False},
#             # 'LMB action': ['switch state', {'actors pass through': False}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#             # obs_settings[]
#         },
#         'trigger description': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'trigger description',
#             'on hover action': None,
#             'LMB action': 'submenu',
#             'value': 'trigger description',
#             # 'LMB action': ['submenu', 'trigger description'],
#             # 'LMB action': ['input string', {'trigger description': {}}],
#             'active': True,
#             'also affects on': None,
#             'after action': None
#             # obs_settings[]
#         },
#         'actions': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': 'actions',
#             'on hover action': None,
#             'LMB action': 'input string',
#             'value': {'actions': {}},
#             # 'LMB action': ['input string', {'actions': {}}],
#             'active': True,
#             'also affects on': None,
#             'after action': 'keep going'
#             # obs_settings[]
#         },
#         'ok': {
#             'rectangle': pygame.Rect(0, 0, 0, 0),
#             'label': '[CONFIRM]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': {
#                 'ghost': False,
#                 'speed': 0.,
#                 'active': False,
#                 'collideable': False,
#                 'gravity affected': False,
#                 'invisible': False,
#                 'trigger': False,
#                 'actors pass through': False,
#                 'trigger description': {},
#                 'actions': {}
#             },
#             # 'value': 'custom obs edit done',
#             'active': True,
#             'after action': None
#         },
#
#         # 'generate list from': (
#         #     'ghost', 'speed', 'active',
#         # ),
#     },
#     'trigger description': {
#         'header': {
#             'rectangle': menu_elements_bindings['central header'],
#             'label': 'EDIT OBSTACLE TRIGGERS:',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'make active': {
#             'rectangle': menu_elements_bindings['central header'],
#             'label': '[Make some other obstacles active] >',
#             'on hover action': 'submenu',
#             'value': 'obs multiple selection',
#             # 'on hover action': ('submenu', 'list obs'),
#             'LMB action': None,
#             'active': True,
#             'after action': None
#         },
#     },
#     'initial setup': {
#         'header': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central header']),
#             'label': 'EDIT EXISTING OR CREATE NEW?',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'existing': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
#             'label': '[LOAD]',
#             'on hover action': None,
#             'LMB action': 'return value',  # Return string type of 'load'
#             'value': 'load',  # Return string type of 'load'
#             'active': True,
#             'after action': None
#         },
#         'new': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
#             'label': '[CREATE NEW MAP]',
#             'on hover action': None,
#             'LMB action': 'return value',  # Return string type of 'new'
#             'value': 'new',  # Return string type of 'new'
#             'active': True,
#             'after action': None
#         },
#         'quit': {
#             'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
#             'label': 'QUIT',
#             'on hover action': None,
#             'LMB action': 'exec',
#             'value': 'pygame.quit()\nraise SystemExit()',
#             'active': True,
#             'after action': None
#         },
#     },
#     'main menu': {
#         'header': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central header']),
#             'label': 'Now edit map: ' + location + ' (ESC to quit)',
#             'on hover action': None,
#             'LMB action': None,
#             'active': False,
#             'after action': None
#         },
#         'save': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
#             'label': '[SAVE CURRENT MAP]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': 'save',
#             # 'LMB action': ('exec', 'save()'),
#             'active': True,
#             'after action': None
#         },
#         'load': {
#             'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
#             'label': '[LOAD...]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': "load",
#             # 'LMB action': ('exec', "reset_menu()\nneed_to_load = True\nreturn"),
#             'active': True,
#             'after action': None
#         },
#         'resize': {
#             'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
#             'label': '[RESIZE MAP...]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': "resize",
#             # 'LMB action': ('exec', "x = create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')\ny = create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')\ncamera.setup(int(x), int(y))\ncreate_snap_mesh()"),
#             'active': True,
#             'after action': None
#         },
#         'quit': {
#             'rectangle': pygame.Rect(menu_elements_bindings['bottom left button']),
#             'label': '[QUIT TO DOS...]',
#             'on hover action': None,
#             'LMB action': 'return value',
#             'value': "quit",
#             # 'LMB action': ('exec', "reset_menu()"),
#             'active': True,
#             'after action': None
#         },
#     },
# }