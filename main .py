# from termcolor import colored, cprint
from graphics import *
from world import *
# from constants import *
# from info_window import *
# from actors_description import*
# from load_content import *
# from locations import *
# from sound import *
# import fonts

# WORLD primary declaration.
world = World()

# world = World(screen)
world.get_screen(screen)
# world.info_windows = dict()
# world.info_windows_id = 0

# world.add_info_window(pygame.Rect(MAXX - INFO_WINDOW_WIDTH, MAXY, INFO_WINDOW_WIDTH, INFO_WINDOW_HEIGHT),
#                       ('This new game', 'has started...'))
# print(world.screen)
# world.sprites = sprites
# generate_maze()
# world.locations = locations

pygame.mouse.set_visible(False)
pygame.event.set_allowed([QUIT, KEYUP, KEYDOWN, MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

fades_speed = 100
# global locations

# TITLE SCREEN
# ---------------------------------------------------
# render_text('PROJECT ONE', world.screen, 90, WHITE, 'DSSTAIN1.TTF', ('center_y', 0), ('center_x', 0))
# black_in(world.screen, world.screen, fades_speed)
# render_text('PRESS ANY KEY', world.screen, 10, WHITE, 'default', ('center_y', MAXY - 50), ('center_x', 0))
# pygame.display.flip()
# world.press_any_key()
# black_out(world.screen, world.screen, 5)
# ---------------------------------------------------
world.location = 'default'
if world.location not in world.locations.keys():
    world.locations[world.location] = dict()
player = {
    'xy': (100, 0)
}
world.add_actor(player)


o = (((0, MAXY-50),(MAXX, 50)), ((0, MAXY_DIV_2+250), (200, 50)),
     ((300, MAXY_DIV_2), (200, 50)), ((MAXX_DIV_2, MAXY_DIV_2 + 150), (10, MAXY_DIV_2)),  ((0,0), (10, MAXY)))
for obs in o:
    world.add_obstacle({'xy': obs[0], 'dimensions': obs[1], 'is gravity affected': False})



def main():
    max_fps = 0
    # location = ('apartment_01_main_room', 172)
    # world.load_new_location['new location'] = location[0]

    while not world.is_quit:
        time_passed = clock.tick(FPS)
        world.game_cycles_counter += 1
        if world.game_cycles_counter > 1000:
            world.game_cycles_counter = 0

        # if world.load_new_location:
        #     print('[main] LOADING: ', world.load_new_location)
        #     # if world.location:
        #     black_out(world.screen, world.screen, fades_speed)
        #     world.location = world.load_new_location['new location']
        #
        #     load_content(world)
        #
        #     # while actors_to_add:
        #     #     player = actors_to_add.pop()
        #     #     world.add_wandering_actor(player[0], player[1], player[2])
        #     world.add_wandering_actor(player_jake, location[0], location[1])
        #
        #     world.player_id = world.player_actors[0]
        #
        #     busy_points = list()
        #     for key in world.wandering_actors.keys():
        #         if key in world.dead_actors:
        #             continue
        #         actor = world.wandering_actors[key]
        #
        #         # # Move all followers to neighbour free cells.
        #         if world.locations[world.location]['net']:
        #             if actor.new_point_on_map not in busy_points:
        #                 busy_points.append(actor.new_point_on_map)
        #             else:
        #                 possible_points = [p for p in world.locations[world.location]['points'][world.wandering_actor.new_point_on_map]['all neighbours']
        #                                        if world.locations[world.location]['points'][p]['default available']
        #                                           and p not in busy_points
        #                                           and p not in world.locations[world.location]['net settings']['points lead to other locations'].keys()
        #                                   ]
        #                 actor.new_point_on_map = choice(possible_points)
        #                 busy_points.append(actor.new_point_on_map)
        #
        #         if actor.new_location == world.location:
        #             world.apply_actor_to_map_settings(actor, actor.new_location)
        #             actor.calculate_self_indexes(locations[world.location]['points'])
        #             # actor.calculate_self_indexes(locations[world.location]['points per rect'])
        #             actor.reset_states()
        #         else:
        #             actor.calculate_self_indexes(locations[world.location]['points'])
        #             # actor.calculate_self_indexes(locations[world.location]['points per rect'])
        #
        #     world.get_all_actors_statistics(world.location)
        #     world.lights_generate_static_illumination()
        #     world.scaling_static_lights_image()
        #     world.point_mouse_cursor_shows = 0
        #     world.particles = dict()
        #     world.define_actors_row_by_initiative()
        #     if world.current_wandering_actor not in world.player_actors_in_current_location:
        #         world.current_wandering_actor = world.player_actors_in_current_location[0]
        #     world.wandering_actor = world.wandering_actors[world.current_wandering_actor]
        #
        #     world.set_follow_target_for_player_actors()
        #     world.instant_follow = True  # Positioning camera on current active actor.
        #
        #     world.process(time_passed) #!!
        #     world.wandering_follow_mode = ('scroll', 0, 0)
        #     # Set screen scroll offset following wandering actor position:
        #     world.wandering_scroll_counter_x = world.wandering_actor.rectangle.centerx * world.wandering_screen_scale
        #     world.wandering_scroll_counter_y = world.wandering_actor.rectangle.centery * world.wandering_screen_scale
        #
        #     black_in(world.screen, world.screen, fades_speed)
        #     world.load_new_location = None
        #     continue

        world.process(time_passed)
        fps = int(clock.get_fps())
        if fps > max_fps:
            max_fps = fps
        pygame.display.set_caption(str(fps) + ' ('+ str(max_fps) +')')  # + str(world.exec_time_))
        pygame.display.update()
        # world.press_any_key()


if __name__ == "__main__":
    main()

