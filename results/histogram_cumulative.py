import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from os import scandir, getcwd
import os.path as path
from itertools import *
import csv

x = []
load_rx = []
load_tx = []
cpu = []
frequency = []
reward = []
currentPath = getcwd()
csv_file = currentPath + '/states_reward_xx.csv'

if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(int(row["row"]))
        cpu.append(float(row["cpu"]))
        frequency.append(float(row["frequency"]))
        reward.append(float(row["reward"]))
        load_rx.append(Bytes_to(int(row["load_rx"])))
        load_tx.append(Bytes_to(int(row["load_tx"])))

#print(list(accumulate(reward)))


fig, ax = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
n, bins, patches = ax.hist(load_rx, x, color='#636363', cumulative=True, label='Controller-Switch messages') #histtype='step'

print(bins)
#print(np.cumsum(reward))
#y = np.cumsum(reward)
#ax.plot(bins, y, 'k--', linewidth=1.5, label='Cumulative reward')

# tidy up the figure
ax.grid(True)
#ax.legend(loc='right')
ax.legend()
#ax.set_title('Cumulative step histograms')
ax.set_xlabel('Time steps')
ax.set_ylim(0, max(y))
ax.set_ylabel('Cumulative reward')

# Secondary axis
ax2 = ax.twinx()
ax2.set_ylim(0, 450)
ax2.set_ylabel("Control channel load (kbps)")

plt.show()