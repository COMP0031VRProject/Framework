from analysis_utils import *

coords_json_file = './data_analytics/data/PR/PR_TestSuite_2_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

res = scaling_factor_int_relavent(r_coords, v_coords)
print(res)