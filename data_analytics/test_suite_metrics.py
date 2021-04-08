from os import walk
from pandas import DataFrame
from analysis_utils import *


path = '/Users/sweetie/GitHubWorkPlace/VRProject/Framework/data_analytics/data/LC/coords/'
_, _, filenames = next(walk(path))

metrics_list = []

for filename in filenames:
    coords_json_file = path + filename
    df = load_single(coords_json_file)

    scaling_factor_relevant_list = []
    max_scaling_factor_grad_list = []
    angle_diffs_relavant_list = []
    angle_diffs_all_list = []
    max_angle_diffs_grad_list = []

    for index, row in df.iterrows():
        r_coords = row['coords_R']
        v_coords = row['coords_V']

        virtual_list = generate_accum_distance_virtual(v_coords)

        # scaling factor integration over relevant area for virtual space 
        sfir = scaling_factor_int_relavent(r_coords, v_coords)
        scaling_factor_relevant_list.append(sfir)

        # maximum scaling factor changing gradient
        scaling_list = generate_scaling_factor_diff(r_coords, v_coords)
        msfdg = max_scaling_factor_diff_grad(scaling_list, virtual_list)
        max_scaling_factor_grad_list.append(msfdg)

        # angle difference integration over relevant area for virtual space
        adir = angle_diffs_int_relavent(r_coords, v_coords)
        angle_diffs_relavant_list.append(adir)

        # angle difference integration over all virtual space
        adi = angle_diffs_int(r_coords, v_coords)
        angle_diffs_all_list.append(adi)
        
        # maximum angle changing gradient
        theta_list = generate_angle_diff(r_coords, v_coords)
        madg = max_angle_diffs_grad(theta_list, virtual_list)
        max_angle_diffs_grad_list.append(madg)

    # Average
    scaling_factor_relevant_avg = np.average(scaling_factor_relevant_list)
    max_scaling_factor_grad_avg = np.average(max_scaling_factor_grad_list)
    angle_diffs_relavant_avg = np.average(angle_diffs_relavant_list)
    angle_diffs_all_avg = np.average(angle_diffs_all_list)
    max_angle_diffs_grad_avg = np.average(max_angle_diffs_grad_list)

    # Standard deviation
    scaling_factor_relevant_sd = np.std(scaling_factor_relevant_list)
    max_scaling_factor_grad_sd = np.std(max_scaling_factor_grad_list)
    angle_diffs_relavant_sd = np.std(angle_diffs_relavant_list)
    angle_diffs_all_sd = np.std(angle_diffs_all_list)
    max_angle_diffs_grad_sd = np.std(max_angle_diffs_grad_list)

    # result
    res = [filename, 
    scaling_factor_relevant_avg, scaling_factor_relevant_sd, 
    max_scaling_factor_grad_avg, max_scaling_factor_grad_sd, 
    angle_diffs_relavant_avg, angle_diffs_relavant_sd, 
    angle_diffs_all_avg, angle_diffs_all_sd, 
    max_angle_diffs_grad_avg, max_angle_diffs_grad_sd]

    metrics_list.append(res)
    print("Finish: " + filename)


# to dataframe & excels
column_name = ['filename', 
    'scaling_factor_relevant_avg', 'scaling_factor_relevant_sd', 
    'max_scaling_factor_grad_avg', 'max_scaling_factor_grad_sd', 
    'angle_diffs_relavant_avg', 'angle_diffs_relavant_sd', 
    'angle_diffs_all_avg', 'angle_diffs_all_sd', 
    'max_angle_diffs_grad_avg', 'max_angle_diffs_grad_sd']

res_df = DataFrame(metrics_list, columns=column_name)

res_df.to_excel("metrics.xlsx", sheet_name='PR')  



    

