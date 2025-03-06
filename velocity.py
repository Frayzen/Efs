import pygame
from pygame.math import clamp
from const import *
from grid import *
from velocity import *


def advect():
    global x_mac, y_mac
    pre = np.sum(np.abs(x_mac)) + np.sum(np.abs(y_mac))

    for x in range(1, GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT):
            pos = np.array([x, y + 0.5])
            v = interpolate_velocity(pos)
            nv = interpolate_velocity(pos - v * dt)
            if xmsk[y, x] == 0:
                x_mac[y, x] *= 0.0
            else:
                x_mac[y, x] = nv[0]

    for x in range(GRID_WIDTH):
        for y in range(1, GRID_HEIGHT - 1):
            pos = np.array([x + 0.5, y])
            v = interpolate_velocity(pos)
            nv = interpolate_velocity(pos - v * dt)
            if ymsk[y, x] == 0:
                y_mac[y, x] *= 0.0
            else:
                y_mac[y, x] = nv[1]
    if CONSERVATIE_ADVECTION:
        aft = np.sum(np.abs(x_mac)) + np.sum(np.abs(y_mac))
        x_mac *= pre / aft
        y_mac *= pre / aft


def interpolate_velocity(pos, draw=False):

    global x_mac, y_mac
    px, py = pos[0], pos[1]

    X1 = clamp(int(px - 0.5), 0, GRID_WIDTH - 2)
    Y1 = clamp(int(py - 0.5), 0, GRID_HEIGHT - 2)
    X2 = X1 + 1
    Y2 = Y1 + 1

    x = clamp(int(px), 0, GRID_WIDTH - 2)
    y = clamp(int(py), 0, GRID_HEIGHT - 2)
    ax = abs(px - X1) - 0.5
    bx = py - int(py)
    cx = 1 - ax
    dx = 1 - bx

    ay = px - int(px)
    by = abs(py - Y1) - 0.5
    cy = 1 - ay
    dy = 1 - by
    # if draw:
    #     # X
    #     pygame.draw.circle(  # 0 0
    #         screen, (0, 255, 0), np.array([X1 + 0.5, y]) * CELL_SIZE, dx * cx * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (0, 255, 0), np.array([X1 + 1.5, y]) * CELL_SIZE, ax * dx * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (0, 255, 0), np.array([X1 + 0.5, y + 1]) * CELL_SIZE, bx * cx * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (0, 255, 0), np.array([X1 + 1.5, y + 1]) * CELL_SIZE, ax * bx * 20
    #     )

    #     # Y
    #     pygame.draw.circle(  # 0 0
    #         screen, (255, 255, 0), np.array([x, Y1 + 0.5]) * CELL_SIZE, dy * cy * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (255, 255, 0), np.array([x + 1, Y1 + 0.5]) * CELL_SIZE, ay * dy * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (255, 255, 0), np.array([x, Y1 + 1.5]) * CELL_SIZE, by * cy * 20
    #     )
    #     pygame.draw.circle(
    #         screen, (255, 255, 0), np.array([x + 1, Y1 + 1.5]) * CELL_SIZE, ay * by * 20
    #     )

    return np.array(
        [
            # X
            x_mac[Y1, x] * dy * cy  # top left
            + x_mac[Y1, x + 1] * ay * dy  # top right
            + x_mac[Y2, x] * by * cy  # bottom left
            + x_mac[Y2, x + 1] * ay * by,  # bottom right
            # Y
            y_mac[y, X1] * dx * cx
            + y_mac[y, X2] * ax * dx
            + y_mac[y + 1, X1] * bx * cx
            + y_mac[y + 1, X2] * ax * bx,
        ]
    )
