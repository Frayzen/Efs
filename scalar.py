import pygame
import math
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

    def draw(self, values=False):
        def map_density_to_color(density):
            adjusted_density = math.log(1 + density) / math.log(1 + 255)
            r = int(255 * adjusted_density)
            g = 0
            b = int(255 * (1 - adjusted_density))

            return (r, g, b)

        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect = (
                    x * CELL_SIZE + 1,
                    y * CELL_SIZE + 1,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1,
                )
                draw_circle((50, 50), RED, 20)

                # color = [clamp(self.field[y, x], 0, 255) or 0] * 3

                color = map_density_to_color(clamp(self.field[y, x], 0, 255))
                pygame.draw.rect(
                    screen,
                    color,
                    rect,
                    CELL_SIZE - 1,
                )
                if values:
                    font = pygame.font.Font(None, 24)
                    density_text = f"{self.field[y,x]:.2f}"
                    text_surface = font.render(
                        density_text, True, (255, 255, 255)
                    )  # White text
                    text_rect = text_surface.get_rect(
                        center=(rect[0] + CELL_SIZE // 2, rect[1] + CELL_SIZE // 2)
                    )
                    screen.blit(text_surface, text_rect)

    def draw_mouse(self):
        x, y = get_mouse_coords()
        pos = np.array([x, y])
        val = self.interpolate_scalar(pos)
        draw_circle((x, y), GREEN, val)

    def interpolate_scalar(self, pos):

        v = self.field
        px, py = pos[0], pos[1]

        i = clamp(px - 0.5, -1, WIDTH - 1)
        if i < 0:
            i = -1
        else:
            i = int(i)

        j = clamp(py - 0.5, -1, HEIGHT - 1)
        if j < 0:
            j = -1
        else:
            j = int(j)

        ic = i + 0.5
        jc = j + 0.5
        # draw_circle((ic, jc), GREEN)
        # draw_circle((ic + 1, jc), RED)
        # draw_circle((ic, jc + 1), WHITE)
        # draw_circle((ic + 1, jc + 1), BLUE)

        x = px - ic
        y = py - jc

        # draw_line((px, py), (px - x, py), BLUE)
        # draw_line((px, py), (px, py - y), BLUE)

        ret = 0
        if i < WIDTH - 1 and j >= 0:
            ret += x * (1 - y) * v[j, i + 1]
        if i < WIDTH - 1 and j < HEIGHT - 1:
            ret += x * y * v[j + 1, i + 1]
        if j < HEIGHT - 1 and i >= 0:
            ret += (1 - x) * y * v[j + 1, i]
        if j >= 0 and i >= 0:
            ret += (1 - x) * (1 - y) * v[j, i]
        return ret
