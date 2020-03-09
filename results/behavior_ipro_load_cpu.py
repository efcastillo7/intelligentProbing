import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from os import scandir, getcwd
import os.path as path
import numpy as np
from numpy import *
import csv

def ReadCSV(csv_file,opt='speed',csv_function='r'):
    x = []
    y = []
    z = []
        
    with open(csv_file, csv_function) as csvfile:
        plots = csv.DictReader(csvfile)
        if opt == 'speed':
            for row in plots:
                x.append(int(row["Row"]))
                y.append(Bytes_to(int(row["TX"])))
                z.append(Bytes_to(int(row["RX"])))
    
            speed_tx_mean = Bytes_to(np.mean(y))
            speed_rx_mean = Bytes_to(np.mean(z))
        elif opt == 'cpu':
            for row in plots:
                x.append(float(row["TIME"]))
                y.append(float(row["CPU"]))
                z.append(float(row["REAL_MB"]))             

    return [x, y, z]

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
        z.append((Bytes_to(int(row[col_rx])) * 100)/100000)

with open(csv_file_cpu,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        r.append(float(row["TIME"]))
        w.append(float(row["CPU"]))

############################ Subplot Overhead #######################
plt.subplot(2, 1, 1)
plt.plot(x,z, '#252525', label='CCO')
plt.xlabel('(a)',fontsize=26)
plt.ylabel('Bandwidth (%)', fontsize=26)
#plt.legend(bbox_to_anchor=(0.83, 0.8))
plt.legend(fontsize=16)
plt.tick_params(direction='out', labelsize=16)
#plt.tight_layout()
#plt.savefig(csv_plot, dpi=300)
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 22,
        }
#plt.text(50, 50, r'Exploration', fontdict=font)
#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']

for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

# shaded area
sixty = [1<x<238 for x in x]
ninety = [250<x<400 for x in x]
plt.fill_between(x,0,z,where=sixty,color='#969696',alpha=0.1)
#plt.fill_between(x,0,z,where=ninety,color='g',alpha=0.15)

# Annotate plot with integral results
#xy -> where the arrow points
#xytext -> where the annotation text is located
#style = dict(size=10, color='gray')
#plt.annotate('Exploration', xy=(150, 400), xytext=(60, 180), arrowprops=dict(facecolor='black', shrink=0.05))
plt.grid()
plt.text(20, 1.3, 'CCO ≈ 1.23%', fontsize=20) #(x,y)
plt.text(100, 0.25, r'Exploration', fontdict=font)
plt.axhline(y=1.23, label='', c='#d62728', linestyle=':',linewidth=2)

############################ Subplot CPU #####################################
plt.subplot(2, 1, 2)
colors=['#252525','#252525']
linestyles= ['-.','solid']
#f_with_out_speed = ReadCSV(currentPath + "/probing_666s/speed_666.csv")
f_with_out_cpu = ReadCSV(currentPath + "/probing_666s/cpu_usage_666.csv","cpu")
#f_with_speed = ReadCSV(currentPath + "/probing_00s/speed_00.csv")
f_with_cpu = ReadCSV(currentPath + "/probing_00s/cpu_usage_00.csv","cpu")

labels = ['CUC without IPro','CUC with IPro']
#x = [f_with_out_cpu[0],f_with_cpu[0]]
#y = [f_with_out_cpu[1], f_with_cpu[1]]
cpu_without_ipo_x = []
cpu_without_ipo_y = []
for i in range(600):
    cpu_without_ipo_x.append(i)

for i in range(600):
    cpu_without_ipo_y.append(39.9)

x = [cpu_without_ipo_x,f_with_cpu[0]]
y = [cpu_without_ipo_y, f_with_cpu[1]]
#print(len(f_with_out_cpu[1]), len(f_with_cpu[1]))
for x_arr, y_arr, label,color,linestyle in zip(x, y, labels, colors,linestyles):
    plt.plot(x_arr, y_arr, label=label, color=color, ls=linestyle)
#plt.plot(x,z, 'b', label='Loaded from file!')
plt.xlabel('(b) \n Time (s)',fontsize=26, horizontalalignment='left')
plt.ylabel('CUC (%)',fontsize=26)
#plt.title('Interesting Graph\nCheck it out')
#plt.legend()
plt.legend(fontsize=16)
plt.tick_params(direction='out', labelsize=16)
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 22,
        }
#plt.text(50, 20, r'Exploration', fontdict=font)

#style = dict(size=10, color='gray')
plt.annotate('CUC increase ≈ 7.4%', xy=(320, 43), xytext=(280, 25), arrowprops=dict(facecolor='black', shrink=0.01),fontsize=20)
#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

#plt.tight_layout()

# shaded area
sixty = [1<r<238 for r in r]
ninety = [250<r<400 for r in r]
plt.fill_between(r,0,w,where=sixty,color='#969696',alpha=0.1)
plt.grid()

#plt.savefig(csv_plot)
plt.subplots_adjust(left=0.15)
plt.tight_layout()
plt.axhline(y=47.3, label='', c='#d62728', linestyle=':',linewidth=2)
#plt.axhline(y=39.9, label='xxxxxxxxx', c='#d62728', linestyle=':')
plt.text(-27, 48.5, '47.3%', fontsize=16)
plt.fill_between(f_with_cpu[0], f_with_cpu[1], 39.9, facecolor='#c4c3c3', interpolate=True)
plt.show()

"""
plt.plot(r,w, '#252525', label='CPU usage')
#plt.plot(x,z, 'b', label='Loaded from file!')
plt.xlabel('(b) \n Time (S)',fontsize=26, horizontalalignment='left')
plt.ylabel('CPU (%)',fontsize=26)
#plt.title('Interesting Graph\nCheck it out')
plt.legend(fontsize=16)
plt.tick_params(direction='out', labelsize=16)
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 22,
        }
plt.text(50, 20, r'Exploration', fontdict=font)

#style = dict(size=10, color='gray')
#plt.annotate('Exploration', xy=(120, 40), xytext=(10, 10), arrowprops=dict(facecolor='black', shrink=0.05))
#Vertical Lines
xcoords = [0, 238]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

#plt.tight_layout()

# shaded area
sixty = [1<r<238 for r in r]
ninety = [250<r<400 for r in r]
plt.fill_between(r,0,w,where=sixty,color='#969696',alpha=0.1)
plt.grid()

#plt.savefig(csv_plot)
plt.subplots_adjust(left=0.15)
plt.tight_layout()
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

ax.set_ylabel('CPU (%)', color='g', fontsize=26)
ax.set_xlabel('Time (s)', fontsize=26)
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
#fig.savefig(csv_plot_cpu, dpi=300)
#plt.show()
"""