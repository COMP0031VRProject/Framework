from analysis_utils import *

coords_json_file = './data_analytics/data/OA/OA_TestSuite_2_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][1]
r_coords = df['coords_R'][1]

diff_list = generate_angle_diff(r_coords, v_coords)
accum_dist = generate_accum_distance_real(r_coords)

visualize_angle_diff_vs_real_distance(accum_dist, diff_list)