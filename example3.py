import numpy as np
from Bot import *
from World import *
from Utils import *
from Mesh import *
import matplotlib.pyplot as plt
import math

mesh1 = Mesh(None, None)
mesh1.loadNodeAndEle('generated_files\\original.1.node', 'generated_files\\original.1.ele')

mesh2 = Mesh(None, None)
mesh2.loadNodeAndEle('generated_files\\expanded.1.node', 'generated_files\\expanded.1.ele')

# Initialize the Bot
bot = Bot(speed=0.1)

# Initial Virtual Position of the Bot
start_position = np.array([0., 0.])

# Goals / Flags for the Bot
first = (4, 0)
centers = [first]
theta = 2 * math.pi / 6
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)
rotate = lambda coord : (coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta)
for i in range(5):
    centers.append(rotate(centers[-1]))
targets = [c for c in centers] + [centers[1]]
targets = [np.array(t) for t in targets]

# Initialize the world for homogeneous scaling
world = World(mesh1, mesh2, start_position, bot, targets)
rRecord, vRecord = world.simulate()

fig, axs = plt.subplots(1,2)
axs[0].set_aspect('equal')
visualize_mesh(axs[0], mesh1)
visualize_targets(axs[0], targets)
visualize_records(axs[0], vRecord)

axs[1].set_aspect('equal')
visualize_mesh(axs[1], mesh2)
visualize_records(axs[1], rRecord)

plt.show()

mesh1.verts = [list(v) for v in mesh1.verts]
mesh1.save("generated_files\\pressure_ring_virtual.json")

mesh2.verts = [list(v) for v in mesh2.verts]
mesh2.save("generated_files\\presure_ring_real.json")