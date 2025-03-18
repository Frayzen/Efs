import pygame
from pygame.math import clamp
from consts import *
import numpy as np
from ui import draw_circle, draw_line, screen


def get_mouse_coords_int():
    return np.array(pygame.mouse.get_pos()) // CELL_SIZE


def get_mouse_coords():
    return np.array(pygame.mouse.get_pos()) / CELL_SIZE


class MacGrid:
    def __init__(self) -> None:
        self.xgrid = np.zeros((HEIGHT, WIDTH + 1))
        self.ygrid = np.zeros((HEIGHT + 1, WIDTH))
        self.s = np.ones((HEIGHT, WIDTH))
        self.s = np.pad(self.s, pad_width=1, mode="constant", constant_values=0)

    def draw(self, weight=1.0):
        # X
        for x in range(WIDTH + 1):
            for y in range(HEIGHT):
                pos = np.array([x, y + 0.5])
                val = weight * np.array([self.xgrid[y, x], 0])
                draw_line(pos, pos + val, RED)
        # Y
        for x in range(WIDTH):
            for y in range(HEIGHT + 1):
                pos = np.array([x + 0.5, y])
                val = weight * np.array([0, self.ygrid[y, x]])
                draw_line(pos, pos + val, RED)

    def draw_centers(self, weight=1.0):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pos = np.array([x + 0.5, y + 0.5])
                val = self.interpolate_velocity(pos) * weight
                if np.sum(np.abs(val)) > 0:
                    draw_circle(pos, GREEN, 2)
                draw_line(pos, pos + val, BLUE)

    def draw_mouse(self, weight=1.0):
        x, y = get_mouse_coords()
        pos = np.array([x, y])
        val = self.interpolate_velocity(pos, True) * weight
        # print("val - ", val)
        draw_circle((x, y), GREEN, 2)
        draw_line(pos, pos + val, RED, 3)

    def interpolate_velocity(self, pos, draw=False):

        return np.array(
            [
                self.interpolate_x(pos, draw),
                # 0,
                self.interpolate_y(pos, False),
            ]
        )

    def interpolate_y(self, pos, draw=False):

        v = self.ygrid
        px, py = pos[0], pos[1]

        i = px - 0.5
        j = int(py)

        if i >= 0:
            i = int(i)
        else:
            i = -1

        x = px - i - 0.5
        y = py - j
        assert x >= 0 and x <= 1
        assert y >= 0 and x <= 1

        if draw:
            draw_circle((i + 0.5, j), GREEN)
            draw_circle((i + 1.5, j), RED)
            draw_circle((i + 0.5, j + 1), WHITE)
            draw_circle((i + 1.5, j + 1), BLUE)
            draw_line((px, py), (px - x, py), BLUE)
            draw_line((px, py), (px, py - y), BLUE)

        ret = 0
        if i >= 0 and i < WIDTH:
            ret += (1 - x) * (1 - y) * v[j, i]
            ret += (1 - x) * y * v[j + 1, i]
        if i < HEIGHT - 1:
            ret += x * (1 - y) * v[j, i + 1]
            ret += x * y * v[j + 1, i + 1]
        return ret

    def draw_s(self):
        for x in range(1, WIDTH + 1):
            for y in range(1, HEIGHT + 1):
                if self.s[y, x] == 0:
                    pygame.draw.rect(
                        screen,
                        RED,
                        (
                            (x - 1) * CELL_SIZE,
                            (y - 1) * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        ),
                    )

    def interpolate_x(self, pos, draw=False):

        u = self.xgrid
        px, py = pos[0], pos[1]

        i = int(px)
        j = py - 0.5

        if j >= 0:
            j = int(j)
        else:
            j = -1

        x = px - i
        y = py - j - 0.5

        assert x >= 0 and x <= 1
        assert y >= 0 and x <= 1

        if draw:
            draw_circle((i, j + 0.5), GREEN)
            draw_circle((i + 1, j + 0.5), RED)
            draw_circle((i, j + 1.5), WHITE)
            draw_circle((i + 1, j + 1.5), BLUE)
            draw_line((px, py), (px - x, py), BLUE)
            draw_line((px, py), (px, py - y), BLUE)

        ret = 0
        if j >= 0 and j < HEIGHT:
            ret += (1 - x) * (1 - y) * u[j, i]
            ret += x * (1 - y) * u[j, i + 1]
        if j < HEIGHT - 1:
            ret += (1 - x) * y * u[j + 1, i]
            ret += x * y * u[j + 1, i + 1]

        return ret
