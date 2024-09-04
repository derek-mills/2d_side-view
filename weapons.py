import pygame

sword = {
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'attack animation': 'stab',
    'stamina consumption': 1.2,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'sword',
    'sprite': 'short sword',
    'reach': 50,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 70, 10), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'short sword demolisher',
            'pierce': False, 'demolisher TTL': 6, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0,
            'attack type': ('slash',),
             'damage': {
                 'slash': 80
             },
            'aftermath': 'disappear'
        },
        {
            'rect': pygame.Rect(0, 0, 75, 10), 'flyer': False,
            'visible': True,
            'demolisher sprite': 'short sword demolisher',
            'pierce': False, 'demolisher TTL': 8, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0,
            'attack type': ('slash',),
            'damage': {
                'slash': 100
            },
            'aftermath': 'disappear'
        },),
    ),
    'description': 'Casual kitchen knife.',
}

kitchen_knife = {
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.4,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'aimed fire': True,
    'attack animation': 'stab',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'class': 'weapons',
    'type': 'melee',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'kitchen knife',
    'sprite': 'kitchen knife',
    # 'demolisher offset': {
    #     1:  (46, 36),
    #     -1: (-46, 36),
    # },
    'reach': 50,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 30, 30), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'kitchen knife demolisher',
            'pierce': False, 'demolisher TTL': 10, 'speed': 12,
            'static': True, 'damage reduce': .1,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('slash',),
             'damage': {
                 'slash': 100
             },
            'aftermath': None
        },),
        # {
        #     'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
        #     'demolisher sprite': None,
        #     'pierce': False, 'demolisher TTL': 50, 'speed': 22,
        #     'damage': 10, 'static': False, 'damage reduce': .1,
        #     'collides': True, 'gravity affected': True,
        #     'bounce': True, 'bounce factor': .9,
        #     'aftermath': 'disappear'
        # },
        # {
        #     'rect': pygame.Rect(0, 0, 30, 30), 'flyer': False,
        #     'demolisher sprite': 'kitchen knife demolisher',
        #     'pierce': False, 'demolisher TTL': 100, 'speed': 12,
        #     'damage': 10, 'static': False, 'damage reduce': .1,
        #     'collides': True, 'gravity affected': True,
        #     'bounce': True, 'bounce factor': 1.,
        #     'aftermath': 'explode'
        # },
    ),
    'description': 'Casual kitchen knife.',
}

fireball_staff = {
    'description': 'Casual kitchen fireball staff.',
    'class': 'weapons',
    'type': 'melee',
    'label': 'fireball staff',
    'sprite': 'staff',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': .5,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 2.,
    'attack animation': 'cast',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 1000,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 70, 70), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'staff demolisher',
            'pierce': True, 'demolisher TTL': 150, 'speed': 30,
            'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': 0.3,
            'attack type': ('fire', ),
             'damage': {
                 'fire': 150,
             },
            'aftermath': 'disappear'
        },),
    ),

}

spikeball_staff = {
    'description': 'Ball of spikes.',
    'class': 'weapons',
    'type': 'melee',
    'label': 'spikeball staff',
    'sprite': 'staff',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': .5,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 2.,
    'attack animation': 'cast',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'actor forward moving speed': 0.3,  # During attack an actor may uncontrollably move forward (min 0.5).
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 1000,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 70, 70), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'spikeball staff demolisher',
            'pierce': False, 'demolisher TTL': 250, 'speed': 30,
            'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': 0.9,
            'attack type': ('pierce',),
             'damage': {
                 'pierce': 100,
             },
            'aftermath': 'disappear'
        },),
    ),

}

whip = {
    'description': 'A powerful whip, called Vampire Killer.',
    'class': 'weapons',
    'type': 'melee',
    'label': 'whip',
    'sprite': 'whip',

    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': .1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'whip',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'whip demolisher short',
            'pierce': False, 'demolisher TTL': 1, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('pierce',),
             'damage': {
                 'pierce': 10,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'whip demolisher medium',
            'pierce': False, 'demolisher TTL': 1, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('pierce',),
             'damage': {
                 'pierce': 30,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'whip demolisher long',
            'pierce': True, 'demolisher TTL': 5, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('pierce',),
             'damage': {
                 'pierce': 60,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

jake_kick = {
    'description': 'A powerful kick, called The Boot of Doom.',
    'class': 'weapons',
    'type': 'melee',
    'label': 'jake kick',
    'sprite': 'boot',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': .1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'kick',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'jake kick demolisher',
            'pierce': False, 'demolisher TTL': 8, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('smash',),
             'damage': {
                 'smash': 10,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

axe = {
    'description': 'Golden Axe 3',
    'class': 'weapons',
    'type': 'melee',
    'label': 'axe',
    'sprite': 'axe',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': .1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'axe swing',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 2.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 45 demolisher',
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'damage': {
                 'smash': 10,
                 'slash': 10
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 0 demolisher',
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'damage': {
                 'smash': 50,
                 'slash': 50
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 315 demolisher',
            'pierce': True, 'demolisher TTL': 6, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'damage': {
                 'smash': 70,
                 'slash': 70
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

demon_2_mid = {
    'description': 'Demon 2 middle ranged weapon',
    'class': 'weapons',
    'type': 'melee',
    'label': 'demon 2 mid',
    'sprite': 'demon 2 mid claw demolisher',
    'attack animation': 'whip',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.5,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 300,
    # 'reach': sprites['demon 2 mid claw demolisher 1']['mask rect'].width,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 mid claw demolisher 1',
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', ),
             'damage': {
                 'slash': 100
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 mid claw demolisher 2',
            'pierce': False, 'demolisher TTL': 5, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', 'pierce'),
             'damage': {
                 'pierce': 100,
                 'slash': 10
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 mid claw demolisher 3',
            'pierce': False, 'demolisher TTL': 6, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash', ),
             'damage': {
                 'smash': 100,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

demon_2_close = {
    'description': 'Demon 2 close combat weapon',
    'class': 'weapons',
    'type': 'melee',
    'label': 'demon 2 close',
    'sprite': 'whip',
    'attack animation': 'stab',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.5,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 200,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
            'visible': True,
            'demolisher sprite': 'demon 2 claw demolisher 2',
            'pierce': False, 'demolisher TTL': 8, 'speed': 0,
            'static': True, 'damage reduce': 0,
            # 'damage': 250, 'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('slash', 'smash', 'pierce'),
             'damage': {
                 'smash': 100,
                 'pierce': 100,
                 'slash': 10
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 claw demolisher',
            'pierce': False, 'demolisher TTL': 10, 'speed': 0,
            'static': True, 'damage reduce': 0,
            # 'damage': 250, 'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('slash', 'smash', 'pierce'),
             'damage': {
                 'smash': 100,
                 'pierce': 100,
                 'slash': 10
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

pistol = {
    'description': 'Handy handgun.',
    'class': 'weapons',
    'type': 'firearms',
    'label': 'pistol',
    'sprite': 'pistol',
    'attack animation': 'pistol shot',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.4,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    # 'need ammo': True,
    # 'ammo': 20,
    'reach': 200,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 2, 2), 'flyer': True,
            'visible': False,
            'demolisher sprite': None,
            'pierce': False, 'demolisher TTL': 120, 'speed': 1,
            'static': False, 'damage reduce': 0,
            # 'damage': 50, 'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('slash', 'smash', 'pierce'),
             'damage': {
                 'fire': 25,
                 'smash': 10,
                 'pierce': 100,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

barrel_explosion = {
    'description': 'Barrel explosion.',
    'class': 'weapons',
    'type': 'firearms',
    'label': 'barrel explosion',
    'sprite': '',
    'attack animation': 'explosion',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'need ammo': False,
    'ammo': 0,
    'reach': 0,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 50, 50), 'flyer': False,
            'visible': False,
            'demolisher sprite': None,
            'pierce': False, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            # 'damage': 500, 'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('fire', 'smash', 'pierce', 'slash'),
            'damage': {
                'fire': 50,
                'smash': 100,
                'pierce': 100,
                'slash': 10
            },
            'aftermath': 'explode'
            # 'aftermath': 'disappear'
        },),
    ),

}

small_shield = {
    'description': 'Small shield.',
    'class': 'weapons',
    'type': 'shields',
    'label': 'small shield',
    'sprite': 'small shield',
    'attack animation': 'protect',
    'sound': 'sound_swing_2',
    # 'amount': 1,
    # 'amount threshold': 1,
    # 'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'ignore user input': False,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'protectors': (
        ({
            'rect': pygame.Rect(0, 0, 50, 50), 'flyer': False,
            'visible': True,
            'keep alive': True,  # If button holding down, we must keep this particular protector alive and not allow to summon the new ones.
            'protector sprite': 'small shield protector',
            'pierce': False, 'protector TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': None,
            # 0: 100% protection (because damage will be multiplied by the amount of protection)
            # 1: 0% protection
            # >1: protector will amplify the damage amount of such type.
            'protection': {
                # 'stamina': 0.08,  # The lesser, the better stamina saving.
                'fire': 0.2,
                'smash': 0.2,
                'pierce': 0.2,
                'slash': 0.2
            },
            'aftermath': None
            # 'aftermath': 'explode'
            # 'aftermath': 'disappear'
        },),
    ),

}