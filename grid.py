from pygame.math import clamp
import scipy as sp
import scipy.linalg as spl

import cupy as cp
from const import *

# Generate initial random colors
density_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float64)

y_mac = np.array(
    [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)],
    dtype=np.float64,
)
x_mac = np.array(
    [[0 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)],
    dtype=np.float64,
)

xmsk = np.ones((GRID_HEIGHT, GRID_WIDTH + 1), dtype=np.float64)
xmsk[:, 0] = 0
xmsk[:, -1] = 0
ymsk = np.ones((GRID_HEIGHT + 1, GRID_WIDTH), dtype=np.float64)
ymsk[0, :] = 0
ymsk[-1, :] = 0


diags = []
offsets = []

n = GRID_WIDTH * GRID_HEIGHT


def build_s(h, w):
    s = np.ones(h * w).reshape(h, w) * 4
    s[0, :] = 3
    s[h - 1, :] = 3
    s[:, 0] = 3
    s[:, w - 1] = 3
    s[0, 0] = 2
    s[h - 1, 0] = 2
    s[h - 1, w - 1] = 2
    s[0, w - 1] = 2
    return s


s = build_s(GRID_HEIGHT, GRID_WIDTH)


s_flat = s.ravel()
# print(s_flat)
# # print(diags)
# mat = sp.diags(diags, offsets, shape=(n, n))
# print("mat = \n", mat.toarray()[0])

# OLD

# diags.append([1 for i in range(n)])
# offsets.append(0)

# S = -1
# right_diag = np.array([S / s_flat[i + 1] for i in range(n - 1)])
# right_diag[GRID_WIDTH - 1 :: GRID_WIDTH] = 0
# diags.append(right_diag)  # right
# offsets.append(1)

# left_diag = np.array([S / s_flat[i - 1] for i in range(1, n)])
# left_diag[GRID_WIDTH - 1 :: GRID_WIDTH] = 0
# diags.append(left_diag)  # left
# offsets.append(-1)

# diags.append([S / s_flat[i + GRID_WIDTH] for i in range(n - GRID_WIDTH)])  # top
# offsets.append(GRID_WIDTH)

# diags.append([S / s_flat[i - GRID_WIDTH] for i in range(GRID_WIDTH, n)])  # bot
# offsets.append(-GRID_WIDTH)


# IMPLEM
sys_width = GRID_WIDTH + 2
sys_heigth = GRID_HEIGHT + 2

sys_n = sys_width * sys_heigth


def not_bound(i):
    x = i % sys_width
    y = i // sys_width
    if x == 0 or x == sys_width - 1 or y == 0 or y == sys_heigth - 1:
        return 0
    return 1


def main_diag(i):
    x = i % sys_width
    y = i // sys_width
    if x == 0 or x == sys_width - 1 or y == 0 or y == sys_heigth - 1:
        return 4
    return s[y - 1, x - 1]


diags.append([-4 for i in range(sys_n)])
offsets.append(0)

diags.append([not_bound(i) for i in range(sys_n - 1)])  # right
offsets.append(1)

diags.append([-not_bound(i) for i in range(1, sys_n)])  # left
offsets.append(-1)

diags.append([not_bound(i) for i in range(sys_n - sys_width)])  # top
offsets.append(sys_width)

diags.append([-not_bound(i) for i in range(sys_width, sys_n)])  # bot
offsets.append(-sys_width)


# print(diags)
mat = sp.diags(diags, offsets, shape=(sys_n, sys_n))
det = spl.det(mat.toarray())
print(mat.toarray())
print("DET = ", det)
assert det != 0
# for i in range(n):
#     print("mat (", i, ")) = \n", mat.toarray()[i])
