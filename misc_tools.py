# import pygame
from math import sqrt, sin, cos, radians
# import copy

import os
import uuid
from numba import njit
from functools import reduce  # forward compatibility for Python 3
import operator
import fonts
from constants import *
@njit
def move_coordinates(angle, player_speed, time_passed):
    dx = sin(radians(angle)) * player_speed * time_passed
    dy = cos(radians(angle)) * player_speed * time_passed
    return dx, dy
# >>> from termcolor import colored,cprint
# >>> cprint('text', 'green', 'on_blue')
# text
# >>> cprint('text', 'green', 'on_red')
# text
# >>> help(cprint)
#
# >>> print(colored('Привет мир!', 'red', attrs=['underline']))
# Привет мир!
# >>> print(colored('Привет мир!', 'red', attrs=['underline','blink']))
# Привет мир!
# >>>

# def check_dot_inside_polygon(dot, polygon):
#     interceptions_quantity = 0
#     point_1 = polygon[0]
#     lines =
#     for point in polygon[1:]:
#         # w = s.walls[w]
#         # print(w)
#         # print(dot)
#         x1 = dot[0]
#         y1 = dot[1]
#         x2 = s.anchor[0]
#         y2 = s.anchor[1]
#         # x3 = w.x1
#         # y3 = w.y1
#         # x4 = w.x2
#         # y4 = w.y2
#         x3 = w['start'][0]
#         y3 = w['start'][1]
#         x4 = w['end'][0]
#         y4 = w['end'][1]
#
#         denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
#         if denominator == 0:
#             continue
#         t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
#         u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
#         if 1 > t > 0 and 1 > u > 0:
#             # interception_x = x1 + t * (x2 - x1)
#             # interception_y = y1 + t * (y2 - y1)
#             interceptions_quantity += 1
#             # current_ray_interceptions.append((int(interception_x), int(interception_y), w))
#         else:
#             # There is no interception
#             pass
#
#     # если количество точек пересечения луча со стенами сектора, проведённого из проверяемой точки до "якоря",
#     # равно нулю или чётно, то точка находится внутри сектора. Если же это количество нечётное, то точка
#     # находится за пределами сектора.
#     if interceptions_quantity == 0 or (interceptions_quantity % 2 == 0):
#         # print('INSIDE. Interceptions: ', interceptions_quantity)
#         return True
#     else:
#         # print('Outside. Interceptions: ', interceptions_quantity)
#         return False

@njit
def check_lines_intersection(line1, line2):
    x1 = line1[0][0]
    y1 = line1[0][1]
    x2 = line1[1][0]
    y2 = line1[1][1]
    x3 = line2[0][0]
    y3 = line2[0][1]
    x4 = line2[1][0]
    y4 = line2[1][1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        # There is no interception
        return False
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
    if 1 > t > 0 and 1 > u > 0:
        return True
    else:
        # There is no interception
        return False

# def get_from_dict(data_dict, map_list):
#     return reduce(operator.getitem, map_list, data_dict)
#
# def set_in_dict(data_dict, map_list, value):
#     get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value

def copy_screen_as_surface(self):
    x = pygame.image.tostring(self.screen, "RGBA")
    return pygame.image.fromstring(x, self.screen.get_size(), "RGBA")

def copy_surface_as_surface(surface):
    x = pygame.image.tostring(surface, "RGBA")
    return pygame.image.fromstring(x, surface.get_size(), "RGBA")

def create_uuid():
    return uuid.uuid1()

def black_out(image, surface, velocity=12):
    # ''' процедура постепенно затемняет переданное ей изображение.
    #     velocity -- скорость данного процесса. '''
    x = pygame.image.tostring(image, "RGBA")
    scr = pygame.image.fromstring(x, image.get_size(), "RGBA")
    x = pygame.image.tostring(image, "RGBA")
    black = pygame.image.fromstring(x, image.get_size(), "RGBA")
    for x in range(0, 255, velocity):
        black.fill(pygame.Color(0, 0, 0, x))
        # self.screen.blit(scr, (0, 0))
        # self.screen.blit(black, (0, 0))
        surface.blit(scr, (0, 0))
        surface.blit(black, (0, 0))
        pygame.display.update()

def render_text(text, screen, font_size, font_color, font_name, *alignment):
# def render_text(text, screen, xy, font_size, font_color, *alignment):
    if font_name != 'default':
        s = pygame.font.Font("./fonts/" + font_name, font_size).render(text, True, font_color)
        txt_sz = s.get_size()
    else:
        s = fonts.all_fonts[font_size].render(text, True, font_color)
        txt_sz = s.get_size()

    text_xy = [0, 0]
    if alignment:
        print(f'[game over] {alignment=}')
        # text_xy = [0, 0]
        for align in alignment:
            # align[0] - description pf text alignment (center, stick left side, stick to the right etc.)
            # align[1] - how many pixels does text offsets from the alignment point.
            if type(align) == tuple:
                text_xy = (int(align[0]), int(align[1]))
                break
            if align == 'center_x':
                text_xy[0] = MAXX_DIV_2 - txt_sz[0] // 2  # + align[1]
            elif align == 'center_y':
                text_xy[1] = MAXY_DIV_2 - txt_sz[1] // 2  # + align[1]
            elif align == '1/4_x':
                text_xy[0] = MAXX_DIV_2 // 4 - txt_sz[0] // 2
            elif align == '1/4_y':
                text_xy[1] = MAXY_DIV_2 // 4 - txt_sz[1] // 2
            elif align == '3/4_x':
                text_xy[0] = MAXX // 4 * 3 - txt_sz[0] // 2
            elif align == '3/4_y':
                text_xy[1] = MAXY // 4 * 3 - txt_sz[1] // 2


    screen.blit(s, text_xy)
    # pygame.display.flip()

def find_destination_behind_target_point(start_point, end_point, vector_length):
    #                o C  [Destination behind end point]
    #               /   ˥
    #              /     ↦ [Vector length] c2
    #             /     ˩
    #      [End] o B
    #           /|
    #       c1 / |
    #         /  | b1
    #[Start] /___|
    #     A o  a1
    a1 = start_point[0] - end_point[0]
    b1 = start_point[1] - end_point[1]
    c1 = max(1.0, sqrt(a1*a1 + b1*b1))  # Prevent zero division errors.
    a2 = a1*vector_length/c1
    b2 = b1*vector_length/c1
    # print(f'{start_point=} {end_point=} {vector_length=}')
    # print('Splatter destination:', end_point[0] - a2, end_point[1] - b2)
    return end_point[0] - a2, end_point[1] - b2

def black_in(image, surface, velocity=12):
    # ''' процедура постепенно проявляет переданное ей изображение.
    #     velocity -- скорость данного процесса. '''
    x = pygame.image.tostring(image, "RGBA")
    scr = pygame.image.fromstring(x, image.get_size(), "RGBA")
    x = pygame.image.tostring(image, "RGBA")
    black = pygame.image.fromstring(x, image.get_size(), "RGBA")
    for x in range(255, 0, -velocity):
        # self.screen.blit(scr, (0, 0))
        surface.blit(scr, (0, 0))
        black.fill(pygame.Color(0, 0, 0, x))
        # self.screen.blit(black, (0, 0))
        surface.blit(black, (0, 0))
        pygame.display.update()

def dissolve(image, surface, velocity=12):
    tmp = pygame.image.tostring(image, "RGBA")
    scr = pygame.image.fromstring(tmp, image.get_size(), "RGBA")
    tmp = pygame.image.tostring(image, "RGBA")
    black = pygame.image.fromstring(tmp, image.get_size(), "RGBA")
    for x in range(255, 0, -velocity):
        surface.blit(scr, (0, 0))
        black.fill(pygame.Color(0, 0, 0, x))
        surface.blit(black, (0, 0))

# @staticmethod
@njit(cache=True)
def get_distance_to(start, end, simplified=False):
    """Returns the distance to a point.
    @param: A Vector2 or list-like object with at least 2 values.
    @return: distance
    """
    x, y = start
    xx, yy = end
    dx = xx-x
    dy = yy-y
    if not simplified:
        return sqrt(dx*dx + dy*dy)
    else:
        return dx * dx + dy * dy


def magnitude(source_point, dest_point):
    """ This function is more simpler and because of that it's faster, but it is not define direct distance, just a sum of differences.
    Этот метод определения расстояния от точки до точки не использует квадратные корни, выдвёт неправильный с точки зрения
    координат мира результат, но при множестве подобных друг другу замеров позволяет просто узнать, какая из множества точек
    находится ближе к месту назаначения, а какие -- дальше. """
    return abs(dest_point[0] - source_point[0]) + abs(dest_point[1] - source_point[1])


def clear():
    os.system('clear')

# @njit(cache=True)
# @njit
def pathfinder(map_, source, destination):
    def l_magnitude(source_point, dest_point):
        return abs(dest_point[0] - source_point[0]) + abs(dest_point[1] - source_point[1])
    diagonal_walk = False
    # diagonal_walk = True
    # def magnitude(source_point, dest_point):
    #     """ This function is more simpler and because of that it's faster, but it is not define direct distance, just a sum of differences.
    #     Этот метод определения расстояния от точки до точки не использует квадратные корни, выдвёт неправильный с точки зрения
    #     координат мира результат, но при множестве подобных друг другу замеров позволяет просто узнать, какая из множества точек
    #     находится ближе к месту назаначения, а какие -- дальше. """
    #     return abs(dest_point[0] - source_point[0]) + abs(dest_point[1] - source_point[1])
    # def print_map(map_list_of_strings, *list_of_dots):
    #     # 'X' is any dot on the map: start point, destination point, route nodes etc.
    #     ##############
    #     ##############
    #     ##############
    #     ########.#####
    #     ########..####
    #     ####.###...###
    #     ####.....X.###
    #     ####.......###
    #     ####X......###
    #     ##############
    #     inner_map_copy = map_list_of_strings[:]
    #     for dot in list_of_dots:
    #         print(f'{dot=}')
    #         l = inner_map_copy[dot[1]]
    #         l = l[:dot[0]] + 'X' + l[dot[0]+1:]
    #         inner_map_copy[dot[1]] = l
    #     for line in inner_map_copy:
    #         print(line)

    # print('\nEnter pathfinder...')
    # print(f'Source: {source} \nDestination: {destination}')

    # print_map(map_, source, destination)
    # clear()
    # exit()

    open_list = dict()
    closed_list = dict()
    distance = l_magnitude(source, destination)
    # print('distance: ', distance)
    # map_copy = copy.deepcopy(map_)
    map_copy = map_.copy()
    # map_copy = map_[:]
    destination_is_busy = False
    if map_[destination[1]][destination[0]] == 1:
    # if map_[destination[1]][destination[0]] == 'x':
        # Destination point is occupied with one of the actors. To let pathfinder algorythm work, we need to cheat with it and
        # pretend that this point is free and create a memo about this fact...
        destination_is_busy = True
        map_copy[destination[1]][destination[0]] = 0
        # map_copy[destination[1]] = map_copy[destination[1]][:destination[0]] + '.' + map_copy[destination[1]][destination[0]+1:]
    marker_position = source
    parent = source
    parent_cost = 0
    cost = 0
    route = []
    route_tmp = []
    previous_marker = marker_position
    # previous_marker = []
    # route_tmp.append(marker_position)
    # route.append(marker_position)

    # string = str(marker_position[0]) + '-' + str(marker_position[1])  # Temporary string for 'list' to 'string' converting.

    open_list[marker_position] = {
        'marker position': marker_position,
        'parent': parent,
        'parent cost': parent_cost,
        'distance': distance,
        'cost': cost
    }

    while marker_position != destination:
        # breaking_flag = False
        previous_marker = marker_position
        # cost = 0
        # string = str(marker_position[0]) + '-' + str(marker_position[1])
        closed_list[marker_position] = open_list[marker_position]
        del(open_list[marker_position])
        # for i in map_copy:
        #     print(i)
        # print(marker_position)
        # input('press any key...')
        # map_copy[marker_position[1]][marker_position[0]] = 'c'
        map_copy[marker_position[1]][marker_position[0]] = 3
        # map_copy[marker_position[1]] = map_copy[marker_position[1]][:marker_position[0]] + 'c' + map_copy[marker_position[1]][(marker_position[0] + 1):]
        parent_cost = closed_list[marker_position]['cost']

        open_list_candidates = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue
                open_list_candidates.add((dx, dy))
        # print('Before: ', open_list_candidates)


        blocked_cells = set()
        for candidate in open_list_candidates:
            dx = candidate[0]
            dy = candidate[1]
            try:
                block = map_copy[marker_position[1] + dy][marker_position[0] + dx]
            except IndexError:
                for line in map_copy:
                    print(line)
                # print(f'ERROR: {marker_position=}')
                continue
            if dx == 0 and block != 0:
            # if dx == 0 and block != '.':
                blocked_cells.add((dx, dy))
                if not diagonal_walk:
                    blocked_cells.add((dx - 1, dy))
                    blocked_cells.add((dx + 1, dy))
            elif dy == 0 and block != 0:
            # elif dy == 0 and block != '.':
                blocked_cells.add((dx, dy))
                if not diagonal_walk:
                    blocked_cells.add((dx, dy + 1))
                    blocked_cells.add((dx, dy - 1))
            elif block != 0:
            # elif block != '.':
                blocked_cells.add((dx, dy))

        # print(blocked_cells)
        # print(set(blocked_cells))
        # blocked_cells = set(blocked_cells)
        open_list_candidates = open_list_candidates - blocked_cells
        # print('After: ', open_list_candidates)
        # for m in map_copy:
        #     print(m)
        #
        # exit()

        # for dx in range(-1, 2):
        #     for dy in range(-1, 2):
        for candidate in open_list_candidates:
            dx = candidate[0]
            dy = candidate[1]
            marker_pos_shattered_x = marker_position[0] + dx
            marker_pos_shattered_y = marker_position[1] + dy
            shattered_marker_pos = (marker_pos_shattered_x, marker_pos_shattered_y)
            block = map_copy[marker_pos_shattered_y][marker_pos_shattered_x]

            if block == 0 and shattered_marker_pos not in open_list.keys():
            # if block == '.' and shattered_marker_pos not in open_list.keys():
                # Блок проходимый и пока не включён в открытый список.
                # Marking parent for current point.
                parent = marker_position

                # Calculating movement cost from the parent point to the current.
                if (abs(dx)) + (abs(dy)) == 2:
                    cost = 14 + parent_cost
                else:
                    cost = 10 + parent_cost

                # Calculating distance from the current point to the finish.
                distance = l_magnitude(shattered_marker_pos, destination) * 10
                # Включаем блок в открытый список:
                open_list[shattered_marker_pos] = {
                    'marker position': shattered_marker_pos,
                    'parent': parent,
                    'parent cost': parent_cost,
                    'distance': distance,
                    'cost': cost
                }
                # map_copy[marker_position[1] - dy][marker_position[0] - dx] = 'O'
                # map_copy[marker_position[1] - dy] = map_copy[marker_position[1] - dy][:marker_position[0] - dx] + 'O' + map_copy[marker_position[1] - dy][(marker_position[0] - dx + 1):]
            elif shattered_marker_pos in open_list.keys():
                # Блок уже включён в открытый список.
                # string = str(marker_position[0] - dx) + '-' + str(marker_position[1] - dy)
                # string_for_marker = str(marker_position[0]) + '-' + str(marker_position[1])
                # tmp_ = open_list[string]

                # Checking if the route through the marker point to the current point is lesser than existing.
                if (abs(dx)) + (abs(dy)) == 2:
                    tmp_cost = 14
                else:
                    tmp_cost = 10

                if (open_list[shattered_marker_pos]['cost']) > (closed_list[marker_position]['cost'] + tmp_cost):
                    # del(open_list[shattered_marker_pos])
                    open_list[shattered_marker_pos] = {
                        'marker position': open_list[shattered_marker_pos]['marker position'],
                        'parent': closed_list[marker_position]['marker position'],
                        'parent cost': closed_list[marker_position]['cost'],
                        'distance': open_list[shattered_marker_pos]['distance'],
                        'cost': closed_list[marker_position]['cost'] + tmp_cost
                    }
            else:
                continue

        min_total_cost = 10000000
        min_point_number = ''

        for i in open_list.keys():
            if min_total_cost > (open_list[i]['distance'] + open_list[i]['cost']):
                min_total_cost = (open_list[i]['distance'] + open_list[i]['cost'])
                min_point_number = i

        try:
            marker_position = open_list[min_point_number]['marker position']
        except KeyError:
            # print("Path blocked.")
            # print('No way from ', source, ' to ', destination)
            # return False
            return None

    # BUILD THE ROUTE within the closed points list.
    # print(f'{closed_list=}')
    while previous_marker != source:
        # route_tmp.append([closed_list[previous_marker]['marker position'][0] + 1, closed_list[previous_marker]['marker position'][1] + 1])
        route_tmp.append([closed_list[previous_marker]['marker position'][0], closed_list[previous_marker]['marker position'][1]])
        previous_marker = closed_list[previous_marker]['parent']
    # print(f'{route_tmp=}')

    # In case of too short route:
    if len(route_tmp) <= 0:
        if not destination_is_busy:
            # Just simply step into a neighbour cell.
            return destination, source
        else:
            # Neighbour cell is busy:
            return None

    if not destination_is_busy:
        route_tmp.insert(0, (destination[0], destination[1]))

    # # Следующий блок кода призван уменьшить количество точек в маршруте, убрав из него те, которые не являются поворотными, а лежат на прямой по ходу движения.
    # need_to_simplify_route = False
    # if need_to_simplify_route:
    #     candidate = route_tmp[-1]  # Точка-кандидат на добавление в маршрут
    #     prev_dx = 0
    #     prev_dy = 0
    #     route.append(source)
    #     for i in reversed(route_tmp):
    #         dx = i[0] - candidate[0]
    #         dy = i[1] - candidate[1]
    #         if dx == prev_dx and dy == prev_dy:
    #             # Если изменений в направлении движения по сравнению с предыдущим кандидатом не наблюдается, то предыдущего кандидата игнорируем,
    #             # и новым кандидатом начинаем считать текущую точку.
    #             candidate = i
    #         else:
    #             # Произошло изменение направления движения в какую-либо сторону (неважно, в какую).
    #             # Значит, предыдущий кандидат является узловой точкой, добавляется в маршрут, а текущая точка назначается новым кандидатом.
    #             route.append(candidate)
    #             candidate = i
    #             prev_dx = dx
    #             prev_dy = dy
    #     route.append(candidate)  # Последняя точка не добавится в маршрут, если она лежит на прямой с предыдущей. Придётся сделать это вручную.
    # print(f'{route=}')

    return route_tmp
    # return route[::-1]
