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

currentPath = getcwd()
print(currentPath)

csv_file = currentPath + '/probing_'+ sys.argv[1] + 's/cpu_usage_' + sys.argv[1] + '.csv'
csv_plot = currentPath + '/probing_'+ sys.argv[1] + 's/cpu_usage_' + sys.argv[1] + '.png'



with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(float(row["TIME"]))
        y.append(float(row["CPU"]))
        z.append(float(row["REAL_MB"]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x, y, '-', lw=1, color='r')

ax.set_ylabel('CPU (%)', color='r')
ax.set_xlabel('time (s)')
ax.set_ylim(0., max(y) * 1.2)

ax2 = ax.twinx()

ax2.plot(x, z, '-', lw=1, color='b')
ax2.set_ylim(0., max(z) * 1.2)

ax2.set_ylabel('Real Memory (MB)', color='b')

ax.grid()

fig.savefig(csv_plot)
plt.show()
