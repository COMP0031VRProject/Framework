import numpy as np
import math
from Utils import *
import matplotlib.pyplot as plt

vertices = []
segments = []

def generate_regular_polygon(vertices, segments, center, circumradius, edges, border_marker):
    theta = 2 * math.pi / edges
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    relative2world = lambda coord : [coord[0] + center[0], coord[1] + center[1]]
    rotate = lambda coord : (coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta)
    verts = []    
    first = (0, circumradius)
    verts.append(first)
    previous = first
    start_index = len(vertices) + 1
    previous_index = start_index
    for _ in range(1, edges):
        next_v = rotate(previous)
        verts.append(next_v)
        segments.append((previous_index, previous_index + 1, border_marker))
        previous_index += 1
        previous = next_v
    segments.append((previous_index, start_index, border_marker))
    verts = [relative2world(x) for x in verts]
    vertices += [(x[0], x[1], border_marker) for x in verts]
    

# 4 vertices for rectangle
vertices.append(( -6,  -6, 2))
vertices.append((6.0,  -6, 2))
vertices.append((6.0, 6.0, 2))
vertices.append(( -6, 6.0, 2))
# 4 segments for rectangle
segments.append((1, 2, 2))
segments.append((2, 3, 2))
segments.append((3, 4, 2))
segments.append((4, 1, 2))

first = (4, 0)

theta = 2 * math.pi / 6
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)
rotate = lambda coord : (coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta)

circumradius = [0.3, 0.5, 0.7, 0.9]

centers = [first]
center = first
marker = 3
edges = 20
for c in circumradius:
    generate_regular_polygon(vertices, segments, center, c, edges, marker)

for i in range(5):
    marker += 1
    center = rotate(center)
    centers.append(center)
    for c in circumradius:
        generate_regular_polygon(vertices, segments, center, c, edges, marker)

fileName = 'input.poly'
with open(fileName, 'w') as file:
    file.write("{0} {1} {2} {3}\n".format(len(vertices), 2, 0, 1))
    for i, vertex in enumerate(vertices):
        file.write("{0} {1} {2} {3}\n".format(i+1, vertex[0], vertex[1], vertex[2]))
    # for i, vertex in enumerate(isolated_vertices):
    #     file.(write"{0} {1} {2} {3}\n".format(i+1+len(vertices), vertex[0], vertex[1], 0))
    
    file.write("{0} {1}\n".format(len(segments), 1))
    for i, segment in enumerate(segments):
        file.write("{0} {1} {2} {3}\n".format(i+1, segment[0], segment[1], segment[2]))
    
    file.write("{0}\n".format(len(centers)))
    for i, center in enumerate(centers):
        file.write("{0} {1} {2}\n".format(i+1, center[0], center[1]))

targets = [x[:2] for x in vertices]

fig, axs = plt.subplots(1,1)
axs.set_aspect('equal')
visualize_targets(axs, targets)
visualize_targets(axs, centers)

plt.show()