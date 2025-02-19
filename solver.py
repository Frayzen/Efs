from ymsks import get_coroutine_origin_tracking_depth
import scipy.sparse as sp
import pygame
import time
import numpy as np
from pygame.math import clamp

# Grid settings
CELL_SIZE = 30  # Pixel size of each cell
GRID_WIDTH = 3  # Number of cells horizontally
GRID_HEIGHT = 3  # Number of cells vertically


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


diags = []
offsets = []

n = GRID_WIDTH * GRID_HEIGHT
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
npmat = mat.toarray()

div = np.arange(n)
res = np.linalg.solve(mat.toarray(), div)


print(mat)
# print(res)
# print(div)

# print(npmat[:, 0])
# print(res)

res = res.reshape((GRID_HEIGHT, GRID_WIDTH))

# print(npmat)
print(res[0, 0] * s[0, 0] + res[1, 0] + res[0, 1])
print(res[0, 1] * s[0, 1] + res[0, 0] + res[0, 2] + res[1, 1])
