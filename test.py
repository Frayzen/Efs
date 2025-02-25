import numpy as np

# Initialize the velocity arrays
x_mac = np.zeros((2, 3))  # X velocities at cell faces
y_mac = np.zeros((3, 2))  # Y velocities at cell faces
x_mac[1, 1] = 1  # Initial condition for velocity
x_mac[0, 1] = -1

# Apply boundary conditions: set edge velocities to zero
x_mac[:, 0] = 0  # Left edge
x_mac[:, -1] = 0  # Right edge
y_mac[0, :] = 0  # Top edge
y_mac[-1, :] = 0  # Bottom edge


def div():

    # Calculate the divergence based on the updated velocities
    d1 = (x_mac[0, 0] - x_mac[0, 1]) + (y_mac[1, 0] - y_mac[0, 0])  # Bottom left
    d2 = (x_mac[0, 1] - x_mac[0, 2]) + (y_mac[1, 1] - y_mac[0, 1])  # Bottom right
    d3 = (x_mac[1, 0] - x_mac[1, 1]) + (y_mac[2, 0] - y_mac[1, 0])  # Top left
    d4 = (x_mac[1, 1] - x_mac[1, 2]) + (y_mac[2, 1] - y_mac[1, 1])  # Top right

    # Create the divergence array for each cell (2x2 grid)
    divergence_array = np.array([[d1, d2], [d3, d4]])

    print("Divergence array:\n", divergence_array)
    return divergence_array


def solve_mac_pressure_system():
    # Matrix A (4x4) for the pressure equation
    A = np.array(
        [
            [-2, 1, 1, 0],  # p_0,0
            [1, -4, 0, 1],  # p_1,0
            [1, 0, -4, 1],  # p_0,1
            [0, 1, 1, -2],  # p_1,1
        ],
        dtype=float,
    )

    # Right-hand side vector b (length 4)
    b = div().ravel()

    # Solve the system
    pressure = np.linalg.solve(A, b)
    return pressure


def update_velocities(pressure):

    # Calculate the pressure gradient (central difference)
    dp_dx = pressure[1] - pressure[0]
    dp_dx2 = pressure[3] - pressure[2]
    dp_dy = pressure[2] - pressure[0]
    dp_dy2 = pressure[3] - pressure[1]
    print("x1 =", dp_dx)
    print("x2 =", dp_dx2)
    print("y1 =", dp_dy)
    print("y2 =", dp_dy2)

    # Update x velocities based on pressure gradient
    x_mac[0, 1] += dp_dx  # Update u at (0,1) face
    x_mac[1, 1] += dp_dx2  # Update u at (1,0) face

    # Update y v+locities based on pressure gradient
    y_mac[1, 0] -= dp_dy  # Update v at (0,0) face
    y_mac[1, 1] -= dp_dy2  # Update v at (1,0) face


if __name__ == "__main__":
    pressure_values = solve_mac_pressure_system()
    print("Pressure values:", pressure_values)

    # Update velocities based on pressure values
    update_velocities(pressure_values)
    print("Updated X Velocities (x_mac):")
    print(x_mac)
    print("Updated Y Velocities (y_mac):")
    print(y_mac)
    div()
