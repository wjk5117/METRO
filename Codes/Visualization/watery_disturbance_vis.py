import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
import numpy as np


# Fig.12(c): Impact on magnetic field
fs = 30
x = np.arange(11)
plt.figure(figsize=[12, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7, labelsize=fs)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
labels = ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20']
l_0 = [115.96, 116.16, 119.62, 117.26, 117.65, 118.92, 120.08, 118.50, 118.97, 118.32]
l_2 = [118.42, 119.37, 118.64, 117.85, 119.58, 119.43, 117.85, 118.28, 119.63, 119.66]
l_4 = [117.84, 117.29, 118.53, 119.18, 118.43, 117.38, 119.40, 118.67, 118.95, 119.17]
l_6 = [117.55, 117.22, 114.77, 117.58, 120.02, 117.64, 117.16, 117.62, 119.01, 118.17]
l_8 = [117.21, 118.64, 117.94, 118.36, 119.75, 119.56, 118.36, 120.44, 119.32, 119.24]
l_10 = [120.56, 118.45, 119.89, 120.16, 120.08, 120.69, 120.03, 118.83, 120.10, 118.52]
l_12 = [117.82, 118.64, 116.85, 117.54, 116.80, 118.95, 120.20, 120.50, 119.07, 118.67]
l_14 = [119.40, 118.23, 117.36, 116.89, 118.12, 118.67, 119.21, 121.34, 120.10, 119.38]
l_16 = [119.26, 119.25, 118.69, 119.10, 121.16, 119.89, 120.56, 119.68, 121.01, 118.58]
l_18 = [117.50, 119.10, 116.98, 117.90, 119.03, 118.59, 119.29, 118.50, 119.36, 120.37]
l_20 = [119.59, 119.23, 118.20, 116.90, 120.57, 119.20, 121.10, 119.15, 117.63, 119.78]

act_data = [np.mean(l_0), np.mean(l_2), np.mean(l_4), np.mean(l_6), np.mean(l_8), np.mean(l_10), np.mean(l_12),
            np.mean(l_14), np.mean(l_16), np.mean(l_18), np.mean(l_20)]
err_data = [np.std(l_0), np.std(l_2), np.std(l_4), np.std(l_6), np.std(l_8), np.std(l_10),
            np.std(l_12), np.std(l_14), np.std(l_16), np.std(l_18), np.std(l_20)]

(_, caps, _) = plt.errorbar(x, act_data, yerr=err_data, ecolor='red', elinewidth=3, fmt='red', linewidth=4, capsize=5)
for cap in caps:
    cap.set_markeredgewidth(3)
plt.ylim((105, 130))
plt.xticks(x, labels)
plt.xlabel(r'Water depth (cm)', fontsize=fs)
plt.ylabel(r'Magnetometer reading (uT)', fontsize=fs)
plt.tight_layout()
plt.savefig("Fig12c.pdf")
plt.close()

# Fig.12(d): Impact on RSS
fs = 30
plt.figure(figsize=[12, 7])
x = np.arange(11)
labels = ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20']
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
plt.grid(zorder=0, linestyle='--', alpha=0.5)

# RFID tag 1:
x_t1 = np.arange(3)
labels_t1 = ['0', '2', '4']
l_0_t1 = [-50.80, -50.20, -50.80, -49.70, -49.70, -49.70, -50.80, -50.70, -50.80, -50.80]
l_2_t1 = [-52.70, -52.80, -52.70, -51.70, -52.40, -51.80, -52.20, -52.20, -52.30, -51.80]
l_4_t1 = [-67.80, -68.70, -68.80]
act_data_t1 = [np.mean(l_0_t1), np.mean(l_2_t1), np.mean(l_4_t1)]
err_data_t1 = [np.std(l_0_t1), np.std(l_2_t1), np.std(l_4_t1)]

# RFID tag 2:
x_t2 = x
labels_t2 = labels
l_0_t2 = [-53.60, -53.60, -53.60, -53.20, -52.80, -52.80, -52.90, -53.60, -52.90, -53.60]
l_2_t2 = [-53.90, -53.90, -53.90, -52.80, -54.20, -54.20, -54.20, -53.90, -52.90, -53.90]
l_4_t2 = [-55.80, -55.80, -54.70, -55.70, -55.70, -54.80, -54.80, -55.80, -54.80, -54.80]
l_6_t2 = [-60.70, -59.80, -60.80, -59.80, -59.80, -59.80, -59.80, -59.80, -60.70, -59.70]
l_8_t2 = [-61.80, -62.20, -62.50, -61.80, -61.80, -61.80, -62.50, -62.70, -62.20, -61.70]
l_10_t2 = [-63.80, -63.70, -62.80, -62.70, -62.70, -62.70, -62.70, -63.80, -62.70, -62.70]
l_12_t2 = [-63.80, -64.70, -63.80, -63.70, -63.70, -63.70, -64.70, -63.80, -63.70, -63.70]
l_14_t2 = [-63.80, -64.80, -64.80, -64.80, -64.80, -64.80, -65.20, -65.00, -65.20, -65.00]
l_16_t2 = [-65.30, -65.80, -66.20, -65.80, -65.80, -66.20, -66.20, -65.80, -65.80, -65.80]
l_18_t2 = [-66.80, -66.70, -66.80, -66.70, -66.80, -66.20, -66.20, -66.70, -66.80, -66.80]
l_20_t2 = [-68.80, -68.20, -68.80, -68.80, -68.20, -68.20, -68.80, -67.50, -68.20, -68.20]

act_data_t2 = [np.mean(l_0_t2), np.mean(l_2_t2), np.mean(l_4_t2), np.mean(l_6_t2), np.mean(l_8_t2), np.mean(l_10_t2),
               np.mean(l_12_t2), np.mean(l_14_t2), np.mean(l_16_t2), np.mean(l_18_t2), np.mean(l_20_t2)]
err_data_t2 = [np.std(l_0_t2), np.std(l_2_t2), np.std(l_4_t2), np.std(l_6_t2), np.std(l_8_t2), np.std(l_10_t2),
               np.std(l_12_t2), np.std(l_14_t2), np.std(l_16_t2), np.std(l_18_t2), np.std(l_20_t2)]

# RFID tag 3:
x_t3 = x
labels_t3 = labels
l_0_t3 = [-47.80, -46.80, -47.20, -47.80, -47.80, -49.20, -49.20, -47.00, -48.50, -48.50]
l_2_t3 = [-53.80, -54.70, -53.20, -53.70, -52.50, -52.50, -52.90, -53.80, -52.80, -52.80]
l_4_t3 = [-54.80, -54.70, -53.50, -53.80, -55.70, -53.90, -55.70, -53.80, -53.90, -55.70]
l_6_t3 = [-57.00, -58.20, -58.20, -58.20, -59.00, -58.80, -58.50, -58.80, -59.20, -58.20]
l_8_t3 = [-59.00, -60.20, -59.80, -60.70, -60.20, -60.70, -59.20, -59.20, -59.80, -59.80]
l_10_t3 = [-62.40, -62.80, -63.80, -61.80, -61.80, -61.50, -62.30, -62.50, -63.40, -63.20]
l_12_t3 = [-63.20, -63.40, -63.80, -63.20, -63.40, -63.40, -63.40, -63.40, -63.40, -64.20]
l_14_t3 = [-64.80, -64.20, -64.80, -64.80, -65.80, -65.80, -65.80, -65.20, -65.80, -65.20]
l_16_t3 = [-65.80, -65.80, -65.80, -66.20, -66.20, -65.80, -65.80, -65.80, -65.80, -65.50]
l_18_t3 = [-66.00, -66.80, -66.80, -66.30, -66.30, -65.80, -66.00, -66.00, -66.30, -66.30]
l_20_t3 = [-67.20, -67.20, -67.20, -67.20, -68.20, -68.50, -68.20, -68.50, -68.20, -68.50]

act_data_t3 = [np.mean(l_0_t3), np.mean(l_2_t3), np.mean(l_4_t3), np.mean(l_6_t3), np.mean(l_8_t3), np.mean(l_10_t3),
               np.mean(l_12_t3), np.mean(l_14_t3), np.mean(l_16_t3), np.mean(l_18_t3), np.mean(l_20_t3)]
err_data_t3 = [np.std(l_0_t3), np.std(l_2_t3), np.std(l_4_t3), np.std(l_6_t3), np.std(l_8_t3), np.std(l_10_t3),
               np.std(l_12_t3), np.std(l_14_t3), np.std(l_16_t3), np.std(l_18_t3), np.std(l_20_t3)]

(_, caps, _) = plt.errorbar(x_t1, act_data_t1, yerr=err_data_t1, ecolor='#4daf4a', elinewidth=3, linewidth=4, fmt='#4daf4a',
                            capsize=5, label="Type 1")
for cap in caps:
    cap.set_markeredgewidth(3)

(_, caps, _) = plt.errorbar(x_t2, act_data_t2, yerr=err_data_t2, ecolor='#377eb8', elinewidth=3, linewidth=4, fmt='#377eb8',
                            capsize=5, label="Type 2")
for cap in caps:
    cap.set_markeredgewidth(3)

(_, caps, _,) = plt.errorbar(x_t3, act_data_t3, yerr=err_data_t3, ecolor='#e21a1c', elinewidth=3, linewidth=4,
                             fmt='#e21a1c', capsize=5, label="Type 3")
for cap in caps:
    cap.set_markeredgewidth(3)

plt.tick_params(labelsize=fs)
plt.ylim((-75, -40))
plt.legend(fontsize=20)
plt.xticks(x, labels)
plt.xlabel(r'Water depth (cm)', fontsize=fs)
plt.ylabel(r'RSS (dBm)', fontsize=fs)
plt.tight_layout()
plt.savefig('Fig12d.pdf')
plt.close()