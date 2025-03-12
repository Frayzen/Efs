import pygame

import pygame
import time
import numpy as np
from pygame.math import clamp
from ui import screen

from consts import CELL_SIZE, HEIGHT, PIX_HEIGHT, PIX_WIDTH, RED, WHITE, WIDTH


def get_mouse_coords():
    return np.array(pygame.mouse.get_pos()) // CELL_SIZE


def draw_cells():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            rect = (
                i * CELL_SIZE,
                j * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, WHITE, rect, 1)


while True:
    draw_cells()
    pygame.display.flip()
