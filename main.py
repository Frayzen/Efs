import pygame

import pygame
import time
import numpy as np
from pygame.math import clamp
from advection import advect
from divergence import clear_divergence
from mac import MacGrid
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
# grid.ygrid[0, 1] = -0.75
# grid.ygrid[-1, 1] = -0.25
# grid.ygrid[-1, 2] = -0.5
# grid.ygrid[1, 1] = -0.5

# grid.ygrid[3, 2] = -0.7
# grid.ygrid[3, 0] = -0.7
# grid.ygrid[3, 1] = -0.25

# grid.xgrid[2, 3] = -0.7
# grid.xgrid[0, 3] = -0.7
grid.xgrid[1, 3] = -0.25


# grid.xgrid[-1, 1] = 0.7
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_cells()
    grid.draw()
    grid.draw_mouse()
    pygame.display.flip()
    # time.sleep(DT)
    input("step")

    clear_divergence(grid)
    advect(grid)
