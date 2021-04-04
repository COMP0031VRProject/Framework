from analysis_utils import *

coords_json_file = './data_analytics/data/PR/PR_TestSuite_2_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

diff_list = generate_scaling_factor_diff(r_coords, v_coords)
plt.plot(diff_list)
plt.show()