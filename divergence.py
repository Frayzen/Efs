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
    div = compute_divergence().ravel()
    print("cunt\n", div)
    # print("mat = \n", mat.toarray()[4])
    # exit()
    res = cp.asnumpy(la.spsolve(mat, cp.asarray(div)))
    res = res.reshape(GRID_HEIGHT, GRID_WIDTH)
    print(np.array(res))
    # print(res[0, 0])
    # print(res[0, 1] / 3)
    # print(res[1, 0] / 3)

    print("FIRST ROW", div[:GRID_WIDTH])

    # res /= s
    # # OLD PART
    print("EQUAL ", res[0, 1] + res[1, 0], " = ", res[0, 0] * 2)
    # print("SHOULD ADD ", res[1, 0], " + ", res[0, 1])
    # # print("res A = ", res[0:2, 0:2])
    # print("BEF", x_mac[0, 1])
    # x_mac[:, 1:-1] += res[:, 1:]  # right one
    # print("AFT RIGHT", x_mac[0, 1])
    # x_mac[:, 1:-1] += res[:, :-1]  # left one
    # print("AFT LEFT", x_mac[0, 1])

    # y_mac[1:-1, :] += res[1:, :]  # bot one
    # y_mac[1:-1, :] += res[:-1, :]  # top one

    # OLD PART
    print(np.array(div, dtype=int).reshape(GRID_HEIGHT, GRID_WIDTH))

    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            y_mac[y, x] += res[y - 1, x]
            y_mac[y, x] -= res[y, x]
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            x_mac[y, x] += res[y, x]
            x_mac[y, x] -= res[y, x - 1]

    print("final A div = ", int(divcompute_cell(0, 0)))
    print("final C div = ", int(divcompute_cell(0, 1)))
    print("final B div = ", int(divcompute_cell(1, 0)))
    print(np.array(res, dtype=int))
    div = compute_divergence()
    print("new div: \n", np.array(div, dtype=int))

    # print("final B div = ", x_mac[0, 1] + y_mac[1, 1] + x_mac[0, 2])
    # print("final B div = ", x_mac[0, 1] + y_mac[1, 1] + x_mac[0, 2])
    # for x in range(0, GRID_WIDTH - 1):
    #     x_mac[:, x] += res[:, x]
    # for x in range(0, GRID_WIDTH - 1):
    #     x_mac[:, x + 1] -= res[:, x]
    # for y in range(0, GRID_HEIGHT - 1):
    #     y_mac[y, :] += res[y, :]
    # for y in range(0, GRID_HEIGHT - 1):
    #     y_mac[y + 1, :] -= res[y, :]

    # for x in range(1, GRID_WIDTH - 2):
    #     for y in range(1, GRID_HEIGHT - 1):
    #         y_mac[y, x] -= res[y, x] - res[y + 1, x]
    # div = compute_divergence()
    # print(div[0])
    # print("AFT", x_mac[0, 1])
    # print("final C div = ", int(divcompute_cell(1, 0)))
    # print("final B div = ", int(divcompute_cell(0, 1)))
    input("hey")

    # for x in range(GRID_WIDTH):
    #     for y in range(GRID_HEIGHT):
    #         # if check_mouse_coords(x, y):
    #         #     print("PREV", y_mac[y, x])
    #         y_mac[y, x] += div[y, x] * ymsk[y, x]
    #         y_mac[y + 1, x] -= div[y, x] * ymsk[y + 1, x]
    #         x_mac[y, x] -= div[y, x] * xmsk[y, x]
    #         x_mac[y, x + 1] += div[y, x] * xmsk[y, x + 1]
    #         # if check_mouse_coords(x, y):
    #         #     print("AFTR", y_mac[y, x])
    #         #     print(div[y, x], xmsk[y, x], ymsk[y, x], xmsk[y, x + 1], ymsk[y + 1, x])
