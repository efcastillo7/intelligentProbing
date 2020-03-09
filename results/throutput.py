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

#probing_frequencies = ['0.7','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
#                        '17','18','19','20','21','22','23','24','25','26','27','28','29','30']

#blue_data = [51.62,58.44,57.35,62.77,90.09,94.47,90.62,67.57,62.67,64.55,61.22,61.63,61.77,59.25,58.11,51.51]
blue_data = [52.43,54.04,66.21,83.83,88.83,86.06,69.94,67.94,66.95,66.75,64.41,62.08,61.11,59.34,52.02]

f, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
 
labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

legend = ['Throughput']

# Setting the positions and width for the bars
pos = list(range(len(blue_data))) 
width = 0.2 # the width of a bar
    
# Plotting the bars
#fig, ax = plt.subplots(figsize=(10,6))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
plt.plot(labels, blue_data, 'k',
                 label='Throughput',
                 marker='o',
                 color='black') #https://matplotlib.org/api/markers_api.html

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 26,
        }
plt.text(3, 50, r'MA higher than 66%', fontdict=font)
    

# Setting axis labels and ticks
plt.legend(legend, loc="upper right")
plt.sca(ax2)
ax2.set_ylabel('MA (%)',fontsize=26)
ax2.set_xlabel('Probing interval (s)',fontsize=26)
#ax.set_title('Grouped bar plot')
#ax2.set_xticks([p + 1.5 * width for p in pos])
ax2.set_xticklabels(labels, fontsize=26)
#ax2.tick_params(direction='out', length=6, width=2, colors='r',grid_color='r', grid_alpha=0.5)
ax2.tick_params(direction='out', labelsize=26) #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html
# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([40., max(blue_data)*1.1])
plt.legend(fontsize=18, loc="upper right")
plt.grid()
#plt.annotate('accuracy higher than 60%', xy=(40, 60), xytext=(15, 15), arrowprops=dict(facecolor='black', shrink=0.05))
#Vertical Lines
xcoords = [2, 9]
colors = ['#08519c','#08519c']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c, linestyle=':')

r = labels
w = blue_data
# shaded area
sixty = [2<float(r)<11 for r in r]
plt.fill_between(r,0,w,where=sixty,color='#969696',alpha=0.1)

plt.subplots_adjust(left=0.15)
plt.show()


