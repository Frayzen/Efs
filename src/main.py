import pygame

import pygame
import time
import numpy as np
from pygame.math import clamp
from advection import advect_scalar, advect_velocities
from divergence import clear_divergence
from draw import draw_ui
from mac import MacGrid, get_mouse_coords_int
from scalar import ScalarGrid
from ui import screen

from consts import (
    BLACK,
    CELL_SIZE,
    DT,
    HEIGHT,
    PIX_HEIGHT,
    PIX_WIDTH,
    RED,
    WHITE,
    WIDTH,
)


def get_mouse_coords():
    return np.array(pygame.mouse.get_pos()) // CELL_SIZE


def draw_cells():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            rect = (
                j * CELL_SIZE,
                i * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, WHITE, rect, 1)


running = True
grid = MacGrid()
density = ScalarGrid()
# density.field[1, 2] = 7
# density.field[0, 2] = 3
# density.field[1, 0] = 3
# grid.ygrid[0, 1] = -0.75
# grid.ygrid[-1, 1] = -0.25
# grid.ygrid[-1, 2] = -0.5
# grid.ygrid[1, 1] = -0.5

# grid.ygrid[3, 2] = -0.7
# grid.ygrid[3, 0] = -0.7
# grid.ygrid[3, 1] = -0.25

# grid.xgrid[2, 3] = -0.7
# grid.xgrid[0, 3] = -0.7
# grid.xgrid[0, 2] = 3
# grid.xgrid[0, 1] = -3
# grid.xgrid[-1, 3] = 5


# grid.xgrid[1, 1] = v
# grid.ygrid[-2, 1] = -v
# grid.ygrid[1, -2] = v
# grid.xgrid[-2, -2] = -v

# density.field[1, 1] = 80
# density.field[-2, 1] = 80
# density.field[1, -2] = 80
# density.field[-2, -2] = 80


prev = False
cur = 0
# grid.s[:, -1] = 1
# grid.s[:, 0] = 1
v = 3
# density.field[HEIGHT // 2, 0] = 500
# x, y = 3, HEIGHT // 2
# grid.s[y + 1, x + 1] = 0
# grid.xgrid[y, x] = 0
# grid.xgrid[y, x + 1] = 0
# grid.ygrid[y, x] = 0
# grid.ygrid[y + 1, x] = 0
# density.field[y, x] = 0
to_wall = False


def set_obstacle(x, y, to_wall):
    grid.s[y + 1, x + 1] = 1 if to_wall else 0
    grid.xgrid[y, x] = 0
    grid.xgrid[y, x + 1] = 0
    grid.ygrid[y, x] = 0
    grid.ygrid[y + 1, x] = 0
    density.field[y, x] = 0


def check_sym(m):
    h, w = m.shape
    res = np.zeros(shape=(h // 2, w))
    for j in range(0, h // 2):
        for i in range(0, w):
            res[j, i] = np.abs(m[j, i] - m[h // 2 - j, i])
    res = np.round(res, 4).max(axis=1)
    print("sim = ", res.max().max())
    return res

def arrow_wall():
    set_obstacle(WIDTH // 2  , HEIGHT // 2, True)
    cur = 4
    for i in range(3):
        # if i % 2 == 0:
        cur += 2
        set_obstacle(WIDTH // 2 + cur - 4, HEIGHT // 2+ i, False)
        set_obstacle(WIDTH // 2  + cur- 4, HEIGHT // 2- i, False)


pause = False
while running:
    # set_obstacle(WIDTH -3, HEIGHT // 2, False)

    if not pause:
        grid.xgrid[:, 0] = v
        grid.xgrid[:, -1] = v
    density.field[HEIGHT // 2 -1, 0 ] = 225
    density.field[HEIGHT // 2, 0 ] = 225
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    density.draw()
    grid.draw_s()

    grid.draw_centers()
    grid.draw_mouse()
    draw_ui(screen)
    # density.draw_mouse()
    keys = pygame.key.get_pressed()
    if not pause:
        advect_velocities(grid)
        advect_scalar(density, grid)
        clear_divergence(grid)

    prev = keys[pygame.K_SPACE]

    if keys[pygame.K_p]:
        time.sleep(0.4)
        pause = not pause
        time.sleep(0.4)
    if keys[pygame.K_SPACE]:
        to_wall = not to_wall
    if pygame.mouse.get_pressed()[0]:
        x, y = get_mouse_coords_int()
        set_obstacle(x, y, to_wall)
    # check_sym(grid.ygrid)

    pygame.display.flip()
    time.sleep(DT)
    # input()

