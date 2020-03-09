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
from statistics import mean, stdev
import csv

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
		jitter.append(round((delay_r[j] - delay_s[j])*1000, 5))

	print(round(mean(delay), 3), round(sum(jitter), 3), Path(csv_file).name)
	#print(round(sum(jitter)*1000, 3), Path(csv_file).name)
	return [jitter, delay_ms]

currentPath = getcwd()
print(currentPath)

state_05 = csvRead(currentPath + '/pcap/probing_05s-rtt.csv')
state_1 = csvRead(currentPath + '/pcap/probing_1s-rtt.csv')
state_2 = csvRead(currentPath + '/pcap/probing_2s-rtt.csv')
state_3 = csvRead(currentPath + '/pcap/probing_3s-rtt.csv')
state_4 = csvRead(currentPath + '/pcap/probing_4s-rtt.csv')
state_5 = csvRead(currentPath + '/pcap/probing_5s-rtt.csv')
state_6 = csvRead(currentPath + '/pcap/probing_6s-rtt.csv')
state_7 = csvRead(currentPath + '/pcap/probing_7s-rtt.csv')
state_8 = csvRead(currentPath + '/pcap/probing_8s-rtt.csv')
state_9 = csvRead(currentPath + '/pcap/probing_9s-rtt.csv')
state_10 = csvRead(currentPath + '/pcap/probing_10s-rtt.csv')
state_11 = csvRead(currentPath + '/pcap/probing_11s-rtt.csv')
state_12 = csvRead(currentPath + '/pcap/probing_12s-rtt.csv')
state_13 = csvRead(currentPath + '/pcap/probing_13s-rtt.csv')
state_14 = csvRead(currentPath + '/pcap/probing_14s-rtt.csv')
state_15 = csvRead(currentPath + '/pcap/probing_15s-rtt.csv')

datos_1 = state_05
datos_2 = state_1
datos_3 = state_2
datos_4 = state_3

#datos_graf = [datos_1, datos_2, datos_3, datos_4]
datos_graf = [state_05[0], state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]

delay_list = [state_05[1], state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]
# Creando el objeto figura
fig = plt.figure(1, figsize=(9, 6))
# Creando el subgrafico
ax = fig.add_subplot(111)
# creando el grafico de cajas
bp = ax.boxplot(datos_graf, showfliers=True)
# visualizar mas facile los atípicos
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
# Hide these grid behind plot objects
ax.set_axisbelow(True)
#ax.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax.set_xlabel('Interval monitoring')
ax.set_ylabel('Jitter')
#plt.grid()
plt.show()

# Creando el objeto figura
fig = plt.figure(1, figsize=(9, 6))
# Creando el subgrafico
ax = fig.add_subplot(111)
# creando el grafico de cajas
bp = ax.boxplot(delay_list, showfliers=True)
# visualizar mas facile los atípicos
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
# Hide these grid behind plot objects
ax.set_axisbelow(True)
#ax.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
ax.set_xlabel('Interval monitoring')
ax.set_ylabel('Delay')
#plt.grid()
plt.show()

"""
fig, ax = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
n, bins, patches = ax.hist(length_p, x, color='#636363', cumulative=True, label='Controller-Switch messages') #histtype='step'

#print(np.cumsum(reward))
y = np.cumsum(rtt)
ax.plot(bins, y, 'k--', linewidth=1.5, label='Cumulative reward')

# tidy up the figure
ax.grid(True)
#ax.legend(loc='right')
ax.legend()
#ax.set_title('Cumulative step histograms')
ax.set_xlabel('Time steps')
ax.set_ylim(0, max(y))
ax.set_ylabel('Cumulative reward')

# Secondary axis
ax2 = ax.twinx()
ax2.set_ylim(0, 450)
ax2.set_ylabel("Control channel load (kbps)")

plt.show()
"""