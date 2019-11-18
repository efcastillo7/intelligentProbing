import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from os import scandir, getcwd
import os.path as path
import numpy as np
from numpy import *
import csv

#current position getcwd()
x = []
load_rx = []
cpu = []
frequency = []
reward = []

currentPath = getcwd()
print(currentPath)
csv_file = currentPath + '/states_reward_xx.csv'
csv_plot = currentPath + '/reward.png'


if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(int(row["row"]))
        load_rx.append(Bytes_to(int(row["load_rx"])))
        cpu.append(float(row["cpu"]))
        frequency.append(float(row["frequency"]))
        reward.append(float(row["reward"]))

############################ Subplot Controller-Switch #######################
#plt.style.use('ggplot')
plt.subplot(2, 1, 1)
plt.plot(x,frequency, '#636363', label='Monitoring interval')
plt.ylabel('Monitoring interval (S)',fontsize=9)
plt.xlabel('(a)',fontsize=9)
plt.legend()
plt.grid()
#Vertical Lines
xcoords = [140, 220]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')
#plt.show()
############################ Subplot Switch-Controller #######################
"""
plt.subplot(3, 1, 2)
plt.plot(x,cpu, '#252525', label='cpu')
#plt.xlabel('Time (S)',fontsize=9)
plt.ylabel('CPU (%)', fontsize=9)
plt.legend(bbox_to_anchor=(0.1, 0.8))
#plt.tight_layout()
#plt.savefig(csv_plot, dpi=300)
plt.grid()
"""
############################ Subplot CPU #####################################

plt.subplot(2, 1, 2)
plt.plot(x,reward, '#636363', label='Reward')
#plt.plot(x,z, 'b', label='Loaded from file!')

plt.xlabel('Time (S)',fontsize=9)
plt.ylabel('Reaward',fontsize=9)
plt.xlabel('(b) \n Time (S)',fontsize=9, horizontalalignment='left')
#plt.title('Interesting Graph\nCheck it out')

plt.legend()
plt.grid()
plt.subplots_adjust(hspace=0.3)
plt.tight_layout()

#Vertical Lines
xcoords = [140, 220]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')
plt.savefig(csv_plot)
plt.show()
