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
