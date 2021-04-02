from analysis_utils import *

coords_json_file = './data_analytics/data/testsuite_1_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

diff_list = generate_angle_diff(r_coords, v_coords)
visualize_angle_diff(diff_list)