# Three-body problem simulation (c) Radim Brnka 2025
# 
# This notebook script will generate a video animation of three-body numerical integration attractor in a bounded environment.
# Developed for the Unmasking Chaos artile, https://synaptory.substack.com/p/unmasking-chaos

%matplotlib notebook

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import HTML

import matplotlib as mpl
mpl.rcParams['animation.embed_limit'] = 10000  # in MB, adjust as needed

# Gravitational constant (don't use the real one, as it won't work :))
G = 1

# Masses (it's easier to have same masses to keep the trajectories within te boundary box
m1, m2, m3 = 1.0, 1.0, 1.0 

# Initial positions (with a small z-offset to ensure 3D variation)
r1_0 = np.array([-1.0,  0.0,  0.1])
r2_0 = np.array([ 1.0,  0.0, -0.1])
r3_0 = np.array([ 0.0,  1.0,  0.0])

# Initial velocities
v1_0 = np.array([0.0,  0.3,  0.0])
v2_0 = np.array([0.0, -0.3,  0.0])
v3_0 = np.array([0.0,  0.0,  0.1])

y0 = np.concatenate([r1_0, r2_0, r3_0, v1_0, v2_0, v3_0])

t_span = (0, 120.0)
t_eval = np.linspace(t_span[0], t_span[1], 2000)

def three_body_equations(t, y):
    x1, y1, z1, x2, y2, z2, x3, y3, z3, vx1, vy1, vz1, vx2, vy2, vz2, vx3, vy3, vz3 = y

    r1 = np.array([x1, y1, z1])
    r2 = np.array([x2, y2, z2])
    r3 = np.array([x3, y3, z3])

    r12 = r2 - r1
    r13 = r3 - r1
    r23 = r3 - r2

    dist12 = np.linalg.norm(r12)
    dist13 = np.linalg.norm(r13)
    dist23 = np.linalg.norm(r23)

    a1 = G * (m2 * r12/dist12**3 + m3 * r13/dist13**3)
    a2 = G * (m1 * (-r12)/dist12**3 + m3 * r23/dist23**3)
    a3 = G * (m1 * (-r13)/dist13**3 + m2 * (-r23)/dist23**3)

    return [
        vx1, vy1, vz1,
        vx2, vy2, vz2,
        vx3, vy3, vz3,
        a1[0], a1[1], a1[2],
        a2[0], a2[1], a2[2],
        a3[0], a3[1], a3[2]
    ]

sol = solve_ivp(three_body_equations, t_span, y0, t_eval=t_eval, rtol=1e-9, atol=1e-9)
print("Integration successful:", sol.success)

x1_sol, y1_sol, z1_sol = sol.y[0], sol.y[1], sol.y[2]
x2_sol, y2_sol, z2_sol = sol.y[3], sol.y[4], sol.y[5]
x3_sol, y3_sol, z3_sol = sol.y[6], sol.y[7], sol.y[8]

# Test a static plot to ensure data is visible
fig_static = plt.figure()
ax_static = fig_static.add_subplot(111, projection='3d')
ax_static.plot(x1_sol, y1_sol, z1_sol, 'r-', label='Body 1')
ax_static.plot(x2_sol, y2_sol, z2_sol, 'g-', label='Body 2')
ax_static.plot(x3_sol, y3_sol, z3_sol, 'b-', label='Body 3')
ax_static.legend()
ax_static.set_xlim(-20, 20)
ax_static.set_ylim(-20, 20)
ax_static.set_zlim(-20, 20)
plt.show()

# Now set up the animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

line1, = ax.plot([], [], [], 'r-', lw=1)
line2, = ax.plot([], [], [], 'g-', lw=1)
line3, = ax.plot([], [], [], 'b-', lw=1)

point1, = ax.plot([], [], [], 'ro', markersize=6*m1*m1)
point2, = ax.plot([], [], [], 'go', markersize=6*m2*m2)
point3, = ax.plot([], [], [], 'bo', markersize=6*m3*m3)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3-Body Problem Simulation')

def init():
    line1.set_data([], [])
    line1.set_3d_properties([])

    line2.set_data([], [])
    line2.set_3d_properties([])

    line3.set_data([], [])
    line3.set_3d_properties([])

    point1.set_data([], [])
    point1.set_3d_properties([])
    point2.set_data([], [])
    point2.set_3d_properties([])
    point3.set_data([], [])
    point3.set_3d_properties([])
    return line1, line2, line3, point1, point2, point3

def update(frame):
    # Update lines (full trajectory up to 'frame')
    line1.set_data(x1_sol[:frame], y1_sol[:frame])
    line1.set_3d_properties(z1_sol[:frame])

    line2.set_data(x2_sol[:frame], y2_sol[:frame])
    line2.set_3d_properties(z2_sol[:frame])

    line3.set_data(x3_sol[:frame], y3_sol[:frame])
    line3.set_3d_properties(z3_sol[:frame])

    # Update points (just the current position)
    # Wrap single values in lists to provide sequences
    point1.set_data([x1_sol[frame]], [y1_sol[frame]])
    point1.set_3d_properties([z1_sol[frame]])

    point2.set_data([x2_sol[frame]], [y2_sol[frame]])
    point2.set_3d_properties([z2_sol[frame]])

    point3.set_data([x3_sol[frame]], [y3_sol[frame]])
    point3.set_3d_properties([z3_sol[frame]])

    return line1, line2, line3, point1, point2, point3

ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, interval=20, blit=False)

plt.show()

# If the interactive plot doesn't appear for some reason, use to_jshtml as a fallback or generage GIF
# HTML(ani.to_jshtml())
# ani.save('animation.gif', writer='imagemagick', fps=30)
