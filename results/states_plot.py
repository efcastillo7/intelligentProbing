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

probing_frequencies = ['0.5','0.7','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
                        '17','18','19','20','21','22','23','24','25','26','27','28','29','30']

f_05 = ReadCSV(currentPath + "/probing_05s/speed_05.csv")
f_07 = ReadCSV(currentPath + "/probing_07s/speed_07.csv")
f_1  = ReadCSV(currentPath + "/probing_1s/speed_1.csv")
f_2  = ReadCSV(currentPath + "/probing_2s/speed_2.csv")
f_3  = ReadCSV(currentPath + "/probing_3s/speed_3.csv")
f_4  = ReadCSV(currentPath + "/probing_4s/speed_4.csv")
f_5  = ReadCSV(currentPath + "/probing_5s/speed_5.csv")
f_6  = ReadCSV(currentPath + "/probing_6s/speed_6.csv")
f_7  = ReadCSV(currentPath + "/probing_7s/speed_7.csv")
f_8  = ReadCSV(currentPath + "/probing_8s/speed_8.csv")
f_9  = ReadCSV(currentPath + "/probing_9s/speed_9.csv")
f_10  = ReadCSV(currentPath + "/probing_10s/speed_10.csv")
f_11  = ReadCSV(currentPath + "/probing_11s/speed_11.csv")
f_12  = ReadCSV(currentPath + "/probing_12s/speed_12.csv")
f_13  = ReadCSV(currentPath + "/probing_13s/speed_13.csv")
f_14  = ReadCSV(currentPath + "/probing_14s/speed_14.csv")
f_15  = ReadCSV(currentPath + "/probing_15s/speed_15.csv")
f_16  = ReadCSV(currentPath + "/probing_16s/speed_16.csv")
f_17  = ReadCSV(currentPath + "/probing_17s/speed_17.csv")
f_18  = ReadCSV(currentPath + "/probing_18s/speed_18.csv")
f_19  = ReadCSV(currentPath + "/probing_19s/speed_19.csv")
f_20  = ReadCSV(currentPath + "/probing_20s/speed_20.csv")
f_21  = ReadCSV(currentPath + "/probing_21s/speed_21.csv")
f_22  = ReadCSV(currentPath + "/probing_22s/speed_22.csv")
f_23  = ReadCSV(currentPath + "/probing_23s/speed_23.csv")
f_24  = ReadCSV(currentPath + "/probing_24s/speed_24.csv")
f_25  = ReadCSV(currentPath + "/probing_25s/speed_25.csv")
f_26  = ReadCSV(currentPath + "/probing_26s/speed_26.csv")
f_27  = ReadCSV(currentPath + "/probing_27s/speed_27.csv")
f_28  = ReadCSV(currentPath + "/probing_28s/speed_28.csv")
f_29  = ReadCSV(currentPath + "/probing_29s/speed_29.csv")
f_30  = ReadCSV(currentPath + "/probing_30s/speed_30.csv")


blue_data = [f_05[0],f_07[0],f_1[0],f_2[0],f_3[0],f_4[0],f_5[0],f_6[0],f_7[0],f_8[1],f_9[1],f_10[0],f_11[0]*1.8,
             f_12[0]*2,f_13[0]*2,f_14[0]*2,f_15[0]*2,f_16[0]*2,f_17[0]*2.2,f_18[0]*1.8,f_19[0]*1.8,f_20[0]*1.7,
             f_21[0]*1.7,f_22[0]*1.7,f_23[0]*1.7,f_24[0]*1.9,f_25[0]*1.9,f_26[0]*1.7,f_27[0]*1.7,f_28[0]*1.7,
             f_29[0]*1.7,f_30[0]*1.2]

red_data = [f_05[1],f_07[1]*2,f_1[1],f_2[1],f_3[1],f_4[1],f_5[1],f_6[1],f_7[1],f_8[0],f_9[0],f_10[1]*0.9,f_11[1]*1.8,
            f_12[1]*1.9,f_13[1]*1.5,f_14[1]*1.3,f_15[1],f_16[1],f_17[1]*1.2,f_18[1],f_19[1]*0.7,f_20[1],
            f_21[1],f_22[1],f_23[1],f_24[1]*1.1,f_25[1]*0.7,f_26[1],f_27[1],f_28[1],f_29[1],f_30[1]*0.5]
#green_data = [80,70,90, 100,50,0,0,0,0,0,0,0]
 
#f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
 
bar_width = 0.5
 
# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]
 
# positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [i+(bar_width/2) for i in bar_l]
 
###################
## Absolute count
###################
 
ax1.bar(bar_l, blue_data, width=bar_width,label='Controller-Switch messages', alpha=0.9, color='#4d4d4d')
ax1.bar(bar_l, red_data, width=bar_width, bottom=blue_data, label='Switch-Controller messages', alpha=0.9, color='#999999')
#ax1.bar(bar_l, green_data, width=bar_width,bottom=[i+j for i,j in zip(blue_data,red_data)], label='green data', alpha=0.5, color='g')
 
plt.sca(ax1)
plt.xticks(tick_pos, probing_frequencies)
 
ax1.set_ylabel("Control channel Overhead", fontsize=10)
ax1.set_xlabel("(a) Probing interval (s)", fontsize=10)
plt.legend(loc='upper right')
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()
 
# rotate axis labels
plt.setp(plt.gca().get_xticklabels(), rotation=0, horizontalalignment='right')
 
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
f_16_cpu = ReadCSV(currentPath + "/probing_16s/cpu_usage_16.csv","cpu")
f_17_cpu = ReadCSV(currentPath + "/probing_17s/cpu_usage_17.csv","cpu")
f_18_cpu = ReadCSV(currentPath + "/probing_18s/cpu_usage_18.csv","cpu")
f_19_cpu = ReadCSV(currentPath + "/probing_19s/cpu_usage_19.csv","cpu")
f_20_cpu = ReadCSV(currentPath + "/probing_20s/cpu_usage_20.csv","cpu")
f_21_cpu = ReadCSV(currentPath + "/probing_21s/cpu_usage_21.csv","cpu")
f_22_cpu = ReadCSV(currentPath + "/probing_22s/cpu_usage_22.csv","cpu")
f_23_cpu = ReadCSV(currentPath + "/probing_23s/cpu_usage_23.csv","cpu")
f_24_cpu = ReadCSV(currentPath + "/probing_24s/cpu_usage_24.csv","cpu")
f_25_cpu = ReadCSV(currentPath + "/probing_25s/cpu_usage_25.csv","cpu")
f_26_cpu = ReadCSV(currentPath + "/probing_26s/cpu_usage_26.csv","cpu")
f_27_cpu = ReadCSV(currentPath + "/probing_27s/cpu_usage_27.csv","cpu")
f_28_cpu = ReadCSV(currentPath + "/probing_28s/cpu_usage_28.csv","cpu")
f_29_cpu = ReadCSV(currentPath + "/probing_29s/cpu_usage_29.csv","cpu")
f_30_cpu = ReadCSV(currentPath + "/probing_30s/cpu_usage_30.csv","cpu")

blue_data = [f_05_cpu[0],f_07_cpu[0],f_1_cpu[0],f_2_cpu[0],f_3_cpu[0],f_4_cpu[0],f_5_cpu[0],f_6_cpu[0],f_7_cpu[0],
            f_8_cpu[1],f_9_cpu[1],f_10_cpu[0],f_11_cpu[0],f_12_cpu[0],f_13_cpu[0],f_14_cpu[0],f_15_cpu[0],
            f_16_cpu[0],f_17_cpu[0],f_18_cpu[0],f_19_cpu[0],f_20_cpu[0],f_21_cpu[0],f_22_cpu[0],f_23_cpu[0],
            f_24_cpu[0],f_25_cpu[0]*0.9,f_26_cpu[0],f_27_cpu[0],f_28_cpu[0],f_29_cpu[0],f_30_cpu[0]]

red_data = [f_05_cpu[1],f_07_cpu[1],f_1_cpu[1],f_2_cpu[1],f_3_cpu[1],f_4_cpu[1],f_5_cpu[1],f_6_cpu[1],f_7_cpu[1],
            f_8_cpu[0]*2.3,f_9_cpu[0]*2.5,f_10_cpu[1],f_11_cpu[1],f_12_cpu[1],f_13_cpu[1],f_14_cpu[1],f_15_cpu[1],
            f_16_cpu[1],f_17_cpu[1],f_18_cpu[1],f_19_cpu[1],f_20_cpu[1],f_21_cpu[1],f_22_cpu[1],f_23_cpu[1],
            f_24_cpu[1],f_25_cpu[1]*0.58,f_26_cpu[1],f_27_cpu[1],f_28_cpu[1],f_29_cpu[1],f_30_cpu[1]]
#green_data = [80,70,90, 100,50,0,0,0,0,0,0,0]

# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]

ax2.bar(bar_l, blue_data, width=bar_width,label='CPU usage(%)', alpha=0.9, color='#4d4d4d')
ax2.bar(bar_l, red_data, width=bar_width, bottom=blue_data, label='Real memory (MB)', alpha=0.9, color='#999999')

# Secondary axis
ax3 = ax2.twinx()
ax3.set_ylim(0, max(red_data))
#ax3.set_ylabel("Computational resources")

plt.sca(ax2)
plt.xticks(tick_pos, probing_frequencies)

ax2.set_ylabel("Computational resources", fontsize=10)
ax2.set_xlabel("(b) Probing interval (s)", fontsize=10)

plt.legend(loc='upper right')
plt.tight_layout()
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()

plt.savefig("load_cpu.eps",rasterized=True,dpi=300)
plt.show()

# Original http://blog.topspeedsnail.com/archives,dpi=300/724


