def setcheckboard():
    h_grid = np.array(
        [[1000 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)],
        dtype=np.float64,
    )
    w_grid = np.array(
        [[1000 for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)],
        dtype=np.float64,
    )
    w_grid[build_checkerboard(w_grid.shape) == 1] *= -1
    h_grid[build_checkerboard(h_grid.shape) == 1] *= -1
    h_grid *= sh * -1
    w_grid *= sw
