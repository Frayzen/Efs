from pygame.math import clamp

from const import *

# Generate initial random colors
density = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float64)

y_grid = np.array(
    [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)],
    dtype=np.float64,
)
x_grid = np.array(
    [[0 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)],
    dtype=np.float64,
)

sx = np.ones((GRID_HEIGHT, GRID_WIDTH + 1), dtype=np.float64)
sx[:, 0] = 0
sx[:, -1] = 0
sy = np.ones((GRID_HEIGHT + 1, GRID_WIDTH), dtype=np.float64)
sy[0, :] = 0
sy[-1, :] = 0


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
    s[0, 0] = 2
    s[0, w - 1] = 2
    return s


s = build_s(GRID_HEIGHT, GRID_WIDTH)


s_flat = s.ravel()
# print(s_flat)


diags.append([s_flat[i] for i in range(n)])
offsets.append(0)

diags.append([1 for _ in range(n - 1)])
offsets.append(1)

diags.append([1 for _ in range(n - 1)])
offsets.append(-1)

diags.append([1 for _ in range(n - GRID_WIDTH)])
offsets.append(GRID_WIDTH)

diags.append([1 for _ in range(n - GRID_WIDTH)])
offsets.append(-GRID_WIDTH)


# print(diags)
mat = sp.diags(diags, offsets, shape=(n, n))
