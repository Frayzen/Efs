from pygame.math import clamp
from consts import DT, HEIGHT, WIDTH
from mac import MacGrid
import numpy as np


def advect(grid: MacGrid):
    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT):
            pos = np.array([i, j + 0.5])
            v = grid.interpolate_velocity(pos)
            new_pos = pos - v * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 1, HEIGHT)
            nv = grid.interpolate_velocity(new_pos)
            grid.xgrid[i, j] = nv[0]
    for i in range(1, WIDTH):
        for j in range(1, HEIGHT - 1):
            pos = np.array([i + 0.5, j])
            v = grid.interpolate_velocity(pos)
            new_pos = pos - v * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 1, HEIGHT)
            nv = grid.interpolate_velocity(new_pos)
            grid.ygrid[i, j] = nv[1]
