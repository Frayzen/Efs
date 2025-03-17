import pygame

import pygame
import time
import numpy as np
from pygame.math import clamp
from advection import advect_scalar, advect_velocities
from divergence import clear_divergence
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
step = False


def set_obstacle(x, y):
    grid.s[y + 1, x + 1] = 0
    grid.xgrid[y, x] = 0
    grid.xgrid[y, x + 1] = 0
    grid.ygrid[y, x] = 0
    grid.ygrid[y + 1, x] = 0
    density.field[y, x] = 0


# set_obstacle(4, 8)
# set_obstacle(5, 8)
# set_obstacle(6, 8)
# set_obstacle(6, 8)
# set_obstacle(7, 8)
# set_obstacle(7, 9)
# set_obstacle(7, 10)
# set_obstacle(7, 11)
# set_obstacle(7, 12)
# set_obstacle(6, 12)
# set_obstacle(5, 12)
# set_obstacle(4, 12)


while running:
    grid.xgrid[:, 0] = v
    grid.xgrid[:, -1] = v
    density.field[HEIGHT // 2, 0] = 3000
    # density.field[:, -1] = 0
    # grid.ygrid[:, ::2] = -0.7
    # grid.ygrid[1:, 1::2] = 0.7
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_cells()
    # grid.draw_s()
    density.draw()

    grid.draw_s()
    # grid.draw()
    # grid.draw_centers()
    grid.draw_mouse()
    # density.draw_mouse()
    keys = pygame.key.get_pressed()

    clear_divergence(grid)
    advect_velocities(grid)
    advect_scalar(density, grid)

    prev = keys[pygame.K_SPACE]

    if keys[pygame.K_SPACE]:
        density.field[HEIGHT // 2, 0] = 500
        # step = True
    if pygame.mouse.get_pressed()[0]:
        x, y = get_mouse_coords_int()
        set_obstacle(x, y)
    if step:
        input("test")
    # print(
    #     "density = ",
    #     np.sum(density.field),
    #     # "\n",
    #     # "y = ",
    #     # np.round(grid.ygrid, 2),
    #     # "\n",
    #     # "y = ",
    #     # np.round(grid.ygrid, 2),
    # )
    # input("test")
    # time.sleep(1)
    # print(grid.xgrid[HEIGHT // 2, -1])

    # density.field[2, 1] = 50

    pygame.display.flip()
    time.sleep(DT)
