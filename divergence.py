from const import *
from grid import *
from velocity import *


def divcompute_cell(x, y):
    v = -y_grid[y][x] + y_grid[y + 1][x] + x_grid[y][x] - x_grid[y][x + 1]
    hsubs = sy[y : y + 2, x]
    wsubs = sx[y, x : x + 2]
    bot = np.sum(wsubs) + np.sum(hsubs)
    # if check_mouse_coords(x, y):
    #     print(bot)
    #     print(v)
    if bot == 0:
        return 0
    return v / bot


def divcompute():
    return np.array(
        [[divcompute_cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    )


def clear_divergence():
    div = divcompute()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # if check_mouse_coords(x, y):
            #     print("PREV", y_grid[y, x])
            y_grid[y, x] += div[y, x] * sy[y, x]
            y_grid[y + 1, x] -= div[y, x] * sy[y + 1, x]
            x_grid[y, x] -= div[y, x] * sx[y, x]
            x_grid[y, x + 1] += div[y, x] * sx[y, x + 1]
            # if check_mouse_coords(x, y):
            #     print("AFTR", y_grid[y, x])
            #     print(div[y, x], sx[y, x], sy[y, x], sx[y, x + 1], sy[y + 1, x])
