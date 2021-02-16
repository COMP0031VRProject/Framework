import numpy as np

from Bot import *
from World import *
from Utils import *

bot = Bot()
vMesh = generate_polygon_mesh(20, 10, (0,0))
rMesh = generate_polygon_mesh(20, 5, (0,0))

start_position = np.array([0.0,0.0])

targets = [np.array([5.0,5.0]), np.array([5.0,2.0])]

world = World(vMesh, rMesh, start_position, bot, targets)

rRecord, vRecord = world.simulate()

fig, axs = plt.subplots(1,2)

visualize_records(axs[0], rRecord)
visualize_records(axs[1], vRecord)

plt.show()