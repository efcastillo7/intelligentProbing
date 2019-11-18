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

# shaded area
sixty = [1<x<238 for x in x]
ninety = [250<x<400 for x in x]
plt.fill_between(x,0,y,where=sixty,color='g',alpha=0.1)
"""
#vertical lines
xcoords = [1, 3.5, 4.5]
colors = ['r','k','b']

for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c)
"""
############################ Subplot Switch-Controller #######################
plt.subplot(3, 1, 2)
plt.plot(x,z, '#252525', label='Switch-Controller messages')
plt.xlabel('(b)',fontsize=9)
plt.ylabel('Control channel load (kbps)', fontsize=9)
#plt.legend(bbox_to_anchor=(0.83, 0.8))
plt.legend(bbox_to_anchor=(0.78, 0.8))
#plt.tight_layout()
#plt.savefig(csv_plot, dpi=300)

#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

# shaded area
sixty = [1<x<238 for x in x]
ninety = [250<x<400 for x in x]
plt.fill_between(x,0,z,where=sixty,color='g',alpha=0.1)
#plt.fill_between(x,0,z,where=ninety,color='g',alpha=0.15)

# Annotate plot with integral results
#xy -> where the arrow points
#xytext -> where the annotation text is located
style = dict(size=10, color='gray')
plt.annotate('Exploration', xy=(150, 400), xytext=(60, 180),
            arrowprops=dict(facecolor='black', shrink=0.05))
plt.grid()

############################ Subplot CPU #####################################
plt.subplot(3, 1, 3)
plt.plot(r,w, '#636363', label='CPU usage')
#plt.plot(x,z, 'b', label='Loaded from file!')
plt.xlabel('(c) \n Time (S)',fontsize=9, horizontalalignment='left')
plt.ylabel('CPU (%)',fontsize=9)
#plt.title('Interesting Graph\nCheck it out')
plt.legend()

style = dict(size=10, color='gray')
plt.annotate('Exploration', xy=(120, 40), xytext=(10, 10),
            arrowprops=dict(facecolor='black', shrink=0.05))
#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

#plt.tight_layout()

# shaded area
sixty = [1<r<238 for r in r]
ninety = [250<r<400 for r in r]
plt.fill_between(r,0,w,where=sixty,color='g',alpha=0.1)
plt.grid()

plt.savefig(csv_plot)
plt.show()

####################### CPU PLOT ##############################################

csv_file_cpu = currentPath + '/probing_'+ sys.argv[1] + 's/cpu_usage_' + sys.argv[1] + '.csv'
csv_plot_cpu = currentPath + '/probing_'+ sys.argv[1] + 's/cpu_usage_' + sys.argv[1] + '.png'

x = []
y = []
z = []

with open(csv_file_cpu,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(float(row["TIME"]))
        y.append(float(row["CPU"]))
        z.append(float(row["REAL_MB"]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x, y, '-', lw=1, color='#252525')

ax.set_ylabel('CPU (%)', color='g', fontsize=9)
ax.set_xlabel('Time (s)', fontsize=9)
ax.set_ylim(0., max(y) * 1.2)


ax2 = ax.twinx()
ax2.plot(x, z, '-', lw=1, color='b')
ax2.set_ylim(0., max(z) * 1.2)
ax2.set_ylabel('Real Memory (MB)', color='b', fontsize=9)
ax.grid()

style = dict(size=10, color='gray')
plt.annotate('Exploration', xy=(20, 30), xytext=(20, 20),
            arrowprops=dict(facecolor='black', shrink=0.05))

xcoords = [5, 150]
colors = ['#08519c','#08519c']

for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

plt.tight_layout()
plt.grid()
fig.savefig(csv_plot_cpu, dpi=300)
#plt.show()
