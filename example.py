import numpy as np

from Bot import *
from World import *
from Utils import *

# Generate the three Meshes
n = 20

virtual = generate_embedded_polygon_mesh(n, 5, 2, (0,0))

homogeneous_scaling_k_real = virtual.copy()
center = homogeneous_scaling_k_real.verts[0]
k = 2
for i,v in enumerate(homogeneous_scaling_k_real.verts):
    # Move all vertices towards center
    homogeneous_scaling_k_real.verts[i] = np.array([(v[0] - center[0]) / k + center[0], (v[1] - center[1]) / k + center[1]])

warped = homogeneous_scaling_k_real.copy()
center = warped.verts[0]
for i in range(1, n + 1):
    # Move vertices of inner circle away from center
    v = warped.verts[i]
    warped.verts[i] = np.array([(v[0] - center[0]) * k + center[0], (v[1] - center[1]) * k + center[1]])

# Initialize the Bot
bot = Bot(speed=0.1)

# Initial Virtual Position of the Bot
start_position = np.array([-5.0,5.0])

# Goals / Flags for the Bot
targets = [[5.0,5.0], [5.0,-5.0], [-5.0,-5.0], [-5.0,5.0]]
targets = [np.array(t) for t in targets]

# Initialize the world for homogeneous scaling
homo_world = World(virtual, homogeneous_scaling_k_real, start_position, bot, targets)
homo_rRecord, homo_vRecord = homo_world.simulate()

# Initialize the world for area of interest (Choi's method)
aoi_world = World(virtual, warped, start_position, bot, targets)
aoi_rRecord, aoi_vRecord = aoi_world.simulate()

# Visualize all
fig, axs = plt.subplots(2,2)

# Real World Trajectory for homogeneous scaling
axs[0][0].set_xlim((-10, 10))
axs[0][0].set_ylim((-10, 10))
axs[0][0].set_aspect('equal')
axs[0][0].set_title('Real World Trajectory for homogeneous scaling')
visualize_records(axs[0][0], homo_rRecord)
visualize_mesh(axs[0][0], homogeneous_scaling_k_real)
# Virtual World Trajectory for homogeneous scaling
axs[0][1].set_xlim((-10, 10))
axs[0][1].set_ylim((-10, 10))
axs[0][1].set_aspect('equal')
axs[0][1].set_title('Virtual World Trajectory for homogeneous scaling')
visualize_records(axs[0][1], homo_vRecord)
visualize_mesh(axs[0][1], virtual)
visualize_targets(axs[0][1], targets)
# Real World Trajectory for Choi's method
axs[1][0].set_xlim((-10, 10))
axs[1][0].set_ylim((-10, 10))
axs[1][0].set_aspect('equal')
axs[1][0].set_title('Real World Trajectory for Choi\'s method')
visualize_records(axs[1][0], aoi_rRecord)
visualize_mesh(axs[1][0], warped)
# Virtual World Trajectory for Choi's method
axs[1][1].set_xlim((-10, 10))
axs[1][1].set_ylim((-10, 10))
axs[1][1].set_aspect('equal')
axs[1][1].set_title('Virtual World Trajectory for Choi\'s method')
visualize_records(axs[1][1], aoi_vRecord)
visualize_mesh(axs[1][1], virtual)
visualize_targets(axs[1][1], targets)

plt.show()