from analysis_utils import *

coords_json_file = './data_analytics/data/OA/OA_TestSuite_2_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

diff_list = generate_scaling_factor_diff(r_coords, v_coords)
accum_dist_virtual = generate_accum_distance_virtual(v_coords)
accum_dist_real = generate_accum_distance_real(r_coords)

plt.plot(accum_dist_virtual, diff_list)
plt.show()
