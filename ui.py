import pygame
import time
import numpy as np
from pygame.math import clamp

from grid import *
from velocity import interpolate_velocity

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")


def check_mouse_coords(x, y):
    x = int(x)
    y = int(y)
    pos = np.array(pygame.mouse.get_pos()) // CELL_SIZE
    return pos[0] == x and pos[1] == y


def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # dv = int(div[y, x] * 100)

            if (
                ymsk[y, x] == 0
                and ymsk[y + 1, x] == 0
                and xmsk[y, x] == 0
                and xmsk[y, x + 1] == 0
            ):
                color = [255, 0, 0]
            else:
                color = [clamp(int(density[y, x]), 0, 255)] * 3
            color = [255] * 3

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


def draw_vel():
    ratio = 0.08
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = interpolate_velocity(pos)
            v[1] *= -1
            pygame.draw.line(
                screen, (225, 0, 0), pos * CELL_SIZE, (pos + v * ratio) * CELL_SIZE, 2
            )

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = np.array([x + 0.5, y])
            v = interpolate_velocity(pos)
            v[1] *= -1
            pygame.draw.line(
                screen,
                (0, 225, 0),
                pos * CELL_SIZE,
                (pos + v * ratio) * CELL_SIZE,
                2,
            )


def draw_vel_cell():
    ratio = 0.5
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = np.array([x + 0.5, y + 0.5])
            v = interpolate_velocity(pos)
            v[1] *= -1
            pygame.draw.line(
                screen,
                (225, 0, 0),
                pos * CELL_SIZE,
                (pos + v / np.linalg.norm(v) * ratio) * CELL_SIZE,
                1,
            )
            pygame.draw.circle(screen, (0, 255, 0), pos * CELL_SIZE, 3)


def sign(x):
    return -1 if x < 0 else 1


def draw_vel_no_interp():
    ratio = 0.2
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = np.array([x + 0.5, y])
            v = np.array([0, -sign(y_mac[y, x]) * np.log(1 + abs(y_mac[y, x]))])
            pygame.draw.line(
                screen, (0, 0, 255), pos * CELL_SIZE, (pos + v * ratio) * CELL_SIZE, 3
            )
            pygame.draw.circle(screen, (255, 0, 0), pos * CELL_SIZE, 2)

    for x in range(GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = np.array([sign(x_mac[y, x]) * np.log(1 + abs(x_mac[y, x])), 0])
            pygame.draw.line(
                screen,
                (0, 225, 0),
                pos * CELL_SIZE,
                (pos + v * ratio) * CELL_SIZE,
                3,
            )
            pygame.draw.circle(screen, (255, 0, 0), pos * CELL_SIZE, 2)
