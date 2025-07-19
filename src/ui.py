# Initialize pygame
import pygame
import numpy as np

from consts import CELL_SIZE, PIX_HEIGHT, PIX_WIDTH, RED


pygame.init()
screen = pygame.display.set_mode((PIX_WIDTH, PIX_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")


def draw_line(start, dest, color=RED, width=2):
    start = np.array(start)
    dest = np.array(dest)
    pygame.draw.line(screen, color, start * CELL_SIZE, dest * CELL_SIZE, width)


def draw_circle(center, color=RED, radius=5):
    center = np.array(center)
    pygame.draw.circle(screen, color, center * CELL_SIZE, radius)
