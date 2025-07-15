## Fluid Simulation Math Explanation

This simulation implements a basic **incompressible fluid solver** using a grid-based **MAC (Marker-and-Cell)** method. The simulation follows the classic fluid pipeline:

### 1. MAC Grid Overview

The MAC grid stores:
- Horizontal velocities ($u$) on vertical cell edges
- Vertical velocities ($v$) on horizontal cell edges
- Scalar quantities (e.g. density $\rho$) at cell centers
- A solid mask $s$ with 1 indicating fluid and 0 indicating obstacles

### 2. Velocity Advection

We use **semi-Lagrangian advection** to update the velocity field.

For each velocity component (e.g., $u$ or $v$), we:
- Trace backward in time using the current velocity vector $\vec{v}$
- Sample the velocity at that previous position using interpolation
- Assign the sampled value to the current cell

In equations:

$$
\vec{x}_{\text{new}} = \vec{x} - \vec{v}(\vec{x}) \cdot \Delta t
$$

Then:

$$
u(i, j) = u(\vec{x}_{\text{new}})
$$

To maintain global energy when `CONSERVATIVE_ADVECTION=True`, we normalize the velocity magnitude:

$$
\text{scale} = \frac{\sum |u_{\text{before}}| + |v_{\text{before}}|}{\sum |u_{\text{after}}| + |v_{\text{after}}|}
$$

Then scale the grid.

### 3. Scalar Advection (e.g., Density)

Same as velocity advection, but applied to the scalar field:

$$
\rho(i, j) = \rho(\vec{x} - \vec{v}(\vec{x}) \cdot \Delta t)
$$

If `CONSERVATIVE_SCALAR=True`, we also preserve total mass by rescaling:

$$
\rho = \rho \cdot \frac{\text{total before}}{\text{total after}}
$$

### 4. Obstacle Handling

For each obstacle cell, velocities at the edges are set to zero, ensuring no fluid enters the obstacle:

```python
grid.xgrid[y, x] = 0
grid.ygrid[y, x] = 0
```

The solid mask `s` is used to check whether a cell is fluid or solid.

### 5. Projection Step (Clear Divergence)

To enforce **incompressibility** ($\nabla \cdot \vec{v} = 0$), we:
- Loop over each cell and compute the discrete divergence:

$$
\nabla \cdot \vec{v}_{i,j} = u_{i+1,j} - u_{i,j} + v_{i,j+1} - v_{i,j}
$$

- If divergence is non-zero, apply a pressure-like correction:

$$
u_{i,j} \mathrel{+}= \frac{d \cdot s_{i,j-1}}{c} \quad,\quad u_{i+1,j} \mathrel{-}= \frac{d \cdot s_{i,j+1}}{c}
$$

$$
v_{i,j} \mathrel{+}= \frac{d \cdot s_{i-1,j}}{c} \quad,\quad v_{i,j+1} \mathrel{-}= \frac{d \cdot s_{i+1,j}}{c}
$$

Where $d$ is the local divergence and $c$ is the number of neighboring fluid cells.

Optionally, `OVERRELAXATION` multiplies divergence $d$ by 1.9 for faster convergence (similar to Gauss-Seidel overrelaxation).

### 6. Time Integration

The simulation steps through time with:

$$
t_{n+1} = t_n + \Delta t
$$

With each step calling:
- `advect_velocities()`
- `advect_scalar()`
- `clear_divergence()`

### 7. Visualization

- Density is rendered as grayscale
- Obstacle cells are visualized via a solid mask
- Velocity vectors can be visualized with line segments

### Summary

This implementation solves the **Navier-Stokes equations** in an incompressible, inviscid form:

$$
\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v} = -\nabla p \\
\nabla \cdot \vec{v} = 0
$$

Using:
- Semi-Lagrangian advection
- Explicit pressure projection
- MAC grid discretization

