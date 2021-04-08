import pandas as pd
import matplotlib as plt
from analysis_utils import *

df_oa = pd.read_excel('./data_analytics/excels/OA.xlsx')
df_pr = pd.read_excel('./data_analytics/excels/PR.xlsx')

# Config
metric_name = 'scaling_factor_relevant_'
bar_width = 0.2
opacity = 0.4
error_config = {'ecolor': '0.3', 'capsize' : 1.5}

# Texts
title = 'Max Scaling Factor Gradient'
x_label = 'Test Suite'
y_label = 'Gradient'

size = 14
test_suites = np.arange(1,size + 1)
avg_name =  metric_name + 'avg'
std_name = metric_name + 'sd'
figure, axs = plt.subplots()



avg_pr = df_pr[avg_name].tolist()
std_pr = df_pr[std_name].tolist()

avg_oa = df_oa[avg_name].tolist()
std_oa = df_oa[std_name].tolist()

rect_PR = axs.bar(test_suites, avg_pr, bar_width,
            alpha=opacity, color='b',
            yerr=std_pr,
            error_kw=error_config,
            label='PR')
rect_OA = axs.bar(test_suites + bar_width, avg_oa, bar_width,
            alpha=opacity, color='r',
            yerr=std_oa,
            error_kw=error_config,
            label='OA')

axs.set_xticks(test_suites + bar_width / 3)
axs.set_xticklabels(test_suites)
axs.set_xlabel(x_label)
axs.set_ylabel(y_label)
axs.set_title(title)
axs.legend()

plt.show()



