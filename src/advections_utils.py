from pygame.math import clamp
from consts import (
    DT,
    HEIGHT,
    WIDTH,
)
from mac import MacGrid
import numpy as np

from scalar import ScalarGrid
from ui import draw_circle, draw_line

def velocity_advection_mzero(pos, grid: MacGrid):
    if not grid.in_bounds(pos):
        return np.array([0.0, 0.0])
    
    i, j = int(pos[0]), int(pos[1])
    if grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        return np.array([0.0, 0.0])

    return grid.interpolate_velocity(pos)

def velocity_advection_mclamp(pos, grid: MacGrid):
    i, j = int(pos[0]), int(pos[1])
    if not grid.in_bounds(pos) or grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        for dj in [-1, 0, 1]:
            for di in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < WIDTH and 0 <= nj < HEIGHT:
                    if grid.s[nj + 1, ni + 1] != 0:
                        pos = np.array([ni + 0.5, nj + 0.5])
                        return grid.interpolate_velocity(pos)
        return np.array([0.0, 0.0])
    return grid.interpolate_velocity(pos)


def compute_wall_normal(i, j, s):
    dx = float(s[j + 1, i + 2]) - float(s[j + 1, i])
    dy = float(s[j + 2, i + 1]) - float(s[j, i + 1])
    n = np.array([dx, dy])
    norm = np.linalg.norm(n)
    return n / norm if norm > 1e-5 else np.array([0.0, 0.0])


def velocity_advection_mref(pos, grid: MacGrid):
    i, j = int(pos[0]), int(pos[1])
    if not grid.in_bounds(pos) or grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        v = grid.interpolate_velocity(pos)
        normal = compute_wall_normal(i, j, grid.s)
        v = v - 2 * np.dot(v, normal) * normal
        new_pos = pos - v * DT
        return grid.interpolate_velocity(new_pos)
    return grid.interpolate_velocity(pos)





def scalar_advection_mzero(pos, velocity_grid: MacGrid, scalar_grid: ScalarGrid):
    if not velocity_grid.in_bounds(pos):
        return 0.0
    i, j = int(pos[0]), int(pos[1])
    if velocity_grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        return 0.0
    return scalar_grid.interpolate_scalar(pos)


def scalar_advection_mclamp(pos, velocity_grid: MacGrid, scalar_grid: ScalarGrid):
    i, j = int(pos[0]), int(pos[1])
    if not velocity_grid.in_bounds(pos) or velocity_grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        for dj in [-1, 0, 1]:
            for di in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < WIDTH and 0 <= nj < HEIGHT:
                    if velocity_grid.s[nj + 1, ni + 1] != 0:
                        pos = np.array([ni + 0.5, nj + 0.5])
                        return scalar_grid.interpolate_scalar(pos)
        return 0.0
    return scalar_grid.interpolate_scalar(pos)

def scalar_advection_mref(pos, velocity_grid: MacGrid, scalar_grid: ScalarGrid):
    i, j = int(pos[0]), int(pos[1])
    if not velocity_grid.in_bounds(pos) or velocity_grid.s[min(j + 1, HEIGHT), min(i + 1, WIDTH)] == 0:
        vel = velocity_grid.interpolate_velocity(pos)
        normal = compute_wall_normal(i, j, velocity_grid.s)
        vel = vel - 2 * np.dot(vel, normal) * normal
        new_pos = pos - vel * DT
        return scalar_grid.interpolate_scalar(new_pos)
    return scalar_grid.interpolate_scalar(pos)


