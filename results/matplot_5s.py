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
y = []
z = []
w = []
r = []

currentPath = getcwd()
print(currentPath)
csv_file = currentPath + '/probing_'+ sys.argv[1] + 's/speed_' + sys.argv[1] + '.csv'
csv_plot = currentPath + '/probing_'+ sys.argv[1] + 's/speed_' + sys.argv[1] + '.png'
csv_file_cpu = currentPath + '/probing_'+ sys.argv[1] + 's/cpu_usage_' + sys.argv[1] + '.csv'

if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

col_rx = "RX"
col_tx = "TX"
if sys.argv[1] == "8":
    col_tx = "RX"
    col_rx = "TX"

with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(int(row["Row"]))
        y.append(Bytes_to(int(row[col_tx])))
        z.append(Bytes_to(int(row[col_rx])))

with open(csv_file_cpu,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        r.append(float(row["TIME"]))
        w.append(float(row["CPU"]))

############################ Subplot Controller-Switch #######################
#plt.style.use('ggplot')
plt.subplot(3, 1, 1)
plt.plot(x,y, '#636363', label='Controller-Switch messages')
plt.ylabel('Control channel load (kbps)',fontsize=9)
plt.xlabel('(a)',fontsize=9)
plt.legend()
plt.subplots_adjust(hspace=0.3)
plt.grid()
#plt.show()

#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']

for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

############################ Subplot Switch-Controller #######################
plt.subplot(3, 1, 2)
plt.plot(x,z, '#252525', label='Switch-Controller messages')
plt.xlabel('(b)',fontsize=9)
plt.ylabel('Control channel load (kbps)', fontsize=9)
#plt.legend(bbox_to_anchor=(0.83, 0.8))
plt.legend(bbox_to_anchor=(0.25, 0.95)) # probing 5s
#plt.tight_layout()
#plt.savefig(csv_plot, dpi=300)

plt.grid()

############################ Subplot CPU #####################################
plt.subplot(3, 1, 3)
plt.plot(r,w, '#636363', label='CPU usage')
#plt.plot(x,z, 'b', label='Loaded from file!')
plt.xlabel('(c) \n Time (S)',fontsize=9, horizontalalignment='left')
plt.ylabel('CPU (%)',fontsize=9)
#plt.title('Interesting Graph\nCheck it out')
#plt.legend()
plt.legend(bbox_to_anchor=(0.15, 0.96))

#plt.tight_layout()
plt.grid()

plt.savefig(csv_plot)
plt.show()