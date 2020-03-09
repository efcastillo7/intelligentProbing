import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from pathlib import Path
from os import scandir, getcwd
import os.path as path
from itertools import *
import csv

x = []
length_p = []
load_tx = []
cpu = []
frequency = []
rtt = []
currentPath = getcwd()
csv_file = currentPath + '/pcap/probing_05s-rtt.csv'

if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    i = 0
    for row in plots:
        try:
            i+=1
            x.append(i)        
            rtt.append(float(row["iRTT"]))  
            length_p.append(0)
        except Exception as e:
            print ('Line {i} is corrupt!'.format(i = i), " File ", Path(csv_file).name)
            pass
              

#print(list(accumulate(rtt)))


fig, ax = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
n, bins, patches = ax.hist(length_p, x, color='#636363', cumulative=True, label='Controller-Switch messages') #histtype='step'

#print(np.cumsum(reward))
y = np.cumsum(rtt)
ax.plot(bins, y, 'k--', linewidth=1.5, label='Cumulative reward')

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
