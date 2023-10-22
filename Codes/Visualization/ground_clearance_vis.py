import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
import numpy as np


plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# Fig.14(a): Ground clearance of difference types of cars
labels = ['Sedans', 'Utility Vehicles', 'Vans', 'Heavy Trucks']
fs = 30
bar_width = 0.4
x = np.arange(4)
large_err = [15.5, 21.08, 28.8, 37.2]
yerror = [1.581, 4.5, 1.939, 2.786]
plt.figure(figsize=[12, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
error_params = dict(elinewidth=4, ecolor='#377eb8', capsize=10, alpha=0.9)
ax = plt.bar(x, large_err, bar_width, yerr=yerror, error_kw=error_params, zorder=3,
             edgecolor='#377eb8', lw=5, fill=False)
plt.xlabel(r"Vehicle type", fontsize=fs)
plt.ylabel(r"Ground clearance $(cm)$", fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.xticks(x, labels)
plt.tight_layout()
plt.savefig('Fig14a.pdf')
plt.close()


# Fig.14(b): Detection accuracy w/ different polarities
plt.figure(figsize=[12, 7])
x = np.arange(5)
plt.grid(axis='both', zorder=0, linestyle='--', alpha=0.5)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
plt.grid(axis='both', zorder=0, linestyle='--', alpha=0.5)
labels = ["15", "20", "25", "30", "35"]
info_tag = [1, 1, 1, 0.87, 0.47]
lane_tag = [1, 1, 1, 0.93, 0.67]
fs = 30
plt.plot(x, info_tag, color='#377eb8', marker="o", markersize="15", linewidth="4", label=r"$\phi$=0$\degree$", markerfacecolor='none', markeredgewidth=3)
plt.plot(x, lane_tag, color='#e21a1c', marker="s", markersize="15", linewidth="4", label=r"$\phi$=90$\degree$", markerfacecolor='none', markeredgewidth=3)
plt.tick_params(labelsize=fs)
plt.legend(loc='lower left', fontsize=fs)
plt.xticks(x, labels)
plt.xlabel(r'Ground clearance (cm)', fontsize=fs)
plt.ylabel(r'Accuracy', fontsize=fs)
plt.ylim(0)
plt.tight_layout()
plt.savefig('Fig14b.pdf')
plt.close()


# Fig.14(c): Distance ratio results
data = {"Ground clearance (cm)": [r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15",
                                  r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20",
                                  r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25",
                                  # 9/10 experiments are successful
                                  r"30", r"30", r"30", r"30", r"30", r"30", r"30", r"30", r"30",
                                  # 5/10 experiments are successful
                                  r"35", r"35", r"35", r"35", r"35"],
        'Distance ratio': [1.008, 0.987, 0.980, 0.998, 0.988, 0.980, 0.989, 0.999, 1.006, 0.989, 
                           1.010, 0.988, 0.985, 0.999, 1.005, 1.004, 1.0, 0.986, 0.987, 1.01,
                           1.013, 1.006, 0.974, 0.999, 0.977, 1.007, 1.012, 1.0, 0.980, 0.971,
                           0.990, 0.979, 1.005, 0.952, 0.973, 0.991, 1.005, 0.950, 0.975,
                           0.95, 0.98, 1.01, 1.02, 0.96]
        }
df = DataFrame(data)
plt.figure(figsize=[12, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)

ax = sns.boxplot(x='Ground clearance (cm)', y='Distance ratio', data=df, linewidth=4, color='red',
                order=[r"15", r"20", r"25", r"30", r"35"], width=0.3, saturation=.75)
for i, box in enumerate([p for p in ax.patches if not p.get_label()]):
    color = box.get_facecolor()
    box.set_edgecolor(color)
    box.set_facecolor((0, 0, 0, 0))
    # iterate over whiskers and median lines
    for j in range(6 * i, 6 * (i + 1)):
        ax.lines[j].set_color(color)
fs = 30
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax.set_xlabel('Ground clearance (cm)', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', alpha=0.7)
plt.ylim(0.94, 1.05)
plt.tight_layout()
plt.savefig('Fig14c.pdf')
plt.close()