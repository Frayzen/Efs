import pygame
import time
import numpy as np
from pygame.math import clamp

# Grid settings
CELL_SIZE = 30  # Pixel size of each cell
GRID_WIDTH = 40  # Number of cells horizontally
GRID_HEIGHT = 40  # Number of cells vertically

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")


def build_checkerboard(shape):
    h, w = shape
    re = np.r_[w * [0, 1]]  # even-numbered rows
    ro = np.r_[w * [1, 0]]  # odd-numbered rows
    return np.row_stack(h * (re, ro))[:h, :w]


# Generate initial random colors

h_grid = np.array(
    [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)],
    dtype=np.float64,
)
w_grid = np.array(
    [[0 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)],
    dtype=np.float64,
)

sw = np.ones((GRID_HEIGHT, GRID_WIDTH + 1), dtype=np.float64)
# sw[:, 0] = 0
# sw[:, -1] = 0
sh = np.ones((GRID_HEIGHT + 1, GRID_WIDTH), dtype=np.float64)
sh[0, :] = 0
sh[-1, :] = 0


def divcompute(x, y):
    v = -h_grid[y][x] + h_grid[y + 1][x] + w_grid[y][x] - w_grid[y][x + 1]
    hsubs = sh[y : y + 2, x]
    wsubs = sw[y, x : x + 2]
    return v / (np.sum(wsubs) + np.sum(hsubs))


div = np.array(
    [[divcompute(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
)


def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            dv = int(div[y, x] * 100)
            if div[y, x] < 0:
                color = (0, 0, min(-dv, 255))
            else:
                color = (min(dv, 255), 0, 0)
            pygame.draw.rect(
                screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )  # Grid outline


def update_velocity():
    global h_grid, w_grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            h_grid[y, x] += div[y, x] * sh[y, x]
            h_grid[y + 1, x] -= div[y, x] * sh[y + 1, x]
            w_grid[y, x] -= div[y, x] * sw[y, x]
            w_grid[y, x + 1] += div[y, x] * sw[y, x + 1]


dampling = 0.999


def intervel(pos):
    global w_grid, h_grid
    x, y = pos[0], pos[1]
    x = clamp(x, 0, GRID_WIDTH)
    y = clamp(y, 0, GRID_HEIGHT)
    X = int(x)
    Y = int(y)
    a = x - X
    b = y - Y
    c = 1 - a
    d = 1 - b
    return np.array(
        [
            w_grid[Y, X] * a + w_grid[Y, X + 1] * c,
            h_grid[Y, X] * b + h_grid[Y + 1, X] * d,
        ]
    )


# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) // CELL_SIZE
    pos += 0.5
    vel = intervel(pos)
    vel[1] *= -1
    pygame.draw.line(screen, (0, 255, 0), pos * CELL_SIZE, (pos + vel) * CELL_SIZE)
    pygame.display.flip()

    div = np.array(
        [
            [divcompute(x, y) * dampling for x in range(GRID_WIDTH)]
            for y in range(GRID_HEIGHT)
        ]
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # elif event.type == pygame.KEYDOWN:  # Press any key to change colors dynamically
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        w_grid[h_grid.shape[0] // 2, 0] += 1
        w_grid[h_grid.shape[0] // 2 + 1, 0] += 1
        w_grid[h_grid.shape[0] // 2 + 2, 0] += 1
    update_velocity()
    time.sleep(0.03)

pygame.quit()
