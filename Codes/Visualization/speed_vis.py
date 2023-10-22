import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
import numpy as np


plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# Fig.13(a): Detection accuracy w/ different polarities
plt.figure(figsize=[11, 7])
x = np.arange(9)
plt.grid(axis='both', zorder=0, linestyle='--', alpha=0.5)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
labels = ["15", "20", "25", "30", "35", "40", "45", "50", "55"]
info_tag = [1, 1, 1, 0.967, 0.967, 0.967, 0.933, 0.933, 0.9]
lane_tag = [1, 1, 1, 1, 0.967, 0.967, 0.967, 0.967, 0.933]
fs = 30
plt.plot(x, info_tag, color='#377eb8', marker="o", markersize="15", linewidth="4", label=r"$\phi$=0$\degree$",  markerfacecolor='none', markeredgewidth=3)
plt.plot(x, lane_tag, color='#e21a1c', marker="s", markersize="15", linewidth="4", label=r"$\phi$=90$\degree$",  markerfacecolor='none', markeredgewidth=3)
plt.tick_params(labelsize=fs)
plt.legend(fontsize=fs)
plt.xticks(x, labels)
plt.xlabel(r'Speed (MPH)', fontsize=fs)
plt.ylabel(r'Accuracy', fontsize=fs)
plt.ylim(0.5, 1.02)
plt.tight_layout()
plt.savefig('fig13a.pdf')
plt.close()


# Fig.13(b): Distance ratio results under varying speeds
data = {"Speed (MPH)": [r"10", r"10", r"10", r"10", r"10", r"10", r"10", r"10", r"10", r"10",
                        r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15", r"15",
                        r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20", r"20",
                        r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25", r"25",
                        r"30", r"30", r"30", r"30", r"30", r"30", r"30", r"30", r"30", r"30",
                        r"35", r"35", r"35", r"35", r"35", r"35", r"35", r"35", r"35", r"35",
                        r"40", r"40", r"40", r"40", r"40", r"40", r"40", r"40", r"40", r"40",
                        r"45", r"45", r"45", r"45", r"45", r"45", r"45", r"45", r"45", r"45",
                        r"50", r"50", r"50", r"50", r"50", r"50", r"50", r"50", r"50", r"50",
                        r"55", r"55", r"55", r"55", r"55", r"55", r"55", r"55", r"55", r"55"],
        'Distance ratio': [1.005, 1.0, 0.998, 1.005, 0.993, 1.004, 1.001, 0.998, 0.994, 1.004,
                           1.0, 0.982, 0.997, 1.007, 0.990, 0.998, 0.981, 1.006, 0.991, 0.999,
                           1.008, 0.987, 0.980, 0.998, 0.988, 0.999, 0.987, 0.981, 0.989, 1.006,
                           0.979, 0.985, 0.989, 0.978, 1.003, 1.002, 0.980, 0.990, 0.980, 0.985,
                           0.996, 0.986, 1.010, 0.984, 1.001, 0.996, 0.987, 0.985, 1.0, 1.009,
                           0.995, 0.980, 0.985, 1.010, 0.985, 0.986, 0.985, 1.01, 0.980, 0.996,
                           1.010, 0.998, 1.012, 0.99, 0.987, 0.999, 1.01, 0.99, 0.988, 1.009,
                           0.998, 1.012, 0.980, 0.985, 0.980, 0.986, 0.980, 0.980, 1.01, 0.999,
                           0.99, 0.985, 1.01, 1.012, 0.97, 0.985, 1.0, 1.011, 0.99, 0.981,
                           1.01, 1.015, 1.02, 0.98, 0.982, 0.99, 1.01, 1.016, 1.014, 0.981]
        }
df = DataFrame(data)
plt.figure(figsize=[11, 7])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
ax = sns.boxplot(x='Speed (MPH)', y='Distance ratio', data=df, linewidth=4, color='red',
                 order=[r"15", r"20", r"25", r"30", r"35", r"40", r"45", r"50", r"55"], width=0.3, saturation=.75,
                 zorder=2)
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
ax.set_xlabel('Speed (MPH)', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
ax.grid(zorder=0, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', zorder=1, alpha=0.7)
plt.ylim(0.95, 1.05)
plt.tight_layout()
plt.savefig('Fig13b_2.pdf')
plt.close()
