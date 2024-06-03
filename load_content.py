from graphics import *

def load_animations(actor):
    # Animation loadings:
    # for i in actor.animations['animations']['side walk'][1]:
    # print(actor.animations)
    sprites[actor.id] = dict()
    sprites[actor.id]['sprites'] = dict()
    sprites[actor.id]['masks'] = dict()
    sprites[actor.id]['outlines'] = dict()
    sprites[actor.id]['avatars'] = dict()
    sprites[actor.id]['avatars']['avatar'] = sprites[actor.name + ' avatar']
    sprites[actor.id]['avatars']['avatar front'] = sprites[actor.name + ' avatar front']

    for animation_type in actor.animations.keys():
        sprites[actor.id]['sprites'][animation_type] = dict()
        sprites[actor.id]['masks'][animation_type] = dict()
        sprites[actor.id]['outlines'][animation_type] = dict()
        # print('[load_animations] added', animation_type )

        # sprites[actor.name][animation_type] = dict()
        # actor.sprites[animation_type] = dict()

        # animation_description = actor.animation_descriptor + ' ' + actor.animations[animation_type]['description']
        for anim_direction in (-1, 1):
            animation_sequence = actor.animations[animation_type][anim_direction]['sequence']
            sprites[actor.id]['sprites'][animation_type][anim_direction] = dict()
            sprites[actor.id]['masks'][animation_type][anim_direction] = dict()
            sprites[actor.id]['outlines'][animation_type][anim_direction] = dict()
            for frame in animation_sequence:
                animation_description = actor.animation_descriptor + ' ' + str(frame)  # For ex., 'Jake 0'
                # txt_description = animation_description + str(frame)
                # sz = self.sprites[txt_description].get_size()
                # print(self.sprites[txt_description].get_palette())
                # exit()
                sprites[actor.id]['sprites'][animation_type][anim_direction][animation_description] = sprites[animation_description]
                sprites[actor.id]['masks'][animation_type][anim_direction][animation_description] = pygame.mask.from_surface(sprites[animation_description]['sprite'])
                sprites[actor.id]['outlines'][animation_type][anim_direction][animation_description] = create_contour_by_mask(sprites[actor.id]['masks'][animation_type][anim_direction][animation_description])
                # sprites[actor.name][animation_type][animation_description] = sprites[animation_description]
                # actor.sprites[animation_type][txt_description] = sprites[txt_description]
                # print('[load_animations]', txt_description, '>>', sprites[actor.id]['sprites'][animation_type][txt_description])