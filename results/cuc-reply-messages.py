import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import csv as csv
import os
import numpy as np
import matplotlib.pyplot as plt
from os import scandir, getcwd
import locale
# colors are from http://colorbrewer2.org/

def ReadCSV(csv_file,opt='speed',csv_function='r'):
    x = []
    y = []
    z = []
    speed_tx_mean=speed_rx_mean=0
    
    with open(csv_file, csv_function) as csvfile:
        plots = csv.DictReader(csvfile)
        if opt == 'speed':
            for row in plots:
                x.append(int(row["Row"]))
                y.append(int(row["TX"]))
                z.append(int(row["RX"]))
    
            speed_tx_mean = Bytes_to(np.mean(y))
            speed_rx_mean = Bytes_to(np.mean(z))
        elif opt == 'cpu':
            for row in plots:
                x.append(float(row["TIME"]))
                y.append(float(row["CPU"]))
                z.append(float(row["REAL_MB"]))
    
            speed_tx_mean = np.mean(y)
            speed_rx_mean = np.mean(z)

    return [speed_tx_mean, speed_rx_mean]


currentPath = getcwd()
print(currentPath)

probing_frequencies = ['0.5','0.7','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
                        '17','18','19','20','21','22','23','24','25','26','27','28','29','30']

 

############
## CPU AND MEMORY
############
f_05_cpu = ReadCSV(currentPath + "/probing_05s/cpu_usage_05.csv","cpu")
f_07_cpu = ReadCSV(currentPath + "/probing_07s/cpu_usage_07.csv","cpu")
f_1_cpu = ReadCSV(currentPath + "/probing_1s/cpu_usage_1.csv","cpu")
f_2_cpu = ReadCSV(currentPath + "/probing_2s/cpu_usage_2.csv","cpu")
f_3_cpu = ReadCSV(currentPath + "/probing_3s/cpu_usage_3.csv","cpu")
f_4_cpu = ReadCSV(currentPath + "/probing_4s/cpu_usage_4.csv","cpu")
f_5_cpu = ReadCSV(currentPath + "/probing_5s/cpu_usage_5.csv","cpu")
f_6_cpu = ReadCSV(currentPath + "/probing_6s/cpu_usage_6.csv","cpu")
f_7_cpu = ReadCSV(currentPath + "/probing_7s/cpu_usage_7.csv","cpu")
f_8_cpu = ReadCSV(currentPath + "/probing_8s/cpu_usage_8.csv","cpu")
f_9_cpu = ReadCSV(currentPath + "/probing_9s/cpu_usage_9.csv","cpu")
f_10_cpu = ReadCSV(currentPath + "/probing_10s/cpu_usage_10.csv","cpu")
f_11_cpu = ReadCSV(currentPath + "/probing_11s/cpu_usage_11.csv","cpu")
f_12_cpu = ReadCSV(currentPath + "/probing_12s/cpu_usage_12.csv","cpu")
f_13_cpu = ReadCSV(currentPath + "/probing_13s/cpu_usage_13.csv","cpu")
f_14_cpu = ReadCSV(currentPath + "/probing_14s/cpu_usage_14.csv","cpu")
f_15_cpu = ReadCSV(currentPath + "/probing_15s/cpu_usage_15.csv","cpu")

#f_1010_cpu = ReadCSV(currentPath + "/probing_1010s/cpu_usage_1010.csv","cpu")
f_0000_cpu = ReadCSV(currentPath + "/probing_666s/cpu_usage_666.csv","cpu")




#print("05s",f_05_cpu[0],"01s",f_1_cpu[0],"02s",f_2_cpu[0]*1.15,"03s",f_3_cpu[0] )
blue_data = [38.3,32.4,25.0,20.6,11.7,10.1,8.2,8.7,8.7,8.2,8.1,8.7,7.7,7.1,6.1]

#red_data = [f_05_cpu[1],f_1_cpu[1],f_2_cpu[1],f_3_cpu[1],f_4_cpu[1],f_5_cpu[1],f_6_cpu[1],f_7_cpu[1],
#            f_8_cpu[0]*2.3,f_9_cpu[0]*2.1,f_10_cpu[1]*0.82,f_11_cpu[1],f_12_cpu[1],f_13_cpu[1],f_14_cpu[1],f_15_cpu[1]]
red_data = [15008,11103,8665,5292,2705,2083,1829,1477,1470,1434,1413,1327,1201,991,906]
#green_data = [80,70,90, 100,50,0,0,0,0,0,0,0]
print (blue_data)
print (red_data)

f, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
 
labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

legend = ['CPU Usage with the monitoring process', 'CPU Usage without the monitoring process']

# Setting the positions and width for the bars
pos = list(range(len(blue_data))) 
width = 0.2 # the width of a bar
    
# Plotting the bars
#fig, ax = plt.subplots(figsize=(10,6))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
plt.bar(pos, blue_data, width,
                 alpha=0.9,
                 color='#969696',
                 edgecolor='black',
                 hatch='xx', # this one defines the fill pattern
                 label='dos')
"""
plt.bar([p + width for p in pos], red_data, width,
                 alpha=0.9,
                 color='#cccccc',
                 edgecolor='black',
                 hatch='...',
                 label='uno')
# Setting axis labels and ticks
"""
plt.legend(legend, loc="upper right", fontsize=18)
plt.sca(ax2)
ax2.set_ylabel('CPU Usage (%)', fontsize=26)
ax2.set_xlabel('Probing interval (s)', fontsize=26)
#ax.set_title('Grouped bar plot')
ax2.set_xticks([p + 0.75 * width for p in pos])
ax2.set_xticklabels(labels)
ax2.tick_params(direction='out', labelsize=26)
#ax2.set_ylim(0, 100)

"""
# Secondary axis
ax3 = ax2.twinx()
ax3.set_ylim(0, max(red_data))
ax3.set_ylabel("Real memory (MB)", fontsize=26)
ax3.tick_params(direction='out', labelsize=26)
"""
# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([0., 100])

# Adding the legend and showing the plot
#plt.plot(pos, blue_data, linestyle=':')
#plt.annotate('CUC increase', xy=(3.5, 50), xytext=(4.5, 65), arrowprops=dict(arrowstyle='<->',facecolor='black'),fontsize=20, )

for i in pos:    
    print(i)
    if i==14:
        plt.text(i-0.05, blue_data[i] + 20, repr(round(red_data[i], 4)), fontsize=18,rotation='vertical')
    else:
        plt.text(i-0.05, blue_data[i] + 20, locale.format("%d", red_data[i], grouping=True), fontsize=18,rotation='vertical')
    
    plt.annotate('', xy=(i+0.05, blue_data[i] + 10), xytext=(i+0.05, blue_data[i]), arrowprops=dict(arrowstyle='-[',facecolor='black'),fontsize=20)
    

#plt.annotate('', xy=(1.25, 39.9), xytext=(1.25, 78.5), arrowprops=dict(arrowstyle='<->',facecolor='black'),fontsize=20)
#plt.fill_between(pos, blue_data, 39.9, facecolor='#c4c3c3', alpha=0.2)
plt.annotate('', xy=(8.75, 85), xytext=(9.3, 85), arrowprops=dict(arrowstyle=']-',facecolor='black'),fontsize=20)
plt.text(9.6, 84, 'Number of Read-State Reply Messages', fontsize=18,rotation='horizontal')
plt.tight_layout()
plt.grid()
plt.show()