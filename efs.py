import pygame
import time
import numpy as np
from pygame.math import clamp

# Grid settings
CELL_SIZE = 20  # Pixel size of each cell
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
            # color = (255, 255, 255)
            pygame.draw.rect(
                screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )  # Grid outline


def clear_divergence():
    global h_grid, w_grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            h_grid[y, x] += div[y, x] * sh[y, x]
            h_grid[y + 1, x] -= div[y, x] * sh[y + 1, x]
            w_grid[y, x] -= div[y, x] * sw[y, x]
            w_grid[y, x + 1] += div[y, x] * sw[y, x + 1]


dampening = 0.9


def intervel(pos):
    global w_grid, h_grid
    px, py = pos[0], pos[1]

    X1 = int(clamp(px - 0.5, 0, GRID_WIDTH - 1))
    Y1 = int(clamp(py - 0.5, 0, GRID_HEIGHT - 1))
    X2 = int(clamp(px + 0.5, 0, GRID_WIDTH - 1))
    Y2 = int(clamp(py + 0.5, 0, GRID_HEIGHT - 1))
    px = clamp(px, 0, GRID_WIDTH)
    py = clamp(py, 0, GRID_HEIGHT)

    a = abs(px - (X1 + 0.5))
    b = abs(py - (Y1 + 0.5))
    c = 1 - a
    d = 1 - b

    return np.array(
        [
            # X
            c * d * w_grid[Y1, X1]
            + a * d * w_grid[Y1, X2]
            + b * c * w_grid[Y2, X1]
            + a * b * w_grid[Y2, X2],
            # Y
            c * d * h_grid[Y1, X1]
            + b * c * h_grid[Y2, X1]
            + a * d * h_grid[Y1, X2]
            + a * b * h_grid[Y2, X2],
        ]
    )


dt = 0.01


def advect():
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = intervel(pos) * dt
            pygame.draw.circle(screen, (0, 0, 255), pos * CELL_SIZE, 2)
            nv = intervel(pos - v)[0]
            pygame.draw.line(
                screen, (0, 0, 255), pos * CELL_SIZE, (pos + v) * CELL_SIZE, 2
            )
            w_grid[y, x] = nv
    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            pos = np.array([x + 0.5, y])
            pygame.draw.circle(screen, (255, 0, 0), pos * CELL_SIZE, 2)
            v = intervel(pos) * dt
            pygame.draw.line(
                screen, (255, 0, 0), pos * CELL_SIZE, (pos + v) * CELL_SIZE, 2
            )
            nv = intervel(pos - v)[1]
            h_grid[y, x] = nv


# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    vel = intervel(pos)
    vel[1] *= -1
    pygame.draw.line(
        screen, (0, 255, 0), pos * CELL_SIZE, pos * CELL_SIZE + vel * dt * CELL_SIZE, 8
    )
    div = np.array(
        [
            [divcompute(x, y) * dampening for x in range(GRID_WIDTH)]
            for y in range(GRID_HEIGHT)
        ]
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # elif event.type == pygame.KEYDOWN:  # Press any key to change colors dynamically

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        w_grid[GRID_HEIGHT // 2, 0] += 10
    else:
        w_grid[GRID_HEIGHT // 2, 0] -= 5
        w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    clear_divergence()
    advect()

    pygame.display.flip()
    time.sleep(dt)


pygame.quit()
