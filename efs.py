import pygame
import time
import numpy as np
from pygame.math import clamp

# Grid settings
CELL_SIZE = 90  # Pixel size of each cell
GRID_WIDTH = 9  # Number of cells horizontally
GRID_HEIGHT = 9  # Number of cells vertically

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

y_grid = np.array(
    [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)],
    dtype=np.float64,
)
x_grid = np.array(
    [[0 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)],
    dtype=np.float64,
)

sw = np.ones((GRID_HEIGHT, GRID_WIDTH + 1), dtype=np.float64)
sw[:, 0] = 0
sw[:, -1] = 0
sh = np.ones((GRID_HEIGHT + 1, GRID_WIDTH), dtype=np.float64)
sh[0, :] = 0
sh[-1, :] = 0


def divcompute(x, y):
    v = -y_grid[y][x] + y_grid[y + 1][x] + x_grid[y][x] - x_grid[y][x + 1]
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
            color = (255, 255, 255)
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
    global y_grid, x_grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            y_grid[y, x] += div[y, x] * sh[y, x]
            y_grid[y + 1, x] -= div[y, x] * sh[y + 1, x]
            x_grid[y, x] -= div[y, x] * sw[y, x]
            x_grid[y, x + 1] += div[y, x] * sw[y, x + 1]


dampening = 0.9


# def intervel(pos):
#     global x_grid, y_grid
#     px, py = pos[0], pos[1]

#     X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 1)
#     Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 1)
#     X2 = clamp(X1 + 1, 0, GRID_WIDTH - 1)
#     Y2 = clamp(Y1 + 1, 0, GRID_HEIGHT - 1)
#     px = clamp(px, 0, GRID_WIDTH)
#     py = clamp(py, 0, GRID_HEIGHT)

#     X = int(clamp(px, 0, GRID_WIDTH - 1))
#     Y = int(clamp(py, 0, GRID_HEIGHT - 1))

#     a = abs(px - (X1 + 0.5))
#     b = abs(py - (Y1 + 0.5))
#     c = 1 - a
#     d = 1 - b

#     return np.array(
#         [
#             # X
#             c * d * x_grid[Y - 1, X1]
#             + a * d * x_grid[Y - 1, X2]
#             + b * c * x_grid[Y, X1]
#             + a * b * x_grid[Y, X2],
#             # Y
#             c * d * y_grid[Y1, X - 1]
#             + b * c * y_grid[Y2, X - 1]
#             + a * d * y_grid[Y1, X]
#             + a * b * y_grid[Y2, X],
#         ]
#     )


def intervel(pos, draw=False):
    global x_grid, y_grid
    px, py = pos[0], pos[1]

    X1 = int(px - 0.5)
    Y1 = int(py - 0.5)

    x = int(px)
    y = int(py)
    if x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1:
        return np.array([0, 0])

    y00 = y_grid[y, X1]
    y01 = y_grid[y, X1 + 1]
    y10 = y_grid[y + 1, X1]
    y11 = y_grid[y + 1, X1 + 1]

    x00 = x_grid[Y1, x]
    x01 = x_grid[Y1, x + 1]
    x10 = x_grid[Y1 + 1, x]
    x11 = x_grid[Y1 + 1, x + 1]

    a = abs(X1 - px)
    b = abs(Y1 - py)

    c = abs(1 - a)
    d = abs(1 - b)

    ax = abs(px - X1) - 0.5
    bx = py - int(py)
    cx = 1 - ax
    dx = 1 - bx

    if draw:
        # X
        pygame.draw.circle(  # 0 0
            screen, (0, 255, 0), np.array([X1 + 0.5, y]) * CELL_SIZE, dx * cx * 20
        )
        pygame.draw.circle(
            screen, (0, 255, 0), np.array([X1 + 1.5, y]) * CELL_SIZE, ax * dx * 20
        )
        pygame.draw.circle(
            screen, (0, 255, 0), np.array([X1 + 0.5, y + 1]) * CELL_SIZE, bx * cx * 20
        )
        pygame.draw.circle(
            screen, (0, 255, 0), np.array([X1 + 1.5, y + 1]) * CELL_SIZE, ax * bx * 20
        )

    return np.array(
        [
            # X
            x00 * c * d + x01 * a * d + x10 * b * c + x11 * a * b,
            # Y
            y00 * c * d + y01 * a * d + y10 * b * c + y11 * a * b,
        ]
    )


# def intervel(pos):
#     global x_grid, y_grid
#     px, py = pos[0], pos[1]

#     # X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 1)
#     # Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 1)
#     X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 1)
#     Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 1)

#     X2 = clamp(X1 + 1, 0, GRID_WIDTH - 1)
#     Y2 = clamp(Y1 + 1, 0, GRID_HEIGHT - 1)
#     px = clamp(px, 0, GRID_WIDTH)
#     py = clamp(py, 0, GRID_HEIGHT)

#     X = int(px)
#     Y = int(py)

#     a = abs(px - (X1 + 0.5))
#     b = abs(py - (Y1 + 0.5))
#     c = 1 - a
#     d = 1 - b

#     return np.array(
#         [
#             # X
#             c * d * x_grid[Y1, X1]
#             + a * d * x_grid[Y1, X2]
#             + b * c * x_grid[Y2, X1]
#             + a * b * x_grid[Y2, X2],
#             # Y
#             c * d * y_grid[Y1, X1]
#             + b * c * y_grid[Y2, X1]
#             + a * d * y_grid[Y1, X2]
#             + a * b * y_grid[Y2, X2],
#         ]
#     )


dt = 0.01


def advect():
    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            p = np.array([x + 0.5, y])
            pos = np.array([x + 0.5, y])
            v = np.array([0, y_grid[y, x]]) * dt
            pygame.draw.circle(screen, (0, 0, 255), pos * CELL_SIZE, 2)
            # nv = intervel(pos - v)[0]

            nv = np.array(
                x_grid[y, x],
                (
                    y_grid[y, x - 1]
                    + y_grid[y, x]
                    + y_grid[y + 1, x - 1]
                    + y_grid[y + 1, x]
                )
                / 4,
            )
            pygame.draw.line(screen, (0, 0, 255), p * CELL_SIZE, (p + v) * CELL_SIZE, 2)
            pygame.draw.line(
                screen,
                (0, 0, 255),
                p * CELL_SIZE,
                (p + intervel(p) * dt) * CELL_SIZE,
                2,
            )
            # w_grid[y, x] = nv
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            p = np.array([x, y + 0.5])

            pos = np.array([x, y + 0.5])
            pygame.draw.circle(screen, (255, 0, 0), p * CELL_SIZE, 2)
            v = np.array([x_grid[y, x], 0]) * dt

            # nv = intervel(pos - v)[1]
            nv = np.array(
                (
                    x_grid[y - 1, x]
                    + x_grid[y - 1, x + 1]
                    + x_grid[y, x]
                    + x_grid[y, x + 1]
                )
                / 4,
                y_grid[y, x],
            )

            pygame.draw.line(screen, (255, 0, 0), p * CELL_SIZE, (p + v) * CELL_SIZE, 2)

            # h_grid[y, x] = nv


# Main loop
running = True
while running:
    # screen.fill((255, 255, 255))
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    vel = intervel(pos, True)
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        x_grid[GRID_HEIGHT // 2, 1] += 1

    # else:
    #     w_grid[GRID_HEIGHT // 2, 0] -= 5
    #     w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    clear_divergence()
    advect()

    pygame.display.flip()
    time.sleep(dt)


pygame.quit()
