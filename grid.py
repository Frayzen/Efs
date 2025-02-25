from pygame.math import clamp
import cupy as cp

from const import *

# Generate initial random colors
density = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float64)

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

diags.append([4 for i in range(n)])
offsets.append(0)

right_diag = np.array([-1 for i in range(n - 1)])
right_diag[GRID_WIDTH - 1 :: GRID_WIDTH] = 0
diags.append(right_diag)  # right

offsets.append(1)

left_diag = np.array([-1 for i in range(1, n)])
left_diag[GRID_WIDTH - 1 :: GRID_WIDTH] = 0
diags.append(left_diag)  # left
offsets.append(-1)


diags.append([-1 for i in range(n - GRID_WIDTH)])  # top
offsets.append(GRID_WIDTH)

diags.append([-1 for i in range(GRID_WIDTH, n)])  # bot
offsets.append(-GRID_WIDTH)


# print(diags)
mat = sp.diags(diags, offsets, shape=(n, n))
print("DET = ", cp.linalg.det(mat.toarray()))
# for i in range(n):
#     print("mat (", i, ")) = \n", mat.toarray()[i])
