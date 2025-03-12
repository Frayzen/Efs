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

    def draw(self):
        # X
        for x in range(WIDTH + 1):
            for y in range(HEIGHT):
                pos = np.array([x, y + 0.5])
                val = np.array([self.xgrid[y, x], 0])
                draw_line(pos, pos + val, RED)
        # Y
        for x in range(WIDTH):
            for y in range(HEIGHT + 1):
                pos = np.array([x + 0.5, y])
                val = np.array([0, self.ygrid[y, x]])
                draw_line(pos, pos + val, RED)

    def draw_centers(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pos = np.array([x + 0.5, y + 0.5])
                val = self.interpolate_velocity(pos)
                draw_line(pos, pos + val, RED)

    def draw_mouse(self):
        x, y = get_mouse_coords()
        pos = np.array([x, y])
        val = self.interpolate_velocity(pos)
        draw_circle((x, y), GREEN, 2)
        draw_line(pos, pos + val, GREEN)

    def interpolate_velocity(self, pos):
        return np.array(
            [
                self.interpolate_x(pos),
                # self.interpolate_y(pos),
                0,
            ]
        )

    def interpolate_y(self, pos):

        v = self.ygrid
        px, py = pos[0], pos[1]

        i = clamp(int(px - 0.5), 0, WIDTH - 1)
        j = clamp(int(py), 0, HEIGHT - 1)

        x = clamp(px - (i + 0.5), 0, WIDTH)
        y = clamp(j + 1 - py, 0, HEIGHT)
        print(pos)
        print(x, y)
        assert x >= 0 and x <= 1 and y >= 0 and y <= 1

        w00 = 1 - x
        w10 = 1 - y
        w01 = x
        w11 = y

        return (
            w00 * w10 * v[j, i]
            + w01 * w10 * v[i + 1, j]
            + w01 * w11 * v[j + 1, i]
            + w00 * w11 * v[j + 1, i + 1]
        )

    def interpolate_x(self, pos):

        u = self.xgrid
        px, py = pos[0], pos[1]

        i = int(px)
        j = int(py + 0.5)

        x = px - i
        y = py - j
        assert x >= 0 and x <= 1 and y >= 0 and y <= 1
        print(j, i)

        w00 = 1 - x
        w10 = 1 - y
        w01 = x
        w11 = y

        ret = 0
        if i >= 0:
            if j > 0:
                ret += w00 * w10 * u[j, i]
            if j < HEIGHT - 1:
                ret += w01 * w11 * u[j + 1, i]
        if i < WIDTH - 1:
            if j > 0:
                ret += w01 * w10 * u[j, i + 1]
            if j < HEIGHT - 1:
                ret += w00 * w11 * u[j + 1, i + 1]
        return ret
