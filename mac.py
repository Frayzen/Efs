import pygame
from pygame.math import clamp
from consts import *
import numpy as np
from ui import screen


class MacGrid:
    def __init__(self) -> None:
        self.xgrid = [HEIGHT, WIDTH + 1]
        self.ygrid = [HEIGHT + 1, WIDTH]

    def draw(self):
        # X
        for x in range(WIDTH + 1):
            for y in range(HEIGHT):
                pos = np.array([x, y + 0.5])
                val = np.array([self.xgrid[y, x], 0])
                pygame.draw.line(screen, RED, pos, pos + val)
        # Y
        for x in range(WIDTH):
            for y in range(HEIGHT + 1):
                pos = np.array([x + 0.5, y])
                val = np.array([0, self.ygrid[y, x]])
                pygame.draw.line(screen, RED, pos, pos + val)

    def draw_centers(self):
        # X
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pos = np.array([x + 0.5, y + 0.5])
                val = np.array([self.xgrid[y, x], 0])
                pygame.draw.line(screen, RED, pos, pos + val)

    def interpolate_velocity(self, pos):

        px, py = pos[0], pos[1]

        X1 = clamp(int(px - 0.5), 0, WIDTH - 2)
        Y1 = clamp(int(py - 0.5), 0, HEIGHT - 2)
        X2 = X1 + 1
        Y2 = Y1 + 1

        x = clamp(int(px), 0, WIDTH - 2)
        y = clamp(int(py), 0, HEIGHT - 2)
        ax = abs(px - X1) - 0.5
        bx = py - int(py)
        cx = 1 - ax
        dx = 1 - bx

        ay = px - int(px)
        by = abs(py - Y1) - 0.5
        cy = 1 - ay
        dy = 1 - by
        return np.array(
            [
                # X
                self.xgrid[Y1, x] * dy * cy  # top left
                + self.xgrid[Y1, x + self.1] * ay * dy  # top right
                + self.xgrid[Y2, x] * by * cy  # bottom left
                + self.xgrid[Y2, x + self.1] * ay * by,  # bottom right
                # Y
                ,
                self.ygrid[y, X1] * dx * cx,
                + self.ygrid[y, X2] * ax * dx
                + self.ygrid[y + self.1, X1] * bx * cx
                + self.ygrid[y + self.1, X2] * ax * bx,
            ]
        )
