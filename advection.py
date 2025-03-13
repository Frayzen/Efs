from pygame.math import clamp
from consts import CONSERVATIVE_ADVECTION, CONSERVATIVE_SCALAR, DT, GREEN, HEIGHT, WIDTH
from mac import MacGrid
import numpy as np

from scalar import ScalarGrid
from ui import draw_line


def advect_velocities(grid: MacGrid):
    pre = np.sum(np.abs(grid.xgrid)) + np.sum(np.abs(grid.ygrid))
    xtemp = grid.xgrid.copy()

    ytemp = grid.ygrid.copy()
    for i in range(1, WIDTH):
        for j in range(HEIGHT):
            pos = np.array([i, j + 0.5])
            v = grid.interpolate_velocity(pos)
            new_pos = pos - v * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 0, HEIGHT)
            nv = grid.interpolate_velocity(new_pos)

            xtemp[j, i] = nv[0]
    for i in range(WIDTH):
        for j in range(1, HEIGHT):
            pos = np.array([i + 0.5, j])
            v = grid.interpolate_velocity(pos)
            new_pos = pos - v * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 0, HEIGHT)
            nv = grid.interpolate_velocity(new_pos)
            ytemp[j, i] = nv[1]
    grid.xgrid = xtemp.copy()
    grid.ygrid = ytemp.copy()

    if CONSERVATIVE_ADVECTION:
        aft = np.sum(np.abs(grid.xgrid)) + np.sum(np.abs(grid.ygrid))
        if aft > 0:
            grid.xgrid *= pre / aft
            grid.ygrid *= pre / aft


def advect_scalar(scalar_grid: ScalarGrid, velocity_grid: MacGrid):
    pre = np.sum(np.abs(scalar_grid.field))
    ftemp = scalar_grid.field

    for i in range(WIDTH):
        for j in range(HEIGHT):
            pos = np.array([i + 0.5, j + 0.5])
            vel = velocity_grid.interpolate_velocity(pos)

            new_pos = pos - vel * DT * 5
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 0, HEIGHT)
            nv = scalar_grid.interpolate_scalar(new_pos)

            ftemp[j, i] = nv
    scalar_grid.field = ftemp.copy()

    aft = np.sum(np.abs(scalar_grid.field))
    if CONSERVATIVE_SCALAR and aft:
        # print("diff = ", pre - aft)
        scalar_grid.field *= pre / aft
