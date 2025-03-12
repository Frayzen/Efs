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
        print("val - ", val)
        draw_circle((x, y), GREEN, 2)
        draw_line(pos, pos + val, WHITE)

    def interpolate_velocity(self, pos):
        return np.array(
            [
                self.interpolate_x(pos),
                self.interpolate_y(pos),
            ]
        )

    def interpolate_y(self, pos):

        v = self.ygrid
        px, py = pos[0], pos[1]

        i = px - 0.5
        j = int(py)

        if i >= 0:
            i = int(i)
        else:
            i = -1

        draw_circle((i + 0.5, j), GREEN)
        draw_circle((i + 1.5, j), GREEN)
        draw_circle((i + 0.5, j + 1), GREEN)
        draw_circle((i + 1.5, j + 1), GREEN)

        x = px - i - 0.5
        y = py - j

        draw_line((px, py), (px - x, py), BLUE)
        draw_line((px, py), (px, py - y), BLUE)

        w00 = 1 - x
        w10 = 1 - y
        w01 = x
        w11 = y

        ret = 0

        # print(i, i + 1)
        if i > 0:
            ret += w00 * w10 * v[j, i]
            ret += w00 * w11 * v[j + 1, i]
        elif i < WIDTH - 1:
            ret += w01 * w10 * v[j, i + 1]
            ret += w01 * w11 * v[j + 1, i + 1]

        return ret

    def interpolate_x(self, pos):

        u = self.xgrid
        px, py = pos[0], pos[1]

        i = int(px)
        j = py - 0.5
        if j >= 0:
            j = int(j)
        else:
            j = -1

        draw_circle((i, j + 0.5), GREEN)
        draw_circle((i, j + 1.5), GREEN)
        draw_circle((i + 1, j + 0.5), GREEN)
        draw_circle((i + 1, j + 1.5), GREEN)

        x = px - i
        y = py - j - 0.5

        draw_line((px, py), (px - x, py), BLUE)
        draw_line((px, py), (px, py - y), BLUE)

        w00 = 1 - x
        w10 = 1 - y
        w01 = x
        w11 = y

        ret = 0

        print(j, j + 1)
        if j > 0:
            ret += w00 * w10 * u[j, i]
            ret += w01 * w10 * u[j, i + 1]
        elif j < HEIGHT - 1:
            ret += w01 * w11 * u[j + 1, i]
            ret += w00 * w11 * u[j + 1, i + 1]

        return ret
