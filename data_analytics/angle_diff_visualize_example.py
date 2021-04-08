from analysis_utils import *

coords_json_file = '/Users/sweetie/GitHubWorkPlace/VRProject/Framework/data_analytics/data/LC/coords/LC_TestSuite_12_coords.json'
df = load_single(coords_json_file)

v_coords = df['coords_V'][0]
r_coords = df['coords_R'][0]

diff_list = generate_angle_diff(r_coords, v_coords)
plt.plot(diff_list)
plt.show()