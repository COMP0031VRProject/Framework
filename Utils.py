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
    relative2world = lambda coord : np.array([coord[0] + center[0], coord[1] + center[1]])
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
    relative2world = lambda coord : np.array([coord[0] + center[0], coord[1] + center[1]])
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

def generate_rectangle_mesh_grid(top_left_position, bottom_right_position, row : int, column : int):
    verts = []
    tInd = []
    width = (bottom_right_position[0] - top_left_position[0])
    height = (top_left_position[1] - bottom_right_position[1])
    column_width = width / column
    row_height = height / row
    firsts = []
    for r in range(row + 1):
        x, y = 0, top_left_position[1] - r * row_height
        firsts.append(len(verts))
        verts.append((x, y))
        alternate = (r % 2) == 1
        if alternate:
            x = -0.5 * column_width
        for _ in range(column):
            x += column_width
            verts.append((x, y))
        if alternate:
            verts.append((width, y))
    for i,first in enumerate(firsts[:-1]):
        if i % 2 == 0:
            next_first = firsts[i + 1]
            last = next_first - 1
            k = 0
            for j in range(first, last):
                k = next_first + j - first
                tInd.append((j, k, k+1))
                tInd.append((j, k+1, j+1))
            tInd.append((last, k+1, k+2))
        else:
            next_first = firsts[i + 1]
            last = next_first - 1
            k = 0
            for j in range(first, last - 1):
                k = next_first + j - first
                tInd.append((j, k, j+1))
                tInd.append((j+1, k, k+1))
            tInd.append((last-1, k+1, last))
    verts = [np.array(x) for x in verts]
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
        axs.plot(xs, ys, color='black', linewidth=1.0)

def visualize_targets(axs : matplotlib.axes.Axes, targets):
    for t in targets:
        axs.plot(t[0], t[1], color='red', marker='x')

def line_implicit_equation(A, B):
    _A = A[1] - B[1]
    _B = B[0] - A[0]
    _C = A[0] * B[1] - B[0] * A[1]
    return lambda p: _A * p[0] + _B * p[1] + _C

def is_point_in_triangle(P, A, B, C):
    x = line_implicit_equation(A,B)(P)
    y = line_implicit_equation(B,C)(P)
    z = line_implicit_equation(C,A)(P)
    return x >= 0 and y >= 0 and z >= 0

def barycentric_coordinates(P, A, B, C):
    ab_line = line_implicit_equation(A, B)
    gamma = ab_line(P) / ab_line(C)
    ca_line = line_implicit_equation(C, A)
    beta = ca_line(P) / ca_line(B)
    bc_line = line_implicit_equation(B, C)
    alpha = bc_line(P) / bc_line(A)
    return alpha, beta, gamma