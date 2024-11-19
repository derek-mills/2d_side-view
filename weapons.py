import pygame

sword = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,    'amount': 1,
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
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'sound': 'sound_swing_2',
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'label': 'short sword',
    'sprite': 'short sword',
    'reach': 50,
    'weight': 40,
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
            'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
            'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                'slash': 100
            },
            'aftermath': 'disappear'
        },),
    ),
    'description': 'Casual kitchen knife.',
}

kitchen_knife = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,    'amount': 1,
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
    'drop invincibility': 100,
    'has crouch attack': False,
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
    'weight': 20,
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
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Casual kitchen fireball staff.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'fireball staff',
    'sprite': 'fireball staff',
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
    'weight': 150,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 70, 70), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'fireball demolisher',
            'pierce': True, 'demolisher TTL': 150, 'speed': 30,
            'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': True,
            'bounce': True, 'bounce factor': 0.3,
            'attack type': ('fire', ),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bounce_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'fire': 150,
             },
            'aftermath': 'disappear'
        },),
    ),

}

spikeball_staff = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,    'description': 'Ball of spikes.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'spikeball staff',
    'sprite': 'fireball staff',
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
    'weight': 100,
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
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bounce_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'pierce': 100,
             },
            'aftermath': 'disappear'
        },),
    ),

}

whip = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,    'description': 'A powerful whip, called Vampire Killer.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': True,
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
    'weight': 30,
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
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'pierce': 60,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

jake_kick = {
    'combo': True, 'combo steps quantity': 3, 'combo next step threshold': 30,
    'description': 'A powerful kick, called The Boot of Doom.',
    'class': 'weapons',
    'drop invincibility': 0,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'jake kick',
    'sprite': 'boot',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'kick',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'weight': 1,
    'demolishers': (
        # 'demolishers set number' #0
        ({
             'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
             'visible': False,
             'demolisher sprite': 'jake kick demolisher',
             'pierce': True, 'demolisher TTL': 3, 'speed': 0,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             # 'attack type': ('smash',),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'blunt': 15,
                 # 
                 # 'slash': 1,
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },),
        # 'demolishers set number' #1
        ({
             'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
             'visible': False,
             'demolisher sprite': 'jake kick demolisher',
             'pierce': True, 'demolisher TTL': 3, 'speed': 0,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             'attack type': ('smash',),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'blunt': 20,
                 'slash': 1,
                 
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },),

        # 'demolishers set number' #2
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'jake kick demolisher',
            'pierce': True, 'demolisher TTL': 5, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('smash',),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'blunt': 50,
                 
                 'slash': 1,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

jake_punch = {
    'combo': True, 'combo steps quantity': 3, 'combo next step threshold': 30,
    'description': 'A powerful punch series.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'jake punch',
    'sprite': 'boot',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'punch',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': False,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'weight': 1,
    'demolishers': (
        # 'demolishers set number' #0
        ({
             'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
             'visible': False,
             'demolisher sprite': '',
             'pierce': True, 'demolisher TTL': 3, 'speed': 0,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             'attack type': ('smash',),
             'push': False,
              'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'blunt': 15,
                 # 
                 'slash': 1,
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },),
        # 'demolishers set number' #1
        ({
             'rect': pygame.Rect(0, 0, 10, 10), 'flyer': False,
             'visible': False,
             'demolisher sprite': '',
             'pierce': True, 'demolisher TTL': 3, 'speed': 0,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             'attack type': ('smash',),
             'push': False,
              'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'blunt': 50,
                 'slash': 1,
                 # 
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },),
        # 'demolishers set number' #2
        ({
            'rect': pygame.Rect(0, 0, 20, 40), 'flyer': False,
             'visible': False,
            'demolisher sprite': '',
            'pierce': True, 'demolisher TTL': 5, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': ('smash',),
            'push': True,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'blunt': 70,
                 'slash': 1,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

axe = {
    'combo': True, 'combo steps quantity': 2, 'combo next step threshold': 50,
    'description': 'Golden Axe 3',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'axe',
    'sprite': 'axe',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 1,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'attack animation': 'axe swing',
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 3.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 170,
    'weight': 70,
    'demolishers': (
        # 'demolishers set number' #0
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 45 demolisher',
            'pierce': False, 'demolisher TTL': 1, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'slash': 10
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        # 'demolishers set number' #1
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 0 demolisher',
            'pierce': False, 'demolisher TTL': 1, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'slash': 30
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        # 'demolishers set number' #2
        ({
            'rect': pygame.Rect(0, 0, 180, 270), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'axe 315 demolisher',
            'pierce': True, 'demolisher TTL': 6, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash','slash'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'slash': 190
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        # 'demolishers set number' #3
        ({
             'rect': pygame.Rect(0, 0, 180, 270), 'flyer': False,
             'visible': True,
             'demolisher sprite': 'axe 315 demolisher',
             'pierce': True, 'demolisher TTL': 2, 'speed': 0,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             # 'attack type': ('smash','slash'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'slash': 90
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },),

    ),

}

demon_2_mid = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Demon 2 middle ranged weapon',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'demon 2 mid',
    'sprite': 'demon 2 mid claw demolisher',
    'attack animation': 'whip',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 1.5,  # Stamina reduce multiplier. The greater, the more stamina will be lost per one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 250,
    # 'reach': sprites['demon 2 mid claw demolisher 1']['mask rect'].width,
    'weight': 10,
    'demolishers': (
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 mid claw demolisher 1',
            'pierce': True, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', ),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
            'pierce': True, 'demolisher TTL': 2, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', 'pierce'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
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
            'pierce': True, 'demolisher TTL': 5, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('smash', ),
            'push': True,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'blunt': 100,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

demon_2_close = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Demon 2 close combat weapon',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'melee',
    'label': 'demon 2 close',
    'sprite': 'whip',
    'attack animation': 'stab',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 1.5,  # Stamina reduce multiplier. The greater, the more stamina will be lost per one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'need ammo': False,
    'ammo': 0,
    'reach': 200,
    'weight': 10,
    'demolishers': (
        # Set 0
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
            'visible': True,
            'demolisher sprite': 'demon 2 claw demolisher 2',
            'pierce': False, 'demolisher TTL': 8, 'speed': 0,
            'static': True, 'damage reduce': 0,
            # 'damage': 250, 'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', 'smash', 'pierce'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'pierce': 100,
                 'slash': 100
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
        # Set 1
        ({
            'rect': pygame.Rect(0, 0, 170, 5), 'flyer': False,
             'visible': True,
            'demolisher sprite': 'demon 2 claw demolisher',
            'pierce': False, 'demolisher TTL': 10, 'speed': 0,
            'static': True, 'damage reduce': 0,
            # 'damage': 250, 'static': True, 'damage reduce': 0,
            'collides': False, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', 'smash', 'pierce'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {
                 'pierce': 100,
                 'slash': 100
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

pistol = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Handy handgun.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
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
    'reach': 2000,
    'weight': 10,
    'demolishers': (
        ({
             'rect': pygame.Rect(0, 0, 2, 2), 'flyer': False,
             'visible': True,
             'demolisher sprite': 'pistol muzzle flash',
             'pierce': True, 'demolisher TTL': 2, 'speed': 1,
             'static': True, 'damage reduce': 0,
             'collides': False, 'gravity affected': False,
             'bounce': False, 'bounce factor': 0.,
             # 'attack type': ('slash', 'smash', 'pierce'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'fire': 225,
             },
             # 'aftermath': 'explode'
             'aftermath': 'disappear'
         },
        {
            'rect': pygame.Rect(0, 0, 5, 2), 'flyer': True,
            'visible': False,
            'demolisher sprite': None,
            'pierce': False, 'demolisher TTL': 120, 'speed': 3,
            'static': False, 'damage reduce': 0,
            # 'damage': 50, 'static': False, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            # 'attack type': ('slash', 'smash', 'pierce'),
             'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                 'fire': 25,
                 
                 'pierce': 100,
             },
            # 'aftermath': 'explode'
            'aftermath': 'disappear'
        },),
    ),

}

barrel_explosion = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Barrel explosion.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
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
    'weight': 10,
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
            'push': False,
             'sounds': {
                 'obstacle hit': 'sound_bullet_wall_hit_1',
                 'body hit': 'sound_meat_blow_1',
                 'protector hit': 'sound_bucket_hit_1',
             },
             'damage': {

                'fire': 50,
                
                'pierce': 100,
                'slash': 10
            },
            'aftermath': 'explode'
            # 'aftermath': 'disappear'
        },),
    ),

}

small_shield = {
    'combo': False, 'combo steps quantity': 0, 'combo next step threshold': 0,
    'description': 'Small shield.',
    'class': 'weapons',
    'drop invincibility': 100,
    'has crouch attack': False,
    'type': 'shields',
    'label': 'small shield',
    'sprite': 'small shield',
    'attack animation': 'protect',
    'sound': 'sound_swing_2',
    'amount': 1,
    'amount threshold': 1,
    'amount decrease speed': 0,
    'affects on': '',
    'stamina consumption': 0.,  # Stamina reduce multiplier. The greater, the more stamina will be lost by one weapon use.
    'mana consumption': 0.,
    'ignore user input': True,  # Steal the ability to control a character for a while.
    # 'ignore user input': False,  # Steal the ability to control a character for a while.
    'animation speed modifier': 1.,  # 0 < x < 1: speed animation up, x > 1: slow down.
    'leave particles': False,
    'droppable': True,
    'weight': 40,
    'protectors': (
        ({
            'rect': pygame.Rect(10, 0, 20, 250), 'flyer': False,
            'mana consumption': 4.,
            'stamina consumption': 1.,
            # 'visible': False,
            'visible': True,
            'keep alive': True,  # If button holding down, we must keep this particular protector alive and not allow to summon the new ones.
            'protector sprite': 'small shield protector',
            'pierce': False, 'protector TTL': 0, 'speed': 0,
            'static': True, 'damage reduce': 0,
            'collides': True, 'gravity affected': False,
            'bounce': False, 'bounce factor': 0.,
            'attack type': None,
            # 0: 100% protection (because damage will be multiplied by the amount of protection)
            # 1: 0% protection
            # >1: protector will amplify the damage amount of such type.
            'protection': {
                'blunt': 0.3,
                'fire': 0.,
                'pierce': 0.5,
                'slash': 0.
            },
            'aftermath': None
            # 'aftermath': 'explode'
            # 'aftermath': 'disappear'
        },),
    ),

}