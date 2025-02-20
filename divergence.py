from const import *
from grid import *
from velocity import *
import cupyx.scipy.sparse.linalg as la
import cupy as cp


def divcompute_cell(x, y):
    v = -y_mac[y][x] + y_mac[y + 1][x] + x_mac[y][x] - x_mac[y][x + 1]
    # if check_mouse_coords(x, y):
    #     print(bot)
    #     print(v)
    return v / s[y, x]


def compute_divergence():
    return np.array(
        [[divcompute_cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    )


def clear_divergence():
    global x_mac, y_mac
    global xmsk, ymsk
    nb_iter = 10

    prevsum = np.sum(np.abs(x_mac)) + np.sum(np.abs(y_mac))
    # print(xmsk)
    # print(ymsk)
    # print(s)
    for it in range(nb_iter):
        div = compute_divergence().ravel()
        for _ in range(2):
            odd = it % 2 == 1

            i = it % 2
            while i < n:
                dv = div[i] / s_flat[i]
                x = i % GRID_WIDTH
                y = i // GRID_WIDTH
                x_mac[y, x] -= dv * xmsk[y, x]
                x_mac[y, x + 1] += dv * xmsk[y, x + 1]
                y_mac[y, x] += dv * ymsk[y, x]
                y_mac[y + 1, x] -= dv * ymsk[y + 1, x]
                i += 2
                if i % GRID_WIDTH == 0 and not odd:
                    i += 1

    div = compute_divergence()
    # print(x_mac)
    # print(y_mac)
    # print(div)
    postsum = np.sum(np.abs(x_mac)) + np.sum(np.abs(y_mac))
    x_mac *= prevsum / postsum
    y_mac *= prevsum / postsum
    # print(np.sum(np.abs(div)) / div.size)
