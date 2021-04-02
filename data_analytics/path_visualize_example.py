from analysis_utils import *
from Mesh import *

#Load Coordinates
coords_json_file = './data_analytics/data/testsuite_1_coords.json'
df = load_single(coords_json_file)

v_mesh = Mesh(None, None)
v_mesh.load("./data_analytics/mesh/pressure_ring_virtual.json")
v_mesh.verts = [np.array(v) for v in v_mesh.verts]

r_mesh = Mesh(None, None)
r_mesh.load("./data_analytics/mesh/pressure_ring_real.json")
r_mesh.verts = [np.array(v) for v in r_mesh.verts]

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]
# visualize_angle_diff(data)
fig, axs = plt.subplots(1, 2)

axs[0].set_aspect('equal')
axs[0].set_xlim((-6., 6.))
axs[0].set_ylim((-6., 6.))
visualize_mesh(axs[0], v_mesh)
visualize_path(axs[0], v_coords)

axs[1].set_aspect('equal')
axs[1].set_xlim((-6., 6.))
axs[1].set_ylim((-6., 6.))
visualize_mesh(axs[1], r_mesh)
visualize_path(axs[1], r_coords)

plt.show()
