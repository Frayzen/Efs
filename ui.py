# Initialize pygame
import pygame

from consts import PIX_HEIGHT, PIX_WIDTH


pygame.init()
screen = pygame.display.set_mode((PIX_WIDTH, PIX_HEIGHT))
pygame.display.set_caption("Dynamic Grid Colors")
