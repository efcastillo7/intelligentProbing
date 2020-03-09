import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from os import scandir, getcwd
import os.path as path
import numpy as np
from numpy import *
import csv

x = []
y = []
z = []

with open('cpu_usage_066.csv','r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(float(row["TIME"]))
        y.append(float(row["CPU"]))
        z.append(float(row["REAL_MB"]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

legend = ['CPU Usage RL-Agent', 'Memory RL-Agent']

lns1 = ax.plot(x, y, '-', lw=1, color='#969696', label='CPU Usage of RL-agent')
ax.set_ylabel('CPU (%)', color='black', fontsize=26)
ax.set_xlabel('time (s)', fontsize=26)
ax.set_ylim(0., max(y) * 1.2)
ax.tick_params(direction='out', labelsize=26)
#ax.legend('CPU Usage RL-Agent', loc="upper right", fontsize=18)

ax2 = ax.twinx()
lns2 = ax2.plot(x, z, '-', lw=1, color='black', label='Memory of RL-agent', linewidth=2, linestyle='dashdot')
ax2.set_ylim(0., max(z) * 1.2)

ax2.set_ylabel('Memory (MB)', color='black', fontsize=26)
tkw = dict(size=4, width=1.5)
ax2.tick_params(axis='y', labelsize=26)
#ax2.legend('RAM Memory RL-Agent', loc="upper right", fontsize=18)

# added these three lines
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0, fontsize=18)

#plt.legend(fontsize=18)
ax.grid()


#fig.savefig(plot)
plt.show()
