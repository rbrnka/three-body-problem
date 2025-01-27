# 3-Body Problem Simulation in Python/Jupyter Lab

This repository contains a Jupyter Notebook demonstrating how to simulate and animate the classical 3-body problem in 3D I used in my [Unmasking Chaos](https://synaptory.substack.com/p/unmasking-chaos) article. The code uses:
- **NumPy** for numerical operations
- **SciPy** for integrating the differential equations
- **Matplotlib** for plotting and animation

You can interactively rotate the 3D plot using an interactive backend in Jupyter (e.g., `%matplotlib widget` with the `ipympl` package installed), generate simple video or GIF animation.

## Overview

The **3-body problem** describes the motion of three-point masses under their mutual gravitational attraction.

### Equations of Motion

Let $r_i(t)$ be the position vector of the $i$-th body with mass $m_i$, where $i \in [1, 2, 3]$. The equations of motion for each body in a gravitational field are governed by:

```math
\frac{d^2 \mathbf{r}_i}{dt^2}
~=~
G \sum_{j \neq i} m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{\|\mathbf{r}_j - \mathbf{r}_i\|^3},
```

where
- $G$ is the gravitational constant,
- $\mathbf{r}_j$ is the position vector of the $j$-th mass,
- $\|\mathbf{r}_j - \mathbf{r}_i\|$ denotes the Euclidean distance between bodies $i$ and $j$.

In practice, this is turned into a system of first-order ODEs by letting

```math
\mathbf{v}_i = \frac{d \mathbf{r}_i}{dt}.
```

Thus, the state vector is

```math
y = \bigl(x_1, y_1, z_1,\, x_2, y_2, z_2,\, x_3, y_3, z_3,\,
         v_{x1}, v_{y1}, v_{z1},\, v_{x2}, v_{y2}, v_{z2},\, v_{x3}, v_{y3}, v_{z3}\bigr).
```

## Requirements

- **Python 3.7+**  
- **NumPy**  
- **SciPy**  
- **Matplotlib**  
- **ipympl** (only if you want to rotate the 3D animation interactively in JupyterLab using `%matplotlib widget`)

### Installation

```bash
pip install numpy scipy matplotlib ipympl
```
If you are using JupyterLab 3.0 or newer, `ipympl` usually works without extra steps. Otherwise, you may need:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

### Usage
1. Clone or Download this repository.
   ```bash
   git clone https://github.com/rbrnka/three-body-problem.git
2. or copy-paste and run in Jupyter Lab
4. Install the required packages if needed.
5. Run the cells in order.
6. Check the memory limit for the animation. The longer the animation, the more memory is needed. I set my limit to 10 GB but if you have less memory, you need to adjust the `mpl.rcParams['animation.embed_limit'] = yourvalue` (in MB).

### Customizing the Simulation

#### Interactive rotation
Ensure you have the following near the top of the notebook: `%matplotlib widget`. If that doesn't work, you can also try: `%matplotlib notebook` (in the classic Jupyter Notebook environment).

#### Timescale
- Change `t_span` to simulate more (or less) time.
- Adjust `t_eval` to refine or coarsen the solution.

#### Masses, Positions, and Velocities
Experiment with different initial conditions for interesting orbital behaviors. **I recommend keeping the masses of all bodies equal to 1.0 to maintain the visualization within the screen boundaries. Alternatively, you can adjust the initial positions to achieve different results.**

#### Realistic Units
If you use the actual gravitational constant $G \sim 6.6743x10^{-11}$, ensure you have realistic masses (in kg), distances (in m), and time steps (in s). This often requires smaller integration steps and more careful parameter choices.

#### Saving as Video or GIF
- MP4 (requires `ffmpeg`): `ani.save('three_body_animation.mp4', writer='ffmpeg', fps=30)`
- GIF (requires `imagemagick` or `pillow`):
```
from matplotlib.animation import PillowWriter
ani.save('three_body_animation.gif', writer=PillowWriter(fps=30))
```
Watch the simulation. You should see three masses attracting each other, leaving colored trajectories. Use your mouse (in an interactive backend) to rotate and zoom.

![Animation](https://github.com/user-attachments/assets/b8065f24-abe3-44a7-8aed-dd4b9dc813ed)

