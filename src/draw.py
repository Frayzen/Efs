from pygame.math import clamp
import pygame
from consts import (
    GREEN,
    HEIGHT,
    RED,
    WIDTH,
)
import numpy as np

from ui import draw_line


def draw_ui(screen):
    ui_state = {
        "show_vectors": True,
        "paused": False,
        "vector_scale": 0.2,
    }

    font = pygame.font.SysFont("Arial", 16)
    info_lines = [
        f"Paused: {ui_state['paused']}",
        f"Show Vectors: {ui_state['show_vectors']}",
        f"Vector Scale: {ui_state['vector_scale']:.2f}",
        "Press SPACE to pause/resume",
        "Press V to toggle vectors",
        "UP/DOWN to change scale",
    ]

    for i, text in enumerate(info_lines):
        rendered = font.render(text, True, (255, 255, 255))
        screen.blit(rendered, (10, 10 + i * 20))
