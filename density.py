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
            if (
                sy[y, x] == 0
                and sy[y + 1, x] == 0
                and sx[y, x] == 0
                and sx[y, x + 1] == 0
            ):
                continue
            pos = np.array([x + 0.5, y + 0.5])
            v = intervel(pos)
            v[1] *= -1
            d_cpy[y, x] = interpolate_density(pos - v * 30 * dt)
    d_sum = np.sum(d_cpy)
    if d_sum and d_sum > 0:
        density = d_cpy * np.sum(density) / d_sum
    # density = d_cpy
