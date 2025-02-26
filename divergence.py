from const import *
from grid import *
from velocity import *
import scipy.sparse.linalg as spl


def divcompute_cell(x, y):
    v = -y_mac[y][x] + y_mac[y + 1][x] + x_mac[y][x] - x_mac[y][x + 1]
    # if check_mouse_coords(x, y):
    #     print(bot)
    #     print(v)
    return v  # / s[y, x]
    # return v


def compute_divergence(define_boundaries=True):
    res = np.array(
        [[divcompute_cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    )
    if define_boundaries:
        res = np.pad(res, pad_width=1, constant_values=0)
    return res


def clear_divergence():
    print("old xmac = \n", x_mac)
    print("old ymac = \n", y_mac)

    div = compute_divergence()
    print("old div: \n", np.array(div, dtype=float))
    div = div.ravel()
    # print("mat = \n", mat.toarray()[4])
    # exit()
    print("sytem is ")
    print(mat.toarray())
    print(div)
    res = spl.spsolve(mat, div)
    ch = mat @ res
    print("CHECK\n", ch)
    res = res.reshape(sys_heigth, sys_width)[1:-1, 1:-1]
    print("res=\n", np.round(res, 2))
    # res = res * 4 / s

    # print("res * 4 / s=\n", np.round(res, 2))
    # print("sum is ", np.sum(res))
    # print(res[0, 0])
    # print(res[0, 1] / 3)
    # print(res[1, 0] / 3)

    # print("FIRST ROW", div[:GRID_WIDTH])

    # res /= s
    # # OLD PART
    # print("EQUAL ", res[0, 1] + res[1, 0], " = ", res[0, 0] * 2)
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
    # print(np.array(div, dtype=int).reshape(GRID_HEIGHT, GRID_WIDTH))

    for x in range(GRID_WIDTH):  # loop on each cell res
        for y in range(GRID_HEIGHT):
            r = res[y, x]
            if x != 0:
                x_mac[y, x] += r  # left
            if x != GRID_WIDTH - 1:
                x_mac[y, x + 1] -= r  # right
            if y != 0:
                y_mac[y, x] -= r  # top
            if y != GRID_HEIGHT - 1:
                y_mac[y + 1, x] += r  # bottom

    # print("final A div = ", int(divcompute_cell(0, 0)))
    # print("final C div = ", int(divcompute_cell(0, 1)))
    # print("final B div = ", int(divcompute_cell(1, 0)))
    # print(np.array(res, dtype=int))
    div = compute_divergence()
    print("new div: \n", np.array(div, dtype=float))

    print("new xmac = \n", x_mac)
    print("new ymac = \n", y_mac)
    input("hey")
