import numpy as np
import cupyx.scipy.sparse as sp

CELL_SIZE = 50  # Pixel size of each cell
GRID_WIDTH = 5  # Number of cells horizontally
GRID_HEIGHT = 10  # Number of cells vertically

# Window settings
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

dt = 0.001
