import seaborn as sns
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import math


# font size
fs = 30


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

plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax.set_xlabel('Speed (MPH)', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
ax.grid(zorder=0, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', zorder=1, alpha=0.7)
plt.ylim(0.95, 1.05)
plt.tight_layout()
plt.savefig('Fig13b_varying_speed.pdf')
plt.close()



# Fig.14(c): Distance ratio results under varying ground clearance
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

plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax.set_xlabel('Ground clearance (cm)', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
plt.grid(zorder=0, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', alpha=0.7)
plt.ylim(0.94, 1.05)
plt.tight_layout()
plt.savefig('Fig14c_ground_clearance.pdf')
plt.close()



# Fig.15: Distance ratio results on rough roads
data = {"Tag": [r"r=3/1", r"r=3/1", r"r=3/1", r"r=3/1", r"r=3/1",
                r"r=2/2", r"r=2/2", r"r=2/2", r"r=2/2", r"r=2/2",
                r"r=1/3", r"r=1/3", r"r=1/3", r"r=1/3", r"r=1/3"],
        'Distance ratio': [1.03, 1.026, 1.01, 1.011, 1.005,
                           0.967, 0.964, 0.953, 0.960, 0.972,
                           0.968, 0.985, 0.950, 0.956, 0.967]
        }
df = DataFrame(data)
plt.figure(figsize=[9, 8])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.tick_params(width=1, length=7)
ax = sns.boxplot(x='Tag', y='Distance ratio', data=df, linewidth=4, color='red', order=[r"r=3/1", r"r=2/2", r"r=1/3"],
                width=0.3, saturation=.75, zorder=2)

for i, box in enumerate([p for p in ax.patches if not p.get_label()]):
    color = box.get_facecolor()
    box.set_edgecolor(color)
    box.set_facecolor((0, 0, 0, 0))
    # iterate over whiskers and median lines
    for j in range(6 * i, 6 * (i + 1)):
        ax.lines[j].set_color(color)

plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax.set_xlabel('Ratio configuration', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
plt.grid(zorder=1, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', alpha=0.7)
plt.ylim(0.94, 1.05)
plt.tight_layout()
plt.savefig('Fig15_rough_road.pdf')
plt.close()