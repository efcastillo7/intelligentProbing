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

xi = []
rtt = []
currentPath = getcwd()
csv_file = currentPath + '/pcap/probing_14s-rtt.csv'

if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

with open(csv_file,'r') as csvfile:
    if not path.exists(csv_file):
            print("The file does not exist")
            sys.exit()
    
    j=0
    for i, row in enumerate(csv.reader(open(csv_file, 'r', encoding='utf-8'))):
        if not i or not row:
            continue
        _,_,_,_,_,_,_,iRTT,_ = row

        try:
            j+=1
            xi.append(j)    
            rtt.append(float(iRTT)*1000)
        except Exception as e:
            print ('Line {i} is corrupt!'.format(i = i), " File ", Path(csv_file).name)
            pass

mu = 200
sigma = 25
n_bins = 60
x = rtt

fig, ax = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
n, bins, patches = ax.hist(rtt, n_bins, density=True, histtype='step', cumulative=True, label='Empirical')

# Add a line showing the expected distribution.
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
y = y.cumsum()
y /= y[-1]

ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Cumulative step histograms')
ax.set_xlabel('Annual rainfall (mm)')
ax.set_ylabel('Likelihood of occurrence')

plt.show()