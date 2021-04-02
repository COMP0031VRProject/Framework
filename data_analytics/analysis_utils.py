import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Function to load a single json file into a pandas data frame
def load_single(file_name):
    data = pd.read_json(file_name)
    df = pd.DataFrame(data)
    return df

# Function to visualize a path by series of coords (real, virtual)
def visualize_path(axs, coords):
    previous = coords[0]
    for current in coords[1:]:
        xs = [previous[0], current[0]]
        ys = [previous[1], current[1]]
        previous = current
        axs.plot(xs, ys, color='red', linewidth=2.0)

# Funtion to visualize the mesh from the mesh file
def visualize_mesh(axs, mesh):
    for t in mesh.tInd:
        verts = [mesh.verts[i] for i in t]
        xs = [v[0] for v in verts]
        xs.append(xs[0])
        ys = [v[1] for v in verts]
        ys.append(ys[0])
        axs.plot(xs, ys, color='black', linewidth=0.5)

# Function to visualize the changing of scaling factors

# Function to visualize the changing of angle differences
def visualize_angle_diff(data):
    """
    data: List -> a list contain the angle difference
    """
    plt.plot(data)
    plt.show()
    
    
