from pygame.math import clamp

from const import *
from grid import *
from velocity import *


def interpolate_density(pos):
    x, y = pos[0], pos[1]
    # if x < 0 or x > GRID_WIDTH - 1 or y < 0 or y > GRID_HEIGHT - 1:
    #     return 0

    X, Y = clamp(int(x - 0.5), 0, GRID_WIDTH - 2), clamp(
        int(y - 0.5), 0, GRID_HEIGHT - 2
    )
    a = abs(x - X) - 0.5
    b = abs(y - Y) - 0.5
    c = 1 - a
    d = 1 - b
    return (
        density[Y, X] * c * d
        + density[Y + 1, X] * b * c
        + density[Y, X + 1] * a * d
        + density[Y + 1, X + 1] * a * b
    )


def update_density():

    global density
    d_cpy = density.copy()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = np.array([x + 0.5, y + 0.5])
            v = interpolate_velocity(pos)
            v[1] *= -1
            d_cpy[y, x] = interpolate_density(pos - v * 30 * dt)
    density = d_cpy
