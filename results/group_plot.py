import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import csv as csv
import os
import numpy as np
import matplotlib.pyplot as plt

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


f_05 = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_05s/speed_05.csv")
f_1  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_1s/speed_1.csv")
f_2  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_2s/speed_2.csv")
f_3  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_3s/speed_3.csv")
f_4  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_4s/speed_4.csv")
f_5  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_5s/speed_5.csv")
f_6  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_6s/speed_6.csv")
f_7  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_7s/speed_7.csv")
f_10  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_10s/speed_10.csv")
f_15  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_15s/speed_15.csv")
f_20  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_20s/speed_20.csv")
f_25  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_25s/speed_25.csv")
f_30  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_30s/speed_30.csv")


blue_data = [f_05[0],f_1[0],f_2[0],f_3[0],f_4[0],f_5[0],f_6[0],f_7[0],f_10[0],f_15[0],f_20[0],f_25[0],f_30[0]]
red_data = [f_05[1],f_1[1],f_2[1],f_3[1],f_4[1],f_5[1],f_6[1],f_7[1],f_10[1],f_15[1],f_20[1],f_20[1],f_30[1]]
green_data = [80,70,90, 100,50,0,0,0,0,0,0,0]
 
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
 
bar_width = 0.5
 
# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]
 
# positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [i+(bar_width/2) for i in bar_l]
 
###################
## Absolute count
###################
 
ax1.bar(bar_l, blue_data, width=bar_width,label='Controller-Switch', alpha=0.5, color='b')
ax1.bar(bar_l, red_data, width=bar_width, bottom=blue_data, label='Switch-Controller', alpha=0.5, color='r')
#ax1.bar(bar_l, green_data, width=bar_width,bottom=[i+j for i,j in zip(blue_data,red_data)], label='green data', alpha=0.5, color='g')
 
plt.sca(ax1)
plt.xticks(tick_pos, ['0.5', '1', '2', '3', '4', '5', '6', '7', '10', '15', '20', '25','30'])
 
ax1.set_ylabel("Control channel load (kbps)")
ax1.set_xlabel("Monitoring interval (S)")
plt.legend(loc='upper right')
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()
 
# rotate axis labels
plt.setp(plt.gca().get_xticklabels(), rotation=0, horizontalalignment='right')
 
############
## CPU AND MEMORY
############
f_05_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_05s/cpu_usage_05.csv","cpu")
f_1_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_1s/cpu_usage_1.csv","cpu")
f_2_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_2s/cpu_usage_2.csv","cpu")
f_3_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_3s/cpu_usage_3.csv","cpu")
f_4_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_4s/cpu_usage_4.csv","cpu")
f_5_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_5s/cpu_usage_5.csv","cpu")
f_6_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_6s/cpu_usage_6.csv","cpu")
f_7_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_7s/cpu_usage_7.csv","cpu")
f_10_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_10s/cpu_usage_10.csv","cpu")
f_15_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_15s/cpu_usage_15.csv","cpu")
f_20_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_20s/cpu_usage_20.csv","cpu")
f_25_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_25s/cpu_usage_25.csv","cpu")
f_30_cpu = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_30s/cpu_usage_30.csv","cpu")



blue_data = [f_05_cpu[0],f_1_cpu[0],f_2_cpu[0],f_3_cpu[0],f_4_cpu[0],f_5_cpu[0],f_6_cpu[0],f_7_cpu[0],f_10_cpu[0],f_15_cpu[0],f_20_cpu[0],f_25_cpu[0],f_30_cpu[0]]
red_data = [f_05_cpu[1],f_1_cpu[1],f_2_cpu[1],f_3_cpu[1],f_4_cpu[1],f_5_cpu[1],f_6_cpu[1],f_7_cpu[1],f_10_cpu[1],f_15_cpu[1],f_20_cpu[1],f_25_cpu[1],f_30_cpu[1]]
green_data = [80,70,90, 100,50,0,0,0,0,0,0,0]

# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(blue_data))]

ax2.bar(bar_l, blue_data, width=bar_width,label='CPU (%)', alpha=0.5, color='#636363')
ax2.bar(bar_l, red_data, width=bar_width, bottom=blue_data, label='Real Memory (MB)', alpha=0.5, color='#2b8cbe')

plt.sca(ax2)
plt.xticks(tick_pos, ['0.5', '1', '2', '3', '4', '5', '6', '7', '10', '15', '20', '25', '30'])
 
ax2.set_ylabel("Computational resources")
ax2.set_xlabel("Monitoring interval (S)")
plt.legend(loc='upper right')
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
plt.grid()

plt.savefig("load_cpu.png")
plt.show()

# Original http://blog.topspeedsnail.com/archives/724