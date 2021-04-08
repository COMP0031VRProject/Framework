from analysis_utils import *

coords_json_file = '/Users/sweetie/GitHubWorkPlace/VRProject/Framework/data_analytics/data/LC/coords/LC_TestSuite_5_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

scaling_list = generate_scaling_factor_diff(r_coords, v_coords)
virtual_list = generate_accum_distance_virtual(v_coords)

max_grad = max_scaling_factor_diff_grad(scaling_list, virtual_list)
print(max_grad)