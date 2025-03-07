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

# x_mac[GRID_HEIGHT // 2, GRID_WIDTH // 2] = -3
# x_mac[GRID_HEIGHT // 2 + 1, GRID_WIDTH // 2] = 3
# y_mac[GRID_HEIGHT // 2, GRID_WIDTH // 2] = 3
# y_mac[GRID_HEIGHT // 2 + 1, GRID_WIDTH // 2] = -3
# x_mac[1, 1] = 8
v = 100
x_mac[1, 1] = v
# x_mac[2, 2] = v
# y_mac[2, 0] = -v
# y_mac[1, 2] = v
# y_mac[1, 1] = 3
# y_mac[2, 1] = -3


# density_grid[1, 1] = 500
# density[GRID_HEIGHT // 2 + 1, GRID_WIDTH // 4] = 50000
step = False

y_mac[GRID_HEIGHT // 2, GRID_WIDTH // 2] = 1000
dt = 1 / max(np.max(y_mac), np.max(x_mac))
while running:
    screen.fill([255] * 3)
    draw_grid(density_grid)
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    vel = interpolate_velocity(pos)
    # vel[1] *= -1  # because vector is in cartesion but pygame is upside down
    # pygame.draw.line(
    #     screen, (0, 255, 0), pos * CELL_SIZE, pos * CELL_SIZE + vel * dt * CELL_SIZE, 2
    # )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # density[:, -1] = 0

    # else:
    #     w_grid[GRID_HEIGHT // 2, 0] -= 5
    #     w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    # for i in range(3):
    # y_mac[GRID_HEIGHT // 2, GRID_WIDTH // 2] = 1000
    clear_divergence()
    # draw_vel_no_interp()
    advect()
    draw_vel_cell()

    # print(density_grid)
    # print(density_grid.sum())
    # print("=====")
    density_grid = update_density(density_grid)

    # print(density_grid)
    # print("DEN IS ", density_grid)
    # input("HEY")
    # time.sleep(dt * 10)

    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        density_grid[:, :] = 0
        density_grid[1, 1] = 2000
        step = True
        # x_mac[:, :] = 0
        # y_mac[:, :] = 0

        # x_mac[GRID_HEIGHT // 2, 8] = 3000
        # y_mac[GRID_HEIGHT // 2, 8] = 3000
        # y_mac[GRID_HEIGHT // 2 + 1, 8] = -3000

        # density[GRID_HEIGHT // 2, 4] = 50000
        # density[GRID_HEIGHT // 2 + 1, 4] = 50000
    # if step:
    #     input("test")


pygame.quit()
