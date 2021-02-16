import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from Mesh import *
from Record import Record

def normalize(x):
    return x / np.linalg.norm(x)

def generate_polygon_mesh(n, size, center):
    theta = 2 * math.pi / n
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    # world2relative = lambda coord : (coord[0] - center[0], coord[1] - center[1])
    relative2world = lambda coord : (coord[0] + center[0], coord[1] + center[1])
    rotate = lambda coord : (coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta)
    first = (0, size)
    verts = [(0,0), first]
    tInd = []
    previous = first
    for i in range(1, n):
        next_v = rotate(previous)
        verts.append(next_v)
        tInd.append((0, i, i+1))
        previous = next_v
    tInd.append((0, n, 1))
    verts = [relative2world(v) for v in verts]
    mesh = Mesh(verts, tInd)
    return mesh

def generate_embedded_polygon_mesh(n, M, size, center):
    theta = 2 * math.pi / n
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    relative2world = lambda coord : (coord[0] + center[0], coord[1] + center[1])
    rotate = lambda coord : (coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta)
    first = (0, size)
    verts = [(0,0), first]
    tInd = []
    previous = first
    for i in range(1, n):
        next_v = rotate(previous)
        verts.append(next_v)
        tInd.append((0, i, i+1))
        previous = next_v
    tInd.append((0, n, 1))

    verts.append((0, size * M))
    for i in range(1, n):
        last = len(verts) - 1
        next_v = (verts[i + 1][0] * M, verts[i + 1][1] * M)
        verts.append(next_v)
        tInd.append((i, last, last + 1))
        tInd.append((i, last+1, i+1))

    tInd.append((1, n, n+1))
    tInd.append((n, n+n, n+1))

    verts = [relative2world(v) for v in verts]
    mesh = Mesh(verts, tInd)
    return mesh

def visualize_mesh(axs : matplotlib.axes.Axes, mesh : Mesh):
    for t in mesh.tInd:
        verts = [mesh.verts[i] for i in t]
        xs = [v[0] for v in verts]
        xs.append(xs[0])
        ys = [v[1] for v in verts]
        ys.append(ys[0])
        axs.plot(xs, ys, color='black', linewidth=0.5)

def visualize_records(axs : matplotlib.axes.Axes, record : Record):
    previous = record.records[0]
    for current in record.records[1:]:
        xs = [previous[0], current[0]]
        ys = [previous[1], current[1]]
        previous = current
        axs.plot(xs, ys, color='black', linewidth=0.5)

