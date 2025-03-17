from pygame.math import clamp
from consts import (
    CONSERVATIVE_ADVECTION,
    CONSERVATIVE_SCALAR,
    DT,
    GREEN,
    HEIGHT,
    PINK,
    RED,
    WHITE,
    WIDTH,
)
from mac import MacGrid
import numpy as np

from scalar import ScalarGrid
from ui import draw_circle, draw_line


def advect_velocities(grid: MacGrid):
    pre = np.sum(np.abs(grid.xgrid)) + np.sum(np.abs(grid.ygrid))
    xtemp = grid.xgrid.copy()

    ytemp = grid.ygrid.copy()
    for i in range(1, WIDTH):
        for j in range(HEIGHT):
            if (
                i < WIDTH - 1
                and i > 1
                and (grid.s[j + 1, i + 1] == 0 or grid.s[j + 1, i + 2] == 0)
            ):
                draw_circle((i + 1, j + 0.5), GREEN)

                print("x =, ", i, j)
                continue

            pos = np.array([i, j + 0.5])
            v = grid.interpolate_velocity(pos)
            new_pos = pos - v * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 0, HEIGHT)
            nv = grid.interpolate_velocity(new_pos)

            xtemp[j, i] = nv[0]
    for i in range(WIDTH):
        for j in range(1, HEIGHT):
            if (
                j < HEIGHT - 1
                and j > 1
                and (grid.s[j + 1, i + 1] == 0 or grid.s[j + 2, i + 1] == 0)
            ):
                draw_circle((i + 0.5, j + 1), RED)
                print("y =, ", i, j)
                continue

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
            if velocity_grid.s[j + 1, i + 1] == 0:
                continue

            pos = np.array([i + 0.5, j + 0.5])
            vel = velocity_grid.interpolate_velocity(pos)

            new_pos = pos - vel * DT
            new_pos[0] = clamp(new_pos[0], 0, WIDTH)
            new_pos[1] = clamp(new_pos[1], 0, HEIGHT)
            draw_line(pos, new_pos, WHITE, 3)

            nv = scalar_grid.interpolate_scalar(new_pos)

            ftemp[j, i] = nv
    scalar_grid.field = ftemp.copy()

    aft = np.sum(np.abs(scalar_grid.field))
    if CONSERVATIVE_SCALAR and aft:
        # print("diff = ", pre - aft)
        scalar_grid.field *= pre / aft
