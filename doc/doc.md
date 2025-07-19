# Fluid Simulation – Math and Concept Overview (for Beginners)

This simulation uses **Computational Fluid Dynamics (CFD)** to model how a fluid moves in 2D. We’re not simulating every water molecule — instead, we split space into a grid and simulate fluid motion at each cell. The method is simplified but captures the **core behavior** of real fluids.

## 1. What's Being Simulated?

We treat the fluid as:
- **Incompressible** (its volume doesn't change)
- **Without viscosity** (no internal friction)
- Interacting with **solid boundaries** (like obstacles)

The main physical laws we enforce:
- **Mass is conserved** → no fluid disappears or appears
- **Incompressibility** → fluid doesn’t squish
- **Advection** → fluid carries itself and other stuff (like smoke) along

---

## 2. The Grid (MAC Grid)

We break the space into a square grid:
- Fluid velocity is stored on the edges of each cell
  - Horizontal velocity (`u`) on vertical edges
  - Vertical velocity (`v`) on horizontal edges
- Quantities like smoke density are stored at the center
- Obstacles are marked in a mask (solid vs fluid)

This setup is called a **MAC grid**, which avoids numerical problems and makes things more accurate.

---

## 3. Advection – How Fluid Carries Things

**Advection** is how quantities like velocity and smoke move with the flow.

We trace each cell **backward in time**:
1. Look at the velocity at a point
2. Go back by `velocity × time_step`
3. Sample the old value from that location

This lets us update:
- The velocity field (fluid moves itself)
- The smoke or dye density (carried by fluid)

This is called **semi-Lagrangian advection** — stable and simple.

---

## 4. Enforcing Incompressibility (Projection)

After moving the fluid, the result might not be divergence-free (i.e. compressible). To fix this, we **project** the velocity field to make it incompressible.

We solve for a pressure-like correction that removes divergence:

$$
\nabla \cdot \vec{v} = 0
$$

If a cell has excess inflow or outflow, we adjust nearby velocities to balance it out. This step is key to making the fluid behave realistically — forming swirls instead of expanding unnaturally.

---

## 5. Solid Boundaries (Obstacles)

Solid cells are marked in a grid. We make sure fluid doesn't enter these by setting their velocities to zero. This allows us to simulate things like fluid flowing around rocks or walls.

---

## 6. Summary of Fluid Steps

Each frame of the simulation does:
1. **Advect velocities** (fluid carries itself)
2. **Advect density** (fluid carries smoke/dye)
3. **Enforce incompressibility** (make velocity divergence-free)

This loop repeats every timestep to animate the fluid.

---

## 7. The Core Equations (for context)

We’re solving a simplified version of the **Navier–Stokes equations**:

$$
\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla) \vec{v} = -\nabla p \quad \text{(momentum)}
$$

$$
\nabla \cdot \vec{v} = 0 \quad \text{(incompressibility)}
$$

We ignore viscosity and external forces for now. Our method focuses on the core of fluid motion — how velocity and density evolve under these rules.

---

## Final Notes

This simulation gives **believable fluid motion** using relatively simple math and a structured grid. It's great for smoke-like effects or educational purposes. If you're new to CFD, focus on:
- Understanding the steps (advect, project, repeat)
- Thinking about how quantities move and interact

Let me know if you want visuals or examples to go along with this!


