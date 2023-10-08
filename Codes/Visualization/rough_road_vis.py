import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns


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
fs = 30
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax.set_xlabel('Ratio configuration', fontsize=fs)
ax.set_ylabel("Relative distance ratio", fontsize=fs)
plt.grid(zorder=1, linestyle='--', alpha=0.5)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth='3', alpha=0.7)
plt.ylim(0.94, 1.05)
plt.tight_layout()
plt.savefig('Fig15.pdf')
plt.close()