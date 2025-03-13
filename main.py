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
density.field[2, 1] = 50
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


grid.xgrid[2, 1] = 3
while running:
    # screen.fill(BLACK)
    screen.fill(RED)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draw_cells()
    # grid.draw_mouse()
    density.draw()
    grid.draw_centers()

    # density.field[2, 1] = 50

    print(density.field)
    pygame.display.flip()
    time.sleep(DT)
    advect_scalar(density, grid)

    clear_divergence(grid)
    advect_velocities(grid)
