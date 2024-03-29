from analysis_utils import *

coords_json_file = './data_analytics/data/PR/PR_TestSuite_2_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

theta_list = generate_angle_diff(r_coords, v_coords)
virtual_list = generate_accum_distance_virtual(v_coords)

max_grad = max_angle_diffs_grad(theta_list, virtual_list)
print(max_grad)