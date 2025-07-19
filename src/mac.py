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
                draw_line(pos, pos + val, PINK)
        # Y
        for x in range(WIDTH):
            for y in range(HEIGHT + 1):
                pos = np.array([x + 0.5, y])
                val = np.array([0, self.ygrid[y, x]])
                draw_line(pos, pos + val, PINK)

    # def draw_centers(self):
    #     for x in range(WIDTH):
    #         for y in range(HEIGHT):
    #             pos = np.array([x + 0.5, y + 0.5])
    #             val = self.interpolate_velocity(pos)
    #             if np.sum(np.abs(val)) > 0:
    #                 draw_circle(pos, GREEN, 2)
    #                 draw_line(pos, pos + val * 0.2, RED)



    def draw_centers(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pos = np.array([x + 0.5, y + 0.5])
                val = self.interpolate_velocity(pos)
                if np.sum(np.abs(val)) > 0:
                    draw_circle(pos + val *0.2,GREEN, radius=3)
                    draw_line(pos, pos + val * 0.2, RED)


    def draw_s(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.s[y + 1, x + 1] == 0:

                    rect = (
                        x * CELL_SIZE + 1,
                        y * CELL_SIZE + 1,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1,
                    )

                    # color = [clamp(self.field[y, x], 0, 255) or 0] * 3

                    pygame.draw.rect(
                        screen,
                        [200] * 3,
                        rect,
                        CELL_SIZE - 1,
                    )

    def draw_mouse(self):
        x, y = get_mouse_coords()
        pos = np.array([x, y])
        val = self.interpolate_velocity(pos)
        draw_circle((x, y), GREEN, 2)
        draw_line(pos, pos + val, WHITE)

    def interpolate_velocity(self, pos):

        return np.array(
            [
                self.interpolate_x(pos),
                # 0,
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

        # draw_circle((i + 0.5, j), GREEN)
        # draw_circle((i + 1.5, j), RED)
        # draw_circle((i + 0.5, j + 1), WHITE)
        # draw_circle((i + 1.5, j + 1), BLUE)

        x = px - i - 0.5
        y = py - j

        # draw_line((px, py), (px - x, py), BLUE)
        # draw_line((px, py), (px, py - y), BLUE)

        ret = 0
        if i >= 0 and i < WIDTH:
            ret += (1 - x) * (1 - y) * v[j, i]
            ret += (1 - x) * y * v[j + 1, i]
        if i < HEIGHT - 1:
            ret += x * (1 - y) * v[j, i + 1]
            ret += x * y * v[j + 1, i + 1]
        return ret

    # def draw_s(self):
    #     for x in range(1, WIDTH):
    #         for y in range(1, HEIGHT):
    #             if self.s[y, x] == 0:
    #                 pygame.draw.rect(
    #                     screen,
    #                     RED,
    #                     (
    #                         x * CELL_SIZE,
    #                         y * CELL_SIZE,
    #                         CELL_SIZE,
    #                         CELL_SIZE,
    #                     ),
    #                     10,
    #                 )

    def interpolate_x(self, pos):

        u = self.xgrid
        px, py = pos[0], pos[1]

        i = int(px)
        j = py - 0.5

        if j >= 0:
            j = int(j)
        else:
            j = -1

        # draw_circle((i, j + 0.5), GREEN)
        # draw_circle((i + 1, j + 0.5), RED)
        # draw_circle((i, j + 1.5), WHITE)
        # draw_circle((i + 1, j + 1.5), BLUE)

        x = px - i
        y = py - j - 0.5

        # draw_line((px, py), (px - x, py), BLUE)
        # draw_line((px, py), (px, py - y), BLUE)

        ret = 0
        if j >= 0 and j < HEIGHT:
            ret += (1 - x) * (1 - y) * u[j, i]
            ret += x * (1 - y) * u[j, i + 1]
        if j < HEIGHT - 1:
            ret += (1 - x) * y * u[j + 1, i]
            ret += x * y * u[j + 1, i + 1]

        return ret
