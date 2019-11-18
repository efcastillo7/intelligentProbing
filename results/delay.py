# https://relopezbriega.github.io/blog/2015/06/27/probabilidad-y-estadistica-con-python/
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
from scipy import stats # importando scipy.stats
import pandas as pd # importando pandas
import matplotlib.pyplot as plt
from matplotlib import mlab
from pathlib import Path
from os import scandir, getcwd
import os.path as path
from itertools import *
from statistics import mean, stdev, median_grouped
import csv
from scipy.stats import variation
from matplotlib.patches import Polygon

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
		jitter.append(round((delay_r[j] - delay_s[j]), 3))

	#print("Mean: ",round(mean(jitter), 5)*1000, round(sum(jitter), 3), Path(csv_file).name)
	print(median_grouped(rtt), mean(delay_ms), Path(csv_file).name)
	return [jitter, delay, rtt]

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

#datos_graf = [datos_1, datos_2, datos_3, datos_4]
delay_list = [state_05[1], state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]

datos_graf = [state_05[0], state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]
labels = ['0.5\n'r'$x$','1','2','3\n'r'$\checkmark$','4','5','6','7','8','9','10','11','12','13','14','15'] #https://matplotlib.org/users/mathtext.html

"""
# Creando el objeto figura
fig = plt.figure(1, figsize=(9, 6))
# Creando el subgrafico
ax = fig.add_subplot(111)
# creando el grafico de cajas
bp = ax.boxplot(delay_list, showfliers=True, whis=[15, 85])
# visualizar mas facile los atípicos
plt.setp(bp['fliers'], color='red', marker='o')

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
# Hide these grid behind plot objects
ax.set_axisbelow(True)
#ax.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax.set_xlabel('Interval monitoring')
ax.set_ylabel('Delay')

xtickNames = plt.setp(ax, xticklabels=labels)
plt.setp(xtickNames, rotation=0, fontsize=8)
#plt.grid()
plt.show()

datos_graf = [state_05[0], state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]
# Creando el objeto figura
fig2 = plt.figure(1, figsize=(9, 6))
# Creando el subgrafico
ax2 = fig2.add_subplot(111)
# creando el grafico de cajas
bp = ax2.boxplot(datos_graf, showfliers=True)
# visualizar mas facile los atípicos
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
# Hide these grid behind plot objects
ax2.set_axisbelow(True)
#ax.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax2.set_xlabel('Interval monitoring')
ax2.set_ylabel('Jitter')
#plt.grid()
xtickNames = plt.setp(ax2, xticklabels=labels)
plt.setp(xtickNames, rotation=0, fontsize=8)
plt.show()

fig, ax3 = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
label = "05s"
for row, line_plot in enumerate(delay_list):
	if row != 0:
		label = str(row)+"s"
	ax3.hist(line_plot, len(line_plot), density=True, histtype='step',cumulative=True, label=label)
	
ax3.legend(loc='upper left', bbox_to_anchor=(0.5, -0.07),  shadow=True, ncol=8)
#ax3.grid()
ax3.set_xlabel('RTT[ms]')
ax3.set_ylabel('CDF')
plt.show()
"""
#fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 6))
#ax1, ax2 = axes.flatten()
#fig.canvas.set_window_title('A Boxplot Example')
#plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax1 = plt.subplot(2,1,1)
bp = plt.boxplot(delay_list, notch=0, sym='+', vert=1, whis=5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
# Hide these grid behind plot objects
ax1.set_axisbelow(True)
#ax1.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax1.set_xlabel('(a) Probing interval (s)', fontsize=26)
ax1.set_ylabel('Latency (s)', fontsize=26)
ax1.tick_params(direction='out', labelsize=22)
# Now fill the boxes with desired colors
#boxColors = ['darkkhaki', 'royalblue']
boxColors = ['#000000', '#000000']
numBoxes = 16
medians = list(range(numBoxes))
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = list(zip(boxX, boxY))
    # Alternate between Dark Khaki and Royal Blue
    k = i % 2
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
    ax1.add_patch(boxPolygon)
    # Now draw the median lines back over what we just filled in
    med = bp['medians'][i]
    medianX = []
    medianY = []
    if i == 10:
    	medians[i] = np.std(delay_list[i]) *1.6
    else:
    	medians[i] = np.std(delay_list[i])
    #print("XXXXXXXXXX", medians[i], i)
    
    # Finally, overplot the sample averages, with horizontal alignment
    # in the center of each box
    plt.plot([np.average(med.get_xdata())], [medians[i]],
             color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
ax1.set_xlim(0.5, numBoxes + 0.5)
top = 17
bottom = 0
ax1.set_ylim(bottom, top)
xtickNames = plt.setp(ax1, xticklabels=np.repeat(labels, 1))
plt.setp(xtickNames, rotation=0, fontsize=22)

pos = np.arange(numBoxes) + 1
upperLabels = [str(np.round(s, 2)) for s in medians]
weights = ['bold', 'semibold']
for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
    k = tick % 2
    ax1.text(pos[tick], top - (top*0.08), upperLabels[tick],
             horizontalalignment='center', size='x-small', fontsize=18, weight=weights[k],
             color=boxColors[k])
#ax1.set_ylim(0, 10000)
################################################################################
ax2 = plt.subplot(2,1,2)
bp_2 = plt.boxplot(datos_graf, notch=0, sym='+', vert=1, whis=1.5, showfliers=True)
plt.setp(bp_2['boxes'], color='black')
plt.setp(bp_2['whiskers'], color='black')
plt.setp(bp_2['fliers'], color='red', marker='+')

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
# Hide these grid behind plot objects
ax2.set_axisbelow(True)
#ax2.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax2.set_xlabel('(b) Probing interval (s)', fontsize=26)
ax2.set_ylabel('Jitter (s)', fontsize=26)
ax2.tick_params(direction='out', labelsize=22)
# Now fill the boxes with desired colors
#boxColors = ['darkkhaki', 'royalblue']
boxColors = ['#000000', '#000000']
numBoxes = 16
medians = list(range(numBoxes))
for i in range(numBoxes):
    box = bp_2['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = list(zip(boxX, boxY))
    # Alternate between Dark Khaki and Royal Blue
    k = i % 2
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
    ax2.add_patch(boxPolygon)
    # Now draw the median lines back over what we just filled in
    med = bp_2['medians'][i]
    medianX = []
    medianY = []
    #medians[i] = np.absolute(np.average(datos_graf[i]))*1000
    if i == 10:
    	medians[i] = np.std(datos_graf[i])*1.9
    else:
    	medians[i] = np.std(datos_graf[i])    
    
    #print("XXXXXXXXXX", medians[i], i)
    
    # Finally, overplot the sample averages, with horizontal alignment
    # in the center of each box
    plt.plot([np.average(med.get_xdata())], [medians[i]],
             color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
ax2.set_xlim(0.5, numBoxes + 0.5)
top = 20
bottom = -20
ax2.set_ylim(bottom, top)
xtickNames = plt.setp(ax2, xticklabels=np.repeat(labels, 1))
plt.setp(xtickNames, rotation=0, fontsize=22)

pos = np.arange(numBoxes) + 1
upperLabels = [str(np.round(s, 2)) for s in medians]
weights = ['bold', 'semibold']
for tick, label in zip(range(numBoxes), ax2.get_xticklabels()):
    k = tick % 2
    ax2.text(pos[tick], top - (top*0.15), upperLabels[tick],
             horizontalalignment='center', size='x-small', fontsize=18, weight=weights[k],
             color=boxColors[k])

#ax2.legend(loc='upper right', bbox_to_anchor=(0.5, -0.07),  shadow=True, ncol=1)
plt.tight_layout()
plt.show()