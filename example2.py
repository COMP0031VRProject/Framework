import numpy as np

from Bot import *
from World import *
from Utils import *

mesh = generate_rectangle_mesh_grid((0,0), (3, -2), 2, 3)

vmesh = generate_rectangle_mesh_grid((0,0), (100, -100), 20, 20)
rmesh = vmesh.copy()

transformation = np.eye(2) * (1 / 5)
rmesh.verts = [np.matmul(x, transformation) for x in rmesh.verts]

# Initialize the Bot
bot = Bot(speed=0.1)

# Initial Virtual Position of the Bot
start_position = np.array([25, -25])

# Goals / Flags for the Bot
targets = [[75, -25], [75, -75], [25, -75], [25, -25]]
targets = [np.array(t) for t in targets]

# Initialize the world for homogeneous scaling
world = World(vmesh, rmesh, start_position, bot, targets)
rRecord, vRecord = world.simulate()

# Visualize all
fig, axs = plt.subplots(1,1)
axs.set_aspect('equal')
visualize_mesh(axs, vmesh)
visualize_records(axs, vRecord)
visualize_targets(axs, targets)

fig, axs = plt.subplots(1,1)
axs.set_aspect('equal')
visualize_mesh(axs, rmesh)
visualize_records(axs, rRecord)

plt.show()
