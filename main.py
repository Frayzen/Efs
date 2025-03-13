import pygame

import pygame
import time
import numpy as np
from pygame.math import clamp
from advection import advect_scalar, advect_velocities
from divergence import clear_divergence
from mac import MacGrid
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
                i * CELL_SIZE,
                j * CELL_SIZE,
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


v = 20
grid.xgrid[1, 1] = v
grid.ygrid[-2, 1] = -v
grid.ygrid[1, -2] = v
grid.xgrid[-2, -2] = -v

density.field[1, 1] = 80
# density.field[-2, 1] = 80
# density.field[1, -2] = 80
density.field[-2, -2] = 80


prev = False
cur = 0
while running:
    screen.fill(RED)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_cells()
    grid.draw_mouse()
    density.draw()

    # print(np.round(density.field, 2))
    grid.draw_centers()
    # density.draw_mouse()
    keys = pygame.key.get_pressed()
    clear_divergence(grid)
    advect_velocities(grid)
    # if keys[pygame.K_SPACE] and not prev:
    #     if cur == 0:
    #         print("DIV")
    #         cur = 1
    #     else:
    #         print("ADV")
    #         cur = 0
    advect_scalar(density, grid)
    prev = keys[pygame.K_SPACE]

    # density.field[2, 1] = 50

    pygame.display.flip()
    time.sleep(DT)
