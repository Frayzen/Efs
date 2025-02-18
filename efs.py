from sys import get_coroutine_origin_tracking_depth
import pygame
import time
import numpy as np
from pygame.math import clamp
from const import *
from grid import *
from ui import *
from density import *
from divergence import *
from velocity import *


dampening = 1


# Main loop
running = True

x_grid[GRID_HEIGHT // 2, 8] = 3000
y_grid[GRID_HEIGHT // 2, 8] = 3000
y_grid[GRID_HEIGHT // 2 + 1, 8] = -3000

density[GRID_HEIGHT // 2, 4] = 50000
density[GRID_HEIGHT // 2 + 1, 4] = 50000

while running:
    # screen.fill()
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    vel = intervel(pos)
    vel[1] *= -1  # because vector is in cartesion but pygame is upside down
    pygame.draw.line(
        screen, (0, 255, 0), pos * CELL_SIZE, pos * CELL_SIZE + vel * dt * CELL_SIZE, 2
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # density[:, -1] = 0
    print(np.sum(density))

    # else:
    #     w_grid[GRID_HEIGHT // 2, 0] -= 5
    #     w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    clear_divergence()
    draw_vel()

    pygame.display.flip()

    advect()
    update_density()
    # time.sleep(dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        density[:, :] = 0
        x_grid[:, :] = 0
        y_grid[:, :] = 0

        x_grid[GRID_HEIGHT // 2, 8] = 3000
        y_grid[GRID_HEIGHT // 2, 8] = 3000
        y_grid[GRID_HEIGHT // 2 + 1, 8] = -3000

        density[GRID_HEIGHT // 2, 4] = 50000
        density[GRID_HEIGHT // 2 + 1, 4] = 50000


pygame.quit()
