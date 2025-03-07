from pygame.math import clamp

from const import *
from ui import screen
from grid import *
from velocity import *


def interpolate_density(pos, density_grid):
    x, y = pos[0], pos[1]

    X, Y = clamp(int(x - 0.5), 0, GRID_WIDTH - 2), clamp(
        int(y - 0.5), 0, GRID_HEIGHT - 2
    )
    a = clamp(abs(x - (X + 0.5)), 0, 1)
    b = clamp(abs(y - (Y + 0.5)), 0, 1)
    c = 1 - a
    d = 1 - b
    if a > 1 or a < 0:
        print("NONONON", a)
        exit(1)
    if b > 1 or b < 0:
        print("NONONON b", b)
        exit(1)
    return (
        density_grid[Y, X] * c * d
        + density_grid[Y + 1, X] * b * c
        + density_grid[Y, X + 1] * a * d
        + density_grid[Y + 1, X + 1] * a * b
    )


def update_density(density_grid):

    bef = np.sum(np.abs(density_grid))

    d_cpy = np.zeros(density_grid.shape)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # if (
            #     ymsk[y, x] == 0
            #     and ymsk[y + 1, x] == 0
            #     and xmsk[y, x] == 0
            #     and xmsk[y, x + 1] == 0
            # ):
            #     continue
            pos = np.array([x + 0.5, y + 0.5])
            v = interpolate_velocity(pos, False)
            v[1] *= -1

            # pygame.draw.line(
            #     screen,
            #     (0, 225, 0),
            #     pos * CELL_SIZE,
            #     (pos - v * 0.1) * CELL_SIZE,
            #     3,
            # )
            # v[1] *= -1

            # pygame.draw.circle(screen, (255, 0, 0), pos * CELL_SIZE, 2)
            pre_pos = pos - v * 0.1
            d_cpy[y, x] = interpolate_density(pre_pos, density_grid)
            # if x == 1 and y == 1:
            #     print("pre = ", pre_pos, " DCPY VAL ", d_cpy[y, x])

    # pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    # pygame.draw.circle(
    #     screen, (0, 255, 0), pos * CELL_SIZE, interpolate_density(pos, density_grid)
    # )

    aft = np.sum(np.abs(d_cpy))
    if aft != 0:
        d_cpy *= bef / aft
    # aft = np.sum(np.abs(d_cpy))
    # print("SUM=\n", aft)
    return d_cpy
    # return density_grid
