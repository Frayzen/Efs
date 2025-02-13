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

    X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 2)
    Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 2)
    X2 = X1 + 1
    Y2 = Y1 + 1

    x = clamp(int(px), 0, GRID_WIDTH - 2)
    y = clamp(int(py), 0, GRID_HEIGHT - 2)
    if x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1:
        return np.array([0, 0])

    ax = abs(px - X1) - 0.5
    bx = py - int(py)
    cx = 1 - ax
    dx = 1 - bx

    ay = px - int(px)
    by = abs(py - Y1) - 0.5
    cy = 1 - ay
    dy = 1 - by

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

        # Y
        pygame.draw.circle(  # 0 0
            screen, (255, 255, 0), np.array([x, Y1 + 0.5]) * CELL_SIZE, dy * cy * 20
        )
        pygame.draw.circle(
            screen, (255, 255, 0), np.array([x + 1, Y1 + 0.5]) * CELL_SIZE, ay * dy * 20
        )
        pygame.draw.circle(
            screen, (255, 255, 0), np.array([x, Y1 + 1.5]) * CELL_SIZE, by * cy * 20
        )
        pygame.draw.circle(
            screen, (255, 255, 0), np.array([x + 1, Y1 + 1.5]) * CELL_SIZE, ay * by * 20
        )

    return np.array(
        [
            # X
            x_grid[Y1, x] * dy * cy  # top left
            + x_grid[Y1, x + 1] * ay * dy  # top right
            + x_grid[Y2, x] * by * cy  # bottom left
            + x_grid[Y2, x + 1] * ay * by,  # bottom right
            # Y
            y_grid[y, X1] * dx * cx
            + y_grid[y, X2] * ax * dx
            + y_grid[y + 1, X1] * bx * cx
            + y_grid[y + 1, X2] * ax * bx,
        ]
    )


dt = 0.01


def advect():
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = intervel(pos)
            nv = intervel(pos - v * dt)
            x_grid[y, x] = nv[0]

            # pygame.draw.circle(screen, (0, 0, 255), pos * CELL_SIZE, 2)
            # pygame.draw.circle(screen, (255, 0, 0), pre_pos * CELL_SIZE, 2)
            # pygame.draw.line(
            #     screen, (225, 0, 0), pos * CELL_SIZE, (pos + pre_v * dt) * CELL_SIZE, 2
            # )
            # pygame.draw.line(
            #     screen, (225, 0, 0), pos * CELL_SIZE, (pos + nv * dt) * CELL_SIZE, 2
            # )

    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            pos = np.array([x + 0.5, y])
            v = intervel(pos)
            nv = intervel(pos - v * dt)
            y_grid[y, x] = nv[1]

            # pygame.draw.circle(screen, (0, 255, 0), pos * CELL_SIZE, 2)
            # pygame.draw.circle(screen, (0, 225, 0), pre_pos * CELL_SIZE, 2)
            # pygame.draw.line(
            #     screen, (0, 255, 0), pos * CELL_SIZE, (pos + pre_v * dt) * CELL_SIZE, 2
            # )
            # pygame.draw.line(
            #     screen, (0, 225, 0), pos * CELL_SIZE, (pos + nv * dt) * CELL_SIZE, 2
            # )


# Main loop
running = True
while running:
    # screen.fill((255, 255, 255))
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    print(pos)
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

    keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    x_grid[GRID_HEIGHT // 2, 0] = 90

    y_grid[GRID_HEIGHT // 2, 0] = 90
    y_grid[GRID_HEIGHT // 2 + 1, 0] = -90

    # else:
    #     w_grid[GRID_HEIGHT // 2, 0] -= 5
    #     w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    clear_divergence()
    advect()

    pygame.display.flip()
    time.sleep(dt)


pygame.quit()
