import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# Fig.17(a): Encoding capacity under diferent segmentation distances
fs = 30
plt.figure(figsize=[12, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
x = np.arange(8)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
labels = ['1', '0.8', '0.5', '0.4', '0.2', '0.1', '0.05', '0.02']
the_data = [24, 32, 56, 72, 152, 312, 632, 1592]
act_data = [24, 32, 56, 56, 120, 248, 488, 1208]


plt.plot(x, the_data, color='#e21a1c', alpha=0.8, marker="s", markersize="15", linewidth="4", label="Capacity w/o coupling", markerfacecolor='none', markeredgewidth=3)
plt.plot(x, act_data, color='#377eb8', alpha=0.8, marker="o", markersize="15", linewidth="4", label="Capacity w/ coupling", markerfacecolor='none', markeredgewidth=3)
plt.tick_params(labelsize=fs)
plt.legend(fontsize=fs)
plt.xticks(x, labels)
plt.xlabel(r'Segmentation distance (m)', fontsize=fs)
plt.ylabel(r'Encoding capacity', fontsize=fs)
plt.tight_layout()
plt.savefig("F17a.pdf")
plt.close


# Fig.17(b): Detection accuracy with diferent segmentation distances
fs = 30
plt.figure(figsize=[12, 7])
x = np.arange(8)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
labels = ['1', '0.8', '0.5', '0.4', '0.2', '0.1', '0.05', '0.02']
large_err = [1, 1, 1, 1, 1, 1, 0.9, 0.3]

plt.plot(x, large_err, color='#e21a1c', alpha=0.8, marker="s", markersize="15", linewidth="4", markerfacecolor='none', markeredgewidth=3)
plt.tick_params(labelsize=fs)
plt.xticks(x, labels)
plt.xlabel(r'Segmentation distance (m)', fontsize=fs)
plt.ylabel(r'Tag detection accuracy', fontsize=fs)
plt.ylim(0)
plt.tight_layout()
plt.savefig('F17b.pdf')
plt.close()