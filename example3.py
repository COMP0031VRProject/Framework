from Mesh import Mesh
from Utils import *
import matplotlib.pyplot as plt
mesh = Mesh(None, None)

mesh.loadNodeAndEle('input.1.node', 'input.1.ele')

fig, axs = plt.subplots(1,1)
axs.set_aspect('equal')
visualize_mesh(axs, mesh)
plt.show()