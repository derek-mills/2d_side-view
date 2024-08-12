# exp = {
#     'name': 'exp orb',
#     'minimum amount': 100,
#     'decrease speed': 0.1,
#     'sprite': 'exp'
# }
from weapons import *
all_items = {
    'exp':  {
        'description': 'exp orb',
        'class': 'instant consume',
        'type': 'stats gainer',
        'label': 'exp',
        'sprite': 'exp',
        'sound': None,

        'amount': 200,
        'amount threshold': 100,
        'amount decrease speed': -.01,
        'affects on': 'exp',
    },
    'health vial': {
        'description': 'health vial',
        'class': 'consumables',
        'type': 'stats gainer',
        'label': 'health vial',
        'sprite': 'health vial',
        'sound': None,
        'amount': 100,
        'amount threshold': 100,
        'amount decrease speed': 0,
        'affects on': '',

    },
    'stash': {
        'description': 'Stash box to store items',
        'class': 'burden',
        'type': '',
        'label': 'stash',
        'sprite': 'stash',
        'sound': None,
        'amount': 0,
        'amount threshold': 0,
        'amount decrease speed': 0,
        'affects on': '',
    },
    'fireball staff': fireball_staff,
    'whip': whip,
    'kitchen knife': kitchen_knife,
    'sword': sword,
}
# all_items = {
#     'exp': exp,
#     'exp2': exp2,
#     'exp3': exp3,
#     'exp4': exp4,
# }