from sys import get_coroutine_origin_tracking_depth
import pygame
import time
import numpy as np
from pygame.math import clamp

# Grid settings
CELL_SIZE = 30  # Pixel size of each cell
GRID_WIDTH = 20  # Number of cells horizontally
GRID_HEIGHT = 20  # Number of cells vertically

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")


def check_mouse_coords(x, y):
    x = int(x)
    y = int(y)
    pos = np.array(pygame.mouse.get_pos()) // CELL_SIZE
    return pos[0] == x and pos[1] == y


def build_checkerboard(shape):
    h, w = shape
    re = np.r_[w * [0, 1]]  # even-numbered rows
    ro = np.r_[w * [1, 0]]  # odd-numbered rows
    return np.row_stack(h * (re, ro))[:h, :w]


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

# fromx = GRID_WIDTH // 2
# fromy = GRID_HEIGHT // 2
# for x in range(3):
#     for y in range(3):
#         sw[fromy, fromx + x] = 0
#         sw[fromy + 2, fromx + x] = 0

#         sh[fromy + y, fromx] = 0
#         sh[fromy + y, fromx + 2] = 0


def box_element(pos):
    x, y = int(pos[0]), int(pos[1])
    sy[y, x] = 0
    sy[y + 1, x] = 0
    sx[y, x] = 0
    sx[y, x + 1] = 0
    density[y, x] = 0


def divcompute(x, y):
    v = -y_grid[y][x] + y_grid[y + 1][x] + x_grid[y][x] - x_grid[y][x + 1]
    hsubs = sy[y : y + 2, x]
    wsubs = sx[y, x : x + 2]
    bot = np.sum(wsubs) + np.sum(hsubs)
    # if check_mouse_coords(x, y):
    #     print(bot)
    #     print(v)
    if bot == 0:
        return 0
    return v / bot


div = np.array(
    [[divcompute(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
)


def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # dv = int(div[y, x] * 100)

            if (
                sy[y, x] == 0
                and sy[y + 1, x] == 0
                and sx[y, x] == 0
                and sx[y, x + 1] == 0
            ):
                color = [255, 0, 0]
            else:
                color = [clamp(int(density[y, x]), 0, 255)] * 3

            pygame.draw.rect(
                screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )  # Grid outline

            # font = pygame.font.Font(
            #     None, int(CELL_SIZE * 0.8)
            # )  # Choose an appropriate font size
            # divergence = int(density[y, x])
            # text = font.render(
            #     f"{divergence}", True, (200, 50, 50)
            # )  # Render the text '10' in black
            # text_rect = text.get_rect(
            #     center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            # )
            # screen.blit(text, text_rect)


# def draw_grid():
#     for x in range(GRID_WIDTH):
#         for y in range(GRID_HEIGHT):
#             dv = int(div[y, x] * 100)
#             # if div[y, x] < 0:
#             #     color = (0, 0, min(-dv, 255))
#             # else:
#             #     color = (min(dv, 255), 0, 0)
#             # color = (255, 255, 255)

#             if (
#                 sh[y, x] == 0
#                 and sh[y + 1, x] == 0
#                 and sw[y, x] == 0
#                 and sw[y, x + 1] == 0
#             ):
#                 color = [255, 0, 0]
#             else:
#                 color = [clamp(int(density[y, x]), 0, 255)] * 3
#             pygame.draw.rect(
#                 screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#             )
#             pygame.draw.rect(
#                 screen,
#                 (0, 0, 0),
#                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
#                 1,
#             )  # Grid outline


def clear_divergence():
    global y_grid, x_grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # if check_mouse_coords(x, y):
            #     print("PREV", y_grid[y, x])
            y_grid[y, x] += div[y, x] * sy[y, x]
            y_grid[y + 1, x] -= div[y, x] * sy[y + 1, x]
            x_grid[y, x] -= div[y, x] * sx[y, x]
            x_grid[y, x + 1] += div[y, x] * sx[y, x + 1]
            # if check_mouse_coords(x, y):
            #     print("AFTR", y_grid[y, x])
            #     print(div[y, x], sx[y, x], sy[y, x], sx[y, x + 1], sy[y + 1, x])


dampening = 1


def intervel(pos, draw=False):

    global x_grid, y_grid
    px, py = pos[0], pos[1]

    X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 2)
    Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 2)
    X2 = X1 + 1
    Y2 = Y1 + 1

    x = clamp(int(px), 0, GRID_WIDTH - 2)
    y = clamp(int(py), 0, GRID_HEIGHT - 2)
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


dt = 0.001


def advect():
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = intervel(pos)
            nv = intervel(pos - v * dt)
            if sx[y, x] == 0:
                x_grid[y, x] *= 0.1
            else:
                x_grid[y, x] = nv[0]

    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            pos = np.array([x + 0.5, y])
            v = intervel(pos)
            nv = intervel(pos - v * dt)
            if sy[y, x] == 0:
                y_grid[y, x] *= 0.1
            else:
                y_grid[y, x] = nv[1]


def draw_vel():
    ratio = 50 * dt
    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = intervel(pos)
            v[1] *= -1
            pygame.draw.line(
                screen, (225, 0, 0), pos * CELL_SIZE, (pos + v * ratio) * CELL_SIZE, 2
            )

    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            pos = np.array([x + 0.5, y])
            v = intervel(pos)
            v[1] *= -1
            pygame.draw.line(
                screen,
                (0, 225, 0),
                pos * CELL_SIZE,
                (pos + v * ratio) * CELL_SIZE,
                2,
            )


def interpolate_density(pos):
    x, y = pos[0], pos[1]
    # if x < 0 or x > GRID_WIDTH - 1 or y < 0 or y > GRID_HEIGHT - 1:
    #     return 0

    X, Y = clamp(int(x - 0.5), 0, GRID_WIDTH - 2), clamp(
        int(y - 0.5), 0, GRID_HEIGHT - 2
    )
    a = abs(x - X) - 0.5
    b = abs(y - Y) - 0.5
    c = 1 - a
    d = 1 - b
    return (
        density[Y, X] * c * d
        + density[Y + 1, X] * b * c
        + density[Y, X + 1] * a * d
        + density[Y + 1, X + 1] * a * b
    )


def update_density():

    global density
    d_cpy = density.copy()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (
                sy[y, x] == 0
                and sy[y + 1, x] == 0
                and sx[y, x] == 0
                and sx[y, x + 1] == 0
            ):
                continue
            pos = np.array([x + 0.5, y + 0.5])
            v = intervel(pos)
            v[1] *= -1
            d_cpy[y, x] = interpolate_density(pos - v * 30 * dt)
    d_sum = np.sum(d_cpy)
    if d_sum and d_sum > 0:
        density = d_cpy * np.sum(density) / d_sum
    # density = d_cpy


# Main loop
running = True

x_grid[GRID_HEIGHT // 2, 8] = 3000
y_grid[GRID_HEIGHT // 2, 8] = 3000
y_grid[GRID_HEIGHT // 2 + 1, 8] = -3000

density[GRID_HEIGHT // 2, 4] = 50000
density[GRID_HEIGHT // 2 + 1, 4] = 50000

while running:
    # screen.fill()
    draw_grid()
    pos = np.array(pygame.mouse.get_pos(), dtype=np.float64) / CELL_SIZE
    vel = intervel(pos)
    vel[1] *= -1  # because vector is in cartesion but pygame is upside down
    pygame.draw.line(
        screen, (0, 255, 0), pos * CELL_SIZE, pos * CELL_SIZE + vel * dt * CELL_SIZE, 2
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
    if pygame.mouse.get_pressed(3)[0]:
        box_element(np.array(pygame.mouse.get_pos()) // CELL_SIZE)
    # density[:, -1] = 0
    print(np.sum(density))

    # else:
    #     w_grid[GRID_HEIGHT // 2, 0] -= 5
    #     w_grid[GRID_HEIGHT // 2, 0] = max(w_grid[GRID_HEIGHT // 2, 0], 0)

    clear_divergence()
    draw_vel()

    pygame.display.flip()

    advect()
    update_density()
    # time.sleep(dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        density[:, :] = 0
        x_grid[:, :] = 0
        y_grid[:, :] = 0

        x_grid[GRID_HEIGHT // 2, 8] = 3000
        y_grid[GRID_HEIGHT // 2, 8] = 3000
        y_grid[GRID_HEIGHT // 2 + 1, 8] = -3000

        density[GRID_HEIGHT // 2, 4] = 50000
        density[GRID_HEIGHT // 2 + 1, 4] = 50000


pygame.quit()
