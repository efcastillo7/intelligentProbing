import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from os import scandir, getcwd
import os.path as path
import numpy as np
from numpy import *
from pathlib import Path
import csv
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import variation
from scipy.stats import sem #error
import statistics 

def csvRead(csv_file):
    x = []
    time_csv = []
    rtt = []
    delay = []
    delay_ms = []
    jitter = []
    time_r = []
    time_s = []
    delay_r = []
    delay_s = []

    if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

    with open(csv_file,'r') as csvfile:
        plots = csv.DictReader(csvfile)
        i = 0
        for row in plots:
            try:
                i+=1
                x.append(i)
                rtt.append(float(row["iRTT"])*1000)
                time_csv.append(float(row["Time"]))
            except Exception as e:
                #print ('Line {i} is corrupt!'.format(i = i), " File ", Path(csv_file).name)
                pass
    time_r = time_csv[1:]
    time_s = time_csv[:-1]

    for i in range(len(time_s)):
        delay.append(time_r[i] - time_s[i])
        delay_ms.append((time_r[i] - time_s[i])*1000)

    delay_r = delay[1:]
    delay_s = delay[:-1]

    for j in range(len(delay_s)):
        jitter.append(round((delay_r[j] - delay_s[j]), 2))

    #Coefficient Of Variation (CV)
    cv = (np.std(delay)/np.mean(delay)) *100
    #print(round(mean(delay), 3), round(sum(jitter), 3), Path(csv_file).name)
    #skew ->simetria
    print("mean:",round(np.mean(delay),2),"var:",np.var(delay),"skew:",skew(delay),"kurt:",kurtosis(delay), 
        "std:",round(np.std(delay),2),"CV:",round(variation(delay), 3),"Len:", len(delay),"Error:",round(sem(delay),3)*100)
    #print(round(sum(jitter)*1000, 3), Path(csv_file).name)
    return [delay, delay, rtt]

currentPath = getcwd()
print(currentPath)

state_05 = csvRead(currentPath + '/pcap/delay/probing_05s-delay.csv')
state_1 = csvRead(currentPath + '/pcap/delay/probing_1s-delay.csv')
state_2 = csvRead(currentPath + '/pcap/delay/probing_2s-delay.csv')
state_3 = csvRead(currentPath + '/pcap/delay/probing_3s-delay.csv')
state_4 = csvRead(currentPath + '/pcap/delay/probing_4s-delay.csv')
state_5 = csvRead(currentPath + '/pcap/delay/probing_5s-delay.csv')
state_6 = csvRead(currentPath + '/pcap/delay/probing_6s-delay.csv')
state_7 = csvRead(currentPath + '/pcap/delay/probing_7s-delay.csv')
state_8 = csvRead(currentPath + '/pcap/delay/probing_8s-delay.csv')
state_9 = csvRead(currentPath + '/pcap/delay/probing_9s-delay.csv')
state_10 = csvRead(currentPath + '/pcap/delay/probing_10s-delay.csv')
state_11 = csvRead(currentPath + '/pcap/delay/probing_11s-delay.csv')
state_12 = csvRead(currentPath + '/pcap/delay/probing_12s-delay.csv')
state_13 = csvRead(currentPath + '/pcap/delay/probing_13s-delay.csv')
state_14 = csvRead(currentPath + '/pcap/delay/probing_14s-delay.csv')
state_15 = csvRead(currentPath + '/pcap/delay/probing_15s-delay.csv')
ipro_v1 = csvRead(currentPath + '/pcap/delay/ipro_v1-delay.csv')

csv_plot = currentPath + '/behavior.svg'
x_axis_name = "Delay [ms]"

fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(14,9))
ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15 = axes.flatten()

############################ Subplot 0.5s #######################
ax0.hist(state_05[0], len(state_05[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax0.grid()
#ax0.text(4, 3, "edwin", fontsize=12)
#ax0.legend(prop={'size': 10})
ax0.set_title('Monitoring interval 0.5s',fontsize=9)
ax0.set_ylabel('CDF',fontsize=9)
ax0.set_xlabel('(a)',fontsize=9)

ax1.hist(state_1[0], len(state_1[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax1.grid()
ax1.set_title('Monitoring interval 1s',fontsize=9)
ax1.set_ylabel('CDF',fontsize=9)
ax1.set_xlabel('(b)',fontsize=9)

ax2.hist(state_2[0], len(state_2[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax2.grid()
ax2.set_title('Monitoring interval 2s',fontsize=9)
ax2.set_ylabel('CDF',fontsize=9)
ax2.set_xlabel('(c)',fontsize=9)

############################ Subplot 1s s#######################

ax3.hist(state_3[0], len(state_3[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax3.grid()
#ax3.legend(prop={'size': 10})
ax3.set_title('Monitoring interval 3s',fontsize=9)
ax3.set_ylabel('CDF',fontsize=9)
ax3.set_xlabel('(d)',fontsize=9)

ax4.hist(state_4[0], len(state_4[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax4.grid()
ax4.set_title('Monitoring interval 4s',fontsize=9)
ax4.set_ylabel('CDF',fontsize=9)
ax4.set_xlabel('(e)',fontsize=9)

ax5.hist(state_5[0], len(state_5[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax5.grid()
ax5.set_title('Monitoring interval 5s',fontsize=9)
ax5.set_ylabel('CDF',fontsize=9)
ax5.set_xlabel('(f)',fontsize=9)

############################ Subplot 5s s#######################

ax6.hist(state_6[0], len(state_6[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax6.grid()
#ax6.legend(prop={'size': 10})
ax6.set_title('Monitoring interval 6s',fontsize=9)
ax6.set_ylabel('CDF',fontsize=9)
ax6.set_xlabel('(g)',fontsize=9)

ax7.hist(state_7[0], len(state_7[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax7.grid()
ax7.set_title('Monitoring interval 7s',fontsize=9)
ax7.set_ylabel('CDF',fontsize=9)
ax7.set_xlabel('(h)',fontsize=9)

ax8.hist(state_8[0], len(state_8[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax8.grid()
ax8.set_title('Monitoring interval 8s',fontsize=9)
ax8.set_ylabel('CDF',fontsize=9)
ax8.set_xlabel('(i)',fontsize=9)

############################ Subplot 10s s#######################

ax9.hist(state_9[0], len(state_9[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax9.grid()
#ax9.legend(prop={'size': 10})
ax9.set_title('Monitoring interval 9s',fontsize=9)
ax9.set_ylabel('CDF',fontsize=9)
ax9.set_xlabel('(j)',fontsize=9)

ax10.hist(state_10[0], len(state_10[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax10.grid()
ax10.set_title('Monitoring interval 10s',fontsize=9)
ax10.set_ylabel('CDF',fontsize=9)
ax10.set_xlabel('(k)',fontsize=9)

ax11.hist(state_11[0], len(state_11[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax11.grid()
ax11.set_title('Monitoring interval 11s',fontsize=9)
ax11.set_ylabel('CDF',fontsize=9)
ax11.set_xlabel('(l)',fontsize=9)
#ax11.legend(loc='upper center', bbox_to_anchor=(0.1, -0.25),  shadow=True, ncol=2)

############################ Subplot 5s s#######################

ax12.hist(state_12[0], len(state_12[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax12.grid()
#ax12.legend(prop={'size': 10})
ax12.set_title('Monitoring interval 12s',fontsize=9)
ax12.set_ylabel('CDF',fontsize=9)
ax12.set_xlabel('(m)',fontsize=9)

ax13.hist(state_13[0], len(state_13[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax13.grid()
ax13.set_title('Monitoring interval 13s',fontsize=9)
ax13.set_ylabel('CDF',fontsize=9)
ax13.set_xlabel('(n)',fontsize=9)

ax14.hist(state_14[0], len(state_14[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax14.grid()
ax14.set_title('Monitoring interval 14s',fontsize=9)
ax14.set_ylabel('CDF',fontsize=9)
ax14.set_xlabel('(o)',fontsize=9)

"""
labels = ['PPA', ' IPro']
x = [f_10_cpu[0],f_00_cpu[0]]
y = [f_10_cpu[1], f_00_cpu[1]]
colors=['#969696','#252525']
for x_arr, y_arr, label,color in zip(x, y, labels, colors):
    ax11.plot(x_arr, y_arr, label=label, color=color)
"""
ax15.hist(state_15[0], len(state_15[0]), density=True, histtype='step',cumulative=True, color="red", label="label")
ax15.grid()
ax15.set_title('Monitoring interval 15s',fontsize=9)
ax15.set_ylabel('CDF',fontsize=9)
#ax15.set_xlabel('(l)',fontsize=9)
ax15.set_xlabel('(p) \n',fontsize=9)

fig.tight_layout()
#fig.tight_layout(pad=0.08, h_pad=None, w_pad=None, rect=None)
#fig.savefig(csv_plot, format="svg")
plt.show()

#gs2.tight_layout(fig, rect=[0.5, 0, 1, 1], h_pad=0.5)

import math

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


print (pearson_def(state_05[0][2:890], state_05[1][2:890]))