from constants import *
from random import randint, choice, choices
from pygame.constants import SRCALPHA

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREENSIZE)

# class ImmutableDict(dict):
#     def set(self):
#         raise NotImplemented()
#
#     def __setitem__(self, *args, **kwargs):
#         raise RuntimeError("This is an immutable dictionary")


# if __name__ == '__main__':
#     my_dict = ImmutableDict({"foo": 1, "bar": 2})
#     print(my_dict["foo"])
#     my_dict["foo"] = 3

def create_contour_by_mask(mask):
    rect = mask.get_rect()
    check_dot = rect.center
    while not mask.get_at(check_dot):
        check_dot = (randint(1, rect.width - 1), randint(1, rect.height - 1))
    contour = mask.connected_component(check_dot)

    dots = contour.outline(OUTLINE_DOTS_COUNTER)
    if len(dots) < 2:
        return
    surface = pygame.Surface((rect.width, rect.height), SRCALPHA).convert_alpha()
    pygame.draw.polygon(surface, (100, 200, 0), dots, 6)
    arr = pygame.PixelArray(surface)
    return {'surface': surface, 'array': arr}

def load_single_frame(source, frame, name, scale_factor=1):
    global sprites, sprites_reference
    snap_x = 0
    sub_surf = source.subsurface(frame)
    cropped_surf = sub_surf.subsurface(sub_surf.get_bounding_rect())
    sz = cropped_surf.get_size()
    sprite_asymmetric = False
    # sub_surf = source.subsurface(frame)
    # cropped_surf = sub_surf.subsurface(sub_surf.get_bounding_rect())
    # scaled_cropped_surf = pygame.transform.scale(cropped_surf, (cropped_surf.get_size()[0] * scale_factor, cropped_surf.get_size()[1] * scale_factor))
    # snap_x = scaled_cropped_surf.get_size()[0] // 2
    # If we can find a magenta dot in the very first row, then consider it as new snap point for x coordinate.
    for dx in range(cropped_surf.get_size()[0]):
        # print(cropped_surf.get_at((dx, 0)))
        dot_color = cropped_surf.get_at((dx, 0))
        # print(name, dot_color)
        if dot_color == (255, 0, 255, 255):
            snap_x = dx
            # Now we must erase the anchor magenta pixel, resize sprite...
            cropped_surf = cropped_surf.subsurface((0, 1, sz[0], sz[1] - 1))
            cropped_surf = cropped_surf.subsurface(cropped_surf.get_bounding_rect())
            # ...and renew the sz variable.
            sz = cropped_surf.get_size()
            sprite_asymmetric = True
            # print(name, frame_count, ': found snap point!', snap_x)
            # print(name, frame_count, ' size is ', cropped_surf.get_size())
            break

    scaled_cropped_surf = pygame.transform.scale(cropped_surf, (sz[0] * scale_factor, sz[1] * scale_factor))
    # scaled_cropped_surf = pygame.transform.scale(cropped_surf, (cropped_surf.get_size()[0] * scale_factor, cropped_surf.get_size()[1] * scale_factor))
    snap_x = scaled_cropped_surf.get_size()[0] // 2 if snap_x == 0 else snap_x

    # tmp_surf = pygame.transform.scale(source.subsurface(frame), (frame[2] * scale_factor, frame[3] * scale_factor))
    # cropped_surf = tmp_surf.subsurface(tmp_surf.get_bounding_rect())
    # snap_x = cropped_surf.get_size()[0] // 2

    sprites[name] = {
        'sprite': scaled_cropped_surf,
        'sprite center': snap_x * scale_factor,
        'sprite asymmetric': sprite_asymmetric
    }
    sprites_reference[name] = {
        'sprite': scaled_cropped_surf,
        'sprite center': snap_x * scale_factor,
        'sprite asymmetric': sprite_asymmetric
    }

def load_frames(source, approximate_frames, name, scale_factor=1):
    frame_count = 0
    global sprites, sprites_reference
    for frame in approximate_frames:
        snap_x = 0
        sub_surf = source.subsurface(frame)
        cropped_surf = sub_surf.subsurface(sub_surf.get_bounding_rect())
        sz = cropped_surf.get_size()
        sprite_asymmetric = False

        # If we can find a magenta dot in the very first row, then consider it as new snap point for x coordinate.
        for dx in range(cropped_surf.get_size()[0]):
            # print(cropped_surf.get_at((dx, 0)))
            dot_color = cropped_surf.get_at((dx, 0))
            # print(name, dot_color)
            if dot_color == (255,0,255,255):
                snap_x = dx * scale_factor
                # Now we must erase the anchor magenta pixel, resize sprite...
                cropped_surf = cropped_surf.subsurface((0,1,sz[0], sz[1] - 1))
                cropped_surf = cropped_surf.subsurface(cropped_surf.get_bounding_rect())
                # ...and renew the sz variable.
                sz = cropped_surf.get_size()
                sprite_asymmetric = True
                # print(name, frame_count, ': found snap point!', snap_x)
                # print(name, frame_count, ' size is ', cropped_surf.get_size())
                break

        scaled_cropped_surf = pygame.transform.scale(cropped_surf, (sz[0] * scale_factor, sz[1] * scale_factor))
        # scaled_cropped_surf = pygame.transform.scale(cropped_surf, (cropped_surf.get_size()[0] * scale_factor, cropped_surf.get_size()[1] * scale_factor))
        snap_x = scaled_cropped_surf.get_size()[0] // 2 if snap_x == 0 else snap_x

        sprites[name + str(frame_count)] = {
            'sprite': scaled_cropped_surf,
            'sprite center': snap_x,
            'sprite asymmetric': sprite_asymmetric
        }
        sprites_reference[name + str(frame_count)] = {
            'sprite': scaled_cropped_surf,
            'sprite center': snap_x,
            'sprite asymmetric': sprite_asymmetric
        }
        # sprites[name + str(frame_count)] = scaled_cropped_surf
        # sprites[name + str(frame_count) + ' snap x'] = snap_x * scale_factor

        # print(snap_x * scale_factor)
        # sprites[name + str(frame_count)] = tmp_surf.subsurface(tmp_surf.get_bounding_rect())
        frame_count += 1
    return

def load_all_frames(source, max_frames, name, width, height, scale_factor=1):
    global sprites, sprites_reference
    x = 0
    y = 0
    # width: int = 300
    # height: int = 500
    max_x, max_y = source.get_size()

    for frame_count in range(max_frames + 1):
        frame = (x, y, width,height)
        snap_x = 0
        sub_surf = source.subsurface(frame)
        cropped_surf = sub_surf.subsurface(sub_surf.get_bounding_rect())
        sz = cropped_surf.get_size()
        sprite_asymmetric = False

        # If we can find a magenta dot in the very first row, then consider it as new snap point for x coordinate.
        for dx in range(cropped_surf.get_size()[0]):
            # print(cropped_surf.get_at((dx, 0)))
            dot_color = cropped_surf.get_at((dx, 0))
            # print(name, dot_color)
            if dot_color == (255,0,255,255):
                snap_x = dx * scale_factor
                # Now we must erase the anchor magenta pixel, resize sprite...
                cropped_surf = cropped_surf.subsurface((0,1,sz[0], sz[1] - 1))
                cropped_surf = cropped_surf.subsurface(cropped_surf.get_bounding_rect())
                # ...and renew the sz variable.
                sz = cropped_surf.get_size()
                sprite_asymmetric = True
                # print(name, frame_count, ': found snap point!', snap_x)
                # print(name, frame_count, ' size is ', cropped_surf.get_size())
                break

        scaled_cropped_surf = pygame.transform.scale(cropped_surf, (sz[0] * scale_factor, sz[1] * scale_factor))
        snap_x = scaled_cropped_surf.get_size()[0] // 2 if snap_x == 0 else snap_x

        sprites[name + ' ' + str(frame_count)] = {
            'sprite': scaled_cropped_surf,
            'sprite center': snap_x,  # Distance from the very left side of a sprite in pixels.
            'sprite asymmetric': sprite_asymmetric
        }
        # sprites_reference[name + ' ' + str(frame_count)] = {
        #     'sprite': scaled_cropped_surf,
        #     'sprite center': snap_x,
        #     'sprite asymmetric': sprite_asymmetric
        # }
        x = x + width
        if x + width > max_x:
            x = 0
            y = y + height

    # print([name for name in sprites.keys() if 'demon' in name])
    # exit()


scaled_sprites_cache = dict()
def fill_scaled_sprites_cache(actor, cache_key, final_scale_factor):
    if actor.location not in scaled_sprites_cache.keys():
        scaled_sprites_cache[actor.location] = dict()
    if actor.name not in scaled_sprites_cache[actor.location].keys():
        scaled_sprites_cache[actor.location][actor.name] = dict()

    if cache_key not in scaled_sprites_cache[actor.location][actor.name].keys():
        current_sprite = sprites[actor.id]['sprites'][actor.current_animation][actor.gaze_direction][actor.current_frame]
        # Fill cache of scaled sprites for current actor.
        # print(f'[actor.fill_scaled_sprites_cache] Caching scaled sprite for {self.name}: "{cache_key}"')
        size_original = current_sprite['sprite'].get_size()
        scaled_sprites_cache[actor.location][actor.name][cache_key] = pygame.transform.scale(current_sprite['sprite'],
                                                                                           (size_original[0] * final_scale_factor,
                                                                                            size_original[1] * final_scale_factor))
    # self.get_scaled_sprite_from_cache(cache_key)

def get_scaled_sprite_from_cache(actor, cache_key):
    return pygame.transform.flip(scaled_sprites_cache[actor.location][actor.name][cache_key], True, False) \
        if actor.current_sprite_flip else scaled_sprites_cache[actor.location][actor.name][cache_key]

def scale_sprite(sprite, final_scale_factor, flip=False):
    size_original = sprite.get_size()
    return pygame.transform.flip(pygame.transform.scale(sprite, (size_original[0] * final_scale_factor,
                                                                 size_original[1] * final_scale_factor)), True, False) \
           if flip else pygame.transform.scale(sprite, (size_original[0] * final_scale_factor,
                                                        size_original[1] * final_scale_factor))

sprites = dict()
# sprites_reference = ImmutableDict()
sprites_reference = dict()
# environment = dict()
avatars = pygame.image.load('img/avatars.png').convert_alpha()
env = pygame.image.load('img/environment.png').convert_alpha()

sprites['light halo casual'] = pygame.image.load('img/light_halo.png').convert_alpha()
sprites['light halo strong'] = pygame.image.load('img/light_halo_strong.png').convert_alpha()
sprites['light halo mild'] = pygame.image.load('img/light_halo_mild_spot.png').convert_alpha()
sprites['light cone right'] = pygame.image.load('img/light_cone.png').convert_alpha()
sprites['light cone left'] = pygame.transform.flip(sprites['light cone right'], True, False)
sprites['light cone up'] = pygame.transform.rotate(sprites['light cone right'], 90)
sprites['light cone down'] = pygame.transform.rotate(sprites['light cone right'], 270)
sprites['light cone 45'] = pygame.image.load('img/light_cone_45.png').convert_alpha()
# self.static_lights[self.location] = pygame.surface.Surface((self.map_sz[0], self.map_sz[1])).convert_alpha()
# self.static_lights[self.location].fill((0, 0, 0, self.darkness_deepness), (0, 0, self.map_sz[0], self.map_sz[1]))
# sz = light_halo.get_size()
# self.static_lights[self.location].blit(light_halo, (x - sz[0] // 2, y - sz[1] // 2), special_flags=BLEND_RGBA_MIN)

# rotated_sprites_sz = pygame.transform.rotate(sprites['light cone up'], 45).get_size()
#
# sprites['light cone 45'] = pygame.surface.Surface((rotated_sprites_sz[0], rotated_sprites_sz[1])).convert_alpha()
# # sprites['light cone 45'].fill((0, 0, 0, DEFAULT_DARKNESS_DEEPNESS))
# sprites['light cone 45'].blit(pygame.transform.rotate(sprites['light cone up'], 45), (0,0))
# sprites['light cone 45'].fill((0, 0, 0, DEFAULT_DARKNESS_DEEPNESS), special_flags=BLEND_RGBA_MAX)
# # sprites['light cone 45'].blit(pygame.transform.rotate(sprites['light cone up'], 45), (0,0), special_flags=BLEND_RGBA_MULT)

sprites['light cone 135'] = pygame.transform.rotate(sprites['light cone 45'], 90)
sprites['light cone 225'] = pygame.transform.rotate(sprites['light cone 45'], 180)
sprites['light cone 315'] = pygame.transform.rotate(sprites['light cone 45'], 270)
# sprites['blood splatter'] = avatars.subsurface((128, 1062, 217, 198))
# sprites['idle sign'] = avatars.subsurface((2, 1096, 107, 107))
sprites['question sign'] = avatars.subsurface((573, 1053, 145, 240))
sprites['void'] = avatars.subsurface((0,1843,20,20))

# ___...---=== JAKE ===---...___
name = 'Jake'
tmp_sprites = pygame.image.load('img/animations/jake_8bit.png').convert_alpha()
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar')
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar front')
load_single_frame(tmp_sprites, ((2660,1720,90,50),), name + 'floor shadow mask')
# load_single_frame(tmp_sprites, ((1744,2194,332,205),), name + ' 98')  # Unconsciousness frame 1
# load_single_frame(tmp_sprites, ((2076,2220,369,176),), name + ' 99')  # Unconsciousness frame 2
load_all_frames(tmp_sprites, 43, name, 200, 300)
# tmp_sprites = pygame.image.load('img/animations/jake.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((1744,2194,332,205),), name + ' 98')  # Unconsciousness frame 1
# load_single_frame(tmp_sprites, ((2076,2220,369,176),), name + ' 99')  # Unconsciousness frame 2
# load_all_frames(tmp_sprites, 20, name)

# ___...---=== JANE ===---...___
name = 'Jane'
tmp_sprites = pygame.image.load('img/animations/jane_8bit.png').convert_alpha()
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar')
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar front')
load_single_frame(tmp_sprites, ((2660,1720,90,50),), name + 'floor shadow mask')
# load_single_frame(tmp_sprites, ((1744,2194,332,205),), name + ' 98')  # Unconsciousness frame 1
# load_single_frame(tmp_sprites, ((2076,2220,369,176),), name + ' 99')  # Unconsciousness frame 2
load_all_frames(tmp_sprites, 43, name, 200, 300)
# tmp_sprites = pygame.image.load('img/animations/jane.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_all_frames(tmp_sprites, 13, name, 300, 500)

# ___...---=== DEMON MALE 1 ===---...___
name = 'demon Hildegarda'
tmp_sprites = pygame.image.load('img/animations/demon_male_1.png').convert_alpha()
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar')
load_single_frame(tmp_sprites, ((2610,1530,180,150),), name + ' avatar front')
load_single_frame(tmp_sprites, ((2660,1720,90,50),), name + 'floor shadow mask')
load_all_frames(tmp_sprites, 43, name, 200, 300)
# tmp_sprites = pygame.image.load('img/animations/demon_female_1.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((1987,2245,459,150),), name + ' 99')  # Lay down
# load_all_frames(tmp_sprites, 8, name, 300, 500)

# ___...---=== DEMON FEMALE 2 ===---...___
# name = 'demon Hula'
# tmp_sprites = pygame.image.load('img/animations/demon_female_2.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((1987,2245,459,150),), name + ' 99')  # Lay down
# load_all_frames(tmp_sprites, 8, name, 300, 500)

# # ___...---=== PHANTOM ===---...___
# name = 'phantom'
# tmp_sprites = pygame.image.load('img/animations/phantom.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_all_frames(tmp_sprites, 4, name, 300, 500)

# load_frames(tmp_sprites, [(300*i, 0, 300, 500) for i in range(0, 6, 1)], 'phantom side walk frame ')
# load_frames(tmp_sprites, ((0,500, 300, 500), (300,500, 300, 500)), 'phantom down walk frame ')
# load_frames(tmp_sprites, ((600,500, 300, 500), (900,500, 300, 500)), 'phantom up walk frame ')

# ___...---=== DUDE ===---...___
# load_single_frame(tmp_sprites, ((600, 0, 300, 500),), 'dude avatar')
# load_single_frame(tmp_sprites, ((600, 0, 300, 500),), 'dude avatar front')
# avatars_dude = pygame.image.load('/media/sid/d90c7353-09c5-492a-aa88-66d695362d79/sid/Images/!games/SPRITES/figures_animation/dude.png').convert_alpha()
# approximate_frames_down_walk = ((20,5,48,148),(115,6,48,148),(211,6,48,148),(307,6,48,148),(403,6,48,148),(499,6,48,148),(596,6,48,148),
# (689,6,48,148),(785,6,48,148),(878,6,53,149),(975,6,53,149),(1071,6,51,144))
# load_frames(avatars_dude, approximate_frames_down_walk, 'dude down walk frame ', 3)
# approximate_frames_side_walk = ((3,314,89,161),(98,314,89,161),(194,314,89,161),(289,314,89,161),(381,314,89,161),(476,314,89,161),(571,314,89,161),(672,314,89,161),
#                                 (774,314,89,161),(863,314,89,161),(954,314,89,161),(1045,314,89,161),)
# load_frames(avatars_dude, approximate_frames_side_walk, 'dude side walk frame ', 3)
# approximate_frames_up_walk = ((102,480,82,148), (195,482,82,148), (292,483,82,148), (390,484,82,148), (482,482,82,148),(579,484,82,148),
# (673,480,82,148), (767,481,82,148), (865,482,82,148),(957,480,82,148),(1048,479,82,148),(17,479,61,151))
# load_frames(avatars_dude, approximate_frames_up_walk, 'dude up walk frame ', 3)

# ___...---=== ZOMBIE ===---...___
# sprites['zombie2 avatar'] = avatars.subsurface((600, 500, 300, 500))  #  Zombie male 1 avatar
# sprites['zombie2 avatar front'] = avatars.subsurface((600, 500, 300, 500))  #  Zombie male 1 avatar FRONT
# sprites['zombie2 round frame 0'] = avatars.subsurface((600, 2001, 300, 300))  # Zombie male 2 round avatar
# sprites['zombie2 round frame 1'] = avatars.subsurface((600, 2301, 300, 300))  # Zombie male 2 round avatar
# sprites['zombie2 side walk frame 0'] = avatars.subsurface((1872,887,153,450))  # player male 1 front avatar
# sprites['zombie2 side walk frame 1'] = avatars.subsurface((2124,887,180,450))  # player male 1 front avatar
# sprites['zombie2 side walk frame 2'] = avatars.subsurface((2376,887,261,450))  # player male 1 front avatar
# sprites['zombie2 side walk frame 3'] = avatars.subsurface((2682,887,157, 450))  # player male 1 front avatar
# sprites['zombie2 side walk frame 4'] = avatars.subsurface((2934,887,201, 450))  # player male 1 front avatar
# sprites['zombie2 side walk frame 5'] = avatars.subsurface((3186,887,262, 450))  # player male 1 front avatar
# sprites['zombie2 down walk frame 0'] = avatars.subsurface((1872,887,153,450))  # player male 1 front avatar
# sprites['zombie2 down walk frame 1'] = avatars.subsurface((2124,887,180,450))  # player male 1 front avatar
# sprites['zombie2 up walk frame 0'] = avatars.subsurface((1872,887,153,450))  # player male 1 front avatar
# sprites['zombie2 up walk frame 1'] = avatars.subsurface((2124,887,180,450))  # player male 1 front avatar
# sprites['zombie2 stand frame 0'] = avatars.subsurface((1588,887,153,450))  # player male 1 front avatar


# Tiny figure
# sprites['player1 side walk frame 0'] = avatars.subsurface((1016,2935,124,144))  # player male 1 front avatar
# sprites['player1 side walk frame 1'] = avatars.subsurface((1274,2939,122,146))  # player male 1 front avatar
# sprites['player1 side walk frame 2'] = avatars.subsurface((1516,2941,136,146))  # player male 1 front avatar
# sprites['player1 side walk frame 3'] = avatars.subsurface((1770,2939,138,148))  # player male 1 front avatar
# sprites['player1 side walk frame 4'] = avatars.subsurface((2040,2935,124,154))  # player male 1 front avatar
# sprites['player1 side walk frame 5'] = avatars.subsurface((2298,2937,122,148))  # player male 1 front avatar
# sprites['player1 side walk frame 6'] = avatars.subsurface((2540,2939,136,140))  # player male 1 front avatar
# sprites['player1 side walk frame 7'] = avatars.subsurface((2794,2936,138,144))  # player male 1 front avatar
# sprites['player1 down walk frame 0'] = avatars.subsurface((1044,3453,92,132))  # player male 1 front avatar
# sprites['player1 down walk frame 1'] = avatars.subsurface((1298,3457,92,122))  # player male 1 front avatar
# sprites['player1 down walk frame 2'] = avatars.subsurface((1554,3459,90,152))  # player male 1 front avatar
# sprites['player1 down walk frame 3'] = avatars.subsurface((1810,3457,92,146))  # player male 1 front avatar
# sprites['player1 down walk frame 4'] = avatars.subsurface((2068,3453,92,132))  # player male 1 front avatar
# sprites['player1 down walk frame 5'] = avatars.subsurface((2324,3457,92,122))  # player male 1 front avatar
# sprites['player1 down walk frame 6'] = avatars.subsurface((2582,3459,90,152))  # player male 1 front avatar
# sprites['player1 down walk frame 7'] = avatars.subsurface((2836,3457,89,140))  # player male 1 front avatar
# # sprites['player1 down walk frame 1'] = avatars.subsurface(())  # player male 1 front avatar
# sprites['player1 up walk frame 0'] = avatars.subsurface((1982, 1344, 200, 440))  # player male 1 front avatar
# sprites['player1 up walk frame 1'] = avatars.subsurface((2236, 1344, 200, 440))  # player male 1 front avatar

# sprites['zombie1'] = avatars.subsurface((300, 0, 300, 500))  #  Zombie female 1 avatar
# sprites['zombie1 front'] = avatars.subsurface((1200, 500, 300, 500))  #  Zombie female 1 avatar FRONT
# sprites['female1 front'] = avatars.subsurface((300, 500, 300, 500))  #  female 1 avatar FRONT
# sprites['zombie3'] = avatars.subsurface((900, 0, 300, 500))  #  Zombie male 2 avatar
# sprites['zombie3 front'] = avatars.subsurface((900, 500, 300, 500))  #  Zombie male 2 avatar FRONT
# sprites['zombie4'] = avatars.subsurface((1200, 0, 300, 500))  #  Zombie male 3 avatar
# sprites['zombie4 front'] = avatars.subsurface((900, 500, 300, 500))  #  Zombie male 2 avatar FRONT
# sprites['zombie punch 1'] = avatars.subsurface((3, 1333, 560, 667))  #
# sprites['zombie guarded 1'] = avatars.subsurface((566, 1333, 560, 667))  #
# sprites['zombie shadow 1'] = avatars.subsurface((1122, 1346, 510, 654))  #

sprites['void sprite'] = env.subsurface((0,1340,10,10))  #
sprites['pinetree'] = env.subsurface((0,400,475,800))  #
sprites['pile 1x #1'] = env.subsurface((0,0,94,199))  #
# sprites['pile 1x #1 trans'] = env.subsurface((1045,0,94,199))  #
sprites['glass 1x #1'] = env.subsurface((95,0,94,199))  #
sprites['glass 1x #2'] = env.subsurface((190,0,94,199))  #
sprites['box 1.5x #23'] = env.subsurface((380,0,94,199))  #
# sprites['box 1.5x #23 trans'] = env.subsurface((1425,0,94,199))  #
# sprites['box 2x pile 2x row'] = env.subsurface((1060,1000,200,271))  #
sprites['box single'] = env.subsurface((285,0,94,199))  #
# sprites['box single trans'] = env.subsurface((1330,0,94,199))  #
sprites['coffee table'] = env.subsurface((475,0,94,199))  #
sprites['metal crate #1 frame 0'] = env.subsurface((0,200,94,199))  #
sprites['metal crate #2 frame 0'] = env.subsurface((95,200,94,199))  #
sprites['wooden door #1 frame 0'] = env.subsurface((572,0,124,281))  # from NW to SE \
sprites['wooden door #2 frame 0'] = pygame.transform.flip(sprites['wooden door #1 frame 0'], True, False)  # from SW to NE /
# sprites['wooden door #2 frame 0'] = env.subsurface((696,0,124,281))  # from SW to NE /
# sprites['light switch'] = env.subsurface((855,0,95,94))  # big light switcher
sprites['light switch #1'] = env.subsurface((950,0,49,70))  # light switcher \
sprites['light switch #2'] = pygame.transform.flip(sprites['light switch #1'], True, False)  # light switcher /
# sprites['obstacle box single'] = pygame.transform.laplacian(sprites['obstacle box single'])
# sprites['obstacle pile 1x #1 w/glass 16 oclock'] = env.subsurface((1463, 869,102,200))  #
sprites['shotgun'] = avatars.subsurface((4, 2923,367,56))  # shotgun image
sprites['9mm_pistol'] = avatars.subsurface((382,2913,129,100))  # PM 9mm pistol image
sprites['kitchen knife'] = avatars.subsurface((514,2918,216,100))  # PM 9mm pistol image
# sprites['shield sign'] = avatars.subsurface((348, 1055, 223, 265))
cursors = pygame.image.load('img/cursors.png').convert_alpha()
sprites['aim cursor'] = cursors.subsurface((0,0,51,51))
sprites['walk cursor'] = cursors.subsurface((51,0,51,51))
sprites['interact cursor'] = cursors.subsurface((102,0,51,51))
sprites['ordinary cursor'] = cursors.subsurface((0,51,51,51))
sprites['knife cursor'] = cursors.subsurface((51,51,51,51))
sprites['fist cursor'] = cursors.subsurface((102,51,51,51))

all_obstacles = ('pile 1x #1', 'box 1.5x #23','box single',)
# sprites['fist'] = avatars.subsurface((725, 1063, 232, 199))

# sz = sprites['shield sign'].get_size()
# sprites['shield sign small'] = pygame.transform.scale(sprites['shield sign'], (sz[0] // 2, sz[1] // 2))

screen.convert_alpha(avatars)
screen.convert_alpha(env)

# for k in sprites.keys():
#     if 'demon' in k:
#         print(k)
