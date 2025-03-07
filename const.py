import numpy as np
import scipy.sparse as sp

CELL_SIZE = 15  # Pixel size of each cell
GRID_WIDTH = 25  # Number of cells horizontally
GRID_HEIGHT = 25  # Number of cells vertically

CONSERVATIE_ADVECTION = True

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

dt = 0.001
