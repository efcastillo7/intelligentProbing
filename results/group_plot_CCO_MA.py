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

blue_data = [0.75, 3.05, 7.9]

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
 
bar_width = 0.5
 
# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]
 
# positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [i+(bar_width/2) for i in bar_l]
 
###################
## Absolute count
###################
 
ax1.bar(bar_l, blue_data, width=bar_width, alpha=0.9, color='#969696', edgecolor='black',hatch='xx')

xtcks_cco = ['IPro','Payless','PPA']
legend = ['CCO']
 
plt.sca(ax1)
plt.xticks(tick_pos, xtcks_cco)
plt.tick_params(direction='out', labelsize=26)
plt.legend(legend, loc="upper right", fontsize=18)
 
ax1.set_ylabel("CCO [%]", fontsize=26)
ax1.set_xlabel("(a)", fontsize=26)
plt.ylim([0, 100])
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()
 
# rotate axis labels
plt.setp(plt.gca().get_xticklabels(), rotation=0, horizontalalignment='right')
 
############
## MA
############

blue_data = [92.69, 79.8, 81.6]

# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]
tick_pos = [i+(bar_width/2) for i in bar_l]

legend = ['Accuracy of Throughput']

ax2.bar(bar_l, blue_data, width=bar_width, alpha=0.9, color='#969696',edgecolor='black', hatch='...')
#ax2.bar(bar_l, red_data, width=bar_width, bottom=blue_data, label='Real Memory (MB)', alpha=0.9, color='#999999')

plt.sca(ax2)
plt.xticks(tick_pos, xtcks_cco)
plt.tick_params(direction='out', labelsize=26)

ax2.set_ylabel("MA [%]", fontsize=26)
ax2.set_xlabel("(b)", fontsize=26)

plt.legend(legend, loc="upper right", fontsize=18)
plt.tight_layout()
plt.ylim([0, 100])
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()
plt.show()

# Original http://blog.topspeedsnail.com/archives,dpi=300/724


