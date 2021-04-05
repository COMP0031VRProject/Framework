import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to load a single json file into a pandas data frame
def load_single(file_name):
    data = pd.read_json(file_name)
    df = pd.DataFrame(data)
    return df

# Function to generate accumulated distance in real
def generate_accum_distance_real(r_coords):
    frames = len(r_coords)
    prev_frame = 0
    accum_dist = 0
    dists = []
    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        dist_r = get_distance(prev_r, curr_r)

        dists.append(accum_dist)
        accum_dist += dist_r
        prev_frame = curr_frame

    return dists

# Function to generate accumulated distance in virtual
def generate_accum_distance_virtual(v_coords):
    frames = len(v_coords)
    prev_frame = 0
    accum_dist = 0
    dists = []
    for curr_frame in range(1, frames):
        prev_r = v_coords[prev_frame]
        curr_r = v_coords[curr_frame]
        dist_r = get_distance(prev_r, curr_r)

        dists.append(accum_dist)
        accum_dist += dist_r
        prev_frame = curr_frame

    return dists 


# Function to generate angle difference list
def generate_angle_diff(r_coords, v_coords):
    if len(r_coords) != len(v_coords):
        print("Error: Real coords does not match virtual coords")
        return

    frames = len(r_coords)
    diff_list = []
    prev_frame = 0
    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        v_r = np.array(curr_r) - np.array(prev_r)

        prev_v = v_coords[prev_frame]
        curr_v = v_coords[curr_frame]
        v_v = np.array(curr_v) - np.array(prev_v)

        theta_rad = get_angle(v_r, v_v)
        theta_deg = np.rad2deg(theta_rad)

        theta = theta_deg  # choose output format 
        diff_list.append(theta)
        prev_frame = curr_frame
        
    return diff_list


def get_angle(v_a, v_b):
    norm_a = np.linalg.norm(v_a)
    norm_b = np.linalg.norm(v_b)
    product = np.dot(v_a, v_b)

    if norm_a * norm_b == 0:
        return 0.0

    cos_t = product / (norm_a * norm_b)
    if abs(cos_t) > 1:
        cos_t = 1

    return np.arccos(cos_t)

# Function to generate scaling factor difference
def generate_scaling_factor_diff(r_coords, v_coords):
    if len(r_coords) != len(v_coords):
        print("Error: Real coords does not match virtual coords")
        return
    
    frames = len(r_coords)
    diff_list = []
    prev_frame = 0
    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        dist_r = get_distance(prev_r, curr_r)

        prev_v = v_coords[prev_frame]
        curr_v = v_coords[curr_frame]
        dist_v = get_distance(prev_v, curr_v)

        if dist_r == 0:
            diff_list.append(1.0)
        else:
            scaling = dist_v / dist_r
            diff_list.append(scaling)
        prev_frame = curr_frame

    return diff_list

        
def get_distance(p_a, p_b):
    return np.linalg.norm(np.array(p_a) - np.array(p_b))

# Generate flag over virtual coords
def generate_flag_coords():
    first = [4, 0]
    centers = [first]
    theta = 2 * math.pi / 6
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    rotate = lambda coord: [coord[0] * cos_theta - coord[1] * sin_theta, coord[0] * sin_theta + coord[1] * cos_theta]
    for i in range(5):
        centers.append(rotate(centers[-1]))
    targets = [c for c in centers] + [centers[1]]

    return targets

# Check one frame in virtual is within the relavent area
def check_in_relavent(p_prev, p_curr, targets):
    for target in targets:
        p_prev_dist = get_distance(target, p_prev)
        p_curr_dist = get_distance(target, p_curr)
        if p_curr_dist <= 0.3 and p_prev_dist <= 0.3:
            return True
    
    return False

# Calculate the single scaling differences over certain <virtual distance>
def calc_scaling_diffs(dist_r, dist_v):
    if dist_r == 0:
        return 0.0
    else:
        return abs(dist_v / dist_r - 1) * dist_v
    

# Scaling factor against <virtual distance> within relavent area integration
def scaling_factor_int_relavent(r_coords, v_coords):
    accum = 0
    targets = generate_flag_coords()

    frames = len(r_coords)
    prev_frame = 0
    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        dist_r = get_distance(prev_r, curr_r)

        prev_v = v_coords[prev_frame]
        curr_v = v_coords[curr_frame]
        dist_v = get_distance(prev_v, curr_v)
        
        if check_in_relavent(prev_v, curr_v, targets):
            accum += calc_scaling_diffs(dist_r, dist_v)

        prev_frame = curr_frame
    
    return accum

# Calculate the single angle differences over certain <virtual distance>
def calc_angle_diffs(theta, dist_v):
    return theta * dist_v
        
# Angle difference against <virtual distance> within relavent area integration
def angle_diffs_int_relavent(r_coords, v_coords):
    targets = generate_flag_coords()

    accum = 0
    frames = len(r_coords)
    prev_frame = 0

    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        v_r = np.array(curr_r) - np.array(prev_r)

        prev_v = v_coords[prev_frame]
        curr_v = v_coords[curr_frame]
        v_v = np.array(curr_v) - np.array(prev_v)
        dist_v = get_distance(prev_v, curr_v)

        if check_in_relavent(prev_v, curr_v, targets):
            theta_rad = get_angle(v_r, v_v)
            theta_deg = np.rad2deg(theta_rad)
            theta = theta_deg  # choose output format
            accum += calc_angle_diffs(theta, dist_v)
             
        prev_frame = curr_frame
    return accum

# Angle difference against <virtual distance> integration
def angle_diffs_int(r_coords, v_coords):
    targets = generate_flag_coords()

    accum = 0
    frames = len(r_coords)
    prev_frame = 0

    for curr_frame in range(1, frames):
        prev_r = r_coords[prev_frame]
        curr_r = r_coords[curr_frame]
        v_r = np.array(curr_r) - np.array(prev_r)

        prev_v = v_coords[prev_frame]
        curr_v = v_coords[curr_frame]
        v_v = np.array(curr_v) - np.array(prev_v)
        dist_v = get_distance(prev_v, curr_v)

        theta_rad = get_angle(v_r, v_v)
        theta_deg = np.rad2deg(theta_rad)
        theta = theta_deg  # choose output format
        accum += calc_angle_diffs(theta, dist_v)
        prev_frame = curr_frame

    return accum

# Function to get the max gradient of angle difference changing
def max_angle_diffs_grad(theta_list, virtual_list):
    if len(theta_list) != len(virtual_list):
        print("Error: Real coords does not match virtual coords")
        return

    max_grad = 0
    length = len(theta_list)
    
    for i in range(0, length-1):
        if (theta_list[i] > 90.0):
            continue

        d_theta = abs(theta_list[i + 1] - theta_list[i])
        d_v = virtual_list[i + 1] - virtual_list[i]

        if d_v == 0.0:
            continue
        grad = d_theta / d_v
        if grad > max_grad:
            max_grad = grad
    
    return max_grad
    
# Function to get the max gradient of scaling factor changing
def max_scaling_factor_diff_grad(scaling_list, virtual_list):
    if len(scaling_list) != len(virtual_list):
        print("Error: Real coords does not match virtual coords")
        return
    max_grad = 0
    length = len(scaling_list)

    for i in range(0, length-1):
        d_s = abs(scaling_list[i + 1] - scaling_list[i])
        d_v = virtual_list[i + 1] - virtual_list[i]

        if d_v == 0.0:
            continue
        grad = d_s / d_v
        if grad > max_grad:
            max_grad = grad

    return max_grad
            
# Function to visualize a path by series of coords (real, virtual)
def visualize_path(axs, coords):
    """
    axs: matplotlib.axes.Axes
    data: List -> a list contain the angle difference
    """
    previous = coords[0]
    for current in coords[1:]:
        xs = [previous[0], current[0]]
        ys = [previous[1], current[1]]
        previous = current
        axs.plot(xs, ys, color='red', linewidth=2.0)

# Funtion to visualize the mesh from the mesh file
def visualize_mesh(axs, mesh):
    """
    axs: matplotlib.axes.Axes
    mesh: Mesh -> a mesh data structure states in the documentation
    """
    for t in mesh.tInd:
        verts = [mesh.verts[i] for i in t]
        xs = [v[0] for v in verts]
        xs.append(xs[0])
        ys = [v[1] for v in verts]
        ys.append(ys[0])
        axs.plot(xs, ys, color='black', linewidth=0.5)

def visualize_targets(axs, targets, color='blue', marker='x'):
    for t in targets:
        axs.plot(t[0], t[1], color=color, marker=marker)

# Function to visualize the changing of scaling factors
def visualize_scaling_diff(axs, scaling_diffs):
    axs.plot(scaling_diffs)

# Function to visualize the changing of 
# angle differences based on frame
def visualize_angle_diff(axs, angle_diffs):
    """
    data: List -> a list contain the angle difference
    """
    axs.plot(angle_diffs)

# Function to visualize the changing of 
# angle differences based on accumulated real distance
def visualize_angle_diff_vs_real_distance(r_dists, angle_diffs):
    plt.plot(r_dists, angle_diffs)
    plt.show()
    
    
