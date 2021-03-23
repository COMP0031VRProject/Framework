import numpy as np
from Bot import *
from World import *
from Utils import *
from Mesh import *
import matplotlib.pyplot as plt
import math

def angles(A, B, C):
    AB_norm = np.linalg.norm(B - A)
    BC_norm = np.linalg.norm(C - B)
    AC_norm = np.linalg.norm(C - A)
    A_angle = np.arccos(np.dot(B - A, C - A) / AB_norm / AC_norm)
    B_angle = np.arccos(np.dot(A - B, C - B) / AB_norm / BC_norm)
    C_angle = np.arccos(np.dot(A - C, B - C) / AC_norm / BC_norm)
    return A_angle, B_angle, C_angle

def random_direction():
    ans = np.array([1., 0.])
    theta = 2 * np.pi * np.random.rand(1,)[0]
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    rotation_matrix = np.eye(2)
    rotation_matrix[0][0] = cos_theta
    rotation_matrix[0][1] = -sin_theta
    rotation_matrix[1][0] = sin_theta
    rotation_matrix[1][1] = cos_theta
    return np.matmul(ans, rotation_matrix)

def delta_area_costs(verts, ni, nv, objective, area_costs):
    changes = {}
    for t in objective.keys():
        if ni in t:
            A, B, C = [verts[i] for i in t]
            if t[0] == ni:
                A = nv
            elif t[1] == ni:
                B = nv
            else:
                C = nv
            area = 0.5 * np.cross(B - A, C - A)
            cost = (area - objective[t]) ** 2
            changes[t] = cost - area_costs[t]
    return changes        

def update_area_costs(changes, area_costs):
    for t in changes.keys():
        area_costs[tuple(t)] += changes[tuple(t)]

def delta_angle_costs(verts, ni, nv, angle_objective, angle_costs):
    changes = {}
    for t in angle_objective.keys():
        if ni in t:
            A, B, C = [verts[i] for i in t]
            if t[0] == ni:
                A = nv
            elif t[1] == ni:
                B = nv
            else:
                C = nv
            A_angle, B_angle, C_angle = angles(A, B, C)
            A_cost = (A_angle - angle_objective[tuple(t)][0]) ** 2
            B_cost = (B_angle - angle_objective[tuple(t)][1]) ** 2
            C_cost = (C_angle - angle_objective[tuple(t)][2]) ** 2
            new_cost = A_cost + B_cost + C_cost
            changes[tuple(t)] = new_cost - angle_costs[tuple(t)]
    return changes
            
def update_angle_costs(changes, angle_costs):
    for t in changes.keys():
        angle_costs[tuple(t)] += changes[tuple(t)]

def area_costs(verts, tInd, area_objective):
    area_costs = {}
    for t in tInd:
        A, B, C = [verts[i] for i in t]
        area = 0.5 * np.cross(B - A, C - A)
        cost = (area - area_objective[tuple(t)]) ** 2
        area_costs[tuple(t)] = cost
    return area_costs

def angle_costs(verts, tInd, angle_objective):
    angle_costs = {}
    for t in tInd:
        A, B, C = [verts[i] for i in t]
        A_angle, B_angle, C_angle = angles(A, B, C)
        angle_costs[tuple(t)] = 0
        angle_costs[tuple(t)] += (A_angle - angle_objective[tuple(t)][0]) ** 2
        angle_costs[tuple(t)] += (B_angle - angle_objective[tuple(t)][1]) ** 2
        angle_costs[tuple(t)] += (C_angle - angle_objective[tuple(t)][2]) ** 2
    return angle_costs

def weighted_cost(costs, weights):
    ans = 0
    for t in costs.keys():
        ans += costs[t] * weights[tuple(t)]
    return ans

# Load Mesh
mesh1 = generate_rectangle_mesh_grid((0,100), (100, 0), 20, 20)
mesh1.verts = np.array(mesh1.verts)
mesh1.save('generated_files\\annealing_before.json')

# Area Objectives
area_objective = {}
for t in mesh1.tInd:
    A, B, C = [mesh1.verts[i] for i in t]
    area_objective[tuple(t)] = 0.5 * np.cross(B - A, C - A)

# expand_list = \
#     [
#          304, 305, 306, 307, 308,\
#     344, 345, 346, 347, 348, 349, 350,\
#     385, 386, 387, 388, 389, 390, 391,\
#          427, 428, 429, 430, 431
#     ]

expand_list = \
    [
              262, 263, 264, 265, 266, 267, 268,
         302, 303, 304, 305, 306, 307, 308, 309, 310,\
    342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352,\
    383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393,\
         425, 426, 427, 428, 429, 430, 431, 432, 433,\
              385, 386, 387, 388, 389, 390, 391\
    ]


for i in expand_list:
    t = mesh1.tInd[i]
    area_objective[tuple(t)] *= 4

# Angle Objectives
angle_objective = {}
for t in mesh1.tInd:
    A, B, C = [mesh1.verts[i] for i in t]
    A_angle, B_angle, C_angle = angles(A, B, C)
    angle_objective[tuple(t)] = (A_angle, B_angle, C_angle)

r = 0.95 # annealing speed
T = 2000.0  # initial temperature
maximum_step_size = 0.2
total_cost_history = []
area_cost_history  = []
angle_cost_history = []
maximum_iteration = 2000

alpha= 1.0 # area cost of relevant area
beta = 1.0 # area cost of irrelevant area
gamma= 100.0 # angle cost of relevant area
delta= 50.0 # angle cost of irrelevant area

area_weights = {}
for i,t in enumerate(mesh1.tInd):
    if i in expand_list:
        area_weights[tuple(t)] = alpha
    else:
        area_weights[tuple(t)] = beta

angle_weights= {}
for i,t in enumerate(mesh1.tInd):
    if i in expand_list:
        angle_weights[tuple(t)] = gamma
    else:
        angle_weights[tuple(t)] = delta

area_costs = area_costs(mesh1.verts, mesh1.tInd, area_objective)
angle_costs=angle_costs(mesh1.verts, mesh1.tInd, angle_objective)

total_area_cost = weighted_cost(area_costs, area_weights)
total_angle_cost= weighted_cost(angle_costs,angle_weights)
print(total_area_cost)
print(total_angle_cost)
total_cost = total_area_cost + total_angle_cost

fixed_boundary = True
update_list = range(len(mesh1.verts))
if fixed_boundary:
    update_list = [i for i,v in enumerate(mesh1.verts) if not (v[0] == 0.0 or v[0] == 100.0 or v[1] == 0.0 or v[1] == 100.0)]

for i in range(maximum_iteration):
    total_cost_history.append(total_cost)
    area_cost_history.append(total_area_cost)
    angle_cost_history.append(total_angle_cost)
    for i in update_list:
        v = mesh1.verts[i]
        step_size = maximum_step_size * np.random.rand(1)[0]
        step = step_size * random_direction()
        nv = v + step
        area_cost_changes = delta_area_costs(mesh1.verts, i, nv, area_objective, area_costs)
        angle_cost_changes= delta_angle_costs(mesh1.verts,i, nv, angle_objective,angle_costs)
        delta_total_area_cost = weighted_cost(area_cost_changes, area_weights)
        delta_total_angle_cost= weighted_cost(angle_cost_changes,angle_weights)
        D = delta_total_area_cost + delta_total_angle_cost
        if D <= 0.0:
            # Better solution
            mesh1.verts[i] = nv
            total_area_cost += delta_total_area_cost
            total_angle_cost += delta_total_angle_cost
            total_cost += D
            update_area_costs(area_cost_changes, area_costs)
            update_angle_costs(angle_cost_changes,angle_costs)
        elif (np.exp(-D / T) > np.random.rand(1)[0]):
            # Random Behavior
            mesh1.verts[i] = nv
            total_area_cost += delta_total_area_cost
            total_angle_cost += delta_total_angle_cost
            total_cost += D
            update_area_costs(area_cost_changes, area_costs)
            update_angle_costs(angle_cost_changes,angle_costs)
    T = r * T
print(total_cost)

fig, axs = plt.subplots(1,2)

axs[0].plot(total_cost_history, label='total cost')
axs[0].plot(area_cost_history, label='area cost')
axs[0].plot(angle_cost_history, label='angle cost')
axs[0].legend()
axs[1].set_aspect('equal')
visualize_mesh(axs[1], mesh1)

plt.show()

mesh1.save('generated_files\\annealing_after.json')