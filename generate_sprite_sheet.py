# import pygame
from fonts import *

pygame.init()
maxx = 280
maxy = 360
cell_w = 20
cell_h = 30

surface = pygame.display.set_mode((maxx, maxy)).convert_alpha()

# surface = pygame.Surface((maxx, maxy)).convert_alpha()
surface.fill((255,0,255,255))

counter = 0
for dy in range(-1, maxy - cell_h, cell_h):
    for dx in range(-1, maxx - cell_w, cell_w):
        pygame.draw.line(surface, (0, 0, 0, 255), (dx,0), (dx,maxy))
        pygame.draw.line(surface, (0, 0, 0, 255), (0, dy), (maxx,dy))
        s = all_fonts[10].render(str(counter), False, (0, 0, 0, 255))
        sz = s.get_size()
        surface.blit(s, (dx + cell_w - sz[0], dy + cell_h - sz[1]))
        counter += 1

pygame.image.save(surface, 'img/gimp_originals/sprite_sheet_net.png')
