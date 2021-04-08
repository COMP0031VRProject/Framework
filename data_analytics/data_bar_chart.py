import pandas as pd
import matplotlib as plt
from analysis_utils import *

df_oa = pd.read_excel('./data_analytics/excels/OA.xlsx')
df_pr = pd.read_excel('./data_analytics/excels/PR.xlsx')
df_lc = pd.read_excel('./data_analytics/excels/LC.xlsx')
df_rlc = pd.read_excel('./data_analytics/excels/RLC.xlsx')

# Config
metric_name = 'scaling_factor_relevant_'
bar_width = 0.2
opacity = 0.4
error_config = {'ecolor': '0.3', 'capsize' : 1.5}

# Texts
title = 'Accumulation of Scaling Factor(SF) Differences to 1'
x_label = 'Test Suite'
y_label = 'SF Difference Integration'
file_name = metric_name + 'figure.png'

size = 14
test_suites = np.arange(1,size + 1)
avg_name =  metric_name + 'avg'
std_name = metric_name + 'sd'
figure, axs = plt.subplots()

avg_pr = df_pr[avg_name].tolist()
std_pr = df_pr[std_name].tolist()

avg_oa = df_oa[avg_name].tolist()
std_oa = df_oa[std_name].tolist()

avg_lc = df_lc[avg_name].tolist()
std_lc = df_lc[std_name].tolist()

avg_rlc = df_rlc[avg_name].tolist()
std_rlc = df_rlc[std_name].tolist()

rect_PR = axs.bar(test_suites - bar_width, avg_pr, bar_width,
            alpha=opacity, color='b',
            yerr=std_pr,
            error_kw=error_config,
            label='PR')
rect_OA = axs.bar(test_suites, avg_oa, bar_width,
            alpha=opacity, color='r',
            yerr=std_oa,
            error_kw=error_config,
            label='OA')
rect_LC = axs.bar(test_suites + bar_width, avg_lc, bar_width,
            alpha=opacity, color='m',
            yerr=std_lc,
            error_kw=error_config,
            label='LC')
rect_RLC = axs.bar(test_suites + 2 * bar_width, avg_rlc, bar_width,
            alpha=opacity, color='c',
            yerr=std_rlc,
            error_kw=error_config,
            label='RLC')

# Only for PR (since the bar is invisible)
x = test_suites - bar_width
y = avg_pr

for a,b in zip(x,y):
    plt.text(a, b+0.05, '%.04f' % b, ha='center', va= 'bottom',fontsize=6)

axs.set_xticks(test_suites + bar_width / 4)
axs.set_xticklabels(test_suites)
axs.set_xlabel(x_label)
axs.set_ylabel(y_label)
axs.set_title(title)
axs.legend(loc="upper right")

plt.savefig('./data_analytics/figures/'+ file_name)
plt.show()



