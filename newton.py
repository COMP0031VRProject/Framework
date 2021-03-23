import torch
import torch.nn as nn
from torch.autograd.functional import jacobian
import matplotlib.pyplot as plt
from Mesh import *
from Utils import *
import math

mesh = generate_rectangle_mesh_grid((0,10), (10, 0), 20, 20)

# fig, axs = plt.subplots(1,1)

# axs.set_aspect('equal')
# visualize_mesh(axs, mesh)

# plt.show()

# originalMesh = SpringMesh(mesh.verts, mesh.tInd.copy())

verts = [torch.tensor(x, dtype=torch.float64) for x in mesh.verts]
tInd = mesh.tInd.copy()

springMesh = SpringMesh(verts, tInd)
boundary = lambda vert: vert[0] == 0.0 or vert[0] == 10.0 \
                        or vert[1] == 0.0 or vert[1] == 10.0
boundaryIndices = [i for i, v in enumerate(mesh.verts) if boundary(v)]


def Fij(Pi, Pj, k, r):
    return k * (torch.linalg.norm(Pi - Pj) - r) * (Pj - Pi) / torch.linalg.norm(Pi - Pj)


def force_magnitude_sum(mesh):
    l = 0
    for vIndex, this in enumerate(mesh.verts):
        force = torch.tensor([0., 0.], dtype=torch.float64)
        for key, edge in mesh.connected(vIndex).items():
            other = mesh.verts[key]
            force += Fij(this, other, k=edge.stiffness, r=edge.rest_length)
        l += torch.linalg.norm(force)
    return l


def Fi_function(mesh, vIndex):
    def Fi(Pi):
        force = torch.tensor([0., 0.], dtype=torch.float64)
        for key, edge in mesh.connected(vIndex).items():
            other = mesh.verts[key]
            force += Fij(Pi, other, k=edge.stiffness, r=edge.rest_length)
        return force

    return Fi


F_fun = [Fi_function(springMesh, i) for i in range(len(springMesh.verts))]

# T = [1550, 1551, 1552,\
#      1651, 1652, 1653]

T = [50]

E = []
for t in T:
    E.append(tuple(sorted([tInd[t][0], tInd[t][1]])))
    E.append(tuple(sorted([tInd[t][1], tInd[t][2]])))
    E.append(tuple(sorted([tInd[t][0], tInd[t][2]])))

for k, v in springMesh.edges.items():
    if k in E:
        v.rest_length = v.length * 2
        v.stiffness = 1.0
    else:
        v.rest_length = v.length
        v.stiffness = 1.0

# print(force_magnitude_sum(springMesh))

transpose = lambda x: torch.transpose(x, 0, 1)

history = []
theta = 1e-3
maximum_iteration = 50

fixed_boundary = False

for i in range(maximum_iteration):
    history.append(force_magnitude_sum(springMesh) / len(springMesh.verts))
    # if(history[-1] < theta): break
    # if i % 20 == 0:
    #     print(history[-1])
    #     fig, axs = plt.subplots(1,1)
    #     visualize_mesh(axs, springMesh)
    #     plt.show()
    for vIndex, this in enumerate(springMesh.verts):
        if fixed_boundary and vIndex in boundaryIndices: continue
        Fi_fun = F_fun[vIndex]
        Fi = torch.reshape(Fi_fun(this), (2, 1))
        j_inverse = torch.inverse(jacobian(Fi_fun, this))
        step = torch.flatten(-transpose(torch.matmul(j_inverse, Fi)))
        springMesh.verts[vIndex] = this + step

print(history[-1])

fig, axs = plt.subplots(1, 3)

axs[0].set_aspect('equal')
visualize_mesh(axs[0], mesh)

axs[1].set_aspect('equal')
visualize_mesh(axs[1], springMesh)

axs[2].plot(history)
axs[2].set_ylabel("Avg. Force Magnitude")
axs[2].set_xlabel("iteration")
plt.show()
