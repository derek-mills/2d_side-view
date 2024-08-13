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
    # Memo for menu generator.
    # If 'generate list from' is 'str' type and has '@' or '*' as a first symbol:
    # *  : a pointer to already existing iteration sequence (like '*a_dictionary.keys()')
    # @  : an execution flag (for example, '@[i for i in an_iteration_sequence]')
    # If menu generation source is a simple string and has no such symbols,
    # generate menu items from this whole string, using vertical stick '|' as a delimiter
    # (for example, 'generate list from': 'menu item 1|menu item 2|menu item 3|').
    # If 'generate list from' is not 'str' type, use it as a native iteration sequence,
    # which will be converted to a list.
    #
    # Memo for the inner menu items.
    # * : pointer to particular global variable.
    # $ : pointer to the inner dict key of this particular menu item ('value', 'label', 'description' etc.).
    # @ : this is the sign of executability of all code which remains after this sign.

    '_template_menu_item_': (
        'description', 'rectangle', 'label', 'value', 'target',
        'on hover action', 'additional info', 'LMB action',
        'active', 'after action'
    ),
    # '_template_menu_item_': {
    #     'description': None,
    #     'rectangle': None,
    #     'label': None,
    #     'value': None,
    #     'target': None,
    #     'on hover action': None,
    #     'additional info': " ",
    #     'LMB action': None,
    #     'active': False,
    #     'after action': None
    # },

    '_template_obs_settings_': ('sprite', 'sprite elevated',
                                'force render', 'invisible',
                                'ghost', 'speed',
                                'item', 'item name',
                                'actors may grab', 'actors pass through',
                                'active', 'actions',
                                'collideable', 'gravity affected',
                                'trigger', 'trigger description',
                                'teleport', 'teleport description'),

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
            'LMB action': 'store value',
            'value': '*item',
            # 'value': '$description',
            'label': '*item',
            # 'label': '$description',
            # 'target': '',
            'description': '*item',
            'active': True,
            'after action': None
        },
    },

    'item single selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE ITEM:',
            'description': 'item single selection',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'generate list from': '*all_items.keys()',
        'predefined keys': {
            'LMB action': 'store value',
            # 'value': '$description',
            # 'label': '$description',
            'value': '*item',
            'label': '*item',
            # 'target': '$description',
            # 'target': '',
            'description': '*item',
            'active': True,
            'after action': 'return to parent'
            # 'after action': 'return value'
        },
    },

    'obs single selection': {
        'generate list from': '*self.obstacles[location].keys()',
        'predefined keys': {
            # 'LMB action': None,
            'value': '$description',
            'label': '$description',
            # 'target': '',
            'description': '*item',
            'active': True,
            # 'after action': 'keep going'
        },
    },

    'clipboard single selection': {
        'generate list from': '*self.clipboard[self.menu_structure["custom obs properties"]["ok"]["value"]["teleport description"]["new location"]]',
        # 'generate list from': '*self.clipboard',
        'predefined keys': {
            'LMB action': 'store value',
            'value': '*item',
            'label': '*item',
            # 'target': '',
            'description': '*item',
            # 'additional info': '*key',
            # 'additional info': '*',
            # 'additional info': '@var',
            'additional info': '@self.menu_structure[menu_name][item][key] = self.menu_structure["custom obs properties"]["ok"]["value"]["teleport description"]["new location"]',
            'active': True,
            # 'after action': None
            'after action': 'return to parent'
        },
    },

    'clipboard multiple selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE SEVERAL ELEMENTS TO DELETE:',
            'description': 'clipboard multiple selection',
            'on hover action': None,
            'target': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'generate list from': '*self.clipboard[self.location]',
        # 'generate list from': '*self.clipboard',
        'predefined keys': {
            'LMB action': 'append value',
            'value': '*item',
            'description': '*item',
            'target': "self.menu_structure['clipboard multiple selection']['ok']['value']",
            'additional info': '@self.menu_structure[menu_name][item][key] = self.menu_structure["custom obs properties"]["ok"]["value"]["teleport description"]["new location"]',
            # 'additional info': '@self.menu_structure[menu_name][item][key] = self.clipboard[(int(self.menu_structure[menu_name][item]["label"][0]),int(self.menu_structure[menu_name][item]["label"][1]))]["location"]',
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
            # 'value default': list(),
            # 'target': '',
            'description': 'multiple clipboard list',
            'active': True,
            # 'after action': 'return to parent',
            'after action': None
            # 'after action': 'keep going',
            # 'after action': None,
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
            'value': '*(item, "self", 0)',
            'description': '*item',
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
            # 'value default': list(),
            # 'target': '',
            'description': 'multiple obstacles list',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
    },

    'action single selection': {
        'header': {
            'rectangle': None,
            'label': 'ADD AN ACTION TO BE PERFORMED NEXT:',
            'description': 'action single selection',
            'on hover action': None,
            'target': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'move': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            # 'colors': {
            #     'frame color': BLUE,
            #     'bg color': YELLOW,
            #     'txt color': DARKGRAY
            # },
            'LMB action': 'append value',
            'label': '[MOVE]',
            'on hover action': None,
            'value': ('move', (0, 0)),
            'description': 'add MOVE action',
            'active': True,
            'after action': 'return to parent',
        },
        'stop': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            # 'colors': {
            #     'frame color': BLUE,
            #     'bg color': YELLOW,
            #     'txt color': DARKGRAY
            # },
            'label': '[STOP]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('stop', (0, 0)),
            # 'value': "('stop', (0, 0))",
            # 'target': '',
            'description': 'add STOP action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'repeat': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            # 'colors': {
            #     'frame color': BLUE,
            #     'bg color': YELLOW,
            #     'txt color': DARKGRAY
            # },
            'label': '[REPEAT]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('repeat', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add REPEAT action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'die': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[die]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('die', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add DIE action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'wait': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[wait]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('wait', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add WAIT action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'turn on actions set': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[turn on actions set]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('turn on actions set', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add \'turn on actions set\' action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'switch visibility': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[switch visibility]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('switch visibility', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add \'switch visibility\' action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'switch passability': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[switch passability]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('switch passability', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add \'switch passability\' action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
        'switch gravity': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': '[SWITCH GRAVITY AFFECTION]',
            'on hover action': None,
            'LMB action': 'append value',
            'value': ('switch gravity', 0),
            # 'value': "('repeat', 0)",
            # 'target': '',
            'description': 'add \'switch gravity\' action',
            'active': True,
            'after action': 'return to parent',
            # 'after action': 'keep going',
            # 'after action': None,
        },
    },

    'sprite single selection': {
        'header': {
            'rectangle': None,
            'label': 'CHOOSE SPRITE TO APPLY:',
            'description': 'sprite single selection',
            'on hover action': None,
            'LMB action': None,
            'active': False,
            'after action': None
        },
        'generate list from': '*self.tiles.keys()',
        'predefined keys': {
            # 'LMB action': None,
            'LMB action': 'store value',
            'value': '*item',
            # 'value': '$description',
            'label': '*item',
            # 'label': '$description',
            # 'target': '',
            'description': '*item',
            'additional info': "*'^self.tiles[self.menu_structure[\"' + menu_name + '\"][' + str(item)+ '][\"value\"]]'",
            'active': True,
            'after action': 'return to parent'
            # 'after action': 'keep going'
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
        'select sprite': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'select sprite >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'sprite single selection',
            'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['sprite']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['sprite']",
            'additional info': "^self.tiles[self.menu_structure['custom obs properties']['ok']['value']['sprite']]",
            # 'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['sprite']",
            'active': True,
            'after action': 'return to parent',
        },
        'sprite elevated': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'sprite elevated',
            'on hover action': None,
            'LMB action': 'switch state',
            'description': 'sprite elevated',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['sprite elevated']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['sprite elevated']",
            'active': True,
            'after action': 'keep going'
        },
        'force render': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'force render',
            'on hover action': None,
            'LMB action': 'switch state',
            'description': 'force render',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['force render']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['force render']",
            'active': True,
            'after action': 'keep going'
        },
        'ghost': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'ghost',
            'on hover action': None,
            'LMB action': 'switch state',
            'description': 'ghost',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['ghost']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['ghost']",
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
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['actors pass through']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['actors pass through']",
            # 'LMB action': ['switch state', {'actors pass through': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
            # obs_settings[]
        },
        'actors may grab': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'actors may grab',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['actors may grab']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['actors may grab']",
            'active': True,
            'after action': 'keep going'
        },
        'speed': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'obs move speed',
            'on hover action': None,
            'LMB action': 'input float',
            # 'value': "self.menu_structure['custom obs properties']['ok']['value']['speed']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['speed']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['speed']",
            'active': True,
            'after action': 'keep going'
        },
        'collideable': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'collideable',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['collideable']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['collideable']",
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
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['gravity affected']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['gravity affected']",
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
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['invisible']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['invisible']",
            # 'value': {'invisible': False},
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'teleport': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['teleport']",),
            # 'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger']",
            #           "self.menu_structure['custom obs properties']['ok']['value']['teleport']"),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport']",
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'teleport on touch': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport on touch',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['teleport description']['on touch']",),
            # 'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger']",
            #           "self.menu_structure['custom obs properties']['ok']['value']['teleport']"),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport description']['on touch']",
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'teleport to map': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport to map >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            # 'submenu': {
            #     'name': 'map single selection',
            #     'exit button': 'all',
            #     # 'exit action': 'store value',
            # },
            'submenu name': 'map single selection',
            # 'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport description']['new location']",
            'active': True,
            'after action': 'return to parent',
        },
        'teleport to point (x,y) on map': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'teleport to point (x,y) on map >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'clipboard single selection',
            # 'submenu exit action': 'store value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy']",
            # 'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']",
            # 'value': menu_structure['custom obs properties']['ok']['value']['trigger description'],
            # 'LMB action': ['submenu', 'trigger description'],
            # 'LMB action': ['input string', {'trigger description': {}}],
            'active': True,
            'after action': 'return to parent',
        },
        'teleport keep x': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'on hover action': None,
            'LMB action': 'exec',
            # 'LMB action': 'store value',
            # 'value': '"keep y"',
            'description': 'keep X coordinate unchanged',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'] = ('keep x', self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'][1])",
            # 'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'][1]",
            # 'additional info': '@self.menu_structure[menu_name][item][key] = self.menu_structure["custom obs properties"]["ok"]["value"]["teleport description"]["new location"]',
            # 'additional info': '@self.menu_structure[menu_name][item][key] = self.clipboard[(int(self.menu_structure[menu_name][item]["label"][0]),int(self.menu_structure[menu_name][item]["label"][1]))]["location"]',
            'label': 'keep X coordinate unchanged',
            'active': True,
            'after action': 'keep going'
        },
        'teleport keep y': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': YELLOW
            },
            'on hover action': None,
            'LMB action': 'exec',
            # 'LMB action': 'store value',
            # 'value': '"keep y"',
            'description': 'keep Y coordinate unchanged',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'] = (self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'][0], 'keep y')",
            # 'target': "self.menu_structure['custom obs properties']['ok']['value']['teleport description']['xy'][1]",
            # 'additional info': '@self.menu_structure[menu_name][item][key] = self.menu_structure["custom obs properties"]["ok"]["value"]["teleport description"]["new location"]',
            # 'additional info': '@self.menu_structure[menu_name][item][key] = self.clipboard[(int(self.menu_structure[menu_name][item]["label"][0]),int(self.menu_structure[menu_name][item]["label"][1]))]["location"]',
            'label': 'keep Y coordinate unchanged',
            'active': True,
            'after action': 'keep going'
        },
        'trigger': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': GRAY
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger']",),
            # 'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger']",
            #           "self.menu_structure['custom obs properties']['ok']['value']['teleport']"),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['trigger']",
            'active': True,
            'after action': 'keep going'
        },
        'triggered obstacles': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': GRAY
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'triggered obstacles >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            # 'submenu': {
            #     'name': 'obs multiple selection',
            #     'exit button': 'ok',  # If it needed to exit a submenu by pressing any button: 'all'
            #     'exit action': 'store value'
            # },
            'submenu name': 'obs multiple selection',
            # 'submenu exit button': 'ok',
            # 'submenu exit button': 'all',  # Menu triggers value return on any button pressed.
            # 'submenu exit action': 'store value',
            # 'submenu after action': 'return to parent',
            # 'submenu exit action': 'append value',
            # 'submenu exit action': 'return self value',
            # 'value': list(),
            'value': "self.menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['trigger description']['make active']",
            'active': True,
            # 'also affects on': None,
            # 'after action': None,
            'after action': 'keep going',
            # 'after action': 'return to parent',
        },
        'trigger disappear': {
            'colors': {
                'frame color': GRAY,
                'bg color': DARKGRAY,
                'txt color': GRAY
            },
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'trigger disappears after use?',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger description']['disappear']",),
            # 'LMB action': ['switch state', {'trigger': False}],
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['trigger description']['disappear']",
            'active': True,
            'after action': 'keep going'
            # obs_settings[]
        },
        'item': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'item',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['item']",
                       "self.menu_structure['custom obs properties']['ok']['value']['actors pass through']",
                       "self.menu_structure['custom obs properties']['ok']['value']['force render']",
                       "self.menu_structure['custom obs properties']['ok']['value']['collideable']",
                       "self.menu_structure['custom obs properties']['ok']['value']['gravity affected']",
                       "self.menu_structure['custom obs properties']['ok']['value']['trigger']",
                       ),
            # 'target': ("self.menu_structure['custom obs properties']['ok']['value']['trigger']",
            #           "self.menu_structure['custom obs properties']['ok']['value']['teleport']"),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['item']",
            'active': True,
            'after action': 'keep going'
        },
        'item name': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'select item type >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'item single selection',
            'submenu exit action': 'store value',
            # 'submenu after action': 'return to parent',
            # 'submenu exit action': 'append value',
            # 'submenu exit action': 'return self value',
            # 'value': list(),
            'value': "self.menu_structure['custom obs properties']['ok']['value']['item name']['name']",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['item name']['name']",
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['item name']['name']",
            'active': True,
            # 'also affects on': None,
            # 'after action': None,
            # 'after action': 'keep going',
            'after action': 'return to parent',
        },
        'active': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'active',
            'on hover action': None,
            'LMB action': 'switch state',
            'target': ("self.menu_structure['custom obs properties']['ok']['value']['active']",),
            'additional info': "*self.menu_structure['custom obs properties']['ok']['value']['active']",
            # 'LMB action': ['switch state', {'active': False}],
            'active': True,
            'also affects on': None,
            'after action': 'keep going'
        },
        'action type': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'label': 'add an action >',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            'submenu name': 'action single selection',
            'submenu exit action': 'append value',
            'submenu after action': 'return to parent',
            'value': "self.menu_structure['custom obs properties']['ok']['value']['actions'][0]",
            'target': "self.menu_structure['custom obs properties']['ok']['value']['actions'][0]",
            'additional info': "self.menu_structure['custom obs properties']['ok']['value']['actions'][0]",
            # 'LMB action': ['input string', {'actions': {}}],
            'active': True,
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
            'LMB action': 'return value',
            # 'LMB action': 'store value',
            'description': 'return custom obs properties',
            # 'target': "",
            'target': "self.menu_structure['custom obs properties']['ok']['value']",
            'value': {
                'sprite': 0,
                'sprite elevated': False,
                'force render': False,
                'ghost': False,
                'actors pass through': False,
                'actors may grab': False,
                'speed': 0.2,
                'collideable': False,
                'gravity affected': False,
                'invisible': False,
                'teleport': False,
                'teleport description': {
                    'new location': '',
                    'on touch': True,
                    'xy': [0, 0]
                },
                'trigger': False,
                'trigger description': {
                    #                 [(ID, room, action set), ]
                    # 'make active':  [(58, 'self', 0), (159, 'room_2', 1),]
                    'make active': list(),
                    'disappear': False
                },
                'item': False,
                'item name': {'name': '',},
                'active': False,
                'actions': {
                    #         # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))
                    #         # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
                    #         # ('turn on actions set', 0), ('switch gravity', 0),
                    #
                    # 0: list(),
                    # 0: (('move', (0, 0, 100, MAXY)), ('move', 'start area'), ('repeat', 0)),
                    0: list(),
                },
            },
            'active': True,
            'after action': None
        },
        'reset': {
            'rectangle': pygame.Rect(0, 0, 0, 0),
            'colors': {
                'frame color': BLUE,
                'bg color': YELLOW,
                'txt color': DARKGRAY
            },
            # 'self dict name': 'custom obs properties',
            'label': '[RESET TO DEFAULT]',
            'on hover action': None,
            'LMB action': 'store value',
            'description': 'return obs properties to default state',
            'target': "self.menu_structure['custom obs properties']['ok']['value']",
            # Here will be stored full obstacle description.
            #  Like that: exec(menu_item['target'] + ' = menu_item[\'value\']')
            'value': {
                'sprite elevated': False,
                'sprite': 0,
                'force render': False,
                'ghost': False,
                'actors pass through': False,
                'actors may grab': False,
                'speed': 0.2,
                'collideable': False,
                'gravity affected': False,
                'invisible': False,
                'teleport': False,
                'teleport description': {
                    'new location': '',
                    'on touch': True,
                    'xy': [0, 0]
                },
                'trigger': False,
                'trigger description': {
                    #                 [(ID, room, action set), ]
                    # 'make active':  [(58, 'self', 0), (159, 'room_2', 1),]
                    'make active': [(0, 'self', 0), ],
                    'disappear': False
                },
                'item': False,
                'item name': {'name': '',},
                'active': False,
                'actions': {
                    #         # (('move', (1100,450)), ('move', 'start'), ('wait', 2), ('repeat', 0))
                    #         # ('die', 0), ('switch visibility', 0), ('switch passability', 0),
                    #         # ('turn on actions set', 0), ('switch gravity', 0),
                    #
                    # 0: list(),
                    # 0: (('move', (0, 0, 100, MAXY)), ('move', 'start area'), ('repeat', 0)),
                    0: list(),
                },
            },
            'active': True,
            'after action': 'keep going'
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
            'target': "self.menu_structure['main menu']['new']['value']",
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
            # 'submenu': {
            #     'name': "map single selection",
            #     'exit button': 'all',  # If it needed to exit a submenu by pressing any button: 'all'
            #     'exit action': 'store value'
            # },
            'submenu name': "map single selection",
            # 'submenu exit action': 'store value',
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
x = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER MAX X:', MAXX, 'int')\n\
y = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2 + 50), 'ENTER MAX Y:', MAXY, 'int')\n\
self.camera.setup(int(x), int(y))\n\
self.create_snap_mesh()",
            'active': True,
            'after action': 'keep going'
        },
        'rename': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
            'label': '[RENAME MAP]',
            'on hover action': None,
            'LMB action': 'exec',
            'value': '''
new_name = self.create_text_input((MAXX_DIV_2, MAXY_DIV_2), 'ENTER NEW MAP NAME:', self.location, 'str')\n
self.rename_map(new_name)
''',
            'target': 'self.menu_walk_tree.append(\'CANCEL MENU\')',
            'active': True,
            'after action': None
        },
        'delete clipboard elements': {
            'rectangle': pygame.Rect(menu_elements_bindings['central right button']),
            'self dict name': 'delete clipboard elements',  # It is necessary if such menu item reveals other menu.
            'label': '[delete clipboard elements]',
            'on hover action': None,
            'LMB action': 'reveal submenu',
            # 'submenu': {
            #     'name': "map single selection",
            #     'exit button': 'all',  # If it needed to exit a submenu by pressing any button: 'all'
            #     'exit action': 'store value'
            # },
            'submenu name': "clipboard multiple selection",
            # 'submenu exit action': 'store value',
            # 'submenu exit action': 'append value',
            # 'submenu exit action': 'return self value',
            'value': "self.menu_structure['main menu']['delete clipboard elements']['target']",
            'target': list(),  # Here will be stored a map name to be load.
            # 'target': "self.location",
            # 'LMB action': 'return value',
            # 'value': "load",
            'active': True,
            'after action': None  # If None, after submenu has done, this level menu returns self 'value'.
            # 'after action': 'return value'
        },
        'export image': {
            'rectangle': pygame.Rect(menu_elements_bindings['bottom right button']),
            'label': '[EXPORT IMAGE TO PNG]',
            'on hover action': None,
            # 'LMB action': 'return value',
            # 'value': "resize",
            # 'submenu exit action': '',
            'LMB action': 'exec',
            'value': "self.export_screen()",
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

}