import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# Fig.16: Impact of temperature
fs = 30
x = np.arange(7)
plt.figure(figsize=[12, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
labels = ['25', '35', '45', '55', '65', '75', '85']

# magnet
l_1 = [90.52, 90.41, 91.87, 90.79, 90.96, 91.90, 91.52, 90.48, 91.85, 92.22]
l_2 = [91.68, 91.03, 90.19, 90.50, 91.19, 91.32, 91.14, 90.45, 89.59, 91.19]
l_3 = [90.70, 90.88, 90.08, 90.85, 91.39, 91.37, 91.61, 90.98, 90.84, 91.44]
l_4 = [91.07, 90.88, 92.76, 91.65, 91.89, 91.09, 92.70, 91.01, 91.80, 91.52]
l_5 = [90.83, 91.84, 91.06, 91.29, 91.94, 92.71, 91.89, 92.62, 91.52, 91.21]
l_6 = [92.43, 90.83, 89.96, 91.16, 92.24, 91.39, 91.33, 90.04, 91.56, 92.03]
l_7 = [89.74, 90.38, 89.91, 89.97, 91.33, 91.79, 91.58, 90.22, 90.94, 89.04]

act_data = [np.mean(l_1), np.mean(l_2), np.mean(l_3), np.mean(l_4), np.mean(l_5), np.mean(l_6), np.mean(l_7)]
err_data = [np.std(l_1), np.std(l_2), np.std(l_3), np.std(l_4), np.std(l_5), np.std(l_6),
            np.std(l_7)]

# sensor array
l_s1 = [92.60, 91.13, 92.11, 91.50, 91.79, 91.73, 91.25, 91.33, 92.94, 92.42]
l_s2 = [90.75, 91.39, 91.57, 92.47, 91.99, 92.84, 92.51, 91.54, 91.79, 92.01]
l_s3 = [92.36, 90.56, 90.68, 90.48, 91.20, 91.53, 92.14, 91.12, 92.33, 93.10]
l_s4 = [88.93, 89.60, 89.99, 90.26, 90.07, 90.19, 91.29, 91.10, 91.17, 91.49]
l_s5 = [89.27, 89.53, 90.78, 90.15, 90.87, 91.98, 89.30, 91.29, 88.78, 91.49]
l_s6 = [89.62, 89.36, 89.65, 90.82, 90.11, 89.90, 90.62, 90.17, 90.49, 91.56]
l_s7 = [88.30, 88.41, 89.38, 87.54, 87.51, 88.02, 88.96, 89.44, 88.53, 89.43]

act_data_sen = [np.mean(l_s1), np.mean(l_s2), np.mean(l_s3), np.mean(l_s4), np.mean(l_s5), np.mean(l_s6), np.mean(l_s7)]
err_data_sen = [np.std(l_s1), np.std(l_s2), np.std(l_s3), np.std(l_s4), np.std(l_s5), np.std(l_s6),
                np.std(l_s7)]

(_, caps, _) = plt.errorbar(x, act_data, yerr=err_data, elinewidth=3, fmt='-.', linewidth=4, capsize=5, label="Magnet")
for cap in caps:
    cap.set_markeredgewidth(3)

(_, caps, _) = plt.errorbar(x, act_data_sen, yerr=err_data_sen, ecolor='red', elinewidth=3, fmt='red', linewidth=4,
                            capsize=5, label="Sensor array")
for cap in caps:
    cap.set_markeredgewidth(3)

plt.ylim((80, 100))
plt.tick_params(labelsize=fs)
plt.legend(fontsize=fs)
plt.xticks(x, labels)
plt.xlabel(r'Temperature ($\degree$C)', fontsize=fs)
plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
plt.tight_layout()
plt.savefig('Fig16.pdf')
plt.close()