import numpy as np
import cupyx.scipy.sparse as sp

CELL_SIZE = 90  # Pixel size of each cell
GRID_WIDTH = 3  # Number of cells horizontally
GRID_HEIGHT = 3  # Number of cells vertically

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

dt = 0.001
