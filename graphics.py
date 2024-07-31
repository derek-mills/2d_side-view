from constants import *
from random import randint, choice, choices
from pygame.constants import SRCALPHA

pygame.init()
clock = pygame.time.Clock()
# pygame.FULLSCREEN    create a fullscreen display
# pygame.DOUBLEBUF     (obsolete in pygame 2) recommended for HWSURFACE or OPENGL
# pygame.HWSURFACE     (obsolete in pygame 2) hardware accelerated, only in FULLSCREEN
# pygame.OPENGL        create an OpenGL-renderable display
# pygame.RESIZABLE     display window should be sizeable
# pygame.NOFRAME       display window will have no border or controls
# pygame.SCALED        resolution depends on desktop size and scale graphics
# pygame.SHOWN         window is opened in visible mode (default)
# pygame.HIDDEN        window is opened in hidden mode
# screen = pygame.display.set_mode((1024,768))
screen = pygame.display.set_mode(SCREENSIZE)
# screen = pygame.display.set_mode(SCREENSIZE, vsync=1)
screen.convert_alpha()
dim_screen_cover = screen.convert_alpha()
dim_screen_cover.fill(BLACK)
dim_screen_cover.set_alpha(180)
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
sprites_reference = dict()
# avatars = pygame.image.load('img/avatars.png').convert_alpha()
items = pygame.image.load('img/items.png').convert_alpha()

# sprites['light halo casual'] = pygame.image.load('img/light_halo.png').convert_alpha()
# sprites['light halo strong'] = pygame.image.load('img/light_halo_strong.png').convert_alpha()
# sprites['light halo mild'] = pygame.image.load('img/light_halo_mild_spot.png').convert_alpha()
# sprites['light cone right'] = pygame.image.load('img/light_cone.png').convert_alpha()
# sprites['light cone left'] = pygame.transform.flip(sprites['light cone right'], True, False)
# sprites['light cone up'] = pygame.transform.rotate(sprites['light cone right'], 90)
# sprites['light cone down'] = pygame.transform.rotate(sprites['light cone right'], 270)
# sprites['light cone 45'] = pygame.image.load('img/light_cone_45.png').convert_alpha()
# sprites['light cone 135'] = pygame.transform.rotate(sprites['light cone 45'], 90)
# sprites['light cone 225'] = pygame.transform.rotate(sprites['light cone 45'], 180)
# sprites['light cone 315'] = pygame.transform.rotate(sprites['light cone 45'], 270)
# sprites['question sign'] = avatars.subsurface((573, 1053, 145, 240))
sprites['void'] = items.subsurface((0,0,10,10))
load_single_frame(items, ((0,0,20,30),), 'exp')

# ___...---=== JAKE ===---...___
name = 'Jake'
tmp_sprites = pygame.image.load('img/animations/jake_8bit.png').convert_alpha()
screen.convert_alpha(tmp_sprites)
load_single_frame(tmp_sprites, ((260,150,20,18),), name + ' avatar')
load_single_frame(tmp_sprites, ((260,150,20,18),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((2660,1720,90,50),), name + 'floor shadow mask')
# load_single_frame(tmp_sprites, ((1744,2194,332,205),), name + ' 98')  # Unconsciousness frame 1
# load_single_frame(tmp_sprites, ((2076,2220,369,176),), name + ' 99')  # Unconsciousness frame 2
load_all_frames(tmp_sprites, 97, name, 20, 30, 8)
# tmp_sprites = pygame.image.load('img/animations/jake.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((1744,2194,332,205),), name + ' 98')  # Unconsciousness frame 1
# load_single_frame(tmp_sprites, ((2076,2220,369,176),), name + ' 99')  # Unconsciousness frame 2
# load_all_frames(tmp_sprites, 20, name)
# print(sprites.keys())
#dict_keys(['question sign', 'Jake avatar', 'Jake avatar front', 'Jake 0', 'Jake 1', 'Jake 2', 'Jake 3', 'Jake 4', 'Jake 5', 'Jake 6', 'Jake 7', 'Jake 8', 'Jake 9', 'Jake 10', 'Jake 11', 'Jake 12', 'Jake 13', 'Jake 14', 'Jake 15', 'Jake 16', 'Jake 17', 'Jake 18', 'Jake 19', 'Jake 20', 'Jake 21', 'Jake 22', 'Jake 23', 'Jake 24', 'Jake 25', 'Jake 26', 'Jake 27', 'Jake 28', 'Jake 29', 'Jake 30', 'Jake 31', 'Jake 32', 'Jake 33', 'Jake 34', 'Jake 35', 'Jake 36', 'Jake 37', 'Jake 38', 'Jake 39', 'Jake 40', 'Jake 41', 'Jake 42', 'Jake 43'])
# print(sprites['Jake 0'])
# {'sprite': <Surface(90x210x32 SW)>, 'sprite center': 45, 'sprite asymmetric': False}
# exit()

# ___...---=== DEMON MALE 1 ===---...___
name = 'demon 1'
tmp_sprites = pygame.image.load('img/animations/jake_8bit.png').convert_alpha()
# tmp_sprites = pygame.image.load('img/animations/demon_male_1.png').convert_alpha()
load_single_frame(tmp_sprites, ((260,150,20,18),), name + ' avatar')
load_single_frame(tmp_sprites, ((260,150,20,18),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((2660,1720,90,50),), name + 'floor shadow mask')
load_all_frames(tmp_sprites, 97, name, 20, 30, 12)
# tmp_sprites = pygame.image.load('img/animations/demon_female_1.png').convert_alpha()
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar')
# load_single_frame(tmp_sprites, ((0, 1000, 300, 500),), name + ' avatar front')
# load_single_frame(tmp_sprites, ((1987,2245,459,150),), name + ' 99')  # Lay down
# load_all_frames(tmp_sprites, 8, name, 300, 500)

# sprites['void sprite'] = env.subsurface((0,1340,10,10))  #
# sprites['pinetree'] = env.subsurface((0,400,475,800))  #
# sprites['pile 1x #1'] = env.subsurface((0,0,94,199))  #
# sprites['glass 1x #1'] = env.subsurface((95,0,94,199))  #
# sprites['glass 1x #2'] = env.subsurface((190,0,94,199))  #
# sprites['box 1.5x #23'] = env.subsurface((380,0,94,199))  #
# sprites['box single'] = env.subsurface((285,0,94,199))  #
# sprites['coffee table'] = env.subsurface((475,0,94,199))  #
# sprites['metal crate #1 frame 0'] = env.subsurface((0,200,94,199))  #
# sprites['metal crate #2 frame 0'] = env.subsurface((95,200,94,199))  #
# sprites['wooden door #1 frame 0'] = env.subsurface((572,0,124,281))  # from NW to SE \
# sprites['wooden door #2 frame 0'] = pygame.transform.flip(sprites['wooden door #1 frame 0'], True, False)  # from SW to NE /
# sprites['light switch #1'] = env.subsurface((950,0,49,70))  # light switcher \
# sprites['light switch #2'] = pygame.transform.flip(sprites['light switch #1'], True, False)  # light switcher /
# sprites['shotgun'] = avatars.subsurface((4, 2923,367,56))  # shotgun image
# sprites['9mm_pistol'] = avatars.subsurface((382,2913,129,100))  # PM 9mm pistol image
# sprites['kitchen knife'] = avatars.subsurface((514,2918,216,100))  # PM 9mm pistol image

# cursors = pygame.image.load('img/cursors.png').convert_alpha()
# sprites['aim cursor'] = cursors.subsurface((0,0,51,51))
# sprites['walk cursor'] = cursors.subsurface((51,0,51,51))
# sprites['interact cursor'] = cursors.subsurface((102,0,51,51))
# sprites['ordinary cursor'] = cursors.subsurface((0,51,51,51))
# sprites['knife cursor'] = cursors.subsurface((51,51,51,51))
# sprites['fist cursor'] = cursors.subsurface((102,51,51,51))

all_obstacles = ('pile 1x #1', 'box 1.5x #23','box single',)

# screen.convert_alpha(avatars)
# screen.convert_alpha(env)
