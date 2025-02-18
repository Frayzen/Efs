from const import *
from grid import *
from velocity import *


def divcompute_cell(x, y):
    v = -y_mac[y][x] + y_mac[y + 1][x] + x_mac[y][x] - x_mac[y][x + 1]
    hsubs = ymsk[y : y + 2, x]
    wsubs = xmsk[y, x : x + 2]
    bot = np.sum(wsubs) + np.sum(hsubs)
    # if check_mouse_coords(x, y):
    #     print(bot)
    #     print(v)
    if bot == 0:
        return 0
    return v / bot


def compute_divergence():
    return np.array(
        [[divcompute_cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    )


def clear_divergence():
    div = compute_divergence()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # if check_mouse_coords(x, y):
            #     print("PREV", y_mac[y, x])
            y_mac[y, x] += div[y, x] * ymsk[y, x]
            y_mac[y + 1, x] -= div[y, x] * ymsk[y + 1, x]
            x_mac[y, x] -= div[y, x] * xmsk[y, x]
            x_mac[y, x + 1] += div[y, x] * xmsk[y, x + 1]
            # if check_mouse_coords(x, y):
            #     print("AFTR", y_mac[y, x])
            #     print(div[y, x], xmsk[y, x], ymsk[y, x], xmsk[y, x + 1], ymsk[y + 1, x])
