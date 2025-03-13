import pygame
from pygame.display import iconify
from pygame.draw import circle
from pygame.math import clamp
from consts import *
import numpy as np
from ui import draw_circle, draw_line, screen


def get_mouse_coords():
    return np.array(pygame.mouse.get_pos()) / CELL_SIZE


class ScalarGrid:
    def __init__(self) -> None:
        self.field = np.zeros((HEIGHT, WIDTH))

    def draw(self):
        # X
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect = (
                    x * CELL_SIZE + 1,
                    y * CELL_SIZE + 1,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1,
                )
                draw_circle((50, 50), RED, 20)
                color = [clamp(self.field[y, x] * 20, 0, 225)] * 3
                pygame.draw.rect(
                    screen,
                    color,
                    rect,
                    CELL_SIZE - 1,
                )

    def draw_mouse(self):
        x, y = get_mouse_coords()
        pos = np.array([x, y])
        val = self.interpolate_scalar(pos)
        draw_circle((x, y), GREEN, val)

    def interpolate_scalar(self, pos):

        v = self.field
        px, py = pos[0], pos[1]

        i = clamp(int(px - 0.5), 0, WIDTH - 2)
        j = clamp(int(py - 0.5), 0, HEIGHT - 2)
        ic = i + 0.5
        jc = j + 0.5
        draw_circle((ic, jc), GREEN)
        draw_circle((ic + 1, jc), RED)
        draw_circle((ic, jc + 1), WHITE)
        draw_circle((ic + 1, jc + 1), BLUE)

        x = px - ic
        y = py - jc

        # draw_line((px, py), (px - x, py), BLUE)
        # draw_line((px, py), (px, py - y), BLUE)

        ret = 0

        ret += (1 - x) * (1 - y) * v[j, i]
        ret += (1 - x) * y * v[j + 1, i]
        ret += x * (1 - y) * v[j, i + 1]
        ret += x * y * v[j + 1, i + 1]
        return ret
