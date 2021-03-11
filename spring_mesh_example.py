import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from Mesh import *
from Utils import *
import math

def F(Pi, Pj, k, r):
    return k * (torch.linalg.norm(Pi - Pj) - r) * (Pj - Pi) / torch.linalg.norm(Pi - Pj)

def force_magnitude_sum(mesh):
    l = 0
    for vIndex, this in enumerate(mesh.verts):
        force = torch.tensor([0.,0.])
        for key,edge in mesh.connected(vIndex).items():
            other = mesh.verts[key]
            force += F(this, other, k=edge.stiffness, r=edge.rest_length)
        # print(vIndex, force)
        l += torch.linalg.norm(force)
    return l

        

mesh = generate_rectangle_mesh_grid((0,10), (10, 0), 5, 5)

# fig, axs = plt.subplots(1,1)

# axs.set_aspect('equal')
# visualize_mesh(axs, mesh)

# plt.show()

verts = [torch.tensor(x, requires_grad=True) for x in mesh.verts]
tInd = mesh.tInd

springMesh = SpringMesh(verts, tInd)

T = [27]
E = []
for t in T:
    E.append(tuple(sorted([tInd[t][0], tInd[t][1]])))
    E.append(tuple(sorted([tInd[t][1], tInd[t][2]])))
    E.append(tuple(sorted([tInd[t][0], tInd[t][2]])))

for k,v in springMesh.edges.items():
    if k in E:
        v.rest_length = v.length * 2
        v.stiffness = 1
    else:
        v.rest_length = v.length

print(force_magnitude_sum(springMesh))

optimizer = optim.Adam(springMesh.verts, lr=0.0001)

theta = 1e-5

history = []
for i in range(2000):
    optimizer.zero_grad()    
    loss = force_magnitude_sum(springMesh)
    history.append(loss.item())
    if(history[-1] < theta):
        print("break early")
        break
    loss.backward(retain_graph=True)
    optimizer.step()

print(history[-1])

fig, axs = plt.subplots(1,3)

axs[0].set_aspect('equal')
axs[0].set_xlim((0,10))
axs[0].set_ylim((0,10))
visualize_mesh(axs[0], mesh)

axs[1].set_aspect('equal')
axs[1].set_xlim((0,10))
axs[1].set_ylim((0,10))
visualize_mesh(axs[1], springMesh)

axs[2].plot(history)

plt.show()