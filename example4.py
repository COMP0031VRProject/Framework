from Mesh import *
from Utils import *
import matplotlib.pyplot as plt 
import numpy as np

vmesh = Mesh(None, None)
vmesh.load('generated_files\\pressure_ring_virtual.json')
vmesh.verts = np.array(vmesh.verts)

rmesh = Mesh(None, None)
rmesh.load('generated_files\\pressure_ring_real.json')
rmesh.verts = np.array(rmesh.verts)

fig, axs = plt.subplots(1,2)

visualize_dot(axs[0], axs[1], vmesh, rmesh, (-3., 3.), (3., -3.), 0.1)

plt.show()