import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import csv as csv
import os
import numpy as np
import matplotlib.pyplot as plt
from os import scandir, getcwd
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

probing_frequencies = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

state_1     = [29.17  , 70.83]
state_2     = [36.9  ,  63.1]
state_3     = [70.86  , 29.14]
state_4     = [77.86  , 22.14]
state_5     = [88.09  , 11.91]
state_6     = [89.33  , 10.67]
state_7     = [90.02 ,  9.98]
state_8     = [91.13 ,  8.87]
state_9     = [91.73 ,  8.27]
state_10    = [92.75  , 7.25]
state_11    = [93.1 ,   6.9]
state_12    = [93.86 ,  6.14]
state_13    = [93.62 ,  6.38]
state_14    = [94.63 ,  5.37]
state_15    = [96.4 ,   3.6]


blue_data = [state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]

red_data =  [state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]
 
f, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
 
bar_width = 0.5
 
# positions of the left bar-boundaries
bar_l = [i+1 for i in list(range(len(blue_data))) ]
print (bar_l)
# positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [i+(bar_width/2) for i in bar_l]
# Setting axis labels and ticks
fontsize_label = 26
fontsize_tick = 18 
 
ax1.bar(tick_pos, blue_data, width=bar_width, 
    alpha=0.9,
    color='#cccccc',
    edgecolor='black',
    hatch='...'
    )
ax1.bar(tick_pos, red_data, width=bar_width, 
    bottom=blue_data, 
    alpha=0.9,
    color='#969696',
    edgecolor='black',
    hatch='xxx',
    )
 
ax1.set_ylabel('Bandwidth (%)', fontsize=fontsize_label)
ax1.set_xlabel('Probing interval (s)', fontsize=fontsize_label)
ax1.tick_params(direction='out', labelsize=fontsize_tick)
plt.xticks(tick_pos, probing_frequencies)
plt.legend(loc='upper right')
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
#plt.ylim([0., 100*1.1])
# rotate axis labels
plt.setp(plt.gca().get_xticklabels(), rotation=0, horizontalalignment='right')
 
legend = ['SDN functions messages', 'CCO']
plt.legend(legend, bbox_to_anchor=(1.0, 1.1), loc="upper right", columnspacing=0.5, ncol=4, fontsize=17)
plt.tight_layout()
plt.grid()

#plt.savefig("load_cpu.eps",rasterized=True,dpi=300)
plt.show()

# Original http://blog.topspeedsnail.com/archives,dpi=300/724


