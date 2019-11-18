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
f_with_out_speed = ReadCSV(currentPath + "/probing_666s/speed_666.csv")
f_with_out_cpu = ReadCSV(currentPath + "/probing_666s/cpu_usage_666.csv","cpu")

f_with_speed = ReadCSV(currentPath + "/probing_00s/speed_00.csv")
f_with_cpu = ReadCSV(currentPath + "/probing_00s/cpu_usage_00.csv","cpu")

csv_plot = currentPath + '/with_without_ipro.svg'

############################ Subplot Controller-Switch #######################
#plt.style.use('ggplot')
labels = ['Controller-Switch messages without IPro', 'Controller-Switch messages with IPro']
colors=['#969696','#252525']
x = f_with_out_speed[0]
y = [f_with_out_speed[1], f_with_speed[1]]
plt.subplot(3, 1, 1)
#plt.plot(f_with_out_speed[0],f_with_out_speed[1],'#969696', f_with_speed[0],f_with_speed[1],'#252525', label='Controller-Switch messages')
for y_arr, label,color in zip(y, labels, colors):
    plt.plot(x, y_arr, label=label, color=color)

plt.ylabel('Control channel load (kbps)',fontsize=9)
plt.xlabel('(a)',fontsize=9)
plt.legend()
plt.subplots_adjust(hspace=0.3)
plt.grid()
#plt.show()

############################ Subplot Switch-Controller #######################
plt.subplot(3, 1, 2)
#plt.plot(f_with_out_speed[0],f_with_out_speed[2],'#969696',f_with_speed[0],f_with_speed[2],'#252525', label='Switch-Controller messages')
labels = ['Switch-Controller messages without IPro', 'Switch-Controller messages with IPro']
y = [f_with_out_speed[2], f_with_speed[2] ]
for y_arr, label,color in zip(y, labels, colors):
    plt.plot(x, y_arr, label=label, color=color)
plt.xlabel('(b)',fontsize=9)
plt.ylabel('Control channel load (kbps)', fontsize=9)
#plt.legend(bbox_to_anchor=(0.83, 0.8))
plt.legend() # probing 5s
#plt.tight_layout()
#plt.savefig(csv_plot, dpi=300)

plt.grid()

############################ Subplot CPU #####################################
plt.subplot(3, 1, 3)
#plt.plot(f_with_out_cpu[0],f_with_out_cpu[1],'#969696',f_with_cpu[0],f_with_cpu[1], '#252525', label='CPU usage')
labels = ['CPU usage without IPro', 'CPU usage with IPro']
x = [f_with_out_cpu[0],f_with_cpu[0]]
y = [f_with_out_cpu[1], f_with_cpu[1]]
for x_arr, y_arr, label,color in zip(x, y, labels, colors):
    plt.plot(x_arr, y_arr, label=label, color=color)
#plt.plot(x,z, 'b', label='Loaded from file!')
plt.xlabel('(c) \n Time (S)',fontsize=9, horizontalalignment='left')
plt.ylabel('CPU (%)',fontsize=9)
#plt.title('Interesting Graph\nCheck it out')
#plt.legend()
plt.legend()

#plt.tight_layout()
plt.grid()

plt.savefig(csv_plot, format="svg")
plt.show()