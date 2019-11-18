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

currentPath = getcwd()
print(currentPath)
f_00_speed = ReadCSV(currentPath + "/probing_00s/speed_00_300.csv")
f_00_cpu = ReadCSV(currentPath + "/probing_00s/cpu_usage_00_300.csv","cpu")

f_05_speed = ReadCSV(currentPath + "/probing_05s/speed_05_300.csv")
f_05_cpu = ReadCSV(currentPath + "/probing_05s/cpu_usage_05_300.csv","cpu")

f_1_speed = ReadCSV(currentPath + "/probing_07s/speed_07_300.csv")
f_1_cpu = ReadCSV(currentPath + "/probing_07s/cpu_usage_07_300.csv","cpu")

f_5_speed = ReadCSV(currentPath + "/probing_5s/speed_5_300.csv")
f_5_cpu = ReadCSV(currentPath + "/probing_5s/cpu_usage_5_300.csv","cpu")

f_10_speed = ReadCSV(currentPath + "/probing_10s/speed_10_300.csv")
f_10_cpu = ReadCSV(currentPath + "/probing_10s/cpu_usage_10_300.csv","cpu")

csv_plot = currentPath + '/behavior.svg'

fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(14,9))
ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11 = axes.flatten()

############################ Subplot 0.5s #######################
ax0.plot(f_05_speed[0], f_05_speed[2],'#969696',f_00_speed[0], f_00_speed[2],'#252525')
ax0.grid()
#ax0.legend(prop={'size': 10})
ax0.set_title('Switch-Controller - 0.5s',fontsize=9)
ax0.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax0.set_xlabel('(a)',fontsize=9)

ax1.plot(f_05_speed[0], f_05_speed[1],'#969696',f_00_speed[0], f_00_speed[1],'#252525')
ax1.grid()
ax1.set_title('Controller-Switch - 0.5s',fontsize=9)
ax1.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax1.set_xlabel('(b)',fontsize=9)

ax2.plot(f_05_cpu[0], f_05_cpu[1], '#969696', f_00_cpu[0], f_00_cpu[1], '#252525')
ax2.grid()
ax2.set_title('CPU usage - 0.5s',fontsize=9)
ax2.set_ylabel('CPU (%)',fontsize=9)
ax2.set_xlabel('(c)',fontsize=9)

############################ Subplot 1s s#######################

ax3.plot(f_1_speed[0], f_1_speed[2],'#969696',f_00_speed[0], f_00_speed[2],'#252525')
ax3.grid()
#ax3.legend(prop={'size': 10})
ax3.set_title('Switch-Controller - 1s',fontsize=9)
ax3.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax3.set_xlabel('(d)',fontsize=9)

ax4.plot(f_1_speed[0], f_1_speed[1],'#969696',f_00_speed[0], f_00_speed[1],'#252525')
ax4.grid()
ax4.set_title('Controller-Switch - 1s',fontsize=9)
ax4.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax4.set_xlabel('(e)',fontsize=9)

ax5.plot(f_1_cpu[0], f_1_cpu[1], '#969696', f_00_cpu[0], f_00_cpu[1], '#252525')
ax5.grid()
ax5.set_title('CPU usage - 1s',fontsize=9)
ax5.set_ylabel('CPU (%)',fontsize=9)
ax5.set_xlabel('(f)',fontsize=9)

############################ Subplot 5s s#######################

ax6.plot(f_5_speed[0], f_5_speed[2],'#969696',f_00_speed[0], f_00_speed[2],'#252525')
ax6.grid()
#ax6.legend(prop={'size': 10})
ax6.set_title('Switch-Controller - 5s',fontsize=9)
ax6.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax6.set_xlabel('(g)',fontsize=9)

ax7.plot(f_5_speed[0], f_5_speed[1],'#969696',f_00_speed[0], f_00_speed[1],'#252525')
ax7.grid()
ax7.set_title('Controller-Switch - 5s',fontsize=9)
ax7.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax7.set_xlabel('(h)',fontsize=9)

ax8.plot(f_5_cpu[0], f_5_cpu[1], '#969696', f_00_cpu[0], f_00_cpu[1], '#252525')
ax8.grid()
ax8.set_title('CPU usage - 5s',fontsize=9)
ax8.set_ylabel('CPU (%)',fontsize=9)
ax8.set_xlabel('(i)',fontsize=9)

############################ Subplot 10s s#######################

ax9.plot(f_10_speed[0], f_10_speed[2],'#969696',f_00_speed[0], f_00_speed[2],'#252525')
ax9.grid()
#ax9.legend(prop={'size': 10})
ax9.set_title('Switch-Controller - 10s',fontsize=9)
ax9.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax9.set_xlabel('(j)',fontsize=9)

ax10.plot(f_10_speed[0], f_10_speed[1],'#969696',f_00_speed[0], f_00_speed[1],'#252525')
ax10.grid()
ax10.set_title('Controller-Switch - 10s',fontsize=9)
ax10.set_ylabel('Control channel \n load (kbps)',fontsize=9)
ax10.set_xlabel('(k) \n Time (s)',fontsize=9)

labels = ['PPA', ' IPro']
x = [f_10_cpu[0],f_00_cpu[0]]
y = [f_10_cpu[1], f_00_cpu[1]]
colors=['#969696','#252525']
for x_arr, y_arr, label,color in zip(x, y, labels, colors):
    ax11.plot(x_arr, y_arr, label=label, color=color)

#ax11.plot(f_10_cpu[0], f_10_cpu[1], '#969696', f_00_cpu[0], f_00_cpu[1], '#252525', label='IPro')
ax11.grid()
ax11.set_title('CPU usage - 10s',fontsize=9)
ax11.set_ylabel('CPU (%)',fontsize=9)
ax11.set_xlabel('(l)',fontsize=9)
ax11.legend(loc='upper center', bbox_to_anchor=(0.1, -0.25),  shadow=True, ncol=2)

fig.tight_layout()
#fig.tight_layout(pad=0.08, h_pad=None, w_pad=None, rect=None)
fig.savefig(csv_plot, format="svg")
plt.show()

#gs2.tight_layout(fig, rect=[0.5, 0, 1, 1], h_pad=0.5)