import pygame
import time
import numpy as np

# Grid settings
CELL_SIZE = 30  # Pixel size of each cell
GRID_WIDTH = 30  # Number of cells horizontally
GRID_HEIGHT = 30  # Number of cells vertically

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")

# Generate initial random colors
h_grid = np.array(
    [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)], dtype=np.float64
)
w_grid = np.array(
    [[0 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)], dtype=np.float64
)
sw = np.ones((GRID_HEIGHT, GRID_WIDTH + 1), dtype=np.float64)
sw[:, 0] = 0
sw[:, -1] = 0
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
            c = min(abs(div[y, x]), 255)
            color = [c] * 3
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
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            h_grid[y, x] += div[y, x] * sh[y, x]
            h_grid[y + 1, x] -= div[y, x] * sh[y + 1, x]
            w_grid[y, x] -= div[y, x] * sw[y, x]
            w_grid[y, x + 1] += div[y, x] * sw[y, x + 1]


dampling = 1


def step():
    global div
    div = np.array(
        [
            [divcompute(x, y) * dampling for x in range(GRID_WIDTH)]
            for y in range(GRID_HEIGHT)
        ]
    )
    update_velocity()


h_grid[1][0] = -100000
w_grid[0][1] = 100000

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # elif event.type == pygame.KEYDOWN:  # Press any key to change colors dynamically
        # if event.type == pygame.KEYDOWN:
    step()

pygame.quit()
