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
            # 'LMB action': None,
            'value': '$description',
            'label': '$description',
            # 'target': '',
            # 'description': '*item',
            'active': True,
            # 'after action': 'keep going'
        },
    },

    'obs single selection': {
        'generate list from': '*self.obstacles[location].keys()',
        'predefined keys': {
            # 'LMB action': None,
            'value': '$description',
            'label': '$description',
            # 'target': '',
            # 'description': '*item',
            'active': True,
            # 'after action': 'keep going'
        },
    },

    'clipboard single selection': {
        'generate list from': '*self.clipboard',
        'predefined keys': {
            # 'LMB action': None,
            'value': '$description',
            'label': '$description',
            # 'target': '',
            # 'description': '*item',
            'active': True,
            # 'after action': 'keep going'
        },
    },

    'obs multiple selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE SEVERAL OBSTACLES:',
            'description': 'obs multiple selection',
            'on hover action': None,
            'target': None,
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
            'colors': {
                'frame color': BLUE,
                'bg color': YELLOW,
                'txt color': DARKGRAY
            },
            'label': '[CONFIRM]',
            'on hover action': None,
            'LMB action': 'store value',
            'value': list(),
            # 'target': '',
            'description': 'multiple obstacles list',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
    },

    'custom obs properties': {
        'header': {
            'rectangle': menu_elements_bindings['central header'],
            'label': 'EDIT OBSTACLE PROPERTIES:',
            'on hover action': None,
            'description': 'custom obs properties',
            'LMB action': None,
            'target': None,
            'active': False,
            'after action': None
        },
        'ghost': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'ghost',
            'on hover action': None,
            'LMB action': 'switch state',
            'description': 'ghost',
            'target': ("menu_structure['custom obs properties']['ok']['value']['ghost']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['ghost']",
            # 'LMB action': ['switch state', {'ghost': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'actors pass through': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'actors pass through',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['actors pass through']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['actors pass through']",
            # 'LMB action': ['switch state', {'actors pass through': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'speed': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'speed',
            'on hover action': None,
            'LMB action': 'input number',
            'target': "menu_structure['custom obs properties']['ok']['value']['speed']",
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['speed']",
            # 'LMB action': ('input number', {'speed': 0}),
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'collideable': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'collideable',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['collideable']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['collideable']",
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
            'target': ("menu_structure['custom obs properties']['ok']['value']['gravity affected']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['gravity affected']",
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
            'target': ("menu_structure['custom obs properties']['ok']['value']['invisible']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['invisible']",
            # 'value': {'invisible': False},
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'teleport': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['trigger']",
                      "menu_structure['custom obs properties']['ok']['value']['teleport']"),
            # 'LMB action': ['switch state', {'trigger': False}],
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['teleport']",
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'teleport to map': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport to map >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'map single selection',
            'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            # 'target': "menu_structure['custom obs properties']['ok']['value']['teleport description']",
            # 'value': menu_structure['custom obs properties']['ok']['value']['trigger description'],
            # 'LMB action': ['submenu', 'trigger description'],
            # 'LMB action': ['input string', {'trigger description': {}}],
            'active': True,
            'after action': 'return to parent',
        },
        'teleport to point (x,y) on map': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport to point (x,y) on map >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'clipboard single selection',
            'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            # 'target': "menu_structure['custom obs properties']['ok']['value']['teleport description']",
            # 'value': menu_structure['custom obs properties']['ok']['value']['trigger description'],
            # 'LMB action': ['submenu', 'trigger description'],
            # 'LMB action': ['input string', {'trigger description': {}}],
            'active': True,
            'after action': 'return to parent',
        },
        'trigger': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['trigger']",
                      "menu_structure['custom obs properties']['ok']['value']['teleport']"),
            # 'LMB action': ['switch state', {'trigger': False}],
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['trigger']",
            'active': True,
            'after action': 'keep going'
            # obs_settings[]
        },
        'triggered obstacles': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'triggered obstacles >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'obs multiple selection',
            'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            # 'submenu exit action': 'append value',
            # 'submenu exit action': 'return self value',
            # 'value': list(),
            'value': "self.menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'active': True,
            # 'also affects on': None,
            # 'after action': None,
            # 'after action': 'keep going',
            'after action': 'return to parent',
        },
        'trigger disappear': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger disappears after use?',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['trigger description']['disappear']",),
            # 'LMB action': ['switch state', {'trigger': False}],
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['trigger description']['disappear']",
            'active': True,
            'after action': 'keep going'
            # obs_settings[]
        },
        'active': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'active',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("menu_structure['custom obs properties']['ok']['value']['active']",),
            'additional info': "*menu_structure['custom obs properties']['ok']['value']['active']",
            # 'LMB action': ['switch state', {'active': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
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
            'colors': {
                'frame color': BLUE,
                'bg color': YELLOW,
                'txt color': DARKGRAY
            },
            'self dict name': 'custom obs properties',
            'label': '[CONFIRM]',
            'on hover action': None,
            'LMB action': 'store value',
            'description': 'return custom obs properties',
            'target': "self.menu_structure['custom obs properties']['ok']['value']",
            # Here will be stored full obstacle description.
            #  Like that: exec(menu_item['target'] + ' = menu_item[\'value\']')
            'value': {
                'ghost': False,
                'actors pass through': False,
                'speed': 0.,
                'collideable': False,
                'gravity affected': False,
                'invisible': False,
                'teleport': False,
                'teleport description': {
                    'new location': '',
                    'xy': [0, 0]
                },
                'trigger': True,
                'trigger description': {
                    'make active': list(),
                    'disappear': False
                },
                'active': False,
                'actions': {
                    #         # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))
                    #         # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
                    #         # ('turn on actions set', 0), ('switch gravity', 0),
                    #
                    0: (('move', (0, 0, 100, MAXY)), ('move', 'start area'), ('repeat', 0)),
                    #              1: (('move', (0, 0)),),
                },
            },
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
            'submenu exit action': '',
            'active': False,
            'target': None,
            'after action': None
        },
        'new': {
            'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
            'label': '[CREATE NEW MAP]',
            'on hover action': None,
            'LMB action': 'return value',
            'submenu exit action': '',
            'value': 'new',
            'target': None,
            'description': 'new',
            'active': True,
            'after action': None
        },
        'save': {
            'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
            'label': '[SAVE]',
            'on hover action': None,
            # 'LMB action': 'return value',
            'submenu exit action': '',
            'value':  "self.save()",
            # 'value': 'save',
            'LMB action': 'exec',
            'active': True,
            'after action': 'keep going'
        },
        'load': {
            'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
            'self dict name': 'load',  # It is necessary if such menu item reveals other menu.
            'label': '[LOAD]',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': "map single selection",
            'submenu exit action': 'store value',
            # 'submenu exit action': 'append value',
            # 'submenu exit action': 'return self value',
            'value': "self.menu_structure['main menu']['load']['target']",
            'target': '',  # Here will be stored a map name to be load.
            # 'target': "self.location",
            # 'LMB action': 'return value',
            # 'value': "load",
            'active': True,
            'after action': None  # If None, after submenu has done, this level menu returns self 'value'.
            # 'after action': 'return value'
        },
        'resize': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
            'label': '[RESIZE MAP]',
            'on hover action': None,
            # 'LMB action': 'return value',
            # 'value': "resize",
            # 'submenu exit action': '',
            'LMB action': 'exec',
            'value': "\
x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', 'digit')\n\
y = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', 'digit')\n\
self.camera.setup(int(x), int(y))\n\
self.create_snap_mesh()",
            'active': True,
            'after action': 'keep going'
        },
        'quit': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom left button']),
            'label': '[QUIT TO DOS...]',
            'on hover action': None,
            # 'LMB action': 'return value',
            'submenu exit action': '',
            'value': "pygame.quit()\nraise SystemExit",
            'LMB action': 'exec',
            'active': True,
            'after action': None
        },
    },
    # 'trigger description': {
    #     'header': {
    #         'rectangle': menu_elements_bindings['central header'],
    #         'label': 'TRIGGER DESCRIPTION:',
    #         'on hover action': None,
    #         'description': 'trigger description',
    #         'LMB action': None,
    #         'active': False,
    #         'after action': None
    #     },
    #     'make active': {
    #         'rectangle': menu_elements_bindings['central header'],
    #         'label': 'Triggers such obstacles be active >',
    #         'on hover action': 'submenu',
    #         'submenu name': 'obs multiple selection',
    #         # 'value': ("menu_structure['trigger description']['ok']['value']['make active']",),
    #         'LMB action': None,
    #         'active': True,
    #         'after action': None
    #     },
    #     'ok': {
    #         'rectangle': pygame.Rect(0, 0, 0, 0),
    #         'label': '[CONFIRM]',
    #         'on hover action': None,
    #         'LMB action': 'return value',
    #         'value': {
    #             'make active': list(),
    #             'change location': {
    #                 'new location': '',
    #                 'xy': [0, 0],
    #             },
    #             'disappear': False
    #         },
    #         'active': True,
    #         'after action': None
    #     },
    # },

    # 'initial setup': {
    #     'header': {
    #         'rectangle': pygame.Rect(menu_elements_bindings['central header']),
    #         'label': 'EDIT EXISTING OR CREATE NEW?',
    #         'on hover action': None,
    #         'description': 'initial setup',
    #         'LMB action': None,
    #         'active': False,
    #         'after action': None
    #     },
    #     'existing': {
    #         'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
    #         'label': '[LOAD]',
    #         'on hover action': None,
    #         'description': 'map single selection',
    #         'LMB action': 'submenu',  # Return string type of 'load'
    #         'value': 'map single selection',  # Return string type of 'load'
    #         # 'LMB action': 'return value',  # Return string type of 'load'
    #         # 'value': 'load',  # Return string type of 'load'
    #         'active': True,
    #         'after action': None
    #     },
    #     'new': {
    #         'rectangle': pygame.Rect(menu_elements_bindings['central left button']),
    #         'label': '[CREATE NEW MAP]',
    #         'on hover action': None,
    #         'LMB action': 'return value',
    #         'value': 'new',
    #         'description': 'new',
    #         'active': True,
    #         'after action': None
    #     },
    #     'quit': {
    #         'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
    #         'label': 'QUIT',
    #         'on hover action': None,
    #         'description': 'quit',
    #         'LMB action': 'exec',
    #         'value': 'pygame.quit()\nraise SystemExit()',
    #         'active': True,
    #         'after action': None
    #     },
    # },

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