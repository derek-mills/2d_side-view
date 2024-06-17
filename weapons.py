import pygame
sword = {
    # 'aimed fire': True,
    'attack animation': 'stab',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'attack type': 'pierce',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'SHORT SWORD',
    'sprite': 'short sword',
    'reach': 50,
    'demolishers': (
        {
            'rect': pygame.Rect(0, 0, 70, 10), 'flyer': False,
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'damage': 50, 'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0,
            'aftermath': 'disappear'
        },
        {
            'rect': pygame.Rect(0, 0, 75, 10), 'flyer': False,
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'damage': 60, 'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0,
            'aftermath': 'disappear'
        },
    ),
    'description': 'Casual kitchen knife.',
}

kitchen_knife = {
    'aimed fire': True,
    'attack animation': 'stab',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'attack type': 'pierce',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'KITCHEN KNIFE',
    'sprite': 'kitchen knife',
    # 'demolisher offset': {
    #     1:  (46, 36),
    #     -1: (-46, 36),
    # },
    'reach': 50,
    'demolishers': (
        {
            'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
            'pierce': False, 'demolisher TTL': 50, 'speed': 22,
            'damage': 10, 'static': False, 'damage reduce': .1,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': .9,
            'aftermath': 'disappear'
        },
        {
            'rect': pygame.Rect(0, 0, 30, 30), 'flyer': False,
            'pierce': False, 'demolisher TTL': 100, 'speed': 12,
            'damage': 10, 'static': False, 'damage reduce': .1,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': 1.,
            'aftermath': 'explode'
        },
    ),
    'description': 'Casual kitchen knife.',
}

fireball_staff = {
    # 'aimed fire': True,
    'attack animation': 'cast',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'attack type': 'pierce',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'FIREBALL STAFF',
    'sprite': 'staff',
    'reach': 50,
    'demolishers': (
        {
            'rect': pygame.Rect(0, 0, 70, 70), 'flyer': False,
            'pierce': False, 'demolisher TTL': 150, 'speed': 30,
            'damage': 150, 'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': 0.3,
            'aftermath': 'disappear'
        },
    ),
    'description': 'Casual kitchen fireball staff.',
}

whip = {
    'attack animation': 'whip',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'attack type': 'pierce',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'WHIP',
    'sprite': 'whip',
    'reach': 170,
    'demolishers': (
        {
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
            'pierce': False, 'demolisher TTL': 5, 'speed': 0,
            'damage': 150, 'static': False, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'aftermath': 'disappear'
        },
    ),
    'description': 'Casual kitchen fireball staff.',
}